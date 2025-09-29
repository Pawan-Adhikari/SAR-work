# initial setup
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import padding
import tifCheck
import Normalize

zipPath = Path('/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/SAR_products_unprocessed/newerBatch/S1A_IW_20230529T001940_DVP_RTC20_G_gpufed_23C6.zip')
zipName = zipPath.name
tifName = zipName.replace(".zip","")+'/'+zipName.replace(".zip","_VV.tif")
loc = 'SAR_products_unprocessed/newerBatch'

try:
    with ZipFile(zipPath, 'r') as zObj:
        print(zObj.namelist())
        zObj.extract(tifName, path=loc)
    zObj.close()
    tifPath = Path(f'{loc}/{tifName}')

    lakeName = 'tilichoTsho'
    lakePath = f'../Training_Dataset/{lakeName}'
    crop_out = cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)
    print(lakePath + f'/Padded/{tifPath.name}_clipped_to_{lakeName}AOI.geojson.tif')
    padding.pad_and_save_tif(crop_out,lakePath + f'/Padded/{crop_out.name}')
except:
    print("Couldn't extract this zip file: ", zipName)

finalOut = Normalize.normalize()
tifCheck.finalCheck(finalOut)

    