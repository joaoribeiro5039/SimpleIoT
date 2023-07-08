![alt text](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/doc/diagram.png)
# Container Descriptions

This document provides an overview of the containers used in the project. Each container serves a specific purpose and contributes to the overall functionality of the system.

## opctobroker

- **Container Name**: opctobroker
- **Image**: joaoribeiro5039/opctobroker:latest

The `opctobroker` container acts as a bridge between the OPC-UA server and multiple message brokers, including RabbitMQ, Kafka, and MQTT. It facilitates the exchange of data between the OPC-UA server and these brokers. The container is responsible for reading OPC-UA values, formatting them as JSON, and publishing them to the respective message brokers. It requires the following environment variables to be set:

- `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker.
- `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication.
- `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication.
- `RABBITMQ_BROKER_QUEUE_PREFIX`: Prefix for RabbitMQ queues.
- `OPC_UA_HOST`: Hostname or IP address of the OPC-UA server.
- `KAFKA_BROKER_HOST`: Hostname or IP address of the Kafka broker.
- `KAFKA_PRODUCER_ID`: ID for the Kafka producer.
- `KAFKA_PRODUCER_PREFIX`: Prefix for Kafka topics.
- `MQTT_BROKER_HOST`: Hostname or IP address of the MQTT broker.
- `MQTT_BROKER_PORT`: Port number of the MQTT broker.
- `MQTT_BROKER_PREFIX`: Prefix for MQTT topics.

 [Source Code Documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/opctobroker/README.md)


## rabbitmqtocassandra

- **Container Name**: rabbitmqtocassandra
- **Image**: joaoribeiro5039/rabbitmqtocassandra:latest

The `rabbitmqtocassandra` container consumes messages from RabbitMQ and stores them in an Apache Cassandra database. It subscribes to RabbitMQ queues with the configured prefix, retrieves the messages, and saves them in Cassandra. The container requires the following environment variables:

- `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker.
- `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication.
- `RABBITMQ_BROKER_QUEUE_PREFIX`: Prefix for RabbitMQ queues.
- `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication.
- `CASSANDRA_DB_HOST`: Hostname or IP address of the Cassandra database.
- `CASSANDRA_DB_TABLENAME`: Name of the Cassandra table where the messages will be stored.

 [Source Code Documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/rabbitmqtocassandra/README.md)

## opcwriter

- **Container Name**: opcwriter
- **Image**: joaoribeiro5039/opcwriter:latest

The `opcwriter` container provides an HTTP API for accessing OPC-UA data. It exposes port 8000, allowing clients to retrieve and modify OPC-UA values using standard HTTP requests. This container serves as an interface for interacting with the OPC-UA server. No additional environment variables are required.

 [Source Code Documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/opcwriter/README.md)

Please note that the `latest` tag used in the image names assumes that the latest version of each container is being used. It's recommended to use specific version tags for production deployments to ensure stability and compatibility.

Ensure that you have the necessary environment variables set appropriately and run the containers using the provided configuration.


 [TestRun](https://youtu.be/3exYziLz77w)