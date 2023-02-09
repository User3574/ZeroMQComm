import zmq


class Worker:
    def __init__(self, func, port:int=5560):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.address = f"tcp://localhost:{port}"
        self.socket.connect(self.address)
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
