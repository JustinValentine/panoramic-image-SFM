import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import pinv

# Function to solve least squares
def solve_least_square_pseudo(M, frames):
    # print(M.shape)
    C = np.zeros((2, 2))
    I = np.identity(1 * frames)

    b = I @ np.linalg.pinv(M.T)

    # Solve for x using least squares
    C, residuals, rank, s = np.linalg.lstsq(M, b, rcond=None)

    return C


def structure_from_motion(W):
    frames, landmarks = W.shape

    # Center the data
    T_data = np.mean(W, axis=1)
    W_centered = (W - T_data.reshape(-1, 1)) 

    # Compute SVD of the centered data 
    U, S, Vt = np.linalg.svd(W_centered)

    # Recover the affine camera and shape matrices
    # M_affine = U[:, :3] @ np.diag(S[:3])
    # S_affine = np.diag(S[:3]) @ Vt[:3, :]
    M = U[:, :2]
    X = Vt[:2, :]
    X = np.diag(S[:2]) @ Vt[:2, :]

    # shear_factor = 0.5  # Replace this with your desired shear value
    # shear_matrix = np.array([[1, shear_factor],
    #                         [0, 1]])
    
    # X = shear_matrix @ X


    # # # Solve for C using least squares
    # C = solve_least_square_pseudo(M, frames)

    # # # Compute Q using Cholesky decomposition
    # Q = np.linalg.cholesky(C)

    # # Compute X
    # X = Q.T @ X

    # Plot the points
    plt.scatter(*X)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title('Reconstructed')
    plt.show()
    

if __name__=='__main__':
    W = np.load('W_test.npy')[:, :]
    structure_from_motion(W)