# initial setup
import hyp3_sdk
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess
import configparser
import padding
import Normalize
import tifCheck
import os


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
before_norm = config.get('Other','before_norm')
after_norm = config.get('Other','after_norm')
job_name = config.get('Other','job_name')

# Authenticate using environment variables
hyp3 = hyp3_sdk.HyP3(username=usr, password=pas)

# Find all your jobs by name
jobs = hyp3.find_jobs(name=job_name)

# Check the status of each job
jobs = hyp3.watch(jobs)
jobs_urls = [job.files[0]['url'] for job in jobs]
jobs_files = [job.files[0] for job in jobs]
for job_file in jobs_files:
    print(job_file['filename'])


for url in jobs_urls:
    subprocess.run(["wget", "-c", url, "-P", loc])
#jobs.download_files(location = loc, create=True)
 
print("Download finished!!!")

zipPaths = []
for path in Path(loc).glob("*.zip"):
    zipPaths.append(path)


#Start matching and extracting and finally cropping. Matching uncesseary for year wise sampling.
for zipPath in zipPaths:
    zipName = zipPath.name
    print(zipName)
    tifName = zipName.replace(".zip","")+'/'+zipName.replace(".zip","_VV.tif")

    try:
        with ZipFile(zipPath, 'r') as zObj:
            print(zObj.namelist())
            zObj.extract(tifName, path=loc)
        zObj.close()

        tifPath = Path(f'{loc}/{tifName}')

        for lakeName in lakeNames:
            lakePath = f'../Training_Dataset/{lakeName}'
            crop_out=cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)
            padded_out = lakePath + f'/Padded/{crop_out.name}'
            padding.pad_and_save_tif(crop_out, padded_out)
            os.system(f"cp {padded_out} /Users/pawanadhikari/Documents/Roadmap/Projects/SAR/to_model/before_norm")
    except:
        print("Cannot extract: ",zipName)


finalOut = Normalize.normalize(before_norm, after_norm)
tifCheck.finalCheck(finalOut)
