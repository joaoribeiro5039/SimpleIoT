import pika
import time
import json
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import concurrent.futures
import uuid
import os
import requests
import datetime

global RabbitMQBroker
RabbitMQBroker = os.getenv("RABBITMQ_BROKER_HOST")
if RabbitMQBroker is None:
    RabbitMQBroker = "localhost"


global RabbitMQ_Queue
RabbitMQ_Queue = os.getenv("RABBITMQ_BROKER_QUEUE_PREFIX")
if RabbitMQ_Queue is None:
    RabbitMQ_Queue = "server"

global RabbitMQBroker_user
RabbitMQBroker_user = os.getenv("RABBITMQ_BROKER_USER")
if RabbitMQBroker_user is None:
    RabbitMQBroker_user = "admin"
    
global RabbitMQBroker_password
RabbitMQBroker_password = os.getenv("RABBITMQ_BROKER_PASSWORD")
if RabbitMQBroker_password is None:
    RabbitMQBroker_password = "admin"


global CassandraDB
CassandraDB = os.getenv("CASSANDRA_DB_HOST")
if CassandraDB is None:
    CassandraDB = "localhost"

global TableName
TableName = os.getenv("CASSANDRA_DB_TABLENAME")
if TableName is None:
    TableName = "Server1"

global connection
credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=credentials)
connection = pika.BlockingConnection(connection_params)
global channel
channel = connection.channel()

global queue_list
queue_list= []
response = requests.get("http://" + RabbitMQBroker + ":15672/api/queues", auth=(RabbitMQBroker_user, RabbitMQBroker_password))
if response.status_code == 200:
    all_queue_list = [queue['name'] for queue in response.json()]
    for queu in all_queue_list:
        if RabbitMQ_Queue in queu:
            queue_list.append(queu)
else:
    print('Failed to retrieve queue list from RabbitMQ Management API.')




cassandra_host = CassandraDB
cassandra_keyspace = "simpleiot"

cluster = Cluster([cassandra_host])
session = cluster.connect()

session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':3}}")
session.set_keyspace(cassandra_keyspace)

query = "CREATE TABLE IF NOT EXISTS {} (id UUID,nodeid TEXT, value TEXT,opc_read_time TEXT,cassandra_write_time TEXT,PRIMARY KEY (id))".format(TableName)
prepared_query = session.prepare(query)
session.execute(prepared_query)

def process_message(channel, method, properties, body):
    message = body.decode()
    _nodeid = method.routing_key
    query = "INSERT INTO {} (id, nodeid, value,opc_read_time,cassandra_write_time) VALUES (?, ?, ?, ?, ?)".format(TableName)
    prepared_query = session.prepare(query)
    msg_obj = json.loads(message)
    msg_value = msg_obj['value']
    msg_opcread = msg_obj['opc_read_time']
    msg_time = str(datetime.datetime.now())
    try:
        session.execute(prepared_query, (uuid.uuid4(), _nodeid, msg_value ,msg_opcread, msg_time))
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except:
        print("Message not delivered")

try:

    for queue in queue_list:
        channel.basic_consume(queue=queue, on_message_callback=process_message)
    channel.start_consuming()

finally:

    print("Restarting")
    session.shutdown()
    cluster.shutdown()
    connection.close()