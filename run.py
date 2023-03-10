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


WORK_DIR = "/home/mac0491/ZeroMQComm"
ENV_PATH=f"{WORK_DIR}/env"

p = subprocess.Popen(['echo $PBS_NODEFILE'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
file = str(p.stdout.read().splitlines()[0],'utf-8')

f = open(file, "r")
lines = f.read().splitlines()
CLIENT = lines[0]
client = None
workers = []
for i, line in enumerate(lines):
    if i == 0:
        print("Run client")
        client = cluster.start_process(
            commands=["python ex_client.py --msg_count 20"],
            pyenv=f"{ENV_PATH}",
            hostname=line,
            name="client"
        )
    else:
        print('Run worker')
        workers.append(cluster.start_process(
            commands=[f"python3 ex_worker.py --address {CLIENT}"],
            pyenv=f"{ENV_PATH}",
            hostname=line,
            name=f"worker_{i}"
        ))


# Wait on client process
for worker in workers:
    cluster.kill_process(worker.hostname, worker.pid, signal="KILL")
