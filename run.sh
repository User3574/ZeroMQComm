input=$(echo $PBS_NODEFILE)
ITER=0
CLIENT=""
MSG=""

WORK_DIR="/home/mac0491/ZeroMQComm"
ENV_PATH="${WORK_DIR}/env"
WORKERS_PER_NODE=$1
SLEEP_TIME=$2
MSG_COUNT=$3

while IFS= read -r line; do
if test $ITER -gt 0
then
        ssh -n -f ${line} "
        cd ${WORK_DIR}
        source ${ENV_PATH}/bin/activate
        for (( i=1; i<=${WORKERS_PER_NODE}; i++ ))
        do
            python3 ex_worker.py --address ${CLIENT} --sleep_time ${SLEEP_TIME} &
        done
        wait
" 
else
	CLIENT=${line}
fi
ITER=$(expr $ITER + 1)
done < ${input}

# Run client
cd ${WORK_DIR}
source ${ENV_PATH}/bin/activate
python ex_client.py --msg_count ${MSG_COUNT}
