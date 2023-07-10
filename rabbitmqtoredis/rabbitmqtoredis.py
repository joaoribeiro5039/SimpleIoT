import pika
import time
import json
import redis
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
    RabbitMQ_Queue = "all"

global RabbitMQBroker_user
RabbitMQBroker_user = os.getenv("RABBITMQ_BROKER_USER")
if RabbitMQBroker_user is None:
    RabbitMQBroker_user = "admin"
    
global RabbitMQBroker_password
RabbitMQBroker_password = os.getenv("RABBITMQ_BROKER_PASSWORD")
if RabbitMQBroker_password is None:
    RabbitMQBroker_password = "admin"


global RedisDB
RedisDB = os.getenv("REDIS_DB_HOST")
if RedisDB is None:
    RedisDB = "localhost"

global connection
credentials = pika.PlainCredentials(RabbitMQBroker_user, RabbitMQBroker_password)
connection_params = pika.ConnectionParameters(RabbitMQBroker, credentials=credentials)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

global queue_list
queue_list= []
response = requests.get("http://" + RabbitMQBroker + ":15672/api/queues", auth=(RabbitMQBroker_user, RabbitMQBroker_password))
if response.status_code == 200:
    all_queue_list = [queue['name'] for queue in response.json()]
    for queu in all_queue_list:
        if RabbitMQ_Queue == "all":
                queue_list.append(queu)
        else:
            if RabbitMQ_Queue in queu:
                queue_list.append(queu)
else:
    print('Failed to retrieve queue list from RabbitMQ Management API.')

redis_client = redis.Redis(host=RedisDB, port=6379)

def process_message(channel, method, properties, body):
    starttime = datetime.datetime.now()
    message = body.decode()
    _nodeid = method.routing_key
    msg_obj = json.loads(message)
    msg_time = str(datetime.datetime.now())
    try:
        redis_key = _nodeid
        value = redis_client.get(redis_key)
        if value:
            objects = json.loads(value.decode())
        else:
            objects = []
        new_object = {
            'value': msg_obj,
            'timestamp': msg_time
        }
        objects.append(new_object)
        updated_value = json.dumps(objects)
        redis_client.set(redis_key, updated_value)
        updated_value = redis_client.get(redis_key)
        updated_objects = json.loads(updated_value.decode())
        if new_object in updated_objects:
            channel.basic_ack(delivery_tag=method.delivery_tag)
    except:
        print("Message not delivered")

    endtime = datetime.datetime.now()
    print(endtime = starttime)

try:
    for queue in queue_list:
        channel.basic_consume(queue=queue, on_message_callback=process_message)
    channel.start_consuming()

finally:

    print("Restarting")
    connection.close()
