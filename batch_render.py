from render_object import render_object
from tqdm import tqdm
import time
import multiprocessing
from pathlib import Path
import numpy as np
import traceback
import logging


SHAPENET_PATH = Path(r'D:\Matija\data\ShapeNetCore.v2')
LOG_FILE = r'.\render.log'
CAMERA_POSES = np.load(r'.\example\camera_poses.npy')
LIGHT_POSES = np.load(r'.\example\light_poses.npy')
CPU_COUNT = multiprocessing.cpu_count()-5

logging.basicConfig(filename=LOG_FILE)
cad_paths = list(SHAPENET_PATH.glob('**/*.obj'))

def call_render_object(obj_path_id):
    try:
        render_object(str(cad_paths[obj_path_id]), CAMERA_POSES, LIGHT_POSES)
        logging.info(f"Rendered object {cad_paths[obj_path_id]}")
    except Exception as e:
        logging.error(f"Error rendering object {cad_paths[obj_path_id]}: \n {traceback.format_exc()}")

def run():
    pool = multiprocessing.Pool(processes=CPU_COUNT)
    _=list(
        tqdm(
            pool.imap_unordered(call_render_object, range(len(cad_paths))), 
            total=len(cad_paths))
    )


if __name__ == '__main__':
    start = time.time()
    run()
    print(f"Rendering took {time.time()-start:.2f} seconds")