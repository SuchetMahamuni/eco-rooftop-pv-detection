from image_fetcher import fetch_esri_image
import os
img_path, meta, success = fetch_esri_image(
    lat=18.464309269919653,   # Bangalore
    lon=73.86504669632464,
    sample_id="test_sadguru_hostel",
    out_dir=os.getcwd(),
    zoom=19
)
# , 
# 
print("Success:", success)
print("Image path:", img_path)
print("Metadata:", meta)
