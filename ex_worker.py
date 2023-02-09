from src import worker

if __name__ == '__main__':
    def length(message):
        return len(message)

    worker = worker.Worker(length)
    worker.run()