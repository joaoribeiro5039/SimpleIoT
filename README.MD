![alt text](https://github.com/joaoribeiro5039/SimpleIoT/doc/diagram.png?raw=true)

## Service Documentation

This documentation provides information on the different services defined in the provided `docker-compose.yml` file.

### rabbitmq
- Image: rabbitmq:3.9.11-management
- Ports:
  - 5672:5672 (AMQP port)
  - 15672:15672 (Management UI port)
- Environment variables:
  - RABBITMQ_DEFAULT_USER=admin
  - RABBITMQ_DEFAULT_PASS=admin
- Volumes:
  - rabbitmq_data:/var/lib/rabbitmq
- Restart: always
- Dependencies: opcuaserver

This service sets up a RabbitMQ message broker with RabbitMQ Management UI. It exposes ports for AMQP (5672) and the management UI (15672). It uses the `admin` username and password for authentication. The data directory of RabbitMQ is mounted to a volume named `rabbitmq_data`. The service will restart automatically and depends on the `opcuaserver` service.

### cassandra
- Image: cassandra:latest
- Ports:
  - 9042:9042 (Cassandra native transport port)
- Volumes:
  - cassandra-data:/var/lib/cassandra

This service sets up a Cassandra database server. It exposes the Cassandra native transport port (9042). The data directory of Cassandra is mounted to a volume named `cassandra-data`.

### opcuaserver
- Image: joaoribeiro5039/opcuaserver:latest
- Ports:
  - 4840:4840

This service sets up an OPC UA server. It exposes port 4840 for OPC UA communication.

### opctorabbitmq
- Image: joaoribeiro5039/opctorabbitmq:latest
- Environment variables:
  - RABBITMQ_BROKER_HOST=rabbitmq
  - RABBITMQ_BROKER_USER=admin
  - RABBITMQ_BROKER_PASSWORD=admin
  - RABBITMQ_BROKER_QUEUE=server1
  - OPC_UA_HOST=opcuaserver:4840
- Restart: always
- Dependencies: rabbitmq

This service connects to the RabbitMQ broker (`rabbitmq`) and OPC UA server (`opcuaserver`). It communicates with RabbitMQ using the provided host, username, password, and queue name. It also specifies the OPC UA server host.

# OPC UA to RabbitMQ Data Publisher

The OPC UA to RabbitMQ Data Publisher is a Python script that reads data from an OPC UA server and publishes it to RabbitMQ queues. It uses the `opcua` library for OPC UA communication and the `pika` library for RabbitMQ integration.

## Dependencies

- `opcua`: A Python library for interacting with OPC UA servers.
- `pika`: A Python library for interacting with RabbitMQ message broker.

Make sure to install these dependencies using `pip` before running the script.

## Environment Variables

The script utilizes the following environment variables:

- `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker. Defaults to "rabbitmq" if not provided.
- `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication. Defaults to "admin" if not provided.
- `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication. Defaults to "admin" if not provided.
- `RABBITMQ_BROKER_QUEUE`: Name of the RabbitMQ queue to publish the data. Defaults to "server1" if not provided.
- `OPC_UA_HOST`: Hostname or IP address of the OPC UA server with the port. Defaults to "opcuaserver:4840" if not provided.

Ensure that you have set these environment variables with the appropriate values before running the script.

## Code Overview

The script performs the following steps:

1. Imports the required libraries and sets up variables based on the provided environment variables.
2. Connects to the OPC UA server using the provided host.
3. Establishes a connection to RabbitMQ using the provided credentials.
4. Defines the `browse_nodes` function to browse the OPC UA server's nodes and publish the data to the corresponding RabbitMQ queue.
5. Calls the `browse_nodes` function to start publishing data.
6. Disconnects from the OPC UA server and closes the RabbitMQ connection when the script is terminated.

## Running the Script

To run the OPC UA to RabbitMQ Data Publisher:

1. Make sure that the OPC UA server and RabbitMQ services are running and accessible using the provided hostnames or IP addresses and ports.
2. Ensure that the required dependencies are installed.
3. Set the appropriate environment variables with the desired values.
4. Execute the script using a Python interpreter or by running the script file.

Note: Customize the code according to your specific requirements, such as modifying the OPC UA server connection details, browsing specific nodes, or publishing data to different RabbitMQ queues.




### rabbitmqtocassandra
- Image: joaoribeiro5039/rabbitmqtocassandra:latest
- Environment variables:
  - RABBITMQ_BROKER_HOST=rabbitmq
  - RABBITMQ_BROKER_USER=admin
  - RABBITMQ_BROKER_PASSWORD=admin
  - CASSANDRA_DB_HOST=cassandra
  - CASSANDRA_DB_TABLENAME=Server1
- Restart: unless-stopped
- Dependencies: opctorabbitmq

This service connects to the RabbitMQ broker (`rabbitmq`) and Cassandra database (`cassandra`). It communicates with RabbitMQ using the provided host, username, and password. It also specifies the Cassandra host and the table name to use.

# RabbitMQ to Cassandra Data Processor

The RabbitMQ to Cassandra Data Processor is a Python script that consumes messages from RabbitMQ queues and inserts them into a Cassandra database. It uses the `pika` library for RabbitMQ communication and the `cassandra-driver` for Cassandra integration.

## Dependencies

- `pika`: A Python library for interacting with RabbitMQ message broker.
- `cassandra-driver`: A Python driver for interacting with Cassandra database.

Make sure to install these dependencies using `pip` before running the script.

## Environment Variables

The script utilizes the following environment variables:

- `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker. Defaults to "rabbitmq" if not provided.
- `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication. Defaults to "admin" if not provided.
- `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication. Defaults to "admin" if not provided.
- `CASSANDRA_DB_HOST`: Hostname or IP address of the Cassandra database. Defaults to "cassandra" if not provided.
- `CASSANDRA_DB_TABLENAME`: Name of the Cassandra table to store the data. Defaults to "Server1" if not provided.

Ensure that you have set these environment variables with the appropriate values before running the script.

## Code Overview

The script performs the following steps:

1. Imports the required libraries and sets up variables based on the provided environment variables.
2. Retrieves the list of existing queues from the RabbitMQ Management API using the provided credentials.
3. Establishes a connection to RabbitMQ using the provided credentials.
4. Connects to the Cassandra database and creates a keyspace if it doesn't exist already. Then, creates a table with the specified table name if it doesn't exist.
5. Defines the `process_message` function to handle incoming messages from RabbitMQ and inserts them into the Cassandra table.
6. Sets up a consumer for each queue in the `queue_list` using the `basic_consume` method, passing the `process_message` function as the callback.
7. Starts consuming messages from RabbitMQ by calling `start_consuming` on the channel.
8. Shuts down the Cassandra session, cluster, and RabbitMQ connection when the script is terminated.

## Running the Script

To run the RabbitMQ to Cassandra Data Processor:

1. Make sure that RabbitMQ and Cassandra services are running and accessible using the provided hostnames or IP addresses and ports.
2. Ensure that the required dependencies are installed.
3. Set the appropriate environment variables with the desired values.
4. Execute the script using a Python interpreter or by running the script file.

Note: Customize the code according to your specific requirements, such as modifying the table schema or adding error handling logic.

### Volumes
- rabbitmq_data: Used to persist RabbitMQ data.
- cassandra-data: Used to persist Cassandra data.

These volumes are created to store the data generated by RabbitMQ and Cassandra services respectively.

Please note that this documentation provides an overview of the services and their configurations defined in the provided `docker-compose.yml`. Additional details about each service and its functionality should be available in the respective Docker images or application documentation.
