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
