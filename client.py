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
    msg_count = 100
    data = "A" * 10000

    msg_send = 0
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN | zmq.POLLOUT)

    # Switch messages between sockets
    while True:
        socks = dict(poller.poll())

        if socks.get(socket) == zmq.POLLIN:
            worker, message = socket.recv_multipart()
            print(f'Receiving from worker {worker.decode()}')

        if socks.get(socket) == zmq.POLLOUT:
            print(f'Sending {msg_send}')
            socket.send_string(data)
            # Send until all messages are sent
            msg_send += 1
            if msg_send == msg_count:
                poller.modify(socket, zmq.POLLIN)
