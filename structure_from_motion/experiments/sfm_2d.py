import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import pinv

EPSILON = 1e-8

def hom_to_cart(p):
    try:
        assert np.size(p)==3
    except:
        raise ValueError
    x = p[0] / p[2]
    y = p[1] / p[2]
    return np.array([x,y])

# Function to solve least squares
def solve_least_square_pseudo(M, frames):
    C = np.zeros((2,2))
    I = np.identity(2 * frames)

    b = I @ np.linalg.pinv(M.T)

    # Solve for x using least squares
    C, residuals, rank, s = np.linalg.lstsq(M, b, rcond=None)

    return C


def structure_from_motion(W, perspective:bool=False):
    m_views, n_points = W.shape

    # Center the data
    T_data = np.mean(W, axis=1)
    W_centered = (W - T_data.reshape(-1, 1))

    if perspective:
    # for each view: mi diag(λi) = Pi M

        lambdas = np.ones((m_views, n_points))  # initial values

        for iter in range(50):
            # normalize lamdas
            # pass over rows:
            for i in range(lambdas.shape[0]):
                lambdas[i,:] /= np.linalg.norm(lambdas[i,:])
            # pass over columns:
            for j in range(lambdas.shape[1]):
                lambdas[:,j] /= np.linalg.norm(lambdas[:,j])

            # form 2m x n measurement matrix, current W is already (xi yi 1, xi yi 1, ...) -- just need to insert 1's to make homogeneous
            # W is rank 3
            W_ = np.zeros((2*m_views, n_points))
            for i in range(m_views):
                W_[i:i+2, :] = lambdas[i, :] * np.array([W[i, :], np.ones(n_points)])
            
            # Factor W with SVD (rank 3 approximation)
            U,D,Vt = np.linalg.svd(W_, full_matrices=True)
            P = U[:,:3] @ np.diag(D[:3])
            M = Vt[:3]

            # stopping criterion: sigma_4 is small
            if D[3] < EPSILON:
                break

            # Estimate lambda from each view reprojected
            # mi (2 x n_points) @ lamdai (diag n_points) = Pi (2 x 3) @ M (3 x n_points)
            # source: https://math.stackexchange.com/questions/1733330/least-squares-solution-for-a-matrix-system-with-diagonal-matrix-constraint
            for i in range(m_views):
                A = W_[i:i+2,:]
                B = P[i:i+2,:] @ M
                lambdas[i, :] = np.linalg.inv(np.eye(n_points)*(A.T @ A)) @ np.diag(A.T @ B)
                # lambdas[i, :] = np.linalg.solve(np.eye(n_points), np.linalg.pinv(W_[i:i+2,:]) @ P[i:i+2,:] @ M)

        print(f"stopping lambda estimation after {iter+1} iterations")
        
        # convert back to cartesian coords
        M = M.T
        for i in range(M.shape[0]):
            X = np.empty((M.shape[0], 2))
            X[i] = hom_to_cart(M[i])
        X = X.T
        

    else:


        # Compute SVD of the centered data 
        U, S, Vt = np.linalg.svd(W_centered)

        print(W.shape)

        # Recover the affine camera and shape matrices
        # M_affine = U[:, :3] @ np.diag(S[:3])
        # S_affine = np.diag(S[:3]) @ Vt[:3, :]
        M = U[:, :2]
        X = Vt[:2, :]
        X = np.diag(S[:2]) @ Vt[:2, :]

        # Solve for C based on orthagonality constraint:
        # Mx C Mx_T = I(n_views x n_views)
        # My C My_T = I
        # Mx C My_T = 0
        # My C Mx_T = 0

        # Pull x,y data from M
        # Mx = M[::2]
        # My = M[1::2]
        # C = pinv(np.vstack((Mx, My, Mx))) @ np.vstack((pinv(Mx.T), pinv(My.T), np.zeros((frames//2, 2))))

        # Solve for C using least squares
        # C = solve_least_square(M, frames)
        # C = solve_least_square_pseudo(M, frames)

        # Compute Q using Cholesky decomposition
        # Q = np.linalg.cholesky(C)

        # Compute X
        # X = Q.T @ X

    # Plot the points
    plt.scatter(*X)
    plt.title('Reconstructed')
    plt.show()
    pass

if __name__=='__main__':
    W = np.load('W_test.npy')
    print('W: ', W.shape)
    structure_from_motion(W, perspective=True)