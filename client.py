#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import tqdm as tqdm
import zmq
import numpy as np
from utils import send_array
from numpy import random


if __name__ == '__main__':
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:5559")

    # Send all requests
    # msg_count = 5000
    msg_count = 500000  # this should work, but currently it deadlocks

    data = ["A" * 10000] * 500000

    # Send all requests
    for request in range(0, msg_count):
        # data = np.array([random.randint(100) for x in range(10)])
        # send_array(socket, data)
        socket.send_string("A" * 10000)

    # Wait for all responses
    for request in tqdm.tqdm(range(0, msg_count)):
        worker, message = socket.recv_multipart()
        # message = socket.recv_string()
        # print(f"REP {request}: [{message}]")
        # print(f"Got {message.decode()} computed by worker {worker.decode()}")

    # TODO: overlap sending of requests and receiving of messages to avoid a deadlock
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    poller.register(socket, zmq.POLLOUT)

    # Switch messages between sockets
    while True:
        socks = dict(poller.poll())

        if socks.get(socket) == zmq.POLLIN:
            message = socket.recv_multipart()

        if socks.get(socket) == zmq.POLLOUT:
            socket.send_multipart(message)
            if all_sent:
                poller.unregister(socket, zmq.POLLOUT)
