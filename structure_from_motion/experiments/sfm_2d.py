import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import pinv

# Function to solve least squares
def solve_least_square_pseudo(M, frames):
    C = np.zeros((2,2))
    I = np.identity(2 * frames)

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

    print(W.shape)

    # Recover the affine camera and shape matrices
    # M_affine = U[:, :3] @ np.diag(S[:3])
    # S_affine = np.diag(S[:3]) @ Vt[:3, :]
    M = U[:, :2]
    X = Vt[:2, :]
    # X = np.diag(S[:2]) @ Vt[:2, :]

    # Solve for C based on orthagonality constraint:
    # Mx C Mx_T = I(n_views x n_views)
    # My C My_T = I
    # Mx C My_T = 0
    # My C Mx_T = 0

    # Pull x,y data from M
    Mx = M[::2]
    My = M[1::2]
    C = pinv(np.vstack((Mx, My, Mx))) @ np.vstack((pinv(Mx.T), pinv(My.T), np.zeros((frames//2, 2))))

    # Solve for C using least squares
    # C = solve_least_square(M, frames)
    # C = solve_least_square_pseudo(M, frames)

    # Compute Q using Cholesky decomposition
    Q = np.linalg.cholesky(C)

    # Compute X
    X = Q.T @ X

    print(X)

    # Plot the points
    plt.scatter(*X)
    plt.title('Reconstructed')
    plt.show()
    pass

if __name__=='__main__':
    W = np.load('W_test.npy')
    structure_from_motion(W)