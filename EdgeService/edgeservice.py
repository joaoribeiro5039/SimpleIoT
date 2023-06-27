import datetime
import time
from opcua import Client
from opcua import ua
from typing import Optional
import pika
import json
import datetime

global LineName
global opc_client
global rabbitmq_connection
global rabbitmq_channel


rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('admin', 'admin')))
rabbitmq_channel = rabbitmq_connection.channel()
opc_client = Client("opc.tcp://localhost:4840")
opc_client.connect()

root = opc_client.get_root_node()
objects = root.get_children()[0]
nodes = objects.get_children()

while True:
    time.sleep(0.01)
    for node in nodes:
            for subnode in node.get_children():
                node_id = str(subnode)
                if "ns=1" in node_id:
                    value = opc_client.get_node(node_id).get_value()
                    rabbitmq_channel.queue_declare(queue=node_id)
                    timestamp = datetime.datetime.now()
                    timestamp_str = timestamp.isoformat()
                    message = {
                            'Node': node_id,
                            'TimeStamp': timestamp_str,
                            'Value': str(value)
                        }
                    message_str = json.dumps(message)
                    rabbitmq_channel.basic_publish(exchange='', routing_key=node_id, body=message_str)