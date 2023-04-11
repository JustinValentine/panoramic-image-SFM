import cv2
assert cv2.__version__[0] == '4', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
import re


# == Camera parameters used for undistorting images ==
# Image dimensions (width, height) in pixels
DIM = (1280, 720)

# Camera matrix (K) containing the intrinsic parameters
# fx, 0, cx
# 0, fy, cy
# 0, 0, 1
K = np.array([[841.6965076463126, 0.0, 649.7075294677106],
              [0.0, 843.3108958966243, 345.194752462267],
              [0.0, 0.0, 1.0]])

# Distortion coefficients (D) in a 4x1 matrix
# k1, k2, k3, k4
D = np.array([[-0.15731861318825355],
              [0.6570238677822058],
              [-1.1777835851933047],
              [0.7512100827398605]])


def undistort(img_path, balance=0.0, dim2=None, dim3=None):
    upsidedown_image = cv2.imread(img_path)
    img = cv2.flip(upsidedown_image, 0)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort

    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    # Get the height and width of the image
    height, width = undistorted_img.shape[:2]

    # Remove the specified number of pixels from the bottom, left, and right
    bottom_removed = height - 404
    left_removed = 37
    right_removed = width - 102

    # Crop the image
    cropped_image = undistorted_img[:bottom_removed, left_removed:right_removed]

    return cropped_image


input_directory = 'images'
output_directory = 'undistorted'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

folder_index = 0

for subdir, dirs, files in os.walk(input_directory):
    file_index = 0
    for file in files:
        if file.endswith('.jpg'):
            image_path = os.path.join(subdir, file)
            undistorted_image = undistort(image_path, balance=0.9, dim2=(2304, 1296), dim3=(1400, 1116))

            # Save the undistorted image with the new format
            output_path = os.path.join(output_directory, f'{folder_index}_{file_index}.png')
            cv2.imwrite(output_path, undistorted_image)
            file_index += 1

    # Get the index of the folder the image came from
    folder_index += 1
