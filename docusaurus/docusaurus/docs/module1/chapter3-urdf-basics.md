---
sidebar_position: 3
---

# Understanding Basic Humanoid URDF

This chapter introduces the Unified Robot Description Format (URDF), a crucial XML format used in ROS 2 to describe all aspects of a robot model, including its visual appearance, collision properties, and physical dynamics. We'll focus on understanding the basic structure of a humanoid robot's URDF.

## What is URDF?

URDF (Unified Robot Description Format) is an XML file format that allows you to describe a robot's kinematic and dynamic properties, visual appearance, and collision models. It's essential for simulating robots in tools like Gazebo, visualizing them in RViz2, and performing motion planning.

A URDF file defines:
*   **Links**: These represent the rigid bodies of the robot (e.g., torso, head, upper arm).
*   **Joints**: These define the connections between links, specifying their type (e.g., fixed, revolute, prismatic) and degrees of freedom.

## Basic Humanoid URDF Structure

A simplified humanoid URDF typically includes a base link (e.g., `base_link` or `torso`), connected to other links (head, arms, legs) via joints.

Here’s a conceptual overview of a simple humanoid structure in URDF:

```xml
<robot name="simple_humanoid">

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.3"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>

  <!-- Head Link connected by a fixed joint to base_link -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="base_to_head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
  </joint>

  <!-- Right Arm (simplified) -->
  <link name="right_arm_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.2"/>
      </geometry>
      <material name="green">
        <color rgba="0 0.8 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="base_to_right_arm_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_arm_link"/>
    <origin xyz="0 -0.1 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

  <!-- ... (similar structure for left arm, legs, etc.) ... -->

</robot>
```

This XML snippet defines two links (`base_link` and `head_link`) and a fixed joint connecting them. It also shows a revolute joint for a right arm. Each link has a visual element to represent its shape and color.

## Visualizing URDF in RViz2

RViz2 is a 3D visualization tool for ROS 2. It can display a robot model defined by a URDF file, along with sensor data and other debugging information.

To visualize a URDF, you typically need:
1.  A URDF file.
2.  A ROS 2 launch file that loads the URDF and starts the `robot_state_publisher` node (to publish the robot's joint states) and RViz2.

## Assignment

1.  Extend the `simple_humanoid.urdf` file to include a left arm with a similar structure to the right arm.
2.  Modify the joint type for one of the arms from `revolute` to `prismatic` and observe how the visualization changes in RViz2 (once you set up the launch file).
3.  Research and add a `collision` element to one of the links in your URDF.
