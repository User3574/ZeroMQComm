import subprocess
from cluster import cluster, io

if __name__ == '__main__':
    bashCommand = "echo $PBS_NODEFILE"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
