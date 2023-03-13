from src import worker
import click
import time


@click.command()
@click.option('--address', default='localhost', help='Client address')
@click.option('--port', default=5560, type=int, help='Client port')
@click.option('--sleep_time', default=1, type=float, help='Sleep time amount')
def main(address: str, port: int, sleep_time: float):
    def length(message):
        return len(message)

    def same(message):
        time.sleep(sleep_time)
        return message

    def sleep(message):
        time.sleep(sleep_time)
        return message

    w = worker.Worker(same, address=address, port=port)
    w.run()


if __name__ == '__main__':
    main()
