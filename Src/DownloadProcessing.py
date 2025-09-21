# initial setup
import asf_search as asf
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess



hyp3 = hyp3_sdk.HyP3(username='pon.adk', password='qeDriz-juhdu3-feckav')

wkt = 'POLYGON ((86.7425991901464 27.935407268344107, 86.7425991901464 27.93062783962911, 86.75104832773593 27.93062783962911, 86.75104832773593 27.935407268344107, 86.7425991901464 27.935407268344107))'

n = 0
results = []
results_2025 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2025-02-01',
                         end='2025-03-01')
results.append(results_2025[n])



results_2024 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2024-02-01',
                         end='2024-03-01')
results.append(results_2024[n])

results_2023 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2023-02-01',
                         end='2023-03-01')
results.append(results_2023[n])
    
results_2022 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2022-02-01',
                         end='2022-03-01')
results.append(results_2022[n])

results_2021 = asf.geo_search(intersectsWith=wkt,
                         platform=[asf.PLATFORM.SENTINEL1],
                         processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                         start='2021-02-01',
                         end='2021-03-01')
results.append(results_2021[n])

granule_ids = [result.properties['sceneName'] for result in results]

for result in results:
    print(result)

# Create a list of job dictionaries using prepare_rtc_job
job_definitions = []
for granule_id in granule_ids:
    job_definitions.append(
         hyp3.prepare_rtc_job(  
                granule_id, 
                name='SomeJob',
                speckle_filter= True,
                resolution=20,
            )
    )
print(job_definitions)

loc='../SAR_products_unprocessed/newBatch'
check = input("Do you want to continue ? (Y/N)")
if check == 'Y':
    #job = hyp3.submit_rtc_job(granule=granule_ids[0], name='MyNewJob') 
    jobs = hyp3.submit_prepared_jobs(job_definitions)
    jobs = hyp3.watch(jobs)
    
    jobs_urls = [job.files[0]['url'] for job in jobs]
    print(jobs_urls)

    check = input("Do you want to continue Download? (Y/N)")
    if (check == 'Y'): 0
    else: quit()

    for url in jobs_urls:
        subprocess.run(["wget", "-c", url, "-P", loc])
    #job.download_files(location = loc, create=True)

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

            with ZipFile(zipPath, 'r') as zObj:
                print(zObj.namelist())
                zObj.extract(tifName, path=loc)
            zObj.close()

            tifPath = Path(f'{loc}/{tifName}')

            lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
            for lakeName in lakeNames:
                lakePath = f'../Training_Dataset/{lakeName}'
                cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)





