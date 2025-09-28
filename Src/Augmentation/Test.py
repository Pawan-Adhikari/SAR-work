import albumentations as A
import cv2
import numpy as np

# Assume 'image' is loaded as a NumPy array (e.g., 100x100x3)
image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8) # Dummy image

# 1. Define the pipeline
pipeline = A.Compose([
    A.HorizontalFlip(p=0.5), # 50% chance to flip
    A.RandomBrightnessContrast(p=0.8), # 80% chance to adjust brightness/contrast
    A.GaussianBlur(p=0.3), # 30% chance to blur
])

# 2. Apply the pipeline
transformed_data = pipeline(image=image)
transformed_image = transformed_data['image']

print(f"Original shape: {image.shape}, Transformed shape: {transformed_image.shape}")
# Note: Shape usually remains the same unless a spatial transform like Resize is used.