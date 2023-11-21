import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,SetLaunchConfiguration,IncludeLaunchDescription,SetEnvironmentVariable,OpaqueFunction,GroupAction
from launch.launch_description_sources import FrontendLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory
from launch.frontend.parse_substitution import parse_substitution
import xacro

#===========================
def launch_arguments():
    return [
        DeclareLaunchArgument("worldFile", default_value="test.yaml"),
    ]
#==========================

def launch_setup(context, *args, **kwargs):
    test_dir = os.path.join(get_package_share_directory("basic_sim"), "test")

    # robot description for state_publisher
    robot_desc1 = xacro.process_file(
        os.path.join(test_dir, "giraff.xacro"),
        mappings={"frame_ns": "giraff1"},
    )
    robot_desc1 = robot_desc1.toprettyxml(indent="  ")

    visualization_nodes = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"use_sim_time": True, "robot_description": robot_desc1}],
    )

    basic_sim = Node(
            package="basic_sim",
            executable="basic_sim",
            #prefix = "xterm -e gdb --args",
            parameters=[
                {"deltaTime": 0.1},
                {"speed": 1.0},
                {"worldFile": os.path.join(test_dir, LaunchConfiguration("worldFile").perform(context))}
                ],
        )
    
    keyboard_control1 = Node(
            package="keyboard_control",
            executable="keyboard_control_plus",
            prefix = "xterm -e",
            parameters=[
                {"linear_v_inc": 0.1},
                {"angular_v_inc": 0.3},
                {"publish_topic": "/giraff1/cmd_vel"}
                ],
        )
    keyboard_control2 = Node(
            package="keyboard_control",
            executable="keyboard_control_plus",
            prefix = "xterm -e",
            parameters=[
                {"linear_v_inc": 0.1},
                {"angular_v_inc": 0.3},
                {"publish_topic": "/giraff2/cmd_vel"}
                ],
        )
    
    return [
        visualization_nodes,
        #basic_sim,
        keyboard_control1,
        keyboard_control2
        ]


def generate_launch_description():

    launch_description = [
        # Set env var to print messages to stdout immediately
        SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1"),
        SetEnvironmentVariable("RCUTILS_COLORIZED_OUTPUT", "1"),
    ]
    
    launch_description.extend(launch_arguments())
    launch_description.append(OpaqueFunction(function=launch_setup))
    
    return  LaunchDescription(launch_description)