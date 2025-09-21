# initial setup
import asf_search as asf
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp

# Authenticate using environment variables
hyp3 = hyp3_sdk.HyP3(username='pon.adk', password='qeDriz-juhdu3-feckav')

# Find all your jobs by name
job = hyp3.find_jobs(name='GlacierLakeRTC')
loc='../SAR_products_unprocessed/newBatch'

# Check the status of each job
job = hyp3.watch(job)
job.download_files(location = loc, create=True)

zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


start_year = 2022
for i in range (4):
    year = start_year + i
    pattern = re.compile(
        rf"S1A_IW_{year}\d+T\d+_DVP_RTC\d+_G_gpuned_\d+\.zip"
    )
    for zipPath in zipPaths:
        zipName = zipPath.name
        if pattern.match(zipName):
            tifName = zipName.replace(".zip","_VV.tif")

            with ZipFile(zipPath, 'r') as zObj:
                zObj.extract(tifName, path=loc)
            zObj.close()

            tifPath = Path(f'{loc}/{tifName}')

            lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
            for lakeName in lakeNames:
                lakePath = f'../Training_Dataset/{lakeName}'
                cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)





