import pika
import time
import json
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import concurrent.futures
import uuid
import os
import requests

global RabbitMQBroker
RabbitMQBroker = os.getenv("RABBITMQ_BROKER_HOST")
if RabbitMQBroker is None:
    RabbitMQBroker = "rabbitmq"


global RabbitMQ_Queue
RabbitMQ_Queue = os.getenv("RABBITMQ_BROKER_QUEUE_PREFIX")
if RabbitMQ_Queue is None:
    RabbitMQ_Queue = "server1"

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
    CassandraDB = "cassandra"

global TableName
TableName = os.getenv("CASSANDRA_DB_TABLENAME")
if TableName is None:
    TableName = "Server1"

response = requests.get("http://" + RabbitMQBroker + ":15672/api/queues", auth=(RabbitMQBroker_user, RabbitMQBroker_password))
if response.status_code == 200:
    all_queue_list = [queue['name'] for queue in response.json()]
else:
    print('Failed to retrieve queue list from RabbitMQ Management API.')

global queue_list
queue_list= []
for queu in RabbitMQ_Queue:
    if RabbitMQ_Queue in queu:
        queue_list.append(queu)


credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=credentials)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

cassandra_host = CassandraDB
cassandra_keyspace = "simpleiot"

cluster = Cluster([cassandra_host])
session = cluster.connect()

session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':3}}")
session.set_keyspace(cassandra_keyspace)

query = "CREATE TABLE IF NOT EXISTS {} (id UUID,nodeid TEXT, value TEXT,PRIMARY KEY (id))".format(TableName)
prepared_query = session.prepare(query)
session.execute(prepared_query)

def process_message(channel, method, properties, body):
    message = body.decode()
    _nodeid = method.routing_key
    query = "INSERT INTO {} (id, nodeid, value) VALUES (?, ?, ?)".format(TableName)
    prepared_query = session.prepare(query)
    session.execute(prepared_query, (uuid.uuid4(), _nodeid, message))

    channel.basic_ack(delivery_tag=method.delivery_tag)

try:
    
    for queue in queue_list:
        channel.basic_consume(queue=queue, on_message_callback=process_message)
    print("Processing")
    channel.start_consuming()
finally:

    print("Restarting")
    session.shutdown()
    cluster.shutdown()
    connection.close()
