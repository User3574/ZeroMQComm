from src import worker

if __name__ == '__main__':
    def length(message):
        return len(message)

    def same(message):
        return message

    worker = worker.Worker(same)
    worker.run()