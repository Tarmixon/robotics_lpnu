"""Скрипт руху по колу для ЛР3."""
import time
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CirclePath(Node):
    def __init__(self):
        super().__init__('circle_path')

        # Параметри швидкості та геометрії
        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.3)
        self.declare_parameter("rate_hz", 20.0)

        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        v = float(self.get_parameter("linear_speed").value)
        w = float(self.get_parameter("angular_speed").value)
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)

        # Час одного кола: T = 2*pi / w
        duration = 2.0 * math.pi / max(abs(w), 1e-6)
        self.get_logger().info(f"Запуск кола: v={v}, w={w}, тривалість={duration:.2f}s")

        msg = TwistStamped()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x = v
        msg.twist.angular.z = w

        t_end = time.time() + duration
        while time.time() < t_end:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(dt)

        # Зупинка
        self.pub.publish(TwistStamped())
        self.get_logger().info("Коло завершено.")

def main(args=None):
    rclpy.init(args=args)
    node = CirclePath()
    node.destroy_node()
    rclpy.shutdown()