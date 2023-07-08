[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)

# Program Explanation

This program is designed to consume messages from RabbitMQ queues and store them in an Apache Cassandra database. It establishes a connection to RabbitMQ and retrieves the list of queues based on the specified prefix. The program then sets up a connection to the Cassandra database.

## RabbitMQ Configuration
The program uses environment variables to configure the RabbitMQ broker details, including the broker host, credentials, and queue prefix. If the environment variables are not set, default values are used. The program establishes a connection to RabbitMQ using the specified credentials and retrieves the list of queues using the RabbitMQ Management API. It filters the queues based on the configured prefix and stores them in the `queue_list` variable.

## Cassandra Configuration
The program uses the `CassandraDB` environment variable to configure the Cassandra database host. If the variable is not set, a default value of "localhost" is used. The program also uses the `CASSANDRA_DB_TABLENAME` environment variable to specify the table name in which the data will be stored. If the variable is not set, a default value of "Server1" is used. The program establishes a connection to the Cassandra cluster and creates the keyspace and table if they don't already exist.

## Message Processing
The program defines the `process_message` function, which is called for each consumed message. It extracts the relevant data from the message and performs an insert operation into the Cassandra table. The query is prepared and executed using the extracted values.

## Consuming Messages
The program sets up a consumer for each queue in the `queue_list`. The `process_message` function is assigned as the callback for message processing. It consumes messages from the queue, processes them, and acknowledges their delivery. If an error occurs during message processing, it is handled and the message is not acknowledged.

The program ensures that consumed messages are stored in the Cassandra database, providing a way to persist the data received from RabbitMQ for further analysis or processing.

Please note that you may need to customize certain aspects of the configuration, such as environment variables and table schema, to match your specific setup and requirements.