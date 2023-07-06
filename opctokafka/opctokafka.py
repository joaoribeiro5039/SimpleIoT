from opcua import Client
import time
import random
import datetime
import numpy as np
import os
import json

from confluent_kafka import Producer


global KafkaBroker
KafkaBroker = os.getenv("KAFKA_BROKER_HOST")
if KafkaBroker is None:
    KafkaBroker = "localhost:29092"

global KafkaProducerID
KafkaProducerID = os.getenv("KAFKA_PRODUCER_ID")
if KafkaProducerID is None:
    KafkaProducerID = "my_producer"

global KafkaProducerPref
KafkaProducerPref = os.getenv("KAFKA_PRODUCER_PREFIX")
if KafkaProducerPref is None:
    KafkaProducerPref = "Server1"

global OPC_Host
OPC_Host = os.getenv("OPC_UA_HOST")
if OPC_Host is None:
    OPC_Host = "localhost:4840"
    



global opc_client
opc_client = Client( "opc.tcp://" + OPC_Host)

def browse_nodes(node):
    childrens = node.get_children()
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

global producer
opc_client.connect()
bootstrap_servers = KafkaBroker
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'my_producer',
    'acks': 'all'
    }

producer = Producer(producer_config)
try:
    root = opc_client.get_root_node()
    objects = root.get_children()
    root_node = opc_client.get_root_node()
    print(root_node)
    while True:
        start_time_Timer = time.time()
        browse_nodes(root_node)
        producer.flush()
        end_time_Timer = time.time()
        print(end_time_Timer - start_time_Timer)


finally:
    # Disconnect from the OPC UA server
    opc_client.disconnect()
    # Close the Kafka producer
    producer.close()