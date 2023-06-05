from fastapi import FastAPI
import asyncio
import datetime
import time
from opcua import Client
from typing import Optional
import pika

global StopFlag

async def Monitor(ocp_url : str, nodestart : str, rabbitmqserver : str): 
    global StopFlag
    client = Client(ocp_url)
    client.connect()
    
    # Establish a connection to RabbitMQ server
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmqserver))
    rabbitmq_channel = rabbitmq_connection.channel()

    while not StopFlag:
        root = client.get_root_node()
        objects = root.get_children()[0]
        nodes = objects.get_children()
        for node in nodes:
            for subnode in node.get_children():
                if nodestart in str(subnode):
                    node_id = str(subnode)
                    value = client.get_node(node_id).get_value()
                    rabbitmq_channel.queue_declare(queue=node_id)
                    rabbitmq_channel.basic_publish(exchange='', routing_key=node_id, body=str(value))

                    print(str(node_id) + " -> " + str(value))
        await asyncio.sleep(0.01)
        
    rabbitmq_connection.close()
    client.disconnect()

app = FastAPI()

#Testing
@app.get("/Testing")
async def root():
    return {"message": "Hello World"}

# Check If OPC UA Server is Available
@app.get("/OPCServer")
def OPCServer(ocp_url : str):
    TestingtUrl = ocp_url
    opc_client = Client(TestingtUrl)
    try:
        opc_client.connect()
        opc_client.disconnect()
        return True
    except:
        return False

# Connect to this OPC Server
@app.post("/ConnectOPCServer")
async def ConnectOPCServer(ocp_url : str, nodestart : str, rabbitmqserver : str,):
    global StopFlag
    StopFlag = False
    asyncio.create_task(Monitor(ocp_url, nodestart, rabbitmqserver))
    return True

# Get Filtered Values of the OPC UA Server
@app.put("/StopClient")
def opcuavalues():
    global StopFlag
    StopFlag = True
    return {True}

#On Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    print("Stopping pending Tasks")
    global StopFlag
    StopFlag = True
    await asyncio.sleep(5)
    print("Shutting down...")