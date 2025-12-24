# ROS 2 Services Examples

This directory contains Python examples for ROS 2 services using `rclpy`.

## Files

- `server.py`: A simple ROS 2 service server that adds two integers.
- `client.py`: A simple ROS 2 service client that sends requests to the server.

## Prerequisites

Ensure you have ROS 2 Humble installed and sourced. Additionally, ensure the `example_interfaces` ROS 2 package is available in your workspace, as it provides the `AddTwoInts.srv` definition used in these examples.

```bash
# Source your ROS 2 environment (if not already done)
source /opt/ros/humble/setup.bash
```

## How to Run

1.  Open two separate terminal windows.
2.  In each terminal, source your ROS 2 environment.
3.  **In the first terminal, navigate to this directory and run the service server:**
    ```bash
    cd <path_to_your_repo>/examples/module1/services
    python3 server.py
    ```
    You should see the server starting and waiting for requests.
4.  **In the second terminal, navigate to this directory and run the service client with two numbers:**
    ```bash
    cd <path_to_your_repo>/examples/module1/services
    python3 client.py 5 3
    ```
    Replace `5` and `3` with any two integers. You should see the client sending a request and the server responding with the sum.

## Troubleshooting

-   **`ModuleNotFoundError: No module named 'example_interfaces.srv'`**: Ensure `example_interfaces` is correctly installed and sourced. You might need to build your ROS 2 workspace if you created a custom package.
-   **`service not available, waiting again...`**: Ensure the service server (`server.py`) is running in a separate terminal.
