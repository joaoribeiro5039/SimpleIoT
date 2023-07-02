import pika
import time
import json
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import concurrent.futures
import uuid

global rabbitmq_queues
rabbitmq_queues = []
for i in range(10):
    for imotor in range(1,6):
        queue = "Server_" + str(i) + "_Motor_" + str(imotor)
        credentials = pika.PlainCredentials('admin', 'admin')
        connection_params = pika.ConnectionParameters('rabbitmq', credentials=credentials)
        connection = pika.BlockingConnection(connection_params)
        rabbitmq_channel = connection.channel()
        obj = {
            "queue" : queue,
            "channel" :rabbitmq_channel
        }
        rabbitmq_queues.append(obj)

cassandra_host = "cassandra"
cassandra_keyspace = "simpleiot"

cluster = Cluster([cassandra_host])
session = cluster.connect()
session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':3}}")
session.set_keyspace(cassandra_keyspace)

for rabbitmq_queue in rabbitmq_queues:
    query = "CREATE TABLE IF NOT EXISTS {} (id UUID,message TEXT,temperature FLOAT,speed FLOAT,datetime TEXT,PRIMARY KEY (id,datetime))".format(rabbitmq_queue["queue"])
    prepared_query = session.prepare(query)
    session.execute(prepared_query)

def process_message(channel, method, properties, body):

    table = method.routing_key
    
    message = body.decode()
    json_data = json.loads(message)
    _temperature = float(json_data["Temperature"])
    _speed = float(json_data["Speed"])
    _datetime = json_data["DateTime"]
    query = "INSERT INTO {} (id, message, temperature, speed, datetime) VALUES (?, ?, ?, ?, ?)".format(table)
    prepared_query = session.prepare(query)
    session.execute(prepared_query, (uuid.uuid4(), message, _temperature, _speed, _datetime))

    channel.basic_ack(delivery_tag=method.delivery_tag)

for rabbitmq_queue in rabbitmq_queues:
    rabbitmq_queue["channel"].basic_consume(queue=rabbitmq_queue["queue"], on_message_callback=process_message)
    

def process_machine_client(rmq_channel):
    rmq_channel.start_consuming()

try:
    while True:
        print("Processing")
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(rabbitmq_queues)) as executor:
            futures = [executor.submit(process_machine_client, rmq_channel["channel"]) for rmq_channel in rabbitmq_queues]
finally:
    print("Restarting")
    session.shutdown()
    cluster.shutdown()
