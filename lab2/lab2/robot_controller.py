#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math


class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Створюємо публікатор для топіка /cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Створюємо таймер, який буде викликати функцію 10 разів на секунду (0.1с)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.counter = 0
        self.get_logger().info('Контролер робота запущено - публікуємо в /cmd_vel')

    def timer_callback(self):
        """Ця функція викликається кожні 0.1 секунди для надсилання команд"""
        msg = Twist()
        
        # Встановлюємо лінійну та кутову швидкості
        # linear.x - рух вперед/назад, angular.z - поворот
        msg.linear.x = 0.5  # Їдемо вперед зі швидкістю 0.5 м/с
        msg.angular.z = 0.3 * math.sin(self.counter * 0.1)  # Рух по синусоїді (хвилею)
        
        # Публікуємо повідомлення
        self.publisher.publish(msg)
        
        self.counter += 1
        
        # Виводимо лог у термінал кожні 5 секунд (50 тіків по 0.1с)
        if self.counter % 50 == 0:
            self.get_logger().info(
                f'Публікую: linear.x={msg.linear.x:.2f}, '
                f'angular.z={msg.angular.z:.2f}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    
    try:
        rclpy.spin(node)  # Змушує вузол працювати нескінченно
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()