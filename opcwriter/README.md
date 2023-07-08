[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)

# OPC-UA FastAPI Server

This project implements a FastAPI server for interacting with an OPC-UA server. It provides endpoints to read OPC-UA values, write OPC-UA values, and read filtered OPC-UA values based on a specific node ID.

## Installation

To run the OPC-UA FastAPI server, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI server with the following command:
   ```
   uvicorn main:app --reload
   ```

The server will start running at `http://localhost:8000`.

## Endpoints

### 1. Testing Endpoint

- URL: `/Testing`
- Method: GET

This endpoint is used for testing purposes and returns a simple "Hello World" message.

### 2. Read All OPC-UA Values Endpoint

- URL: `/ReadAllOPCValues`
- Method: GET

This endpoint retrieves all the values from the OPC-UA server specified by the `opcUrl` parameter. It returns a JSON object with the node IDs as keys and their corresponding values.

Parameters:

- `opcUrl` (string): The URL of the OPC-UA server.

### 3. Write OPC-UA Value Endpoint

- URL: `/WriteOPCUAValue`
- Method: PUT

This endpoint writes a value to the OPC-UA server for the specified node ID. It updates the value of the node with the given `nodeid` parameter to the provided `value`.

Parameters:

- `opcUrl` (string): The URL of the OPC-UA server.
- `nodeid` (string): The node ID of the OPC-UA server to write the value to.
- `value` (string): The value to write to the OPC-UA server.

### 4. Read Filtered OPC-UA Values Endpoint

- URL: `/ReadFilteredOPCUAValues`
- Method: GET

This endpoint retrieves filtered values from the OPC-UA server based on a specific node ID. It returns a JSON object with the node IDs as keys and their corresponding values, filtered based on the `nodeid` parameter.

Parameters:

- `opcUrl` (string): The URL of the OPC-UA server.
- `nodeid` (string): The node ID used to filter the values.

## Example Usage

To read all OPC-UA values from a server:

```
GET /ReadAllOPCValues?opcUrl=<OPC-UA server URL>
```

To write a value to an OPC-UA server:

```
PUT /WriteOPCUAValue
Content-Type: application/json

{
    "opcUrl": "<OPC-UA server URL>",
    "nodeid": "<Node ID>",
    "value": "<Value>"
}
```

To read filtered OPC-UA values based on a specific node ID:

```
GET /ReadFilteredOPCUAValues?opcUrl=<OPC-UA server URL>&nodeid=<Node ID>
```

Please note that for secure connections, you can provide additional parameters such as `UserName`, `Password`, and `Secure_Policy`.

## On Shutdown

The server gracefully shuts down when the application receives a shutdown event. The shutdown event can be triggered by stopping the server or terminating the application. Upon shutdown, a message "Shutting down..." is printed.

Feel free to modify and extend this code to meet your specific OPC-UA server requirements.