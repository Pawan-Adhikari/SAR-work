from pathlib import Path
import padding
import os

lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
loc = '../Training_Dataset/'
for lakes in lakeNames:
    lake_path = loc + lakes
    #os.mkdir(lake_path+'/Padded', exists_ok = True)
    for tif_path in Path(lake_path).glob("*.tif"):
        padding.pad_and_save_tif(tif_path,lake_path + f'/Padded/{tif_path.name}')
