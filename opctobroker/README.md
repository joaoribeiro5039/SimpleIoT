[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)

# OPC-UA Data Publisher

This project implements an OPC-UA data publisher that reads values from an OPC-UA server and publishes them to various message brokers such as RabbitMQ, Apache Kafka, and MQTT. The values are published in JSON format, including the OPC-UA node ID, value, and timestamp.

## Installation

To run the OPC-UA Data Publisher, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
3. Set the necessary environment variables based on your configuration. The variables include:

   - `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker (optional).
   - `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication (optional).
   - `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication (optional).
   - `RABBITMQ_BROKER_QUEUE_PREFIX`: Prefix for RabbitMQ queues (optional).

   - `KAFKA_BROKER_HOST`: Hostname or IP address of the Kafka broker (optional).
   - `KAFKA_PRODUCER_ID`: ID for the Kafka producer (optional).
   - `KAFKA_PRODUCER_PREFIX`: Prefix for Kafka topics (optional).

   - `MQTT_BROKER_HOST`: Hostname or IP address of the MQTT broker (optional).
   - `MQTT_BROKER_PORT`: Port number of the MQTT broker (optional).
   - `MQTT_BROKER_PREFIX`: Prefix for MQTT topics (optional).

   - `OPC_UA_HOST`: Hostname or IP address of the OPC-UA server.

4. Run the OPC-UA Data Publisher with the following command:
   ```
   python opcpublisher.py
   ```

The publisher will start reading values from the OPC-UA server and publishing them to the configured message brokers.

## Message Brokers

### RabbitMQ

If the RabbitMQ environment variables are set, the OPC-UA data publisher will publish messages to RabbitMQ queues. The messages will be sent with the specified queue prefix followed by the OPC-UA node ID. The default prefix is "server1".

### Kafka

If the Kafka environment variables are set, the OPC-UA data publisher will publish messages to Kafka topics. The messages will be sent with the specified topic prefix followed by the OPC-UA node ID. The default prefix is "server1".

### MQTT

If the MQTT environment variables are set, the OPC-UA data publisher will publish messages to MQTT topics. The messages will be sent with the specified topic prefix followed by the OPC-UA node ID. The default prefix is "server1".

## OPC-UA Server

The OPC-UA server connection details are specified using the `OPC_UA_HOST` environment variable. Provide the hostname or IP address of the OPC-UA server. The default port is 4840.

## On Shutdown

The OPC-UA data publisher gracefully shuts down when the application is terminated. Upon shutdown, the publisher disconnects from the OPC-UA server and closes connections to the message brokers.

Feel free to modify and extend this code to meet your specific requirements, such as adding additional message brokers or customizing the data format.