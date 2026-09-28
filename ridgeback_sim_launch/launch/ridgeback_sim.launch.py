#!/usr/bin/env python3
"""
Launch file for Ridgeback AMR simulation in Ignition Fortress
Starts Gazebo, spawns the robot, and brings up bridge + control nodes.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('ridgeback_sim_launch')
    worlds_dir = os.path.join(pkg_share, 'worlds')
    model_path = os.path.join(pkg_share, 'models', 'ridgeback.sdf')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world = LaunchConfiguration('world', default='empty')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true', description='Use simulated time'
    )
    declare_world = DeclareLaunchArgument(
        'world', default_value='empty', choices=['empty', 'obstacles'],
        description='World environment'
    )

    world_file = [worlds_dir, '/', world, '.sdf']

    gazebo_env = {
        'IGN_GAZEBO_RESOURCE_PATH': os.path.join(
            os.path.expanduser('~'), '.local/share/ignition'
        ),
    }

    ignition_server = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', '-s', '-v', '1', world_file],
        output='screen',
        additional_env=gazebo_env,
        name='ignition_server'
    )

    ignition_gui = ExecuteProcess(
        cmd=['ign', 'gazebo', '-g'],
        output='screen',
        additional_env=gazebo_env,
        name='ignition_gui'
    )

    spawn_ridgeback = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-file', model_path,
            '-name', 'ridgeback',
            '-x', '0', '-y', '0', '-z', '0.15',
            '-allow_renaming', 'false',
        ],
        output='screen',
        name='spawn_ridgeback'
    )
    # Give the server a few seconds to come up before spawning
    delayed_spawn = TimerAction(period=5.0, actions=[spawn_ridgeback])

    ignition_bridge = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
            '/model/ridgeback/odometry@nav_msgs/Odometry[ignition.msgs.Odometry',
            '/model/ridgeback/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/model/ridgeback/imu_sensor/imu@sensor_msgs/Imu[ignition.msgs.IMU',
            '/model/ridgeback/gpu_lidar/scan@sensor_msgs/LaserScan[ignition.msgs.LaserScan',
        ],
        output='screen',
        name='ros_gz_bridge'
    )

    cmd_vel_repeater = Node(
        package='topic_tools',
        executable='relay',
        arguments=['/cmd_vel', '/model/ridgeback/cmd_vel'],
        output='screen'
    )

    sensor_listener = Node(
        package='ridgeback_sim_control',
        executable='sensor_listener',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_world,
        ignition_server,
        ignition_gui,
        delayed_spawn,
        ignition_bridge,
        cmd_vel_repeater,
        sensor_listener,
    ])
