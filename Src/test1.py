import rasterio
import os
from pathlib import Path

def check_geotiff_specifications(file_path):
    # Supported EPSG codes from Labelbox documentation
    supported_crs = [
        "EPSG:3857",
        "EPSG:3395",
        "EPSG:4326"
    ]
    
    try:
        # Check file size
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"✅ File Size: {file_size_mb:.2f} MB (Recommended < 1 GB)")

        with rasterio.open(file_path) as src:
            # Check Coordinate System (CRS)
            crs_code = src.crs.to_string()
            print(f"✅ Coordinate System: {crs_code}")
            if crs_code in supported_crs:
                print("   - CRS is a supported type.")
            else:
                print("   - ⚠️ CRS is NOT a supported type. Please convert it.")

            # Check CRS Type (Projected CRS)
            if src.crs.is_projected:
                print("✅ CRS Type: Projected (Supported)")
            else:
                print("⚠️ CRS Type: Geographic (NOT Supported). Please convert it.")

            # Check number of bands
            print(f"✅ Number of Bands: {src.count}")
            if src.count <= 4:
                print("   - Number of bands is supported.")
            else:
                print("   - ⚠️ Number of bands is NOT supported. Please reduce to 4 or less.")

    except rasterio.errors.RasterioIOError as e:
        print(f"❌ Error: Unable to open the GeoTIFF file. Check the file path and integrity. Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# Example usage:
# Replace with the path to your padded GeoTIFF file
geotiff_folder = "//Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label_reproj"
for filename in Path(geotiff_folder).glob('*.tif'):
    print(filename)
    check_geotiff_specifications(filename)