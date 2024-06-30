# Python ShapeNet Renderer 

A simple script to batch render objects from the [ShapeNet](https://shapenet.org/) dataset using `pyrender`.

## Usage
1. Generate camera and light poses by running:

    ```
    python pose_generator.py
    ```

    Feel free to experiment with different parameters and numbers of poses.

2. Render the dataset by running:
    ```sh
    python batch_render.py
    ```
    