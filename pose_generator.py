import numpy as np


def create_pose_matrix(position, angles):
    x, y, z = position
    theta_x, theta_y, theta_z = angles

    # Translation matrix
    T = np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

    # Rotation matrices
    R_x = np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x), 0],
        [0, np.sin(theta_x), np.cos(theta_x), 0],
        [0, 0, 0, 1]
    ])

    R_y = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y), 0],
        [0, 1, 0, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y), 0],
        [0, 0, 0, 1]
    ])

    R_z = np.array([
        [np.cos(theta_z), -np.sin(theta_z), 0, 0],
        [np.sin(theta_z), np.cos(theta_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Combined rotation matrix
    R = R_z @ R_y @ R_x

    # Combined transformation matrix
    M = T @ R

    return M

def generate_poses(n_poses=4, distance=0.8, angle_jitter=-0.1):
    pose_angle = 2*np.pi/n_poses+angle_jitter
    R_y = np.array([
        [np.cos(pose_angle), 0, np.sin(pose_angle), 0],
        [0, 1, 0, 0],
        [-np.sin(pose_angle), 0, np.cos(pose_angle), 0],
        [0, 0, 0, 1]
    ])
    lig_offset = np.pi/16
    R_y_light = np.array([
        [np.cos(lig_offset), 0, np.sin(lig_offset), 0],
        [0, 1, 0, 0.1],
        [-np.sin(lig_offset), 0, np.cos(lig_offset), 0],
        [0, 0, 0, 1]
    ])
    cam_pose = create_pose_matrix(
        [distance, distance*np.sqrt(3)/2, distance], 
        [-np.pi/6, np.pi/4, 0])
    light_pose = R_y_light@cam_pose
    cam_poses = np.array([cam_pose])
    light_poses = np.array([light_pose])

    for _ in range(n_poses):
        cam_pose = R_y@cam_pose
        light_pose = R_y@light_pose
        cam_poses = np.append(cam_poses, np.array([cam_pose]), axis=0)
        light_poses = np.append(light_poses, np.array([light_pose]), axis=0)

    return cam_poses[:-1], light_poses[:-1]


if __name__=='__main__':
    cam_poses, light_poses = generate_poses()
    np.save('.\example\camera_poses.npy', cam_poses)
    np.save('.\example\light_poses.npy', light_poses)
