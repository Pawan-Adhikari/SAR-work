# initial setup
import asf_search as asf
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess

loc='../SAR_products_unprocessed/newBatch'

zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


start_year = 2021
for i in range (5):
    year = start_year + i
    pattern_string = r"S1A_IW_" + str(year) + r"\d+T\d+_DVP_RTC\d+_G_.*_.*\.zip"
    pattern = re.compile(
        pattern_string
    )
    print(pattern)
    for zipPath in zipPaths:
        zipName = zipPath.name
        if pattern.match(zipName):
            print(zipName)
            tifName = zipName.replace(".zip","")+'/'+zipName.replace(".zip","_VV.tif")

            tifPath = Path(f'{loc}/{tifName}')

            lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
            for lakeName in lakeNames:
                lakePath = f'../Training_Dataset/{lakeName}'
                cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)