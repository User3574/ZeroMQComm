import subprocess
import os
from cluster import cluster


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def kill_process(hostname: str, pid: int, signal="TERM"):
    """
    Kill a process with the given `pid` on the specified `hostname`
    :param hostname: Hostname where the process is located.
    :param pid: PGID of the process to kill.
    :param signal: Signal used to kill the process. One of "TERM", "KILL" or "INT".
    """
    import signal as pysignal

    assert signal in ("TERM", "KILL", "INT")
    cluster.logging.debug(f"Killing PGID {pid} on {hostname}")
    if not cluster.is_local(hostname):
        res = subprocess.run([f'ssh {hostname} kill -{signal} {pid}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if res.returncode != 0:
            cluster.logging.error(
                f"error: {res}")
            return False
    else:
        if signal == "TERM":
            signal = pysignal.SIGTERM
        elif signal == "KILL":
            signal = pysignal.SIGKILL
        elif signal == "INT":
            signal = pysignal.SIGINT
        os.killpg(pid, signal)
    return True


def run(hosts: list, sleep_time: float, msg_count: int, workers_per_node: int):
    CLIENT = hosts[0]
    workers = []

    for i, host in enumerate(hosts[1:]):
        for i in range(workers_per_node):
            workers.append(cluster.start_process(
                commands=[f"python3 ex_worker.py --address {CLIENT} --sleep_time {sleep_time}"],
                pyenv=f"{ENV_PATH}",
                hostname=host,
                name=f"worker_{i}"
            ))
    
    p = subprocess.Popen([f"python ex_client.py --msg_count {msg_count}"], stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    p.wait()
    print(str(out, 'utf-8'))
            
    # Wait on client process
    for worker in workers:
        kill_process(worker.hostname, worker.pid)
    

WORK_DIR = "/home/mac0491/ZeroMQComm"
ENV_PATH = f"{WORK_DIR}/env"

p = subprocess.Popen(['echo $PBS_NODEFILE'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
file = str(p.stdout.read().splitlines()[0], 'utf-8')

f = open(file, "r")
hosts = f.read().splitlines()

sleep_times = [0.1] #1
msg_counts = [1000]
workers_per_nodes = [1,2,4,8,16,32,64,128,256]
for sleep_time in sleep_times:
    for workers_per_node in workers_per_nodes:
        for msg_count in msg_counts:
            print(f"Sleep: {sleep_time}, Workers: {workers_per_node}, Messages: {msg_count}")
            run(hosts, sleep_time, msg_count, workers_per_node)
