import numpy as np
import cv2

def compute_hand_eye_calibration(base_to_object_matrices, cam_to_object_matrices):
    """
    base_to_object_matrices: List of T_base^object matrices (4x4 numpy arrays)
    cam_to_object_matrices: List of T_cam^object matrices (4x4 numpy arrays)
    Returns:
        T_base^cam: 4x4 homogeneous transformation matrix from robot base to camera
    """
    assert len(base_to_object_matrices) == len(cam_to_object_matrices), "Matrix list sizes must match"
    
    # Prepare data for OpenCV hand-eye calibration function
    base_rotations = []
    base_translations = []
    cam_rotations = []
    cam_translations = []

    for T_base_obj, T_cam_obj in zip(base_to_object_matrices, cam_to_object_matrices):
        # Decompose the base-to-object matrix into rotation and translation
        R_base_obj = T_base_obj[:3, :3]  # Extract rotation
        t_base_obj = T_base_obj[:3, 3]   # Extract translation

        # Decompose the cam-to-object matrix into rotation and translation
        R_cam_obj = T_cam_obj[:3, :3]    # Extract rotation
        t_cam_obj = T_cam_obj[:3, 3]     # Extract translation

        # Convert rotation matrices to rotation vectors (Rodrigues format) for OpenCV
        rot_vec_base_obj, _ = cv2.Rodrigues(R_base_obj)
        rot_vec_cam_obj, _ = cv2.Rodrigues(R_cam_obj)

        # Append data to the lists
        base_rotations.append(rot_vec_base_obj)
        base_translations.append(t_base_obj)
        cam_rotations.append(rot_vec_cam_obj)
        cam_translations.append(t_cam_obj)

    # Convert lists to NumPy arrays
    base_rotations = np.array(base_rotations)
    base_translations = np.array(base_translations)
    cam_rotations = np.array(cam_rotations)
    cam_translations = np.array(cam_translations)

    # Perform hand-eye calibration using OpenCV
    retval, R_base_cam, t_base_cam = cv2.calibrateHandEye(
        R_gripper2base=base_rotations,
        t_gripper2base=base_translations,
        R_target2cam=cam_rotations,
        t_target2cam=cam_translations,
        method=cv2.CALIB_HAND_EYE_TSAI  # Use Tsai-Lenz algorithm
    )

    # Convert rotation vector to rotation matrix
    R_base_cam_mat, _ = cv2.Rodrigues(R_base_cam)

    # Construct the final transformation matrix T_base^cam
    T_base_cam = np.eye(4)
    T_base_cam[:3, :3] = R_base_cam_mat  # Set rotation
    T_base_cam[:3, 3] = t_base_cam       # Set translation

    return T_base_cam

# 예제 입력 (로봇 좌표계와 카메라 좌표계에서 물체의 변환 행렬들)
T_base_to_object_1 = np.array([[0.866, -0.5, 0, 1.0],
                               [0.5, 0.866, 0, 0.5],
                               [0, 0, 1, 1.5],
                               [0, 0, 0, 1]])

T_cam_to_object_1 = np.array([[0.707, -0.707, 0, 0.8],
                              [0.707, 0.707, 0, 0.6],
                              [0, 0, 1, 1.2],
                              [0, 0, 0, 1]])

T_base_to_object_2 = np.array([[1, 0, 0, 1.5],
                               [0, 1, 0, 0.8],
                               [0, 0, 1, 1.3],
                               [0, 0, 0, 1]])

T_cam_to_object_2 = np.array([[0.866, -0.5, 0, 0.9],
                              [0.5, 0.866, 0, 0.7],
                              [0, 0, 1, 1.4],
                              [0, 0, 0, 1]])

# 여러 개의 변환 행렬 리스트
base_to_object_matrices = [T_base_to_object_1, T_base_to_object_2]
cam_to_object_matrices = [T_cam_to_object_1, T_cam_to_object_2]

# 최종 변환 행렬 계산
T_base_cam = compute_hand_eye_calibration(base_to_object_matrices, cam_to_object_matrices)

# 결과 출력
print("T_base^cam (robot base to camera transformation matrix):")
print(T_base_cam)
