# Camera Calibration using Fisheye Lens Model

This repository contains a Python script for calibrating a fisheye camera using a checkerboard pattern. It is based on the OpenCV library and the calibration technique detailed in [this Medium article](https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0) by Kenneth Jiang.

## Overview

The camera calibration process calculates the camera matrix (K) and distortion coefficients (D), which are essential for correcting the distortion in the captured images. The script provided in this repository takes a set of checkerboard images, detects the checkerboard corners, and then uses the detected corners to compute the camera matrix and distortion coefficients.
