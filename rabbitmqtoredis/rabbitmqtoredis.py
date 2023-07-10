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

global internal_buffer
global start_time

def process_message(channel, method, properties, body):
    global internal_buffer
    global start_time
    new_message = {
        'message': body.decode(),
        '_nodeid': method.routing_key,
        'msg_time': str(datetime.datetime.now())
        }
    internal_buffer.append(new_message)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    this_time = int(time.time())
    timedif = this_time - start_time

    if timedif > 10:
        start_time = int(time.time())
        redis_queues_key = redis_client.get("queues")
        redis_queues_list = json.loads(redis_queues_key.decode())
        for redis_queue_key in redis_queues_list:
            filtered_messages = []
            filtered_messages = [message for message in internal_buffer if message['_nodeid'] == redis_queue_key]
            if len(filtered_messages)>0:
                existed_values = redis_client.get(redis_queue_key)
                if existed_values:
                    existed_data = json.loads(existed_values.decode())
                else:
                    existed_data = []
                existed_data.append(filtered_messages)
                redis_client.set(redis_queue_key, json.dumps(existed_data))
            for added_filter in filtered_messages:
                internal_buffer.remove(added_filter)
try:
    internal_buffer = []
    start_time = int(time.time())
    redis_client.set("queues", json.dumps(queue_list))
    for queue in queue_list:
        channel.basic_consume(queue=queue, on_message_callback=process_message)
    channel.start_consuming()

finally:

    print("Restarting")
    connection.close()
