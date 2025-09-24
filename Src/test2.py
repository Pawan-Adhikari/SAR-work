import rasterio
import numpy as np

def get_min_max_values(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
        min_val = np.min(data)
        max_val = np.max(data)
        print(f"File: {file_path}")
        print(f"Minimum Value: {min_val}")
        print(f"Maximum Value: {max_val}")
        return min_val, max_val

# Replace with the path to your GeoTIFF file
file_to_check = "/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label_converted/S1A_IW_20210122T001130_DVP_RTC20_G_gpufed_5E3C_VV.tif_clipped_to_chamlangTshoAOI.geojson.tif"
get_min_max_values(file_to_check)