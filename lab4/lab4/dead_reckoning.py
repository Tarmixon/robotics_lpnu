import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, PoseStamped
import math
import time

class DeadReckoning(Node):
    def __init__(self):
        super().__init__('dead_reckoning')
        
        # Підписуємося на команди швидкості, які ми реально відправляємо роботу
        self.subscription = self.create_subscription(
            TwistStamped,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        
        # Публікуємо нашу розраховану "ідеальну" позицію
        self.publisher_ = self.create_publisher(PoseStamped, '/ideal_pose', 10)
        
        # Початковий стан робота
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

    def cmd_vel_callback(self, msg):
        current_time = self.get_clock().now()
        # Обчислюємо проміжок часу dt
        dt = (current_time - self.last_time).nanoseconds / 1e9
        
        v = msg.twist.linear.x
        w = msg.twist.angular.z

        # Алгоритм Dead Reckoning
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += w * dt

        self.last_time = current_time
        self.publish_ideal_pose()

    def publish_ideal_pose(self):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'odom'
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        # Спрощене перетворення кута в орієнтацію
        pose.pose.orientation.z = math.sin(self.theta / 2.0)
        pose.pose.orientation.w = math.cos(self.theta / 2.0)
        self.publisher_.publish(pose)

def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoning()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()