import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import pinv

EPSILON = 1e-8

def plot3d(x, title:str):
    # TODO make sure to covert homogenous coords back to cartesian in 3D
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(*x)
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show()

def hom_to_cart(p):
    try:
        assert np.size(p)==3 or np.size(p)==4
    except:
        raise ValueError
    n = np.size(p)
    cart = []
    for i in range(n-1):
        cart.append(p[i] / p[-1])
    return np.array(cart)

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

            # form 3m x n measurement matrix, current W is ALREADY (xi yi 1, xi yi 1, ...) - need to modify to homoeneous and set y=0
            # W is rank 4
            W_ = np.zeros((3*m_views, n_points))
            for i in range(m_views):
                W_[i:i+3, :] = lambdas[i, :] * np.array([W[i, :], np.zeros(n_points), np.ones(n_points)])
            
            # Factor W with SVD (rank 4 approximation)
            U,D,Vt = np.linalg.svd(W_, full_matrices=True)
            P = U[:,:4] @ np.diag(D[:4])
            M = Vt[:4]

            # stopping criterion: sigma_5 is small
            if D[4] < EPSILON:
                break

            # Estimate lambda from each view reprojected
            # mi (3 x n_points) @ lamdai (diag n_points) = Pi (3 x 4) @ M (4 x n_points)
            # source: https://math.stackexchange.com/questions/1733330/least-squares-solution-for-a-matrix-system-with-diagonal-matrix-constraint
            for i in range(m_views):
                A = W_[i:i+3,:]
                B = P[i:i+3,:] @ M
                lambdas[i, :] = np.linalg.inv(np.eye(n_points)*(A.T @ A)) @ np.diag(A.T @ B)
                # lambdas[i, :] = np.linalg.solve(np.eye(n_points), np.linalg.pinv(W_[i:i+3,:]) @ P[i:i+3,:] @ M)

        print(f"stopping lambda estimation after {iter+1} iterations")
        
        # convert back to cartesian coords
        M = M.T
        for i in range(M.shape[0]):
            X = np.empty((M.shape[0], 3))
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
    plot3d(X, 'Reconstructed points')   # should be more of a 2D plane-?
    # plt.scatter(*X)
    # plt.title('Reconstructed')
    # plt.show()
    pass

if __name__=='__main__':
    W = np.load('W_test.npy')
    print('W: ', W.shape)
    structure_from_motion(W, perspective=True)