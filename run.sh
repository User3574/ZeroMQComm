#!/bin/bash

input=$(echo $PBS_NODEFILE)
ITER=0
CLIENT=""
MSG=""

while IFS= read -r line; do
if test $ITER -gt 0
then
	echo "Creating worker"
        ssh -n -f ${line} "
        source ZeroMQComm/env/bin/activate
        python ZeroMQComm/ex_worker.py --address $CLIENT &
" 
else
	CLIENT=${line}
fi
ITER=$(expr $ITER + 1)
done < ${input}

# Run client
echo "Running client"
cd ZeroMQComm
source env/bin/activate
python ex_client.py --msg_count 20

