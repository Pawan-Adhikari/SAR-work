# initial setup
import hyp3_sdk
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess
import configparser



loc='../SAR_products_unprocessed/newBatch'

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

# Authenticate using environment variables
hyp3 = hyp3_sdk.HyP3(username=usr, password=pas)

# Find all your jobs by name
jobs = hyp3.find_jobs(name=job_name)

# Check the status of each job
jobs = hyp3.watch(jobs)
jobs_urls = [job.files[0]['url'] for job in jobs]
print(jobs_urls)

check = input("Do you want to continue Download? (Y/N)")
if (check == 'Y'): 0
else: quit()

for url in jobs_urls:
    subprocess.run(["wget", "-c", url, "-P", loc])
#jobs.download_files(location = loc, create=True)

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

            for lakeName in lakeNames:
                lakePath = f'../Training_Dataset/{lakeName}'
                cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)




