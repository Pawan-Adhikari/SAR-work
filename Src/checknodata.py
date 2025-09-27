import rasterio
import numpy as np

# Replace with the path to your image and mask
mask_path = '/Users/pawanadhikari/Downloads/S1A_IW_20230925T121409_DVP_RTC20_G_gpufed_C3D9_VV.tif_clipped_to_chamlangTshoAOI.geojson.tif    '


# Open and read the labeled mask
with rasterio.open(mask_path) as src_mask:
    mask_data = src_mask.read(1)

    # Check the mask's NoData value from its metadata
    mask_nodata_value = src_mask.nodata
    print(f"Mask's metadata NoData value: {mask_nodata_value}")

# Check the data type of the mask array
print(f"Mask array data type: {mask_data.dtype}")

# Get unique values and their counts in the mask
unique_values, counts = np.unique(mask_data, return_counts=True)
print("\nUnique values and their counts in the mask:")
for value, count in zip(unique_values, counts):
    print(f"Value: {value}, Count: {count}")

# Check for the presence of the NoData value in the array
# This is the key step to see if it was loaded or ignored.
if mask_nodata_value is not None:
    is_nodata_in_array = np.isin(mask_data, mask_nodata_value).any()
    print(f"\nIs the NoData value ({mask_nodata_value}) present in the loaded array? {is_nodata_in_array}")