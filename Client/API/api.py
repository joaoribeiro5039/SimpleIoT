from fastapi import FastAPI
import asyncio
import datetime
import time
from opcua import Client
from typing import Optional
import pika

global LineName
global opc_client
global rabbitmq_connection
global rabbitmq_channel

def data_change_handler(node, value, data_type):
    global rabbitmq_channel
    rabbitmq_channel.queue_declare(queue=node)
    rabbitmq_channel.basic_publish(exchange='', routing_key=node, body=str(value))



app = FastAPI()


#On Shutdown
@app.on_event("startup")
async def shutdown_event():
    print("Starting API")
    await asyncio.sleep(2)


#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}

# Check If OPC UA Server is Available
@app.get("/OPCServer")
def OPCServer(ocp_url : str):
    TestingtUrl = ocp_url
    opc_test_client = Client(TestingtUrl)
    try:
        opc_test_client.connect()
        opc_test_client.disconnect()
        return True
    except:
        return False

# Connect to this OPC Server
@app.post("/StartClient")
async def ConnectOPCServer(ocp_url : str, rabbitmqserver : str,):
    global opc_client
    global rabbitmq_connection
    global LineName
    if opc_client.isconnected():
        opc_client.disconnect()

    opc_client = Client(ocp_url)
    opc_client.connect()
    root = opc_client.get_root_node()
    objects = root.get_children()[0]
    nodes = objects.get_children()
    
    global rabbitmq_connection
    global rabbitmq_channel
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmqserver))
    rabbitmq_channel = rabbitmq_connection.channel()

    for node in nodes:
        for subnode in node.get_children():
            if LineName in str(subnode):
                node_id = str(subnode)
                subscription = opc_client.create_subscription(100, data_change_handler)
                monitored_item = subscription.subscribe_data_change(node_id)
                subscription.start()
    return True

# Get Filtered Values of the OPC UA Server
@app.put("/StopClient")
def opcuavalues():
    global opc_client
    global rabbitmq_connection
    rabbitmq_connection.close()
    opc_client.disconnect()
    return {True}

# Get Filtered Values of the OPC UA Server
@app.put("/SetLine")
def opcuavalues(line : str):
    global LineName
    LineName = line
    return LineName

#On Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    print("Stopping pending Tasks")
    await asyncio.sleep(2)
    print("Shutting down...")