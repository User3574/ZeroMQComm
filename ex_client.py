from src import client
import json
import time
import click


@click.command()
@click.option('--msg_count', default=100000, help='Amount of messages to send')
def main(msg_count):
    client = client.Client()

    # Create dummy array
    msg_count = 100000
    array = [[x, x + 1] for x in range(msg_count)]

    # Serialize array
    array = [json.dumps(x).encode() for x in array]

    start = time.time()
    results = client.compute(array)
    end = time.time()

    print(f'Computation time: {end - start} for messages: {msg_count}')
    # print(results)


if __name__ == '__main__':
    main()
