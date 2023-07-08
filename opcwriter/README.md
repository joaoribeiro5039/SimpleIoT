[main documentation](https://github.com/joaoribeiro5039/SimpleIoT/blob/main/README.MD)
# Program Explanation

This program is an API built with FastAPI that interacts with an OPC UA server. It provides endpoints for reading and writing OPC UA values, as well as retrieving filtered values from the OPC UA server.

## OPC UA Connection Setup

The program defines two functions for interacting with the OPC UA server:

1. `ReadAllOPCUAValues`: This function connects to the OPC UA server specified by the `opcUrl` parameter and retrieves all the values from the server. It supports optional parameters for authentication (`UserName` and `Password`) and security policy (`Secure_Policy`).

2. `WriteOPCUAValue`: This function connects to the OPC UA server specified by the `opcUrl` parameter and writes the `value` to the OPC UA node identified by the `nodeid` parameter. Similar to `ReadAllOPCUAValues`, it also supports optional authentication and security policy parameters.

The OPC UA server connection is established using the `opcua.Client` class from the `opcua` library. The connection is made to the OPC UA server at the provided `opcUrl`. If authentication and security policy parameters are provided, they are used to configure the security settings of the connection.

## API Endpoints

The FastAPI application is created using the `FastAPI` class and stored in the `app` variable.

### Testing Endpoint

The `/Testing` endpoint is a GET request handler that returns a JSON response with a "message" key set to "Hello World". It serves as a simple test endpoint to verify the API's functionality.

### Reading OPC UA Values

The `/ReadAllOPCValues` endpoint is a GET request handler that accepts the `opcUrl`, `UserName`, `Password`, and `Secure_Policy` parameters. It calls the `ReadAllOPCUAValues` function, passing the provided parameters, and returns the retrieved OPC UA values as a JSON response.

### Writing OPC UA Value

The `/WriteOPCUAValue` endpoint is a PUT request handler that accepts the `opcUrl`, `nodeid`, `value`, `UserName`, `Password`, and `Secure_Policy` parameters. It calls the `WriteOPCUAValue` function, passing the provided parameters, to write the specified `value` to the OPC UA node identified by the `nodeid`. It returns a JSON response indicating the success of the write operation.

### Reading Filtered OPC UA Values

The `/ReadFilteredOPCUAValues` endpoint is a GET request handler that accepts the `opcUrl`, `nodeid`, `UserName`, `Password`, and `Secure_Policy` parameters. It calls the `ReadAllOPCUAValues` function, passing the provided parameters, to retrieve all OPC UA values from the server. It then filters the values based on the `nodeid` and returns the filtered values as a JSON response.

### Shutdown Event

The `@app.on_event("shutdown")` decorator is used to define a function that is executed when the application is shutting down. In this case, the function simply prints a "Shutting down..." message.

## Usage

To use this API, you can send HTTP requests to the specified endpoints:

- `/Testing`: Send a GET request to test the API functionality. It returns a JSON response with a "message" key set to "Hello World".

- `/ReadAllOPCValues`: Send a GET request with the appropriate parameters (`opcUrl`, `UserName`, `Password`, and `Secure_Policy`) to retrieve all OPC UA values from the server.

- `/WriteOPCUAValue`: Send a PUT request with the appropriate parameters (`opcUrl`, `nodeid`, `value`, `UserName`, `Password`, and `Secure_Policy`) to write a value to an OPC UA node.

- `/ReadFilteredOPCUAValues`: Send a GET request with the appropriate parameters (`opcUrl`, `nodeid`, `UserName`, `Password`, and `Secure_Policy`) to retrieve filtered OPC UA values from the server based on the specified `nodeid`.

Please ensure that you provide the correct OPC UA server details, authentication credentials (if required), and security policy (if applicable) when making the API requests.