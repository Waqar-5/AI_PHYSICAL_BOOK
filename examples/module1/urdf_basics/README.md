# ROS 2 URDF Basics Example

This directory contains a basic example of a Humanoid URDF file.

## Files

- `simple_humanoid.urdf`: A simplified URDF file describing a humanoid robot.

## Prerequisites

Ensure you have ROS 2 Humble installed and sourced. To visualize URDF files, you will typically need the `urdf_tutorial` package or similar tools like `robot_state_publisher` and `rviz2`.

```bash
# Source your ROS 2 environment (if not already done)
source /opt/ros/humble/setup.bash
```

## How to Visualize

To visualize this URDF in RViz2, you would typically use a launch file that loads the URDF and starts the necessary ROS 2 nodes. For a simple local visualization, you can use the `urdf_tutorial` package if installed, or manually set up `robot_state_publisher` and `rviz2`.

Here's a conceptual way to visualize it using `robot_state_publisher` and `rviz2`:

1.  **Ensure `robot_state_publisher` and `rviz2` are installed:**
    ```bash
    sudo apt install ros-humble-robot-state-publisher ros-humble-rviz2
    ```
2.  **Create a simple launch file (e.g., `display.launch.py`) in your ROS 2 workspace:**
    ```python
    import os
    from ament_index_python.packages import get_package_share_directory
    from launch import LaunchDescription
    from launch_ros.actions import Node

    def generate_launch_description():
        # Get the URDF file path
        urdf_path = os.path.join(
            '<path_to_your_repo>',
            'examples',
            'module1',
            'urdf_basics',
            'simple_humanoid.urdf'
        )

        with open(urdf_path, 'r') as infp:
            robot_desc = infp.read()

        return LaunchDescription([
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[{'robot_description': robot_desc}]
            ),
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                arguments=['-d', os.path.join(get_package_share_directory('urdf_tutorial'), 'rviz', 'urdf.rviz')]
            )
        ])
    ```
    **Note**: Replace `<path_to_your_repo>` with the actual absolute path to your repository. Also, `get_package_share_directory('urdf_tutorial')` assumes `urdf_tutorial` package is installed to get a default RViz config. You might need to adjust this.

3.  **Run the launch file from your ROS 2 workspace:**
    ```bash
    ros2 launch <your_package_name> display.launch.py
    ```

## Troubleshooting

-   **RViz2 not showing robot**: Ensure `robot_state_publisher` is running and publishing the `robot_description` topic. Check the `Fixed Frame` in RViz2 (often `base_link` or `odom`).
-   **Errors loading URDF**: Verify the XML syntax of `simple_humanoid.urdf`.
