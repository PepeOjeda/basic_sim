# BasicSim

A minimal ROS2 robotic simulator, with emphasis on **minimal**. Meant to replace [Stage](https://github.com/rtv/Stage) for applications where you only need extremely basic 2D movement (since Stage in not supported in ROS2).

Does:

- Publishes `/clock`, with the ability to speed up or slow down time.
- Publishes a static `map -> odom` TF for when you don't need to simulate actual localization.
- Publishes `odom -> (robot)_base_link` TF for each robot.
- Listens to `/(robot)/cmd_vel` and applies the velocity commands to move the robot.
- Reads ros2 OccupancyGrid files (same format as map_server) and keeps the robot outside of walls.
- Keeps track of multiple robots in the same simulation session.
- Simulates 2D laser scanners.

Does not do:
- Physics.
- Velocity or acceleration limits.
- Any sensors other than 2D laser scanners.
- Robot-robot collision.