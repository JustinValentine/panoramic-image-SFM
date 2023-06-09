import cv2
import os
import numpy as np
from cylindrical_image_projection import CylindricalProjector


def load_images(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        images.append(img)
    return images

def stitch_images(images):
    projector = CylindricalProjector()

    cylindrical_images = [projector.project_onto_cylinder(img) for img in images]

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA) if int(cv2.__version__.split('.')[0]) >= 4 else cv2.Stitcher_create()

    (status, stitched) = stitcher.stitch(cylindrical_images)

    if status == 0:
        return stitched
    else:
        print("Error during stitching. Status code:", status)
        return None

def main():
    image_directory = 'undistorted'
    image_paths = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith('.png')]

    images = load_images(image_paths)
    stitched = stitch_images(images)

    if stitched is not None:
        cv2.imwrite('result.png', stitched)
        print("Stitched image saved as 'result.png'.")

if __name__ == "__main__":
    main()
