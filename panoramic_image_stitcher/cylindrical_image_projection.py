# cylindrical_image_projection.py
import numpy as np
import cv2

# Reference: https://stackoverflow.com/questions/68543804/image-stitching-problem-using-python-and-opencv

class CylindricalProjector:
    def __init__(self, focal_length=1100):
        self.f = focal_length
        self.center = None

    def convert_xy(self, x, y):
        xt = (self.f * np.tan((x - self.center[0]) / self.f)) + self.center[0]
        yt = ((y - self.center[1]) / np.cos((x - self.center[0]) / self.f)) + self.center[1]

        return xt, yt
    
    def project_onto_cylinder(self, initial_image):
        h, w = initial_image.shape[:2]
        self.center = [w // 2, h // 2]

        # Creating a blank transformed image
        TransformedImage = np.zeros(initial_image.shape, dtype=np.uint8)
        
        # Storing all coordinates of the transformed image in 2 arrays (x and y coordinates)
        AllCoordinates_of_ti =  np.array([np.array([i, j]) for i in range(w) for j in range(h)])
        ti_x = AllCoordinates_of_ti[:, 0]
        ti_y = AllCoordinates_of_ti[:, 1]
        
        # Finding corresponding coordinates of the transformed image in the initial image
        ii_x, ii_y = self.convert_xy(ti_x, ti_y)

        # Rounding off the coordinate values to get exact pixel values (top-left corner)
        ii_tl_x = ii_x.astype(int)
        ii_tl_y = ii_y.astype(int)

        # Finding transformed image points whose corresponding 
        # initial image points lies inside the initial image
        GoodIndices = (ii_tl_x >= 0) * (ii_tl_x <= (w-2)) * \
                    (ii_tl_y >= 0) * (ii_tl_y <= (h-2))

        # Removing all the outside points from everywhere
        ti_x = ti_x[GoodIndices]
        ti_y = ti_y[GoodIndices]
        
        ii_x = ii_x[GoodIndices]
        ii_y = ii_y[GoodIndices]

        ii_tl_x = ii_tl_x[GoodIndices]
        ii_tl_y = ii_tl_y[GoodIndices]

        # Bilinear interpolation
        dx = ii_x - ii_tl_x
        dy = ii_y - ii_tl_y

        weight_tl = (1.0 - dx) * (1.0 - dy)
        weight_tr = (dx)       * (1.0 - dy)
        weight_bl = (1.0 - dx) * (dy)
        weight_br = (dx)       * (dy)
        
        TransformedImage[ti_y, ti_x, :] = ( weight_tl[:, None] * initial_image[ii_tl_y,     ii_tl_x,     :] ) + \
                                        ( weight_tr[:, None] * initial_image[ii_tl_y,     ii_tl_x + 1, :] ) + \
                                        ( weight_bl[:, None] * initial_image[ii_tl_y + 1, ii_tl_x,     :] ) + \
                                        ( weight_br[:, None] * initial_image[ii_tl_y + 1, ii_tl_x + 1, :] )

        # Getting x coorinate to remove black region from right and left in the transformed image
        min_x = min(ti_x)

        # Cropping out the black region from both sides (using symmetricity)
        TransformedImage = TransformedImage[:, min_x : -min_x, :]

        return TransformedImage #, ti_x-min_x, ti_y


# img1 = cv2.imread("webcam_3.jpg")

# if img1 is None:
#     print("Error: Could not read the image.")

# else:
#     projector = CylindricalProjector()
#     cylindrical_img1 = projector.project_onto_cylinder(img1)

#     print("Image dimensions:", cylindrical_img1.shape)
#     print("Image type:", cylindrical_img1.dtype)

#     cv2.imwrite("result.png", cylindrical_img1)
