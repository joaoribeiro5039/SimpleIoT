import datetime
import time
from opcua import Client
from opcua import ua
from typing import Optional
import json
import datetime
import pika
import concurrent.futures


global machine_clients
machine_clients = []


def Get_Nodes(opcClient, rabbitmq_connect,rabbitmq_queue):
    rabbitmq_queue = "Server_" + rabbitmq_queue
    rabbitmq_channel = rabbitmq_connect.channel()
    rabbitmq_channel.queue_declare(queue=rabbitmq_queue)
    root = opcClient.get_root_node()
    objects = root.get_children()[0]
    nodes = objects.get_children()
    for node in nodes:
        for subnode in node.get_children():
            node_id = str(subnode)
            if "ns=1" in node_id:
                value = opcClient.get_node(node_id).get_value()
                timestamp = datetime.datetime.now()
                timestamp_str = timestamp.isoformat()
                message = {
                        'Node': node_id,
                        'TimeStamp': timestamp_str,
                        'Value': str(value)
                    }
                message_str = json.dumps(message)
                rabbitmq_channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=message_str)

def process_machine_client(machine_client):
    print(machine_client["url"])
    Get_Nodes(machine_client["opc_client"], machine_client["rabbitmq_connect"], str(machine_client["id"]))

try:

    # create objects and variables from json file
    with open("monitorconfig.json", "r") as f:
        jsonservers = json.load(f)

    for server in jsonservers:

        credentials = pika.PlainCredentials('admin', 'admin')
        connection_params = pika.ConnectionParameters('cloud', credentials=credentials)
        connection = pika.BlockingConnection(connection_params)

        opc_client = Client(server["url"])
        opc_client.connect()
        obj = {
            "opc_client": opc_client,
            "rabbitmq_connect": connection,
            "id": server["id"],
            "url": server["url"]
        }
        machine_clients.append(obj)

    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(machine_clients)) as executor:
            futures = [executor.submit(process_machine_client, machine_client) for machine_client in machine_clients]

finally:
    for machine_client in machine_clients:
        machine_client["opc_client"].disconnect()