from osgeo import gdal, ogr
from pathlib import Path

def crop(input_tif, aoi_geojson, outDir):
    output_tif_name = f"{Path(input_tif).name}_clipped_to_{Path(aoi_geojson).name}.tif"
    output_tif = Path(f"{outDir}/{output_tif_name}")
    # Warp options
    warp_options = gdal.WarpOptions(
        format='GTiff',
        cutlineDSName=aoi_geojson,
        cropToCutline=True,
        dstNodata=0,
        multithread=True
    )

    # Perform warp (crop) by passing the input file path as a string
    gdal.Warp(
        destNameOrDestDS=output_tif, 
        srcDSOrSrcDSTab=input_tif, # FIX: Pass the file path as a string
        options=warp_options
    )

    print(f"Cropped raster saved to: {output_tif}")

"""
gdalwarp \
  -cutline AOI_tshoRolpa.geojson \
  -crop_to_cutline \
  -of GTiff \
  -overwrite \
  S1A_IW_20241229T122232_DVP_RTC30_G_gpuned_7180/S1A_IW_20241229T122232_DVP_RTC30_G_gpuned_7180_VV.tif \
  output_clipped.tif
  """