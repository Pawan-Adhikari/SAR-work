import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os
from pathlib import Path

def reproject_to_wgs84(input_path, output_path, target_crs='EPSG:3857'):
    print('It least I was called')
    with rasterio.open(input_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=target_crs,
                resampling=Resampling.nearest)
    print(f"Successfully reprojected and saved to {output_path}")

# Example Usage:
output_folder = "/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label_reproj"
geotiff_folder = "/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label"
print('atleast program ran')
for filename in Path(geotiff_folder).glob('*.tif'):
    print(filename)
    output_file = output_folder + '/' + filename.name
    reproject_to_wgs84(filename, output_file)
