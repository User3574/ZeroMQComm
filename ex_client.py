from src import client

if __name__ == '__main__':
    client = client.Client()

    # Create dummy array
    msg_count = 100
    array = ["A" * x for x in range(msg_count)]

    # Serialize array
    array = [x.encode() for x in array]

    results = client.compute(array)
    print(results)
