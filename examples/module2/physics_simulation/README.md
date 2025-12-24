# Gazebo Physics Simulation Example

This example demonstrates how to interact with Gazebo's physics engine using ROS 2 (`rclpy`) services to control and observe the state of an entity.

## Prerequisites

1.  **ROS 2 Humble**: Ensure ROS 2 Humble is installed and sourced.
2.  **Gazebo**: Gazebo (preferably Garden or newer) must be installed.
3.  **Gazebo ROS 2 Packages**: The `ros_gz_sim` package (or `ros_gz_bridge` and `ros_gz_interfaces` if using older versions) should be installed to provide ROS 2 interfaces for Gazebo services.
    ```bash
    sudo apt install ros-humble-ros-gz-sim
    ```
4.  **Python Packages**: `rclpy`, `gazebo_msgs`
    ```bash
    pip install rclpy gazebo_msgs
    ```

## How to Run

1.  **Launch Gazebo**:
    Open a terminal and launch an empty Gazebo world:
    ```bash
    gazebo
    ```
    Or, for a more controlled environment (e.g., with a ground plane):
    ```bash
    ros2 launch ros_gz_sim_demos gz_sim.launch.py # This usually launches an empty world or default.
    ```
    Alternatively, launch a simple world manually from your ROS 2 workspace if you have one:
    ```bash
    # Example: ros2 launch my_pkg my_world.launch.py
    ```
    Make sure a `box` model is present in the Gazebo world. If not, you can manually insert one from the Gazebo editor (Insert -> Add Box) or include it in your `.world` file. The script assumes an entity named `box`.

2.  **Run the Python Script**:
    Open a new terminal, source your ROS 2 environment, and run the script:
    ```bash
    python3 example_gazebo_physics.py
    ```

## Script Functionality

The `example_gazebo_physics.py` script performs the following actions:

1.  **Connects to Gazebo Services**: It establishes connections to `/gazebo/get_entity_state` and `/gazebo/set_entity_state` ROS 2 services.
2.  **Resets Box Position**: It initially sets the `box` entity to a position of (0, 0, 2.0) meters, allowing it to fall under gravity.
3.  **Observes State**: It periodically queries and prints the `box`'s position.
4.  **Applies Impulse**: After a short delay, it applies a linear and angular impulse to the `box`, causing it to move and rotate.
5.  **Observes State Again**: It continues to query and print the `box`'s position and velocity after the impulse.

This example showcases how you can programmatically interact with Gazebo's physics simulation to control and analyze the behavior of entities.
