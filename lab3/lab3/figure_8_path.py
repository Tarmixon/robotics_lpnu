"""Figure-8 path - STUDENT TASK."""
import time
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

from .diff_drive_math import twist_to_wheel_speeds


class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        # Оголошуємо параметри швидкості
        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.3)
        self.declare_parameter("wheel_radius", 0.15)
        self.declare_parameter("wheel_separation", 0.7)
        self.declare_parameter("rate_hz", 20.0)

        # Створюємо публікатор команд швидкості
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        # Отримуємо значення швидкостей з параметрів
        v = float(self.get_parameter("linear_speed").value)
        w = float(self.get_parameter("angular_speed").value)
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)

        # Розраховуємо час, необхідний для проходження одного кола (T = 2*pi / w)
        duration = (2.0 * math.pi / abs(w)) * 1.1
        
        self.get_logger().info(f"Починаємо рух по вісімці! v={v:.2f}, w={w:.2f}")

        # --- ЧАСТИНА 1: КОЛО ВЛІВО (w > 0) ---
        self.get_logger().info(f"1. Малюємо ліве коло. Час: {duration:.2f}s")
        self.drive_circle(v, abs(w), duration, dt)

        # --- ЧАСТИНА 2: КОЛО ВПРАВО (w < 0) ---
        self.get_logger().info(f"2. Малюємо праве коло. Час: {duration:.2f}s")
        self.drive_circle(v, -abs(w), duration, dt)

        # Зупинка після завершення
        self.pub.publish(TwistStamped())
        self.get_logger().info("Вісімка завершена!")


    def drive_circle(self, v, w, duration, dt):
        """Допоміжна функція для руху по колу протягом заданого часу"""
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


def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()