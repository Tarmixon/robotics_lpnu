import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan


class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__("obstacle_avoidance")

        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("goal_x", 3.0)
        self.declare_parameter("goal_y", 3.0)

        scan_topic = self.get_parameter("scan_topic").value
        odom_topic = self.get_parameter("odom_topic").value
        cmd_vel_topic = self.get_parameter("cmd_vel_topic").value

        self.goal_x = float(self.get_parameter("goal_x").value)
        self.goal_y = float(self.get_parameter("goal_y").value)

        self.cmd_pub = self.create_publisher(TwistStamped, cmd_vel_topic, 10)

        self.create_subscription(LaserScan, scan_topic, self.scan_callback, 10)
        self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)

        self.timer = self.create_timer(0.1, self.control_loop)

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.front_distance = float("inf")
        self.left_distance = float("inf")
        self.right_distance = float("inf")

        self.goal_tolerance = 0.2
        self.obstacle_threshold = 0.6

        self.get_logger().info("Obstacle avoidance node started")

    def scan_callback(self, msg):       
        ranges = list(msg.ranges)

        if not ranges:
            self.front_distance = float("inf")
            self.left_distance = float("inf")
            self.right_distance = float("inf")
            return

        valid = [r if math.isfinite(r) and r > 0.0 else float("inf") for r in ranges]
        n = len(valid)
        center = n // 2
        window = 20

        front_ranges = valid[max(0, center - window): min(n, center + window)]
        left_ranges = valid[min(n - 1, center + 40): min(n, center + 100)]
        right_ranges = valid[max(0, center - 100): max(0, center - 40)]

        self.front_distance = min(front_ranges) if front_ranges else float("inf")
        self.left_distance = min(left_ranges) if left_ranges else float("inf")
        self.right_distance = min(right_ranges) if right_ranges else float("inf")

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        self.yaw = self.quaternion_to_yaw(q.x, q.y, q.z, q.w)

    def quaternion_to_yaw(self, x, y, z, w):
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        return math.atan2(siny_cosp, cosy_cosp)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def control_loop(self):
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = ""

        dx = self.goal_x - self.x
        dy = self.goal_y - self.y
        distance_to_goal = math.sqrt(dx * dx + dy * dy)

        goal_angle = math.atan2(dy, dx)
        angle_error = self.normalize_angle(goal_angle - self.yaw)

        if distance_to_goal < 0.15:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = 0.0
            self.cmd_pub.publish(cmd)
            self.get_logger().info(f"Goal reached at x={self.x:.2f}, y={self.y:.2f}")
            return

        # якщо попереду близько перешкода — повертайся
        if self.front_distance < 0.5:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = 0.5

        # якщо сильно не дивишся на ціль — спочатку повернись до цілі
        elif abs(angle_error) > 0.25:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = max(-0.6, min(0.6, 1.5 * angle_error))

        # інакше їдь вперед
        else:
            cmd.twist.linear.x = min(0.12, 0.08 * distance_to_goal)
            cmd.twist.angular.z = max(-0.4, min(0.4, 1.0 * angle_error))

        self.get_logger().info(
            f"x={self.x:.2f}, y={self.y:.2f}, "
            f"goal=({self.goal_x:.2f}, {self.goal_y:.2f}), "
            f"dist={distance_to_goal:.2f}, "
            f"front={self.front_distance:.2f}, "
            f"ang_err={angle_error:.2f}, "
            f"lin={cmd.twist.linear.x:.2f}, ang={cmd.twist.angular.z:.2f}"
        )

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    stop_cmd = TwistStamped()
    stop_cmd.header.stamp = node.get_clock().now().to_msg()
    stop_cmd.twist.linear.x = 0.0
    stop_cmd.twist.angular.z = 0.0
    node.cmd_pub.publish(stop_cmd)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()