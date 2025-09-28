from pathlib import Path
import padding
import os

lakeNames = ['tshoRolpa', 'imjaTsho', 'chamlangTsho', 'gokyoTsho']
loc = '/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label_converted'
lake = 'chamlangTsho'
lake_path = '/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/Final_prelabelled/'
#os.mkdir(lake_path+'/Padded', exists_ok = True)
for tif_path in Path(loc).glob("*.tif"):
    padding.pad_and_save_tif(tif_path,lake_path + tif_path.name)

