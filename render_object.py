import trimesh
import pyrender
import numpy as np
from pathlib import Path
from PIL import Image


def render_object(obj_path:str, camera_poses:np.ndarray, light_poses:np.ndarray, 
                  width=512, height=512, ambient_light=[0.1, 0.1, 0.1], 
                  light_color=[1.0, 1.0, 1.0], light_intensity=2.7,
                  inner_cone_angle=np.pi/10.0, outer_cone_angle=np.pi/6.0):
    obj_path = Path(obj_path)
    if not obj_path.exists():
        raise FileNotFoundError(f"Object file not found at {obj_path}")
    renders_path = obj_path.parent / 'renders'
    renders_path.mkdir(exist_ok=True)

    # Load the object mesh
    trimesh_scene = trimesh.load(obj_path)
    bounds = trimesh_scene.bounds
    if isinstance(trimesh_scene, trimesh.Scene):
        scene = pyrender.Scene.from_trimesh_scene(trimesh_scene)
        scene.ambient_light = np.array(ambient_light)
    else:
        mesh = pyrender.Mesh.from_trimesh(trimesh_scene)
        scene = pyrender.Scene(ambient_light=np.array(ambient_light))
        scene.add(mesh)

    # Center the object
    T_corr = np.array([
        [0, 0, 0, (bounds[0, 0] + bounds[1, 0]) / 2],
        [0, 0, 0, (bounds[0, 1] + bounds[1, 1]) / 2],
        [0, 0, 0, (bounds[0, 2] + bounds[1, 2]) / 2],
        [0, 0, 0, 0]
    ])

    # Light, Camera, Action!
    light=pyrender.SpotLight(
        color=np.array(light_color), intensity=light_intensity,
        innerConeAngle=inner_cone_angle, outerConeAngle=outer_cone_angle)
    camera = pyrender.PerspectiveCamera(
        yfov=0.96, aspectRatio=width/height, 
        zfar=1000, znear=0.1)
    light_node=scene.add(light)
    camera_node=scene.add(camera)

    # Rendering
    r = pyrender.OffscreenRenderer(width, height)
    flags = pyrender.RenderFlags.SHADOWS_SPOT
    for i, (camera_pose, light_pose) in enumerate(zip(camera_poses, light_poses)):
        scene.set_pose(camera_node, pose=camera_pose+T_corr)
        scene.set_pose(light_node, pose=light_pose+T_corr)
        color, _ = r.render(scene, flags=flags)
        rgb = Image.fromarray(np.uint8(color))
        rgb.save(renders_path/f'{i}.png')


if __name__ == '__main__':
    obj_path = r"C:\Users\matij\Downloads\ShapeNetCore.v2\ShapeNetCore.v2\04530566\5b86640d3bc2e43decac3f40526a2cc2\models\model_normalized.obj"
    camera_poses = np.load('cam_poses.npy')
    light_poses = np.load('light_poses.npy')
    render_object(obj_path, camera_poses, light_poses)