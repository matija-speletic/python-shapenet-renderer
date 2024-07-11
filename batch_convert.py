from tqdm import tqdm
import time
import multiprocessing
from pathlib import Path
import numpy as np
import traceback
import logging
import trimesh


SHAPENET_PATH = Path(
    r'C:\Users\matij\Downloads\ShapeNetCore.v2\ShapeNetCore.v2')
LOG_FILE = 'convert.log'
logging.basicConfig(filename=LOG_FILE)

cad_paths = list(SHAPENET_PATH.glob('**/*.obj'))


def convert_obj_to_npy(file_index):
    try:
        file_path = cad_paths[file_index]

        mesh = trimesh.load(str(file_path), force='mesh')

        points, _ = trimesh.sample.sample_surface(mesh, 1024)

        np.save(file_path.with_suffix('.npy'), points)
    except Exception as e:
        logging.error(
            f"Error converting object {file_path}: \n {traceback.format_exc()}")


def run():

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    _ = list(
        tqdm(
            pool.imap_unordered(convert_obj_to_npy, range(len(cad_paths))),
            total=len(cad_paths))
    )


if __name__ == '__main__':
    start = time.time()
    run()
    print(f"Conversion took {time.time()-start:.2f} seconds")
