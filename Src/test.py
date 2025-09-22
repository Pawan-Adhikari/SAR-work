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

print(years)
print(lakeNames)