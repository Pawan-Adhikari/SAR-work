# initial setup
import re
from pathlib import Path
from zipfile import ZipFile
import Crop_Product as cp
import subprocess
import configparser
import padding
import Normalize
import tifCheck

config = configparser.ConfigParser()
config.read('config.ini')
loc=config.get('Other','store_location')
lakeNames = config.get('Other', 'lakeNames').split(', ')
years = config.get('Other', 'years').split(', ')


""""
Already Downloaded:
    "https://d3gm2hf49xd6jj.cloudfront.net/7fc84a8e-02a9-4cb3-bfaf-ecafada2246b/S1A_IW_20230327T123042_DVP_RTC20_G_gpufed_8EBF.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/91acaa39-b445-4d50-af44-780982ce280b/S1A_IW_20210328T001922_DVP_RTC20_G_gpufed_831F.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/206d5be8-7ec0-488a-98ec-0fcdeb4d7a33/S1A_IW_20240329T002748_DVP_RTC20_G_gpufed_82A9.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/79879aa4-2091-4b7d-ad48-f2f1c0e615ab/S1A_IW_20220328T002734_DVP_RTC20_G_gpufed_1B71.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/ed96bb75-7bda-4468-baf5-337710cfa405/S1A_IW_20250328T123041_DVP_RTC20_G_gpufed_1FD0.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/218e12e4-b9d3-4e28-b0b0-59f3a7ee78f7/S1A_IW_20210527T001925_DVP_RTC20_G_gpufed_0876.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/89600189-0f96-4a3f-b167-9094340f5729/S1A_IW_20220527T002736_DVP_RTC20_G_gpufed_A644.zip,"
    "https://d3gm2hf49xd6jj.cloudfront.net/8bcdc6d4-45d1-475a-9a1c-93494f79d405/S1A_IW_20240528T002749_DVP_RTC20_G_gpufed_AB22.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/3f16976f-81a0-4599-8c94-010d671dbd72/S1A_IW_20250527T123040_DVP_RTC20_G_gpufed_8370.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/04005bce-30b5-423e-8404-09b08b3c589c/S1A_IW_20230428T002744_DVP_RTC20_G_gpufed_5C31.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/bb3fc660-f45f-4363-b20f-5c33c1b69913/S1A_IW_20240429T001943_DVP_RTC20_G_gpufed_9E44.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/1c9b9ab8-aeb9-4183-b736-23f9b6524b6e/S1A_IW_20220428T001929_DVP_RTC20_G_gpufed_6FAE.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/476c5ff3-924a-4a91-91d7-5fb8e940c388/S1A_IW_20210426T002729_DVP_RTC20_G_gpufed_22EB.zip",
    "https://d3gm2hf49xd6jj.cloudfront.net/8bebe84b-c3ee-4c9f-977d-d8eea38dcd40/S1A_IW_20250429T002742_DVP_RTC20_G_gpufed_C9D1.zip" 
"""

urls = [
    "https://d3gm2hf49xd6jj.cloudfront.net/3b44eb09-92fa-40b8-bdf6-b5759e8e3942/S1A_IW_20230529T001940_DVP_RTC20_G_gpufed_23C6.zip"
]


for url in urls:
    subprocess.run([
        "aria2c",
        "-c",        # continue download if file already exists
        "-x", "16",  # max connections per server
        "-s", "16",  # split into 16 segments
        "-d", loc,   # download directory
        url
    ])
#jobs.download_files(location = loc, create=True)
 
print("Download finished!!!")

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

            try:
                with ZipFile(zipPath, 'r') as zObj:
                    print(zObj.namelist())
                    zObj.extract(tifName, path=loc)
                zObj.close()

                tifPath = Path(f'{loc}/{tifName}')

                for lakeName in lakeNames:
                    lakePath = f'../Training_Dataset/{lakeName}'
                    crop_out=cp.crop(tifPath,f'{lakePath}/{lakeName}AOI.geojson', lakePath)
                    padding.pad_and_save_tif(crop_out,lakePath + f'/Padded/{crop_out.name}')
            except:
                print("Cannot extract: ",zipName)

finalOut = Normalize.normalize()
tifCheck.finalCheck(finalOut)