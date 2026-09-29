# ridgeback_sim

A ROS 2 simulation of a Clearpath Ridgeback-style mobile base in Ignition Gazebo. The robot is driven with standard `geometry_msgs/msg/Twist` commands on `/cmd_vel`, which are relayed and bridged into the simulator.

## Features

- Ridgeback model (SDF) with a four-wheel differential drive, IMU and GPU lidar
- `ros_gz_bridge` connecting ROS 2 and Ignition Gazebo topics
- Command relay from `/cmd_vel` to the model-specific Gazebo topic
- Interactive keyboard-style velocity commander (`ridgeback_sim_control`)
- Sensor listener node for checking IMU and lidar data

## Repository layout

```
ridgeback_sim/
├── ridgeback_sim_launch/     # launch file, robot model (SDF), bridge config
│   ├── launch/ridgeback_sim.launch.py
│   └── models/ridgeback.sdf
└── ridgeback_sim_control/    # velocity_commander.py and related nodes
```

## Requirements

- Ubuntu with ROS 2 (fill in your distro, e.g. Humble)
- Ignition Gazebo (fill in your version, e.g. Fortress)
- `ros_gz_bridge` and `ros_gz_sim` for your ROS 2 / Gazebo pairing
- `colcon`

## Build

```bash
cd ~/ridgeback_sim
colcon build
source install/setup.bash
```

## Run

```bash
ros2 launch ridgeback_sim_launch ridgeback_sim.launch.py
```

In a second terminal (source the workspace first):

```bash
source ~/ridgeback_sim/install/setup.bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}}"
```

Stop the robot:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"
```

## How commands reach the robot

```
ROS /cmd_vel
   → relay node
   → ROS /model/ridgeback/cmd_vel
   → ros_gz_bridge
   → Gazebo /model/ridgeback/cmd_vel
   → DiffDrive plugin
```

The DiffDrive plugin in `ridgeback.sdf` must use `<topic>/model/ridgeback/cmd_vel</topic>` so it matches the bridge. The bridge argument must use the ROS 2 message type name:

```
/model/ridgeback/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist
```

## Verify it works

Check the pose in Gazebo while publishing commands:

```bash
ign topic -e -t /model/ridgeback/tf -n 1
```

`position.x` should increase while a forward command is being published.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Robot doesn't move, `ros2 topic info /model/ridgeback/cmd_vel` shows 0 subscribers | Bridge failed to start. Check for old-style type names like `geometry_msgs/Twist`; use `geometry_msgs/msg/Twist`. |
| Subscriber exists but robot still doesn't move | SDF `<topic>` doesn't match the Gazebo topic the bridge publishes to. Rebuild after editing the SDF, since the sim uses the copy under `install/`. |
| Extra models like `ridgeback_0` appear | Leftover processes from an earlier run. Stop everything and relaunch. |

## Known limitations

- DiffDrive ignores `linear.y`, so the base cannot strafe. A holonomic drive plugin is needed for that.
- Odometry uses a global topic name; change `<odom_topic>` to a per-model name before running multiple robots.

## Roadmap

- Bridge odometry and lidar into ROS 2 with correct message types
- SLAM and Nav2 integration
- Multi-robot support with per-model topic names


