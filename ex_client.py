from src import client
import json

if __name__ == '__main__':
    client = client.Client()

    # Create dummy array
    msg_count = 100000
    array = [[x, x+1] for x in range(msg_count)]

    # Serialize array
    array = [json.dumps(x).encode() for x in array]

    results = client.compute(array)
    #print(results)
