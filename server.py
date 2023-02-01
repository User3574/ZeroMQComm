#
#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Hello" from client, replies with "World"
#
import zmq
import json
import numpy as np
from utils import recv_array

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5560")

    while True:
        message = recv_array(socket)
        print(f"REQ: {message}")
        result = np.sum(message)
        socket.send_string(str(result))
