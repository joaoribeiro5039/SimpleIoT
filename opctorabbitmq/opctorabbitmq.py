from opcua import Client
import time
import random
import datetime
import numpy as np
import pika
import os
import json

import pika

global RabbitMQBroker
RabbitMQBroker = os.getenv("RABBITMQ_BROKER_HOST")
if RabbitMQBroker is None:
    RabbitMQBroker = "localhost"

global RabbitMQBroker_user
RabbitMQBroker_user = os.getenv("RABBITMQ_BROKER_USER")
if RabbitMQBroker_user is None:
    RabbitMQBroker_user = "admin"
    
global RabbitMQBroker_password
RabbitMQBroker_password = os.getenv("RABBITMQ_BROKER_PASSWORD")
if RabbitMQBroker_password is None:
    RabbitMQBroker_password = "admin"


global RabbitMQ_Queue
RabbitMQ_Queue = os.getenv("RABBITMQ_BROKER_QUEUE_PREFIX")
if RabbitMQ_Queue is None:
    RabbitMQ_Queue = "server1"
    
    
global OPC_Host
OPC_Host = os.getenv("OPC_UA_HOST")
if OPC_Host is None:
    OPC_Host = "localhost:4840"
    



global opc_client
opc_client = Client( "opc.tcp://" + OPC_Host)

def browse_nodes(node):
    # Browse the children of the current node
    childrens = node.get_children()
    for chlid in childrens:
        nodes = chlid.get_children()
        for node in nodes:
            if "ns=1" in str(node):
                for childnode in node.get_children():
                    childnodeid = childnode.nodeid
                    value = childnode.get_value()
                    queue_name = RabbitMQ_Queue + "." + childnodeid.Identifier
                    print(queue_name)
                    obj = {
                        'value':str(value),
                        'opc_read_time': str(datetime.datetime.now())
                    }
                    obj_json = json.dumps(obj)
                    channel.queue_declare(queue=queue_name)
                    channel.basic_publish(exchange='', routing_key=queue_name, body=obj_json)

try:
    # Connect to the OPC UA server
    opc_client.connect()
    
    credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
    connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()


    root = opc_client.get_root_node()
    objects = root.get_children()
    root_node = opc_client.get_root_node()
    print(root_node)
    while True:
        browse_nodes(root_node)

finally:
    # Disconnect from the OPC UA server
    opc_client.disconnect()
    connection.close()