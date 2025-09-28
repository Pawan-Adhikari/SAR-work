import os
import tifffile
import numpy as np

# --- CONFIGURATION ---
BASE_DIR = "/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset"

# The directory containing the original integer/uint masks
INPUT_MASK_DIR = os.path.join(BASE_DIR, "Labelled")

# The new directory for the FLOAT32 masks (Create this folder!)
OUTPUT_MASK_DIR = os.path.join(BASE_DIR, "Labelled_converted")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_MASK_DIR, exist_ok=True)

print(f"Starting conversion of masks to float32. Reading from: {INPUT_MASK_DIR}")
print(f"Output will be saved in: {OUTPUT_MASK_DIR}")
print("-" * 50)


# --- PROCESS MASKS (Convert to float32, ensure 0 or 1 values) ---
mask_files = [f for f in os.listdir(INPUT_MASK_DIR) if f.endswith(('.tif', '.tiff'))]
print(f"Processing {len(mask_files)} mask files...")
success_count = 0

for filename in mask_files:
    input_path = os.path.join(INPUT_MASK_DIR, filename)
    output_path = os.path.join(OUTPUT_MASK_DIR, filename)
    
    try:
        # 1. Read the original mask data
        mask = tifffile.imread(input_path).copy()
        
        # 2. Ensure mask is binary (0 or 1) and then convert to float32
        # This step is crucial to handle masks that might be non-binary integers (e.g., 255)
        # Use np.round() for any stray float values and then clip to 0/1.
        mask_binary = np.clip(np.round(mask), 0, 1)
        mask_f32 = mask_binary.astype(np.float32)
        
        # 3. Save the new float32 array
        tifffile.imwrite(output_path, mask_f32, dtype=np.float32)
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error processing mask {filename}: {e}")

print("-" * 50)
print(f"✅ Mask conversion complete. Successfully processed {success_count}/{len(mask_files)} files.")
print("Remember to update your data loading paths to point to 'Labelled_F32'.")
