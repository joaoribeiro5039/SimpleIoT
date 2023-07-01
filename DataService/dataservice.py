import pika
from cassandra.cluster import Cluster
import concurrent.futures

# RabbitMQ connection parameters

global rabbitmq_queues
rabbitmq_queues = []
for i in range(10):
    for imotor in range(1,6):
        queue = "Server_" + str(i) + "_Motor_" + str(imotor)
        credentials = pika.PlainCredentials('admin', 'admin')
        connection_params = pika.ConnectionParameters('localhost', credentials=credentials)
        connection = pika.BlockingConnection(connection_params)
        rabbitmq_channel = connection.channel()
        obj = {
            "queue" : queue,
            "channel" :rabbitmq_channel
        }
        rabbitmq_queues.append(obj)

# Cassandra connection parameters
cassandra_host = "localhost"
cassandra_keyspace = "simpleiot"

# Connect to RabbitMQ


# Connect to Cassandra
cluster = Cluster([cassandra_host])
session = cluster.connect()
session.execute(f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor':3}}")
session.set_keyspace(cassandra_keyspace)

# Create tables in Cassandra if they don't exist
for rabbitmq_queue in rabbitmq_queues:
    session.execute("CREATE TABLE IF NOT EXISTS "+ rabbitmq_queue["queue"] +  " (id UUID PRIMARY KEY,message TEXT)")

# Callback function to process messages from RabbitMQ
def process_message(channel, method, properties, body):
    table = method.routing_key
    # Write message to the corresponding table in Cassandra
    
    session.execute(f"INSERT INTO {table} (id, message) VALUES (uuid(), %s)", (body.decode(),))

    # Acknowledge the message to remove it from the queue
    channel.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages from RabbitMQ queues

for rabbitmq_queue in rabbitmq_queues:
    rabbitmq_queue["channel"].basic_consume(queue=rabbitmq_queue["queue"], on_message_callback=process_message)
    

def process_machine_client(rmq_channel):
    rmq_channel.start_consuming()


print(len(rabbitmq_queues))
with concurrent.futures.ThreadPoolExecutor(max_workers=len(rabbitmq_queues)) as executor:
    futures = [executor.submit(process_machine_client, rmq_channel["channel"]) for rmq_channel in rabbitmq_queues]
