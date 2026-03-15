import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/world/demo/model/vehicle_blue/link/chassis/sensor/lidar/scan', self.scan_callback, 10)

    def scan_callback(self, msg):
        # Беремо центральну частину скану (перед роботом)
        # Масив ranges містить відстані. 0 - це зазвичай центр або край.
        center_index = len(msg.ranges) // 2
        dist_front = msg.ranges[center_index]

        drive_msg = TwistStamped()
        drive_msg.header.stamp = self.get_clock().now().to_msg()
        drive_msg.header.frame_id = 'base_link'

        if dist_front < 1.0: # Якщо перешкода ближче ніж 1 метр
            self.get_logger().info('STOP! Obstacle detected!')
            drive_msg.twist.linear.x = 0.0
            drive_msg.twist.angular.z = 0.5 # Починаємо повертати
        else:
            drive_msg.twist.linear.x = 0.3 # Їдемо вперед
            drive_msg.twist.angular.z = 0.0

        self.publisher_.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    rclpy.shutdown()