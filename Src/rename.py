import os
from pathlib import Path

To_rename = Path('/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/temp/')

for tiff in To_rename.glob('*.tif'):
    new_name = str((tiff.name)).replace('.tif','',1).replace('.geojson','')
    tiff.rename(To_rename.joinpath(new_name))
    print(tiff.name)

       