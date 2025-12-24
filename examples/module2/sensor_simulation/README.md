# ROS 2 Sensor Simulation Example (LaserScan)

This example demonstrates a basic ROS 2 node that publishes mock `sensor_msgs/msg/LaserScan` data, simulating a 2D LiDAR sensor. This is a fundamental concept for understanding how simulated sensor data can be generated and integrated into a ROS 2 system.

## Prerequisites

1.  **ROS 2 Humble**: Ensure ROS 2 Humble is installed and sourced.
2.  **Python Packages**: `rclpy`, `sensor_msgs` (usually included with ROS 2 Python installation).
    ```bash
    pip install rclpy # if not already installed with ROS 2
    ```

## How to Run

1.  **Source your ROS 2 Environment**:
    Open a terminal and source your ROS 2 setup file:
    ```bash
    source /opt/ros/humble/setup.bash
    ```
    (Adjust path if your ROS 2 installation is different.)

2.  **Run the Python Script**:
    Navigate to the directory containing `example_ros2_sensors.py` and execute it:
    ```bash
    python3 example_ros2_sensors.py
    ```
    This will start the ROS 2 node that publishes `LaserScan` messages.

3.  **Observe the Topic (Optional)**:
    Open a *new* terminal, source your ROS 2 environment, and echo the `scan` topic to see the published messages:
    ```bash
    ros2 topic echo /scan
    ```
    You should see `LaserScan` messages being published approximately once per second.

    You can also use `rqt_plot` to visualize the ranges:
    ```bash
    rqt_plot /scan/ranges
    ```

## Script Functionality

The `example_ros2_sensors.py` script creates a ROS 2 node (`mock_laser_scan_publisher`) that:

1.  **Initializes a Publisher**: It creates a publisher for messages of type `sensor_msgs/msg/LaserScan` on the topic `/scan`.
2.  **Configures LaserScan Parameters**: Sets up common LiDAR parameters such as:
    *   `angle_min`, `angle_max`: Defines the field of view (-90 to +90 degrees).
    *   `angle_increment`: The angular resolution between each ray (0.5 degrees).
    *   `range_min`, `range_max`: The minimum and maximum detection distances (0.1m to 10.0m).
    *   `frame_id`: 'laser_frame', indicating the sensor's coordinate frame.
3.  **Generates Mock Data**: In the `publish_laser_scan` callback, it generates a synthetic set of ranges. For this example, it simulates a "wavy wall" directly in front of the sensor (around 5 meters away) and distances that decrease towards the edges of the field of view.
4.  **Publishes Messages**: The generated `LaserScan` message is published to the `/scan` topic at a rate of 1 Hz.

This example provides a foundation for understanding how to simulate and publish sensor data within the ROS 2 ecosystem, which is crucial for developing and testing robotic perception algorithms.