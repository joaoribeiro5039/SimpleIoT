[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)
# Program Explanation

This program is designed to connect to an OPC UA server, read values from specific nodes, and send those values to different messaging systems, such as RabbitMQ, Kafka, and MQTT. It uses the `opcua`, `pika`, `confluent_kafka`, and `paho.mqtt.client` libraries for OPC UA, RabbitMQ, Kafka, and MQTT communication, respectively.

## OPC UA Connection Setup

The program first establishes a connection to the OPC UA server specified by the `OPC_Host` environment variable. It uses the `opcua.Client` class from the `opcua` library to create a client and connect to the OPC UA server using the provided OPC UA host URL. It retrieves the root node and its children to access the OPC UA nodes that hold the desired values.

## Messaging System Integration

The program supports integration with RabbitMQ, Kafka, and MQTT messaging systems. It checks for the presence of specific environment variables to determine whether to enable each messaging system.

### RabbitMQ Integration

The program checks for the presence of the following environment variables to enable RabbitMQ integration:

- `RABBITMQ_BROKER_HOST`: Specifies the RabbitMQ broker host. If not provided, the default value is set to "localhost".
- `RABBITMQ_BROKER_USER`: Specifies the RabbitMQ broker username. If not provided, the default value is set to "admin".
- `RABBITMQ_BROKER_PASSWORD`: Specifies the RabbitMQ broker password. If not provided, the default value is set to "admin".
- `RABBITMQ_BROKER_QUEUE_PREFIX`: Specifies the RabbitMQ queue prefix. If not provided, the default value is set to "server1".

If all the required environment variables are present, the program establishes a connection to the RabbitMQ broker using the `pika` library. It creates a channel and sets up the necessary queues for publishing messages.

### Kafka Integration

The program checks for the presence of the following environment variables to enable Kafka integration:

- `KAFKA_BROKER_HOST`: Specifies the Kafka broker host and port. If not provided, the default value is set to "localhost:29092".
- `KAFKA_PRODUCER_ID`: Specifies the Kafka producer ID. If not provided, the default value is set to "my_producer".
- `KAFKA_PRODUCER_PREFIX`: Specifies the Kafka producer prefix. If not provided, the default value is set to "server1".

If all the required environment variables are present, the program establishes a connection to the Kafka broker using the `confluent_kafka` library. It creates a Kafka producer and configures it with the provided settings.

### MQTT Integration

The program checks for the presence of the following environment variables to enable MQTT integration:

- `MQTT_BROKER_HOST`: Specifies the MQTT broker host. If not provided, the default value is set to "localhost".
- `MQTT_BROKER_PORT`: Specifies the MQTT broker port. If not provided, the default value is set to "1883".
- `MQTT_BROKER_PREFIX`: Specifies the MQTT broker prefix. If not provided, the default value is set to "server1".

If all the required environment variables are present, the program establishes a connection to the MQTT broker using the `paho.mqtt.client` library.

## Publishing OPC UA Values to Messaging Systems

The program continuously loops through the OPC UA nodes and retrieves their values. For each OPC UA value, it creates a JSON object containing the OPC UA node ID, value, and timestamp. The JSON object is then converted to a JSON string.

The program publishes the OPC UA values to the enabled messaging systems as follows:

- RabbitMQ: If RabbitMQ integration is enabled, the program publishes the JSON string to a RabbitMQ queue. The queue name is derived from the `RabbitMQ_Queue` environment variable and the OPC UA node ID.
- Kafka: If Kafka integration is enabled, the program publishes the JSON string to a Kafka topic. The topic name is derived from the `KafkaProducerPref` environment variable and the OPC UA node ID.
- MQTT: If MQTT integration is enabled, the program publishes the JSON string to an MQTT topic. The topic name is derived from the `MQTTBroker_Prefix` environment variable and the OPC UA node ID.

## Program Cleanup

Finally, the program disconnects from the OPC UA server and performs cleanup operations for each enabled messaging system:

- RabbitMQ: If RabbitMQ integration is enabled, the program closes the RabbitMQ connection.
- Kafka: If Kafka integration is enabled, the program flushes and closes the Kafka producer.
- MQTT: If MQTT integration is enabled, the program disconnects from the MQTT broker.

## Usage

To use this program, make sure to set the appropriate environment variables according to the messaging systems you want to integrate with.

Ensure that the OPC UA server is running and accessible at the provided OPC UA host URL (`OPC_Host`).

Start the program, and it will continuously read OPC UA values and publish them to the enabled messaging systems.