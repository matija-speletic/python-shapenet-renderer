from PIL import Image, ImageOps, ImageChops
import multiprocessing
from pathlib import Path
from tqdm import tqdm

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    print(diff.getpixel((200,200)))
    diff = ImageChops.add(diff, diff, 2.0)
    
    bbox = diff.getbbox(alpha_only=False)
    print(bbox)
    if bbox:
        return im.crop(bbox)
    
def process_image(image_paths):
    image_path, output_path = image_paths

    # Open the image
    img = Image.open(image_path)

    # Step 2: Crop out the white padding
    img = trim(img)  # Use border=0 to trim the white areas

    # Step 3: Add white padding to make the image square
    width, height = img.size
    if width != height:
        # Determine the amount of padding needed to make the image square
        diff = abs(width - height)
        if width > height:
            padding = (0, diff // 2, 0, diff - diff // 2)
        else:
            padding = (diff // 2, 0, diff - diff // 2, 0)

        # Add white padding to make it square
        img = ImageOps.expand(img, padding, fill='white')

    # Step 4: Add an additional 20px white padding around the image
    img = ImageOps.expand(img, border=30, fill='white')

    # Save the processed image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)



def find_render_png_files(folder_path):
    png_files = []
    folder_path = Path(folder_path)
    for file in folder_path.glob('**/renders/*.png'):
        png_files.append(file)
    return png_files


def run(folder_path):
    # png_files = find_render_png_files(folder_path)
    # for png_file in png_files:
    #     output_path = png_file.parent.parent/'renders_padded'/png_file.name
    #     output_path.parent.mkdir(parents=True, exist_ok=True)
    #     process_image(png_file, output_path)
    num_cores = multiprocessing.cpu_count()-7
    pool = multiprocessing.Pool(processes=num_cores)
    png_files = find_render_png_files(folder_path)
    output_paths = [png_file.parent.parent/'renders_padded'/png_file.name for png_file in png_files]
    _ = list(
        tqdm(
            # pool.imap_unordered(convert_obj_to_npy, range(len(cad_paths))),
            # total=len(cad_paths))
            pool.imap_unordered(process_image, zip(png_files, output_paths)),
            total=len(png_files)
    ))


if __name__ == '__main__':
    run(r'C:\Users\matij\Downloads\ShapeNetCore.v2\ShapeNetCore.v2')


