from pathlib import Path
import Crop_Product as cp

zipPath = []
for path in Path('../SAR_products_unprocessed').glob("*.zip"):
    zipPath.append(path.name)

print(zipPath)

cp.crop("../SAR_products_unprocessed/S1A_IW_20241229T122232_DVP_RTC30_G_gpuned_7180/S1A_IW_20241229T122232_DVP_RTC30_G_gpuned_7180_VV.tif", "../Training_Dataset/TshoRolpa/tshoRolpaAOI.geojson","../Training_Dataset/TshoRolpa" )