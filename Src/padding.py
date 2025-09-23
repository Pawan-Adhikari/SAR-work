import numpy as np
import rasterio

def pad_and_save_tif(input_path, output_path, target_size=(256, 256)):
    try:
        with rasterio.open(input_path) as src:
            # Read the image data as a NumPy array and get the metadata
            img_array = src.read(1)  # Reads the first band
            profile = src.profile

        current_h, current_w = img_array.shape

        # Calculate padding needed for height and width
        pad_h = (target_size[0] - current_h) // 2
        pad_w = (target_size[1] - current_w) // 2
        
        # Apply zero-padding
        padded_img_array = np.pad(
            img_array,
            ((pad_h, pad_h), (pad_w, pad_w)),
            mode='constant',
            constant_values=0
        )

        # Update the metadata to reflect the new dimensions and geotransform
        profile.update(
            width=padded_img_array.shape[1],
            height=padded_img_array.shape[0],
            transform=rasterio.transform. Affine(
                profile['transform'].a,  # a (x-pixel size)
                profile['transform'].b,  # b (rotation)
                profile['transform'].c - (pad_w * profile['transform'].a),  # c (x-offset)
                profile['transform'].d,  # d (rotation)
                profile['transform'].e,  # e (y-pixel size, negative)
                profile['transform'].f - (pad_h * profile['transform'].e)  # f (y-offset)
            )
        )

        # Write the padded array to a new GeoTIFF file with the updated metadata
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(padded_img_array, 1)

        print(f"Padded GeoTIFF saved successfully to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")