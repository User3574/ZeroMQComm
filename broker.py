import zmq

if __name__ == '__main__':
    context = zmq.Context()
    frontend = context.socket(zmq.DEALER)
    backend = context.socket(zmq.DEALER)

    frontend.bind("tcp://*:5559")
    backend.bind("tcp://*:5560")

    zmq.proxy(frontend, backend)
