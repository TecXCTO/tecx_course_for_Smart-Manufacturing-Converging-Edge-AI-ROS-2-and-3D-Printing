from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Global Coordinate Frame Origin Node Definition
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='world_to_cell_base',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'cell_base_link']
        ),

        # 2. Arm 1 Coordinate Frame: Additive Deposition Subsystem Offset
        # Positioned 0.5 meters to the left (-0.5m Y) of the center cell base
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='cell_base_to_arm_additive',
            arguments=['0', '-0.5', '0', '0', '0', '0', 'cell_base_link', 'arm_additive_base']
        ),

        # 3. Arm 2 Coordinate Frame: Subtractive Milling Subsystem Offset
        # Positioned 0.5 meters to the right (+0.5m Y) of the center cell base
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='cell_base_to_arm_subtractive',
            arguments=['0', '0.5', '0', '0', '0', '0', 'cell_base_link', 'arm_subtractive_base']
        ),

        # 4. Shared Build Plate Assembly Coordinate Mapping Target Center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='cell_base_to_build_plate',
            arguments=['0.6', '0', '-0.1', '0', '0', '0', 'cell_base_link', 'shared_build_plate']
        )
    ])
  
