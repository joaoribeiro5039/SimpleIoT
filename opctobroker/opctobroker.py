from opcua import Client
import time
import random
import datetime
import numpy as np
import pika
import threading
import os
import json
from confluent_kafka import Producer
import pika

#region Read RabbitMQ Env Variables
global usingRabbit
usingRabbit = False
global RabbitMQBroker
RabbitMQBroker = os.getenv("RABBITMQ_BROKER_HOST")
if RabbitMQBroker is None:
    RabbitMQBroker = "localhost"
else:
    usingRabbit = True

global RabbitMQBroker_user
RabbitMQBroker_user = os.getenv("RABBITMQ_BROKER_USER")
if RabbitMQBroker_user is None:
    RabbitMQBroker_user = "admin"
else:
    usingRabbit = True
    
global RabbitMQBroker_password
RabbitMQBroker_password = os.getenv("RABBITMQ_BROKER_PASSWORD")
if RabbitMQBroker_password is None:
    RabbitMQBroker_password = "admin"
else:
    usingRabbit = True

global RabbitMQ_Queue
RabbitMQ_Queue = os.getenv("RABBITMQ_BROKER_QUEUE_PREFIX")
if RabbitMQ_Queue is None:
    RabbitMQ_Queue = "server1"
else:
    usingRabbit = True

#endregion

#region Read Kafka Env Variables
global usingKafka
usingKafka =True
global KafkaBroker
KafkaBroker = os.getenv("KAFKA_BROKER_HOST")
if KafkaBroker is None:
    KafkaBroker = "localhost:29092"
else:
    usingKafka = True

global KafkaProducerID
KafkaProducerID = os.getenv("KAFKA_PRODUCER_ID")
if KafkaProducerID is None:
    KafkaProducerID = "my_producer"
else:
    usingKafka = True

global KafkaProducerPref
KafkaProducerPref = os.getenv("KAFKA_PRODUCER_PREFIX")
if KafkaProducerPref is None:
    KafkaProducerPref = "server1"
else:
    usingKafka = True
#endregion


global OPC_Host
OPC_Host = os.getenv("OPC_UA_HOST")
if OPC_Host is None:
    OPC_Host = "localhost:4840"

global stopflag
stopflag = False
def browse_nodes_RabbitMQ():
    opc_client = Client( "opc.tcp://" + OPC_Host)
    opc_client.connect()
    node = opc_client.get_root_node()
    childrens = node.get_children()
    
    credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
    connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=credentials)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    try:
        while True:
            for chlid in childrens:
                nodes = chlid.get_children()
                for node in nodes:
                    if "ns=1" in str(node):
                        for childnode in node.get_children():
                            childnodeid = childnode.nodeid
                            value = childnode.get_value()
                            queue_name = RabbitMQ_Queue + "." + childnodeid.Identifier
                            obj = {
                                'value':str(value),
                                'opc_read_time': str(datetime.datetime.now())
                            }
                            obj_json = json.dumps(obj)
                            channel.queue_declare(queue=queue_name)
                            channel.basic_publish(exchange='', routing_key=queue_name, body=obj_json)
    finally:
        opc_client.disconnect()
        connection.close()
        stopflag = True


def browse_nodes_Kafka():
    opc_client = Client( "opc.tcp://" + OPC_Host)
    opc_client.connect()
    node = opc_client.get_root_node()
    childrens = node.get_children()
    
    bootstrap_servers = KafkaBroker
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'my_producer',
        'acks': 'all'
        }

    producer = Producer(producer_config)


    try:
        while True:
            for chlid in childrens:
                nodes = chlid.get_children()
                for node in nodes:
                    if "ns=1" in str(node):
                        for childnode in node.get_children():
                            childnodeid = childnode.nodeid
                            value = childnode.get_value()
                            obj = {
                                'value':str(value),
                                'opc_read_time': str(datetime.datetime.now())
                            }
                            obj_json = json.dumps(obj)
                            topic = KafkaProducerPref + "." + childnodeid.Identifier
                            producer.produce(topic=topic, value=obj_json)
    finally:
        opc_client.disconnect()
        producer.flush()
        producer.close()
        stopflag = True

if usingRabbit:
    background_thread_Rabbit = threading.Thread(target=browse_nodes_RabbitMQ)
    background_thread_Rabbit.daemon = True
    background_thread_Rabbit.start()
    
if usingKafka:
    background_thread_Kafka = threading.Thread(target=browse_nodes_Kafka)
    background_thread_Kafka.daemon = True
    background_thread_Kafka.start() 

    

while not stopflag:
    print("Running")


if usingRabbit:
    background_thread_Rabbit.join()
    
if usingKafka:
    background_thread_Kafka.join()

print("Main program stopped")
