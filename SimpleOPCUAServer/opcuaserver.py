from opcua import ua, Server
import time
import random
import datetime
import json
import numpy as np



# create server
server = Server()
server.name = "SimpleOPCUA"
server.set_endpoint("opc.tcp://localhost:4840")

# create objects and variables from json file
with open("nodes.json", "r") as f:
    jsonnodes = json.load(f)

for node in jsonnodes:
    obj = server.nodes.objects.add_object(node["node_id"], node["name"])
    for var in node["variables"]:
        opc_var = obj.add_variable(var["node_id"], var["name"], var["value"])
        opc_var.set_writable(True)

# start server
server.start()

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

try:
    start_time = time.time()
    while True:
        time.sleep(0.01)
        end_time = time.time()
        timeElapsed = round(end_time - start_time,6)
        for node in jsonnodes:
            for var in node["variables"]:
                var_node = server.get_node(var["node_id"])
                if "Motor1" in str(var_node):
                    if "Temperature" in str(var_node):
                        var_node.set_value(get_Temperature_value(timeElapsed,10.0))
                    if "Speed" in str(var_node):
                        var_node.set_value(get_Speed_value(timeElapsed,300.0))
                    
                if "Motor2" in str(var_node):
                    if "Temperature" in str(var_node):
                        var_node.set_value(get_Temperature_value(timeElapsed,20.0))
                    if "Speed" in str(var_node):
                        var_node.set_value(get_Speed_value(timeElapsed,400.0))
                    
                if "Motor3" in str(var_node):
                    if "Temperature" in str(var_node):
                        var_node.set_value(get_Temperature_value(timeElapsed,30.0))
                    if "Speed" in str(var_node):
                        var_node.set_value(get_Speed_value(timeElapsed,500.0))
                    
                if "Motor4" in str(var_node):
                    if "Temperature" in str(var_node):
                        var_node.set_value(get_Temperature_value(timeElapsed,40.0))
                    if "Speed" in str(var_node):
                        var_node.set_value(get_Speed_value(timeElapsed,600.0))
                    
                if "Motor5" in str(var_node):
                    if "Temperature" in str(var_node):
                        var_node.set_value(get_Temperature_value(timeElapsed,50.0))
                    if "Speed" in str(var_node):
                        var_node.set_value(get_Speed_value(timeElapsed,700.0))
                
                if "DateTime" in var["name"]:
                    var_node.set_value(datetime.datetime.now())



finally:
    server.stop()



