# initial setup
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import padding
import tifCheck
import Normalize

loc='../SAR_products_unprocessed/newerBatch'

zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


for zipPath in zipPaths:
    zipName = zipPath.name
    tifName = zipName.replace(".zip","")+'/'+zipName.replace(".zip","_VV.tif")

    try:
        with ZipFile(zipPath, 'r') as zObj:
            print(zObj.namelist())
            zObj.extract(tifName, path=loc)
        zObj.close()
        tifPath = Path(f'{loc}/{tifName}')

        lakeNames = ['tilichoTsho']
        for lakeName in lakeNames:
            lakePath = f'../Training_Dataset/{lakeName}'
            crop_out = cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)
            print(lakePath + f'/Padded/{tifPath.name}_clipped_to_{lakeName}AOI.geojson.tif')
            padding.pad_and_save_tif(crop_out,lakePath + f'/Padded/{crop_out.name}')
    except:
        print("Couldn't extract this zip file: ", zipName)

finalOut = Normalize.normalize()
tifCheck.finalCheck(finalOut)

