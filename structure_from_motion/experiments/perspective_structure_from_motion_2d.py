import numpy as np
import cv2

def normalize_points(points):
    mean = np.mean(points, axis=1, keepdims=True)
    std_dev = np.std(points)
    norm_points = (points - mean) / std_dev
    T = np.array([[1 / std_dev, 0, -mean[0] / std_dev],
                  [0, 1 / std_dev, -mean[1] / std_dev],
                  [0, 0, 1]])
    return norm_points, T

def fundamental_matrix(points1, points2):
    norm_points1, T1 = normalize_points(points1)
    norm_points2, T2 = normalize_points(points2)

    num_points = points1.shape[1]
    A = np.zeros((num_points, 9))
    for i in range(num_points):
        x1, y1 = norm_points1[:, i]
        x2, y2 = norm_points2[:, i]
        A[i] = [x1 * x2, x1 * y2, x1, y1 * x2, y1 * y2, y1, x2, y2, 1]

    _, _, Vt = np.linalg.svd(A)
    F_norm = Vt[-1].reshape(3, 3)
    U, S, Vt = np.linalg.svd(F_norm)
    S[-1] = 0
    F = U @ np.diag(S) @ Vt
    F = T2.T @ F @ T1

    return F

def extract_motion_structure(W, K):
    num_frames = W.shape[0]
    num_points = W.shape[1]

    # Create the W matrix with updated y image components
    W_updated = np.zeros((2 * num_frames, num_points))
    W_updated[:num_frames, :] = W
    W = W_updated

    for i in range(num_frames - 1):
        points1 = W[2 * i: 2 * i + 2]
        points2 = W[2 * i + 2: 2 * i + 4]
        F = fundamental_matrix(points1, points2)

        E = K.T @ F @ K
        _, R, t = cv2.recoverPose(E, points1.T, points2.T, K, distanceThresh=1e-6)

        if i == 0:
            M = np.zeros((2 * num_frames, 4))
            M[2 * i: 2 * (i + 1)] = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
            M[2 * (i + 1): 2 * (i + 2)] = K @ np.hstack([R, t])

    U, S, Vt = np.linalg.svd(W)
    S = np.diag(S)[:3, :]
    U = U[:, :3]
    Vt = Vt[:3, :]

    R = U @ np.sqrt(S)
    S = np.sqrt(S) @ Vt

    return R, S



W = np.load('W_test.npy')

# Create the identity matrix K
K = np.eye(3)

# Call the extract_motion_structure function
motion_matrix, structure_matrix = extract_motion_structure(W, K)