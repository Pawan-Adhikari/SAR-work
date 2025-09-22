# Imports and libraries
import asf_search as asf
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess
import configparser


#Initiation:
config = configparser.ConfigParser()
config.read('config.ini')
start_date=config.get('Other','start_date')
end_date=config.get('Other','end_date')    
usr = config.get('Login','user')
pas = config.get('Login','password')
wkt = config.get('Other','wkt')     
n = config.getint('Other','number_of_products_per_month')    
loc=config.get('Other','store_location')
lakeNames = config.get('Other', 'lakeNames').split(', ')
years = config.get('Other', 'years').split(', ')
job_name = config.get('Other','job_name')

#hyp3 authentication
hyp3 = hyp3_sdk.HyP3(username=usr, password=pas)

#Searching:
results = []
for year in years:
    results_thisYear = asf.geo_search(intersectsWith=wkt,
                            platform=[asf.PLATFORM.SENTINEL1],
                            processingLevel=[asf.PRODUCT_TYPE.GRD_HD,asf.PRODUCT_TYPE.GRD_HS, asf.PRODUCT_TYPE.GRD_MD, asf.PRODUCT_TYPE.GRD_MS, asf.PRODUCT_TYPE.GRD_FD],
                            start=year + '-' + start_date,
                            end=year + '-' + end_date)
    results.append(results_thisYear[n])

granule_ids = [result.properties['sceneName'] for result in results]

#Display found products
for result in results:
    print(result)

# Prepare RTC jobs from products
job_definitions = []
for granule_id in granule_ids:
    job_definitions.append(
         hyp3.prepare_rtc_job(  
                granule_id, 
                name=job_name,
                speckle_filter= True,
                resolution=20,
            )
    )
print(job_definitions)

#Check and continue with processing
check = input("Do you want to continue ? (Y/N)")
if check == 'Y':
    #job = hyp3.submit_rtc_job(granule=granule_ids[0], name='MyNewJob') 
    jobs = hyp3.submit_prepared_jobs(job_definitions)
    jobs = hyp3.watch(jobs)
    
    jobs_urls = [job.files[0]['url'] for job in jobs]
    print(jobs_urls)

#Check and continue with downloading
    check = input("Do you want to continue Download? (Y/N)")
    if (check == 'Y'): 0
    else: quit()

    for url in jobs_urls:
        subprocess.run(["wget", "-c", url, "-P", loc])
    #job.download_files(location = loc, create=True)

#Preparing to unzip
zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


#Start matching and extracting and finally cropping. Matching uncesseary for year wise sampling.
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

            for lakeName in lakeNames:
                lakePath = f'../Training_Dataset/{lakeName}'
                cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)





