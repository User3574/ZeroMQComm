import tqdm as tqdm
import zmq
import numpy as np
from utils import send_array
from numpy import random


if __name__ == '__main__':
    #  Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.set(zmq.SNDHWM, 8192)
    socket.set(zmq.RCVHWM, 8192)
    socket.connect("tcp://localhost:5559")

    # Send all requests
    msg_count = 500000
    data = "A" * 10000

    msg_send = 0
    msg_received = 0
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN | zmq.POLLOUT)

    # Switch messages between sockets
    while msg_received < msg_count:
        socks = dict(poller.poll())

        if (socks.get(socket) & zmq.POLLIN) == zmq.POLLIN:
            # print("Receiving")
            worker, message = socket.recv_multipart()
            # print(worker)
            msg_received += 1
            if msg_received % 1000 == 0:
                print(f"R{msg_received}/{msg_count}")

        if (socks.get(socket) & zmq.POLLOUT) == zmq.POLLOUT:
            if msg_send % 1000 == 0:
                print(f"S{msg_send}/{msg_count}")
            socket.send_string(data)
            # Send until all messages are sent
            msg_send += 1
            if msg_send == msg_count:
                poller.modify(socket, zmq.POLLIN)
