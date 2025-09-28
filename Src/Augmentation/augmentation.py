import rasterio
import numpy as np
import albumentations as A
import os
from glob import glob

# -----------------------------
# Define augmentations
# -----------------------------
transform = A.Compose([
    A.Rotate(limit=270, border_mode=0, p=1.0),  # random rotation
    A.HorizontalFlip(p=0.5),                    # 50% chance horizontal flip
    A.VerticalFlip(p=0.5),                      # 50% chance vertical flip
])

# -----------------------------
# Augmentation function
# -----------------------------
def augment_tiff(image_file, mask_file, out_dir, n_aug=5):
    os.makedirs(out_dir, exist_ok=True)

    with rasterio.open(image_file) as src:
        img = src.read()
        meta = src.meta.copy()

    with rasterio.open(mask_file) as src:
        mask = src.read(1)

    img = np.transpose(img, (1, 2, 0))

    for i in range(n_aug):
        augmented = transform(image=img, mask=mask)
        aug_img = augmented['image']
        aug_mask = augmented['mask']

        aug_img_chw = np.transpose(aug_img, (2, 0, 1))

        base_name = os.path.splitext(os.path.basename(image_file))[0]
        img_out = os.path.join(out_dir, f"{base_name}_aug_{i}_nomasking.tiff")
        mask_out = os.path.join(out_dir, f"{base_name}_aug_{i}_withmasking.tiff")

        with rasterio.open(img_out, 'w', **meta) as dst:
            dst.write(aug_img_chw)

        with rasterio.open(mask_out, 'w', **meta, count=1) as dst:
            dst.write(aug_mask, 1)

# -----------------------------
# Automate over dataset
# -----------------------------
def augment_dataset(dataset_root, masked_root, output_root, n_aug=5):
    """
    dataset_root: folder containing original lake folders
    masked_root: folder containing masked TIFFs organized by lake
    output_root: folder to save augmented data
    """
    lake_folders = [f.path for f in os.scandir(dataset_root) if f.is_dir() and f.name != "masked_data"]

    for lake_folder in lake_folders:
        lake_name = os.path.basename(lake_folder)
        images = sorted(glob(os.path.join(lake_folder, "*.tif")))

        for img_file in images:
            # Skip already augmented files
            if "_aug_" in img_file or "_nomasking" in img_file:
                continue

            # Mask file location
            mask_file = os.path.join(masked_root, lake_name, os.path.basename(img_file).replace(".tif", "_withmasking.tiff"))

            if os.path.exists(mask_file):
                out_dir = os.path.join(output_root, lake_name)
                augment_tiff(img_file, mask_file, out_dir, n_aug=n_aug)
                print(f"Augmented: {img_file}")
            else:
                print(f"Mask not found for: {img_file}")

# -----------------------------
# Example usage
# -----------------------------
dataset_root = r"C:\Users\Satish Regmi\Desktop\nasa space apps challenge\SAR_1\SAR-work\Training_Dataset"
masked_root = os.path.join(dataset_root, "masked_data")
output_root = r"C:\Users\Satish Regmi\Desktop\nasa space apps challenge\SAR_1\SAR-work\augmented_data"

augment_dataset(dataset_root, masked_root, output_root, n_aug=5)
