from src import worker
import click
import time


@click.command()
@click.option('--address', default='localhost', help='Client address')
@click.option('--sleep_time', default=1, help='Sleep time amount')
def main(address, sleep_time):
    def length(message):
        return len(message)

    def same(message):
        time.sleep(sleep_time)
        return message

    def sleep(message):
        time.sleep(sleep_time)
        return message

    w = worker.Worker(same, address=address)
    w.run()


if __name__ == '__main__':
    main()
