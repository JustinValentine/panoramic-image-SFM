# Image Stitching Pipeline

This repository contains a collection of Python scripts for an image stitching pipeline. The pipeline includes capturing images from multiple cameras, removing lens distortion, projecting the images onto a cylindrical surface, and stitching the images together using OpenCV.

## Overview

1. **image_capture.py**: Captures images from multiple cameras connected to the computer.
2. **remove_lens_distortion.py**: Removes lens distortion from the captured images using precomputed camera calibration parameters.
3. **cylindrical_image_projection.py**: Projects the undistorted images onto a cylindrical surface.
4. **opencv_stitch.py**: Stitches the cylindrical images together using OpenCV's `Stitcher` class.
