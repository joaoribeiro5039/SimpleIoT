API Documentation:

This API provides functionality to connect to an OPC UA server, monitor specific nodes, and publish their values to a RabbitMQ server.

## Endpoints:

### Testing
- Description: This endpoint is used for testing purposes to check if the API is working.
- Method: GET
- Path: `/Testing`
- Response:
  - `200 OK`: Successful response with a message.

### Check If OPC UA Server is Available
- Description: This endpoint is used to check the availability of the OPC UA server.
- Method: GET
- Path: `/OPCServer`
- Query Parameters:
  - `ocp_url` (string, required): The URL of the OPC UA server.
- Response:
  - `200 OK`: If the OPC UA server is available.
  - `500 Internal Server Error`: If the OPC UA server is not available.

### Connect to OPC Server
- Description: This endpoint is used to connect to the OPC UA server and start monitoring specified nodes.
- Method: POST
- Path: `/ConnectOPCServer`
- Body Parameters:
  - `ocp_url` (string, required): The URL of the OPC UA server.
  - `nodestart` (string, required): The starting node identifier to monitor.
  - `rabbitmqserver` (string, required): The address of the RabbitMQ server.
- Response:
  - `200 OK`: If the connection to the OPC UA server is successful and monitoring is started.
  - `500 Internal Server Error`: If there was an error connecting to the OPC UA server.

### Stop the Client
- Description: This endpoint is used to stop the OPC UA server monitoring.
- Method: PUT
- Path: `/StopClient`
- Response:
  - `200 OK`: If the OPC UA server monitoring is successfully stopped.

## Usage:

1. Start the API using the appropriate server (e.g., uvicorn) and host configuration.
2. Test the API by accessing the `/Testing` endpoint.

   Example: `GET http://localhost:8000/Testing`

3. Check the availability of the OPC UA server by accessing the `/OPCServer` endpoint and providing the `ocp_url` query parameter.

   Example: `GET http://localhost:8000/OPCServer?ocp_url=opc.tcp://example.com:4840`

4. Connect to the OPC UA server and start monitoring specific nodes by accessing the `/ConnectOPCServer` endpoint with the necessary parameters.

   Example: 
   ```bash
   POST http://localhost:8000/ConnectOPCServer
   Body:
   {
       "ocp_url": "opc.tcp://example.com:4840",
       "nodestart": "ns=2;s=Node1",
       "rabbitmqserver": "localhost"
   }
   ```

5. Stop the OPC UA server monitoring by accessing the `/StopClient` endpoint.

   Example: `PUT http://localhost:8000/StopClient`

   This will stop the monitoring process and disconnect from the OPC UA server.

## Important Notes:

- Make sure to replace `http://localhost:8000` in the example URLs with the appropriate host and port based on your setup.
- The API uses asynchronous programming with asyncio for the OPC UA server monitoring.