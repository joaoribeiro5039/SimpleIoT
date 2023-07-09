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
import paho.mqtt.client as mqtt
import platform

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
    RabbitMQ_Queue = platform.node()
else:
    usingRabbit = True

#endregion

#region Read Kafka Env Variables
global usingKafka
usingKafka = False
global KafkaBroker
KafkaBroker = os.getenv("KAFKA_BROKER_HOST")
if KafkaBroker is None:
    KafkaBroker = "localhost:29092"
else:
    usingKafka = True

global KafkaProducerid
KafkaProducerid = os.getenv("KAFKA_PRODUCER_ID")
if KafkaProducerid is None:
    KafkaProducerid = platform.node()
else:
    usingKafka = True

global KafkaProducerPref
KafkaProducerPref = os.getenv("KAFKA_PRODUCER_PREFIX")
if KafkaProducerPref is None:
    KafkaProducerPref = platform.node()
else:
    usingKafka = True
#endregion


#region Read Mqtt Env Variables
global usingmqtt
usingmqtt = False
global MQTTBroker_Host
MQTTBroker_Host = os.getenv("MQTT_BROKER_HOST")
if MQTTBroker_Host is None:
    MQTTBroker_Host = "localhost"
else:
    usingmqtt = True
    
global MQTTBroker_Port
MQTTBroker_Port = os.getenv("MQTT_BROKER_PORT")
if MQTTBroker_Port is None:
    MQTTBroker_Port = "1883"
else:
    usingmqtt = True

global MQTTBroker_Prefix
MQTTBroker_Prefix = os.getenv("MQTT_BROKER_PREFIX")
if MQTTBroker_Prefix is None:
    MQTTBroker_Prefix = platform.node()
else:
    usingmqtt = True
#endregion

global OPC_Host
OPC_Host = os.getenv("OPC_UA_HOST")
if OPC_Host is None:
    OPC_Host = "localhost:4840"

try:
    opc_client = Client( "opc.tcp://" + OPC_Host)
    opc_client.connect()
    node = opc_client.get_root_node()
    childrens = node.get_children()

    if usingRabbit:
            rabbit_credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
            rabbit_connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=rabbit_credentials)
            rabbit_connection = pika.BlockingConnection(rabbit_connection_params)
            rabbit_channel = rabbit_connection.channel()

    if usingKafka:
        kafka_bootstrap_servers = KafkaBroker
        kafka_producer_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'client.id': KafkaProducerid,
            'acks': 'all'
            }
        kafka_producer = Producer(kafka_producer_config)
    
    if usingmqtt:
        mqtt_client = mqtt.Client()
        mqtt_client.connect(MQTTBroker_Host, int(MQTTBroker_Port))

    while True:
        for chil in childrens:
            nodes = chil.get_children()
            for node in nodes:
                if "ns=1" in str(node):
                    for childnode in node.get_children():
                        childnodeid = childnode.nodeid
                        value = childnode.get_value()
                        obj = {
                            'nodeid': str(node),
                            'value':str(value),
                            'opc_read_time': str(datetime.datetime.now())
                        }
                        obj_json = json.dumps(obj)

                        kafkatopic = KafkaProducerPref + "." + childnodeid.Identifier
                        
                        if usingKafka:
                            kafka_producer.produce(topic=kafkatopic, value=obj_json)

                        queue_name = RabbitMQ_Queue + "." + childnodeid.Identifier
                        if usingRabbit:
                            rabbit_channel.queue_declare(queue=queue_name)
                            rabbit_channel.basic_publish(exchange='', routing_key=queue_name, body=obj_json)

                        mqtttopic = MQTTBroker_Prefix + "." + childnodeid.Identifier
                        if usingmqtt:
                            mqtt_client.publish(mqtttopic,obj_json)

finally:

    opc_client.disconnect()
    
    if usingKafka:
        kafka_producer.flush()
        kafka_producer.close()
    
    if usingRabbit:
        rabbit_connection.close()

    if usingmqtt:
        mqtt_client.disconnect()
