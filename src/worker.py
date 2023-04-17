import json
import zmq


class Worker:
    def __init__(self, func, address="localhost", port: int = 5560):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.address = f"tcp://{address}:{port}"
        self.socket.connect(self.address)
        self.func = func

    def run(self):
        message_id = 0
        while True:
            id, message = self.socket.recv_multipart()

            # Decode
            message = json.loads(message.decode())

            # Compute
            result = self.func(message)

            # Serialize
            result = json.dumps(result).encode()

            # Send
            self.socket.send_multipart([
                id,
                result
            ])

            message_id += 1
            #print(f'Sending {message_id}')
