# initial setup
import asf_search as asf
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp



hyp3 = hyp3_sdk.HyP3(username='pon.adk', password='qeDriz-juhdu3-feckav')

wkt = 'POLYGON ((86.7425991901464 27.935407268344107, 86.7425991901464 27.93062783962911, 86.75104832773593 27.93062783962911, 86.75104832773593 27.935407268344107, 86.7425991901464 27.935407268344107))'

results = []
results_2025 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2025-06-01',
                         end='2025-07-01')
results.append(results_2025[0])



results_2024 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2024-06-01',
                         end='2024-07-01')
results.append(results_2024[0])

results_2023 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2023-06-01',
                         end='2023-07-01')
results.append(results_2023[0])
    
results_2022 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2022-06-01',
                         end='2022-07-01')
results.append(results_2022[0])

granule_ids = [result.properties['sceneName'] for result in results]

print(granule_ids)

# Create a list of job dictionaries using prepare_rtc_job
job_definitions = []
for granule_id in granule_ids:
    job_definitions.append(
         hyp3.prepare_rtc_job(  
                granule_id, 
                name='GlacierLakeRTC',
                speckle_filter= True,
                resolution=10
            )
    )
print(job_definitions)

loc='../SAR_products_unprocessed/newBatch'
check = input("Do you want to continue ? (Y/N)")
if check == 'Y':
    #job = hyp3.submit_rtc_job(granule=granule_ids[0], name='MyNewJob') 
    job = hyp3.submit_prepared_jobs(job_definitions)
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





