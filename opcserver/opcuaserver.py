from opcua import ua, Server
import time
import random
import datetime
import json
import numpy as np

global server

server = Server()
server.name = "SimpleOPCUA"
endpoint = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(endpoint)

print(endpoint)

with open("nodes.json", "r") as f:
    jsonnodes = json.load(f)

for node in jsonnodes:

    obj = server.nodes.objects.add_object(node["node_id"], node["name"])
    for var in node["variables"]:
        opc_var = obj.add_variable(var["node_id"], var["name"], var["value"])
        opc_var.set_writable(True)

server.start()


def get_Temperature_value(time, amplitude):
    frequency = 0.01
    x = amplitude + amplitude * np.sin(2 * np.pi * frequency * time) * np.cos(np.pi * frequency*0.23 * time) + amplitude/5 * np.cos(np.pi * frequency*5 * time)
    x =round(x * random.uniform(0.99, 1.01),3)
    return x

def get_Speed_value(time, amplitude):
    frequency = 0.01
    x = amplitude + amplitude * np.sin(2 * np.pi * frequency * time) * np.cos(np.pi * frequency*0.23 * time) + amplitude/8 * np.cos(np.pi * frequency*4 * time)
    x =round(x * random.uniform(0.99, 1.01),3)
    if x < 0:
        x = x * -1
    return x

def UpdateServerValues(starttime):
    end_time = time.time()
    timeElapsed = round(end_time - starttime,6)
    dt_time = datetime.datetime.now()
    for i in range(1,6):
        temperature = get_Temperature_value(timeElapsed,5.0 + i*10.0)
        speed = get_Speed_value(timeElapsed,200.0 + i*100.0)
        server.get_node("ns=1;s=Motor" + str(i) + ".DateTime").set_value(dt_time)
        server.get_node("ns=1;s=Motor" + str(i) + ".Temperature").set_value(temperature)
        server.get_node("ns=1;s=Motor" + str(i) + ".Speed").set_value(speed)
try:
    start_time = time.time()
    while True:
        time.sleep(0.04)
        start_time_Timer = time.time()
        UpdateServerValues(start_time)
        end_time_Timer = time.time()
        print(end_time_Timer - start_time_Timer)

finally:
    server.stop()



