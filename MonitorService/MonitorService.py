import datetime
import time
from opcua import Client
from opcua import ua
import json
import datetime

global LineName
global opc_client

opc_client = Client("opc.tcp://machine:4843")
opc_client.connect()
root = opc_client.get_root_node()
objects = root.get_children()[0]
nodes = objects.get_children()

while True:
    time.sleep(1)
    for node in nodes:
            for subnode in node.get_children():
                node_id = str(subnode)
                if "ns=1" in node_id:
                    value = opc_client.get_node(node_id).get_value()
                    timestamp = datetime.datetime.now()
                    timestamp_str = timestamp.isoformat()
                    message = {
                            'Node': node_id,
                            'TimeStamp': timestamp_str,
                            'Value': str(value)
                        }
                    message_str = json.dumps(message)
                    print(message_str)