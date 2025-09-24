from labelbox import Client
from uuid import uuid4
import os

client = Client(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbWZ3OXB4OW4xNXR3MDd5ODhpZXhkNWRnIiwib3JnYW5pemF0aW9uSWQiOiJjbWZ3OXB4OWcxNXR2MDd5ODBieXhheTVlIiwiYXBpS2V5SWQiOiJjbWZ3Y3kyOWIxYzh0MDcwdzBxYzgwN2JxIiwic2VjcmV0IjoiZmZlY2RlYWJlMmRhNzUyYWUwZWQzYTFiMDJjOGMwZjQiLCJpYXQiOjE3NTg2MjAwMDcsImV4cCI6MTc2MTAzOTIwN30.P4DZ9WmhumQd7_EWcus0oc3It1Wp0CWel0Fjuv5dS-k")
new_dataset_name = "SAR_images_test"

# Create the new dataset
dataset = client.create_dataset(name=new_dataset_name)
print(f"Created new dataset: '{dataset.name}' with ID '{dataset.uid}'")

# Create a list to hold all the data row objects
assets = []
# Define the local folder containing your images
image_folder = "/Users/pawanadhikari/Documents/Roadmap/Projects/SAR/Training_Dataset/to_label_reproj"

# Replace these with your Azure Storage Account and Container names
storage_account_name = "tomask"
container_name = "padded"

# Loop through all files in the directory
for filename in os.listdir(image_folder):
    if filename.endswith(".tif"):
        # This is the corrected line to generate the public URL
        hosted_url = f"https://{storage_account_name}.blob.core.windows.net/{container_name}/{filename}"
        
        # Create a unique global key (e.g., using the filename)
        global_key = filename
        
        # Append the new data row dictionary to the list
        assets.append({
            "global_key": global_key,
            "row_data": {
                "tile_layer_url": hosted_url,
            },
            "media_type": "TMS_GEO",
        })

# Push all data rows at once
task = dataset.create_data_rows(assets)
task.wait_till_done()

print(f"Successfully uploaded {len(assets)} assets.")
print(f"Task errors (if any): {task.errors}")