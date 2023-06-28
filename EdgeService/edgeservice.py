import datetime
import time
from opcua import Client
from opcua import ua
from typing import Optional
import json
import datetime
from confluent_kafka import Producer
import concurrent.futures



global machine_clients
machine_clients = []

global Kafka_Producer
Kafka_Producer = []



# create objects and variables from json file
with open("monitorconfig.json", "r") as f:
    jsonservers = json.load(f)

for server in jsonservers:

    kafka_broker = "cloud:9092"
    conf = {
        'bootstrap.servers': kafka_broker,
        'client.id': 'my_producer',
        'acks': 'all'
    }
    producer = Producer(conf)
    opc_client = Client(server["url"])
    opc_client.connect()
    obj = {
        "opc_client": opc_client,
        "kafka_producer": producer,
        "id": server["id"],
        "url": server["url"]
    }
    machine_clients.append(obj)

def Get_Nodes(opcClient, kafkaprod,kafkatopicprefix):
    while True:
        root = opcClient.get_root_node()
        objects = root.get_children()[0]
        nodes = objects.get_children()
        for node in nodes:
                for subnode in node.get_children():
                    node_id = str(subnode)
                    if "ns=1" in node_id:
                        topic = kafkatopicprefix + "_" + node_id.split("=")[2].replace(".","_")
                        value = opcClient.get_node(node_id).get_value()
                        timestamp = datetime.datetime.now()
                        timestamp_str = timestamp.isoformat()
                        message = {
                                'Node': node_id,
                                'TimeStamp': timestamp_str,
                                'Value': str(value)
                            }
                        message_str = json.dumps(message)
                        kafkaprod.produce(topic, value=message_str)
                        print(message_str)

def process_machine_client(machine_client):
    print(machine_client["url"])
    Get_Nodes(machine_client["opc_client"], machine_client["kafka_producer"], str(machine_client["id"]))

try:
    time.sleep(2)
    # Create a ThreadPoolExecutor with maximum worker threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_machine_client, machine_client) for machine_client in machine_clients]
    concurrent.futures.wait(futures)

finally:
    for machine_client in machine_clients:
        machine_client["opc_client"].disconnect()
        machine_client["kafka_producer"].flush()
