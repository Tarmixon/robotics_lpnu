# Laboratory Work 4: Dead Reckoning Analysis

## Overview
This package implements the **Dead Reckoning** navigation method for a differential drive robot. The goal is to calculate the robot's pose (position and orientation) by integrating velocity commands over time and comparing this mathematical model with the ground truth data from Gazebo.

## Dead Reckoning Logic
The position is updated in real-time using kinematic equations:
- $x_{new} = x_{old} + v \cdot \cos(\theta) \cdot \Delta t$
- $y_{new} = y_{old} + v \cdot \sin(\theta) \cdot \Delta t$
- $\theta_{new} = \theta_{old} + \omega \cdot \Delta t$

## Drift Analysis (Why the arrow is far from the robot)
During the experiments, a significant drift (error accumulation) was observed. The "Ideal Pose" (arrow in RViz) diverges from the actual robot trajectory because:
1. **Discrete Integration:** We assume velocity is constant during $\Delta t$, which is an approximation.
2. **Physical Factors:** Gazebo simulates wheel slip and friction, which the mathematical model doesn't account for.
3. **Latency:** There is a delay between sending a command and the physical response of the robot.

## Execution
1. **Build the package:**
   ```bash
   colcon build --packages-select lab4
   source install/setup.bash
2. **Launch**
    ```bash
    ros2 launch lab4 dead_reckoning_bringup.launch.py