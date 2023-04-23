# Robot Control with PS4 Controller

This repository contains a Python script for controlling a robot using a PS4 controller. It utilizes the `hid` library for reading PS4 controller inputs and the `serial` library for sending commands to the robot. The script also captures images from multiple cameras connected to the robot as it moves.

## Overview

The script connects to the robot via a serial connection, reads input from a PS4 controller, calculates the desired wheel velocities, and sends commands to the robot accordingly. Additionally, it captures images from all available cameras connected to the robot and saves them in a designated folder.

## Usage

1. Connect the robot and cameras to your computer.
2. Connect the PS4 controller to your computer.
3. Run the robot control script
`robot_drive_mac.py`
