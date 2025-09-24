import numpy as np
from PIL import Image
from pathlib import Path


def convert_and_save_image(input_path, output_path):
    # Open the image as a 32-bit float
    img_pil = Image.open(input_path)
    
    # Convert the PIL image to a NumPy array for processing
    img_array = np.array(img_pil)

    # Normalize the array to the 0-255 range
    # This assumes your data has a valid range to be normalized
    min_val = np.min(img_array)
    max_val = np.max(img_array)
    normalized_array = (img_array - min_val) / (max_val - min_val) * 255

    # Convert the normalized array to an 8-bit unsigned integer type
    # This is required for saving as a PNG or JPEG
    converted_image = Image.fromarray(normalized_array.astype(np.uint8))
    
    # Save the converted image as a PNG
    converted_image.save(output_path, format="PNG")
    
    print(f"Successfully converted '{input_path}' to '{output_path}'")

# Example Usage
input_image_path = "S1A_IW_20230720T122237_DVP_RTC20_G_gpufed_536B_VV.tif"
output_image_path = "converted_image.png"
loc = '../Training_Dataset/to_label/'
for tif_path in Path(loc).glob("*.tif"):
    convert_and_save_image(input_image_path, output_image_path) 
