[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)
# Program Explanation

This program is a data processing application that consumes messages from RabbitMQ and stores them in an Apache Cassandra database. It establishes a connection to RabbitMQ, retrieves messages from specified queues, processes the messages, and saves them in Cassandra.

## Environment Variables

The program utilizes several environment variables to configure the connection details and other parameters. These variables are read using the `os.getenv()` function. The available environment variables are:

- `RABBITMQ_BROKER_HOST`: Hostname or IP address of the RabbitMQ broker. If not provided, the default value is set to "localhost".
- `RABBITMQ_BROKER_QUEUE_PREFIX`: Prefix for the RabbitMQ queues. If not provided, the default value is set to "server".
- `RABBITMQ_BROKER_USER`: Username for RabbitMQ authentication. If not provided, the default value is set to "admin".
- `RABBITMQ_BROKER_PASSWORD`: Password for RabbitMQ authentication. If not provided, the default value is set to "admin".
- `CASSANDRA_DB_HOST`: Hostname or IP address of the Cassandra database. If not provided, the default value is set to "localhost".
- `CASSANDRA_DB_TABLENAME`: Name of the Cassandra table where the messages will be stored. If not provided, the default value is set to "Server1".

## Connection Setup

The program establishes a connection to RabbitMQ using the provided connection parameters. It creates a channel to communicate with RabbitMQ and retrieves the list of queues from the RabbitMQ Management API using an HTTP GET request. The queue names that match the specified queue prefix are stored in the `queue_list` variable.

A connection is also established to the Apache Cassandra database using the provided Cassandra host. The keyspace "simpleiot" is created if it does not exist, and the session is set to use this keyspace. A table named with the value of the `CASSANDRA_DB_TABLENAME` environment variable is created if it does not exist.

## Message Processing

The program defines a `process_message` function that is called for each consumed message. The function processes the message by extracting the necessary data and inserts it into the Cassandra table. The message is parsed as JSON, and the required fields (nodeid, value, opc_read_time) are extracted. A unique identifier (UUID) is generated for each message, and the data is inserted into the Cassandra table using a prepared query.

## Message Consumption

The program sets up a consumer for each queue in the `queue_list`. It consumes messages from each queue and invokes the `process_message` function for each message received. The `channel.start_consuming()` method starts the message consumption process, and it continues to consume messages until interrupted.

## Cleanup and Shutdown

In the event of program termination, the "finally" block is executed. It performs necessary cleanup tasks such as printing a restart message, shutting down the Cassandra session and cluster, and closing the RabbitMQ connection.

Please ensure that the required environment variables are set correctly before running this program. The program expects RabbitMQ and Cassandra to be running and accessible using the provided configuration.