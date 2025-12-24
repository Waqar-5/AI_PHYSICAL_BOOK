---
sidebar_position: 1
---

# ROS 2 Nodes and Topics

This chapter introduces two fundamental communication concepts in ROS 2: Nodes and Topics. Nodes are processes that perform computation, and Topics are the buses over which nodes exchange messages.

## What is a Node?

In ROS 2, a node is essentially an executable process that performs a specific task. For example, one node might be responsible for reading data from a sensor, another for processing that data, and yet another for sending commands to a motor. ROS 2 applications are typically built as a system of many small, purpose-specific nodes.

## What is a Topic?

Topics are a crucial element of the ROS 2 communication graph. They are named buses over which nodes exchange messages asynchronously. A node can publish data to a topic, or subscribe to a topic to receive data. This publish/subscribe model allows for flexible, decoupled communication between nodes.

## Python Example: Publisher and Subscriber (rclpy)

Here, we will create a simple publisher and subscriber using `rclpy`, the Python client library for ROS 2.

### Prerequisites

Ensure you have ROS 2 Humble installed and sourced.

```bash
# Source your ROS 2 environment (if not already done)
source /opt/ros/humble/setup.bash
```

### Publisher Node

This node will publish string messages to a topic named `chatter`.

`examples/module1/nodes_topics/publisher.py`:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2! {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node

This node will subscribe to the `chatter` topic and print the received messages.

`examples/module1/nodes_topics/subscriber.py`:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### How to Run

1.  Open two separate terminal windows.
2.  In each terminal, source your ROS 2 environment.
3.  In the first terminal, run the publisher:
    ```bash
    python3 <path_to_your_repo>/examples/module1/nodes_topics/publisher.py
    ```
4.  In the second terminal, run the subscriber:
    ```bash
    python3 <path_to_your_repo>/examples/module1/nodes_topics/subscriber.py
    ```
You should see the publisher sending messages and the subscriber receiving them.

## Assignment

1.  Modify the publisher node to publish messages to a different topic name (e.g., `my_custom_chatter`).
2.  Update the subscriber node to listen to `my_custom_chatter` instead of `chatter`.
3.  Run both nodes and confirm they are communicating on the new topic.
