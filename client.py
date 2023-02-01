#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq
import numpy as np
from utils import send_array
from numpy import random


if __name__ == '__main__':
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    #  Do 10 requests, waiting each time for a response
    for request in range(1, 11):
        data = np.array([random.randint(100) for x in range(10)])
        send_array(socket, data)
        message = socket.recv_string()
        print(f"REP {request}: [{message}]")
