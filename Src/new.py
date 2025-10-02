import rasterio
import numpy as np
from pathlib import Path
import os

mask_dir = Path('/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/For_website/from_model')

for mask in mask_dir.glob("*.tif"):

    with rasterio.open(str(mask)) as src_mask:
        resolution = src_mask.res
        print(f"Pixel Resolution (x, y): {resolution}")
        width = src_mask.width
        height = src_mask.height
        print(f"Width (columns): {width}")
        print(f"Height (rows): {height}")
        mask_data = src_mask.read(1)
    unique_values, counts = np.unique(mask_data, return_counts=True)
    print(f"Number of lake pixels in {mask.stem}:",counts[1])
    Pixels = counts[1]
    Area = Pixels * 4 * (10e-5)
    print('Area: ', Area)