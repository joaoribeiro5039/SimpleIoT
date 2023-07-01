from opcua import ua, Server
import time
import random
import datetime
import json
import numpy as np
from confluent_kafka import Producer



global opc_servers
opc_servers = []

global Kafka_Producer

bootstrap_servers = 'cloud:9092'
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'my-producer',
    'acks': 'all'
}
Kafka_Producer = Producer(producer_config)


for i in range(10):
    server = Server()
    server.name = "SimpleOPCUA"
    endpoint = "opc.tcp://0.0.0.0:484" + str(i)
    server.set_endpoint(endpoint)
    obj = {
        "opcserver" : server,
        "id" : i
    }
    opc_servers.append(obj)
    print(i)
    print(endpoint)

# create objects and variables from json file
with open("nodes.json", "r") as f:
    jsonnodes = json.load(f)

for server in opc_servers:
    for node in jsonnodes:
        obj = server["opcserver"].nodes.objects.add_object(node["node_id"], node["name"])
        for var in node["variables"]:
            opc_var = obj.add_variable(var["node_id"], var["name"], var["value"])
            opc_var.set_writable(True)
    server["opcserver"].start()


def get_Temperature_value(time, amplitude):
    frequency = 0.01
    x = amplitude + amplitude * np.sin(2 * np.pi * frequency * time) * np.cos(np.pi * frequency*0.23 * time) + amplitude/5 * np.cos(np.pi * frequency*5 * time)
    x =round(x * random.uniform(0.98, 1.02),3)
    return x

def get_Speed_value(time, amplitude):
    frequency = 0.01
    x = amplitude + amplitude * np.sin(2 * np.pi * frequency * time) * np.cos(np.pi * frequency*0.23 * time) + amplitude/8 * np.cos(np.pi * frequency*4 * time)
    x =round(x * random.uniform(0.98, 1.02),3)
    if x < 0:
        x = x * -1
    return x

def UpdateServerValues(server, starttime):
    end_time = time.time()
    timeElapsed = round(end_time - starttime,6)
    for i in range(4):
        temperature = get_Temperature_value(timeElapsed,10.0 + i*10.0)
        speed = get_Speed_value(timeElapsed,300.0 + i*100.0)
        dt_time = datetime.datetime.now()
        data = {
            'Temperature': str(temperature),
            'Speed': str(speed),
            'DateTime': str(dt_time)
            }
        server["opcserver"].get_node("ns=1;s=Motor" + str(i+1) + ".DateTime").set_value(dt_time)
        server["opcserver"].get_node("ns=1;s=Motor" + str(i+1) + ".Temperature").set_value(temperature)
        server["opcserver"].get_node("ns=1;s=Motor" + str(i+1) + ".Speed").set_value(speed)

        topic =  "Server_" + str(server["id"]) + "_Motor_" + str(i+1)
        print(topic)
        data_str = json.dumps(data)
        Kafka_Producer.produce(topic, value=data_str)
try:
    start_time = time.time()
    while True:
        start_time_Timer = time.time()
        for server in opc_servers:
            UpdateServerValues(server,start_time)
        Kafka_Producer.flush()
        end_time_Timer = time.time()
        print(end_time_Timer - start_time_Timer)

finally:
    for server in opc_servers:
        server["opcserver"].stop()



