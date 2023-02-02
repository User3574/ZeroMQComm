#
#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Hello" from client, replies with "World"
#
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
        # message = recv_array(socket)
        # print(f"REQ: {message}")
        # result = np.sum(message)
        # socket.send_string(str(result))
        # src, message = socket.recv_multipart()
        # print(message)
        # socket.send_multipart([
        #     src,
        #     str(worker_id).encode(),
        #     message + message
        # ])
        message = socket.recv_multipart()[0]
        socket.send_multipart([
            str(worker_id).encode(),
            message + message
        ])
