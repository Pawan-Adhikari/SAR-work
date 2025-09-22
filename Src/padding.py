import numpy as np
from PIL import Image

def pad_and_save_tif(input_path, output_path, target_size=(256, 256)):
    try:
        img = Image.open(input_path)
        img_array = np.array(img)
        current_h, current_w = img_array.shape[:2]

        # Calculate padding needed for height and width
        pad_h = (target_size[0] - current_h) // 2
        pad_w = (target_size[1] - current_w) // 2

        # Step 3: Apply zero-padding
        # 'pad_width' takes a tuple of tuples for each dimension.
        # mode='constant' fills the new area with a constant value.
        # constant_values=0 sets that value to zero.
        padded_img_array = np.pad(
            img_array,
            ((pad_h, pad_h), (pad_w, pad_w)),
            mode='constant',
            constant_values=0
        )

        # Step 4: Convert the padded array back to a PIL Image object
        # It's important to convert the data type back to what Pillow expects
        padded_img = Image.fromarray(padded_img_array.astype(img_array.dtype))
        
        # Step 5: Save the new image as a TIFF file
        padded_img.save(output_path, format='TIFF')

        print(f"Padded image saved successfully to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
