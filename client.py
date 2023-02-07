import tqdm as tqdm
import zmq
import numpy as np
from utils import send_array
from numpy import random


class Client:
    def __init__(self, addr="tcp://localhost:5559", port=8192):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)

        self.socket.set(zmq.SNDHWM, port)
        self.socket.set(zmq.RCVHWM, port)
        self.socket.connect(addr)

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN | zmq.POLLOUT)

    def compute(self, array):
        msg_send = 0
        msg_received = 0
        msg_count = len(array)
        results = {}

        # Switch messages between sockets
        while msg_received < msg_count:
            socks = dict(self.poller.poll())

            if (socks.get(self.socket) & zmq.POLLIN) == zmq.POLLIN:
                message_id, message = self.socket.recv_multipart()

                # Decode
                message_id = message_id.decode()
                message = message.decode()

                # Append
                results[message_id] = message
                msg_received += 1
                if msg_received % 1000 == 0:
                    print(f"R{msg_received}/{msg_count}")

            if (socks.get(self.socket) & zmq.POLLOUT) == zmq.POLLOUT:
                if msg_send % 1000 == 0:
                    print(f"S{msg_send}/{msg_count}")

                # Send until all messages are sent
                self.socket.send_multipart([
                    str(msg_send).encode(),
                    array[msg_send].encode()
                ])
                msg_send += 1
                if msg_send == msg_count:
                    self.poller.modify(self.socket, zmq.POLLIN)

        return results


if __name__ == '__main__':
    client = Client()

    # Create dummy array
    msg_count = 100
    array = ["A" * x for x in range(msg_count)]

    results = client.compute(array)
    print(results)
