#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import GetEntityState, SetEntityState
from gazebo_msgs.msg import EntityState
from geometry_msgs.msg import Pose, Twist
import time
import math

class GazeboPhysicsControl(Node):
    def __init__(self):
        super().__init__('gazebo_physics_control')
        self.get_logger().info('Gazebo Physics Control Node Started')

        # Create clients for Gazebo services
        self.get_state_cli = self.create_client(GetEntityState, '/gazebo/get_entity_state')
        self.set_state_cli = self.create_client(SetEntityState, '/gazebo/set_entity_state')

        while not self.get_state_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /gazebo/get_entity_state not available, waiting...')
        while not self.set_state_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /gazebo/set_entity_state not available, waiting...')

        self.get_logger().info('Gazebo services are ready.')

    def get_entity_state(self, entity_name='box'):
        request = GetEntityState.Request()
        request.name = entity_name
        future = self.get_state_cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            return future.result().state
        else:
            self.get_logger().error(f'Failed to get state for entity: {entity_name}')
            return None

    def set_entity_state(self, entity_name='box', pose=None, twist=None):
        request = SetEntityState.Request()
        request.state.name = entity_name
        if pose:
            request.state.pose = pose
        if twist:
            request.state.twist = twist
        future = self.set_state_cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            if not future.result().success:
                self.get_logger().warn(f'Failed to set state for entity {entity_name}: {future.result().status_message}')
            return future.result().success
        else:
            self.get_logger().error(f'Service call failed for set_entity_state for {entity_name}')
            return False

def main(args=None):
    rclpy.init(args=args)
    physics_control_node = GazeboPhysicsControl()

    box_name = 'box' # This assumes a 'box' model exists in your Gazebo world

    try:
        # 1. Reset the box to a known position
        initial_pose = Pose()
        initial_pose.position.x = 0.0
        initial_pose.position.y = 0.0
        initial_pose.position.z = 2.0 # Place it in the air to fall
        initial_pose.orientation.w = 1.0 # No rotation

        physics_control_node.get_logger().info(f'Resetting {box_name} to Z=2.0...')
        physics_control_node.set_entity_state(box_name, pose=initial_pose)
        time.sleep(1.0) # Give it a moment to stabilize/start falling

        # 2. Observe its state as it falls (or after it settles)
        physics_control_node.get_logger().info(f'Observing state of {box_name}...')
        for _ in range(5):
            state = physics_control_node.get_entity_state(box_name)
            if state:
                physics_control_node.get_logger().info(f'[{box_name}] Position: x={state.pose.position.x:.2f}, y={state.pose.position.y:.2f}, z={state.pose.position.z:.2f}')
            time.sleep(0.5)

        # 3. Apply an impulse to make it move
        physics_control_node.get_logger().info(f'Applying an impulse to {box_name}...')
        impulse_pose = Pose() # Current pose
        state_before_impulse = physics_control_node.get_entity_state(box_name)
        if state_before_impulse:
            impulse_pose = state_before_impulse.pose
        
        impulse_twist = Twist()
        impulse_twist.linear.x = 1.0 # Push it forward
        impulse_twist.angular.z = math.pi / 2 # Spin it

        physics_control_node.set_entity_state(box_name, pose=impulse_pose, twist=impulse_twist)
        time.sleep(1.0)

        # 4. Observe its state again
        physics_control_node.get_logger().info(f'Observing state of {box_name} after impulse...')
        for _ in range(5):
            state = physics_control_node.get_entity_state(box_name)
            if state:
                physics_control_node.get_logger().info(f'[{box_name}] Position: x={state.pose.position.x:.2f}, y={state.pose.position.y:.2f}, z={state.pose.position.z:.2f}')
                physics_control_node.get_logger().info(f'[{box_name}] Linear Velocity: x={state.twist.linear.x:.2f}, y={state.twist.linear.y:.2f}, z={state.twist.linear.z:.2f}')
            time.sleep(0.5)

    except Exception as e:
        physics_control_node.get_logger().error(f"An error occurred: {e}")
    finally:
        physics_control_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
