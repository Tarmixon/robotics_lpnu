import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Назви пакетів (переконайтеся, що пакет lab3 містить ваш робот.sdf)
    lab4_pkg = get_package_share_directory('lab4')
    lab3_pkg = get_package_share_directory('lab3')

    # 1. Запуск Gazebo з вашим світом (беремо з ЛР3)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(lab3_pkg, 'launch', 'bringup.launch.py')]),
    )

    # 2. Вузол Dead Reckoning (головне завдання ЛР4)
    dead_reckoning_node = Node(
        package='lab4',
        executable='dead_reckoning',
        name='dead_reckoning',
        parameters=[{
            'odom_topic': '/model/vehicle_blue/odometry',
            'cmd_vel_topic': '/cmd_vel'
        }],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        dead_reckoning_node
    ])