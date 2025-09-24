# initial setup
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import padding
import os

loc='../SAR_products_unprocessed/newBatch'

zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


for zipPath in zipPaths:
    zipName = zipPath.name
    tifName = zipName.replace(".zip","")+'/'+zipName.replace(".zip","_VV.tif")

    with ZipFile(zipPath, 'r') as zObj:
        print(zObj.namelist())
        zObj.extract(tifName, path=loc)
    zObj.close()

    tifPath = Path(f'{loc}/{tifName}')

    lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
    for lakeName in lakeNames:
        lakePath = f'../Training_Dataset/{lakeName}'
        crop_out = cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)
        print(lakePath + f'/Padded/{tifPath.name}_clipped_to_{lakeName}AOI.geojson.tif')
        #padding.pad_and_save_tif(crop_out,lakePath + f'/Padded/{tifPath.name}_clipped_to_{lakeName}AOI.geojson.tif')

