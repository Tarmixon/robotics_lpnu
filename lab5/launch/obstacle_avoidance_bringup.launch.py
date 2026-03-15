import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    lab3_pkg = get_package_share_directory('lab3')
    lab5_pkg = get_package_share_directory('lab5')

    # 1. Запуск Gazebo та RViz (ваша модель робота)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(lab3_pkg, 'launch', 'bringup.launch.py')]),
    )

    # 2. Запуск моста для Лідара (щоб не запускати вручну)
    lidar_bridge = ExecuteProcess(
        cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge', 
             '/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
        output='screen'
    )

    # 3. Ваш вузол оминання перешкод
    obstacle_node = Node(
        package='lab5',
        executable='obstacle_avoidance',
        name='obstacle_avoidance',
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        lidar_bridge,
        obstacle_node
    ])