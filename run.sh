#!/bin/bash
#PBS -qqexp
#PBS -lselect=2,walltime=01:00:00

WORK_DIR="/home/mac0491/ZeroMQComm"

ml Python/3.8.6-GCCcore-10.2.0

cd ${WORK_DIR}
source env/bin/activate

python3 run.py
