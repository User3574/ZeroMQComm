import random

import zmq
import json
import numpy as np
from utils import recv_array

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:5560")

    worker_id = random.randint(1, 10)
    print(f"Worker {worker_id}")

    while True:
        message = socket.recv_multipart()[0]
        socket.send_multipart([
            str(worker_id).encode(),
            message + message
        ])
        print('Sending')
