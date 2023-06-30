import datetime
import time
from opcua import Client
from opcua import ua
from typing import Optional
import json
import datetime
from pika
import concurrent.futures



global machine_clients
machine_clients = []

global Kafka_Producer
Kafka_Producer = []


def Get_Nodes(opcClient, kafkaprod,kafkatopicprefix):
        root = opcClient.get_root_node()
        objects = root.get_children()[0]
        nodes = objects.get_children()
        print(kafkatopicprefix)
        for node in nodes:
                for subnode in node.get_children():
                    node_id = str(subnode)
                    if "ns=1" in node_id:
                        topic = "Server" + kafkatopicprefix + "_" + node_id.split("=")[2].replace(".","_")
                        value = opcClient.get_node(node_id).get_value()
                        timestamp = datetime.datetime.now()
                        timestamp_str = timestamp.isoformat()
                        message = {
                                'Node': node_id,
                                'TimeStamp': timestamp_str,
                                'Value': str(value)
                            }
                        message_str = json.dumps(message)
                        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
                        print(topic)
        kafkaprod.flush()

def process_machine_client(machine_client):
    print(machine_client["url"])
    Get_Nodes(machine_client["opc_client"], machine_client["kafka_producer"], str(machine_client["id"]))

try:
    
    # create objects and variables from json file
    with open("monitorconfig.json", "r") as f:
        jsonservers = json.load(f)

    for server in jsonservers:
        # RabbitMQ connection parameters
        connection_params = pika.ConnectionParameters('localhost')
        
        # Create a connection to the RabbitMQ broker
        connection = pika.BlockingConnection(connection_params)
        
        # Create a channel
        channel = connection.channel()
        
        # Declare a queue
        queue_name = 'my_queue'
        channel.queue_declare(queue=queue_name)


        opc_client = Client(server["url"])
        opc_client.connect()
        obj = {
            "opc_client": opc_client,
            "kafka_producer": producer,
            "id": server["id"],
            "url": server["url"]
        }
        machine_clients.append(obj)

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(process_machine_client, machine_client) for machine_client in machine_clients]

finally:
    for machine_client in machine_clients:
        machine_client["opc_client"].disconnect()
        machine_client["kafka_producer"].flush()
