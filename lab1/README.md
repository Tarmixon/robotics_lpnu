# Lab 1: Building a Robot in Gazebo

**Author:** [Your Name / Surname] (GitHub: Tarmixon)
**Course:** Introduction to Robotics

---

## 🎯 Objective
To get familiar with the SDF format and the Gazebo Harmonic simulation environment. To create a custom mobile robot model, configure its motion physics, and integrate sensors for environment perception.

## 🛠 What was done
In this laboratory work, the `robot.sdf` world was created, which includes:

1. **Mobile Robot (4WD):**
   * Created a chassis (main body) with specified inertia and mass parameters.
   * Added **4 wheels** (two on each side), connected to the chassis using `revolute` joints.

2. **Motion Control:**
   * Integrated the `gz-sim-diff-drive-system` (Differential Drive) plugin.
   * Configured the plugin for 4-wheel drive (all 4 wheels are properly linked to the control system).
   * The robot subscribes to the `/cmd_vel` topic to receive velocity commands.

3. **LiDAR Sensor:**
   * Mounted a separate object (`link`) for the LiDAR sensor on the chassis using a `fixed` joint.
   * Configured the `gpu_lidar` to scan with 640 rays.
   * Enabled ray visualization in the simulator (`<visualize>true</visualize>`).
   * Sensor data is published to the `/lidar` topic.

4. **Testing Environment:**
   * Added 3 static obstacles for LiDAR testing:
     - Red box (`red_box`)
     - Green cylinder (`green_cylinder`)
     - Gray wall (`gray_wall`)

---

## 🚀 How to run the simulation

1. **Open a terminal** in the main project folder (`robotics_lpnu`) and start the Docker container:
   ```bash
   ./scripts/cmd run
   ```

2. **Launch the Gazebo world** (inside the container):
   ```bash
   gz sim /opt/ws/src/code/lab1/worlds/robot.sdf
   ```

## 🎮 How to control the robot and check sensors

To interact with the robot, open a **second terminal**, navigate to the project folder, and enter the container:
```bash
./scripts/cmd bash
```

**Checking LiDAR data:**
To see the array of distance data to obstacles in real-time, run:
```bash
gz topic -e -t /lidar
```

**Moving the robot:**
To make the robot move forward with a slight turn (moving in an arc), send a Twist message to the control topic:
```bash
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.2}"
```
*(To stop the robot, send the same command with values set to 0).*
