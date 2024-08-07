# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/20_extracting-image-data.ipynb.

# %% auto 0
__all__ = ['extract_jpg']

# %% ../notebooks/20_extracting-image-data.ipynb 16
from . import file_to_bytes, get_blocks, get_blocktypes 
import numpy as np 
import io 
import re
import matplotlib.pyplot as plt 
from PIL import Image

# %% ../notebooks/20_extracting-image-data.ipynb 17
def extract_jpg(pdz_file, BLOCKTYPE=137, save_file=False):
    '''Extract and save jpg images from `pdz_file`.
    
    Returns a list of jpg images where ims = [ im0, im1, ... ].
    '''

    # parse into blocks
    pdz_bytes = file_to_bytes(pdz_file)
    block_list = get_blocks(pdz_bytes, verbose=False)

    # read block 137 (if present)

    blocktypes_list = get_blocktypes(block_list)

    if BLOCKTYPE not in blocktypes_list:

        print(f'Could not find jpg image data in: {pdz_file}')

    else:
        jpg_i = blocktypes_list.index(BLOCKTYPE)
        jpg_dict = block_list[jpg_i]

        jpg_sandwich = jpg_dict['bytes'].tobytes()

        # code below thanks to Lars Maxfield
        # Repeatedly search for jpgs by consuming jpg_sandwich

        ims = []
        while True:
            match_jpg_start = re.search(b'\xff\xd8', jpg_sandwich)
            match_jpg_end = re.search(b'\xff\xd9', jpg_sandwich)

            if not match_jpg_start or not match_jpg_end:
                
                break

            jpg_start = match_jpg_start.span()[0]
            jpg_end = match_jpg_end.span()[1]
            jpg = jpg_sandwich[jpg_start:jpg_end]

            ims.append(np.array(Image.open(io.BytesIO(jpg))))

            jpg_sandwich = jpg_sandwich[jpg_end:]

        if save_file is True:
            for i, im in enumerate(ims):
                jpg_file = re.sub('\.pdz$', f'-{i}.jpg', pdz_file)
                
                print(f"Saving image file: '{jpg_file}'")
                plt.imsave(jpg_file, im)

        return ims

    return None
