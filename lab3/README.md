# Laboratory Work 3: Robot Motion Control

## Overview
This package implements various motion control strategies for a 4-wheeled differential drive robot in a ROS 2 / Gazebo environment. The focus is on implementing both timed (open-loop) and odometry-based (closed-loop) trajectories.
## Implemented Trajectories

### 1. Circular Path (circle_path.py)
- **Control Type:** Open-loop (timed).
- **Logic:** Calculates the time required to complete a 360-degree turn based on the angular velocity ($T = 2\pi / \omega$).
- **Launch:** ```bash
ros2 run lab3 circle_path
### 2. Square Path (square_path.py)
- **Control Type:** Closed-loop (Odometry feedback).
- **Logic:** Uses real-time data from the `/model/vehicle_blue/odometry` topic. It monitors position (x, y) to travel a specific side length and orientation (yaw) to perform precise 90-degree turns.
- **Launch:**
```bash
ros2 run lab3 square_path --ros-args -p linear_speed:=0.2 -p angular_speed:=0.25
### 3. Figure-8 Path (figure_8_path.py)
- **Control Type:** Combined timed motion.
- **Logic:** Executes two consecutive circles in opposite directions (clockwise and counter-clockwise) to form a "figure-eight" shape.
- **Launch:**
```bash
ros2 run lab3 figure_8_path
## Setup and Installation

1. **Build the package:**
   ```bash
   cd /opt/ws
   colcon build --packages-select lab3
   source install/setup.bash
### Section 6: Visualization and Technical Details
```markdown
## Visualization in RViz2
To visualize the robot's actual path:
1. Ensure the **Fixed Frame** is set to `vehicle_blue/odom`.
2. Ensure the **Path** display is active and subscribed to the `/path` topic.
3. Use the **Reset** button in the bottom-left corner of RViz2 to clear previous trajectories.

## Technical Details
- **Message Type:** `geometry_msgs/TwistStamped`
- **Odometry Topic:** `/model/vehicle_blue/odometry`
- **Coordinate System:** REP-105 compliant (base_link, odom).
- **Robot Model:** Custom 4-wheeled vehicle defined in `robot.sdf`.
