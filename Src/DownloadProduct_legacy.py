import asf_search
import json
import subprocess

#defining an wkt object as AOI
#Here we have a rectangle around Tso rolpa  
wkt = 'POLYGON ((84.11507928703094 28.449348450866324, 84.11507928703094 28.444435230744986, 84.11828517120028 28.444435230744986, 84.11828517120028 28.449348450866324, 84.11507928703094 28.449348450866324))'

#Creating authenticated login session.
#session = asf.ASFSession().auth_with_creds('pon.adk', 'qeDriz-juhdu3-feckav')


# Search for Sentinel-1 SAR products in that region
results = asf_search.geo_search(intersectsWith=wkt,
                         platform=[asf_search.PLATFORM.SENTINEL1],
                         processingLevel=[asf_search.PRODUCT_TYPE.GRD_HD,asf_search.PRODUCT_TYPE.GRD_HS, asf_search.PRODUCT_TYPE.GRD_MD, asf_search.PRODUCT_TYPE.GRD_MS, asf_search.PRODUCT_TYPE.GRD_FD],
                         start='2024-01-01',
                         end='2025-01-01')

print(results)
#filtering for size below ~700mb
#filteredResults = [r for r in results if(r.properties['bytes']<1725868128)]
#print(filteredResults)
#first_result= filteredResults[0]
first_result = results[0]


#specifying filename to save
date = first_result.properties["processingDate"]
url = first_result.properties['url']
print(url)

# Download to local folder
file_Path = date
subprocess.run([
    "wget", "--continue", "--tries=3", "-O", file_Path, url
])


#This saves the polygon and properties of downloaded image/product.
with open('polygon.json', 'w') as f:
    json.dump(wkt, f, indent=4)
with open('properties.json', 'w') as f:
    json.dump(first_result.properties, f, intent = 4)

#alternative approaches to download
#wget.download(url, file_Path)
#first_result.download(path='.', session=session)


