#!/bin/bash
#PBS -qqexp
#PBS -lselect=2,walltime=00:30:00

input=$(echo $PBS_NODEFILE)
ITER=0
CLIENT=""
MSG=""

WORK_DIR="/home/beranekj/projects/ZeroMQComm"
ENV_PATH="${WORK_DIR}/venv"
WORKERS_PER_NODE=4

while IFS= read -r line; do
if test $ITER -gt 0
then
        ssh -n -f ${line} "
        cd ${WORK_DIR}
        source ${ENV_PATH}/bin/activate
        for (( i=1; i<=${WORKERS_PER_NODE}; i++ ))
        do
            echo "Creating worker ${i}"
            python3 ex_worker.py --address ${CLIENT} &
        done
        wait
" 
else
	CLIENT=${line}
fi
ITER=$(expr $ITER + 1)
done < ${input}

# Run client
echo "Running client"
cd ${WORK_DIR}
source ${ENV_PATH}/bin/activate
python ex_client.py --msg_count 20
