# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq

if __name__ == '__main__':
    # Prepare our context and sockets
    context = zmq.Context()
    frontend = context.socket(zmq.DEALER)
    backend = context.socket(zmq.DEALER)
    frontend.bind("tcp://*:5559")
    # Create two workers
    backend.bind("tcp://*:5560")

    zmq.proxy(frontend, backend)
    #
    # # Initialize poll set
    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    poller.register(frontend, zmq.POLLIN)

    # Switch messages between sockets
    while True:
        socks = dict(poller.poll())

        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv_multipart()
            print("Got request from client, sending to worker")
            backend.send_multipart(message)

        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv_multipart()
            print("Got response from worker, sending to client")
            frontend.send_multipart(message)
