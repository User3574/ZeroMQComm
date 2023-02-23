from src import worker
import click
import time


@click.command()
@click.option('--address', default='localhost', help='Client address')
def main(address):
    def length(message):
        return len(message)

    def same(message):
        time.sleep(1)
        return message

    w = worker.Worker(same, address=address)
    w.run()


if __name__ == '__main__':
    main()
