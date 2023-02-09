import zmq
from typing import List


class Client:
    def __init__(self, port: int = 5559, watermark: int = 8192):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)

        self.socket.set(zmq.SNDHWM, watermark)
        self.socket.set(zmq.RCVHWM, watermark)

        self.address = f"tcp://localhost:{port}"
        self.socket.connect(self.address)

        self.poller = zmq.Poller()

    def compute(self, array: List[bytes]):
        self.poller.register(self.socket, zmq.POLLIN | zmq.POLLOUT)

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
                    array[msg_send]
                ])
                msg_send += 1
                if msg_send == msg_count:
                    self.poller.modify(self.socket, zmq.POLLIN)

        # Sort by id
        results = {key: value for key, value in sorted(results.items(), key=lambda item: int(item[0]))}
        return list(results.values())
