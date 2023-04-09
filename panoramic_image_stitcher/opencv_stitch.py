import cv2
import numpy as np


def load_images(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        img = cv2.resize(img, (1272, 713))  # You may need to adjust the dimensions depending on your images
        images.append(img)
    return images


def stitch_images(images):
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA) if int(cv2.__version__.split('.')[0]) >= 4 else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)

    if status == 0:
        return stitched
    else:
        print("Error during stitching. Status code:", status)
        return None



def main():
    image_paths = ['4.png', '5.png']
    images = load_images(image_paths)
    stitched = stitch_images(images)

    if stitched is not None:
        cv2.imwrite('result.png', stitched)
        print("Stitched image saved as 'result.png'.")

if __name__ == "__main__":
    main()
