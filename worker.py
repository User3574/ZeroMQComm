import random

import zmq
import json
import numpy as np
from utils import recv_array


class Worker:
    def __init__(self, func, addr="tcp://localhost:5560"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(addr)
        self.func = func

    def run(self):
        message_id = 0

        while True:
            id, message = self.socket.recv_multipart()

            # Decode
            id = id.decode()
            message = message.decode()

            # Compute
            result = self.func(message)

            # Send
            self.socket.send_multipart([
                str(id).encode(),
                str(result).encode()
            ])

            message_id += 1
            print(f'Sending {message_id}')


if __name__ == '__main__':
    def length(message):
        return len(message)

    worker = Worker(length)
    worker.run()
