#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        
        # Створюємо підписника на топік /lidar
        self.subscription = self.create_subscription(
            LaserScan,
            '/lidar',
            self.listener_callback,
            10)
        self.subscription  # запобігає попередженню про невикористану змінну
        
        self.get_logger().info('Підписник лідара запущено - чекаю на дані...')

    def listener_callback(self, msg):
        """Ця функція викликається щоразу, коли приходить нове повідомлення від лідара"""
        
        # msg.ranges містить масив з 640 вимірів відстаней
        ranges = msg.ranges
        
        # Відфільтровуємо помилкові значення (занадто близько або занадто далеко)
        valid_ranges = [r for r in ranges if msg.range_min < r < msg.range_max]
        
        if valid_ranges:
            # Знаходимо найближчу перешкоду
            min_distance = min(valid_ranges)
            self.get_logger().info(f'Найближча перешкода на відстані: {min_distance:.2f} метрів')
        else:
            self.get_logger().info('Перешкод не виявлено (або вони поза зоною видимості)')


def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    
    try:
        rclpy.spin(node)  # Змушує вузол працювати, поки ви його не зупините (Ctrl+C)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()