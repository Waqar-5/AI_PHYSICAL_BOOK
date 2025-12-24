# ROS 2 Nodes and Topics Examples

This directory contains Python examples for ROS 2 nodes and topics using `rclpy`.

## Files

- `publisher.py`: A simple ROS 2 publisher node that sends string messages.
- `subscriber.py`: A simple ROS 2 subscriber node that receives and prints string messages.

## How to Run

1.  **Open two separate terminal windows.**
2.  **Source your ROS 2 environment in each terminal.**
    ```bash
    source /opt/ros/humble/setup.bash
    ```
    (Replace `/opt/ros/humble/setup.bash` with your actual ROS 2 installation path if different.)
3.  **In the first terminal, navigate to this directory and run the publisher:**
    ```bash
    cd <path_to_your_repo>/examples/module1/nodes_topics
    python3 publisher.py
    ```
    You should see messages being published.
4.  **In the second terminal, navigate to this directory and run the subscriber:**
    ```bash
    cd <path_to_your_repo>/examples/module1/nodes_topics
    python3 subscriber.py
    ```
    You should see the subscriber receiving and printing the messages.

## Troubleshooting

-   **`ModuleNotFoundError`**: Ensure your ROS 2 environment is sourced correctly and Python dependencies are installed.
-   **No messages received**: Double-check that both publisher and subscriber are running, sourced to the same ROS 2 environment, and communicating on the same topic name (`/chatter` by default in these examples).
