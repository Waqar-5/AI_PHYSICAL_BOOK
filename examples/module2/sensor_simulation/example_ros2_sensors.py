#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import time

class MockLaserScanPublisher(Node):
    def __init__(self):
        super().__init__('mock_laser_scan_publisher')
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(1.0, self.publish_laser_scan) # Publish every 1 second
        self.get_logger().info('Mock LaserScan Publisher Node Started')

        self.angle_min = -math.pi / 2.0  # -90 degrees
        self.angle_max = math.pi / 2.0   # +90 degrees
        self.angle_increment = math.pi / 360.0 # 0.5 degrees per step
        self.range_min = 0.1
        self.range_max = 10.0
        self.num_ranges = int((self.angle_max - self.angle_min) / self.angle_increment)

    def publish_laser_scan(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame' # Standard frame for laser scans

        msg.angle_min = self.angle_min
        msg.angle_max = self.angle_max
        msg.angle_increment = self.angle_increment
        msg.time_increment = 0.0 # Time between measurements, can be 0 for simplicity
        msg.scan_time = 1.0 # Total time for one scan

        msg.range_min = self.range_min
        msg.range_max = self.range_max

        ranges = []
        intensities = []
        
        # Generate mock data: a simple 'wall' in front, some varying distances
        for i in range(self.num_ranges):
            angle = msg.angle_min + i * msg.angle_increment
            
            # Simple simulation: a 'wall' at 5m directly in front (angle=0),
            # and distances increasing towards the sides.
            if abs(angle) < math.pi / 6: # +/- 30 degrees
                distance = 5.0 + math.sin(angle * 6) * 0.5 # A wavy wall
            else:
                distance = self.range_max - (abs(angle) / msg.angle_max) * 3.0 # Shorter range towards edges

            # Clamp distances to min/max range
            distance = max(self.range_min, min(self.range_max, distance))
            
            ranges.append(distance)
            intensities.append(100.0) # Mock intensity

        msg.ranges = ranges
        msg.intensities = intensities

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing mock LaserScan with {len(ranges)} ranges.')

def main(args=None):
    rclpy.init(args=args)
    node = MockLaserScanPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
