---
sidebar_position: 2
---

# ROS 2 Services

This chapter introduces ROS 2 Services, which provide a synchronous request/response communication mechanism between nodes. Unlike topics, where data flows continuously, services are used for operations that require a specific input and return a single result.

## What is a Service?

A ROS 2 service defines a pair of messages: one for the *request* and one for the *response*. A node can act as a *service server*, offering a service and waiting for requests. Other nodes can act as *service clients*, sending requests to a service server and blocking until a response is received.

Services are ideal for operations like:
*   Triggering an action (e.g., "take a picture")
*   Querying information (e.g., "get current robot pose")
*   Performing a one-time calculation (e.g., "add two numbers")

## Python Example: Service Server and Client (rclpy)

Here, we will create a simple service server and client using `rclpy` to demonstrate the request/response pattern. The service will add two integers.

### Define the Service Interface

First, we need to define the service message. Create a file `AddTwoInts.srv` in a new ROS 2 package. For simplicity in this example, we will just describe the service messages in text.

`AddTwoInts.srv`:
```
int64 a
int64 b
---
int64 sum
```

This defines a service that takes two `int64` integers (`a` and `b`) as a request and returns a single `int64` integer (`sum`) as a response.

### Service Server Node

This node will provide the `add_two_ints` service.

`examples/module1/services/server.py`:
```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Assuming example_interfaces is available

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Service server ready.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending response: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client Node

This node will send requests to the `add_two_ints` service.

`examples/module1/services/client.py`:
```python
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Assuming example_interfaces is available

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    if len(sys.argv) != 3:
        minimal_client.get_logger().info('Usage: ros2 run <package_name> minimal_client_async A B')
        minimal_client.get_logger().info('Please provide two integers for A and B')
        minimal_client.destroy_node()
        rclpy.shutdown()
        sys.exit(1)
    
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    response = minimal_client.send_request(a, b)
    minimal_client.get_logger().info(f'Result of add_two_ints: for {a} + {b} = {response.sum}')
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### How to Run

1.  Open two separate terminal windows.
2.  In each terminal, source your ROS 2 environment.
3.  **Important**: Ensure the `example_interfaces` ROS 2 package is installed and built in your workspace, or available in your ROS 2 environment. This package provides the `AddTwoInts.srv` definition.
4.  In the first terminal, run the service server:
    ```bash
    python3 <path_to_your_repo>/examples/module1/services/server.py
    ```
5.  In the second terminal, run the service client with two numbers:
    ```bash
    python3 <path_to_your_repo>/examples/module1/services/client.py 5 3
    ```
    You should see the client sending a request and the server responding with the sum.

## Assignment

1.  Modify the `AddTwoInts` service definition to perform a different arithmetic operation (e.g., subtraction or multiplication).
2.  Update both the service server and client nodes to use the new service definition and operation.
3.  Test your modified service.
