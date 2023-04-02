import numpy as np
import os
import subprocess
import calibrate_camera


def load_or_calibrate():
    try:
        # Check if the files exist and are not empty
        if (os.path.exists('DIM.npy') and os.path.getsize('DIM.npy') > 0 and
            os.path.exists('K.npy') and os.path.getsize('K.npy') > 0 and
            os.path.exists('D.npy') and os.path.getsize('D.npy') > 0):

            DIM = np.load('DIM.npy')
            K = np.load('K.npy')
            D = np.load('D.npy')

        else:
            raise FileNotFoundError('One or more files are missing or empty.')

    except FileNotFoundError:
        print("Running calibrate_camera.py...")
        calibrate_camera()
        DIM = np.load('DIM.npy')
        K = np.load('K.npy')
        D = np.load('D.npy')

    return DIM, K, D

DIM, K, D = load_or_calibrate()

# Your code using DIM, K, and D here...
