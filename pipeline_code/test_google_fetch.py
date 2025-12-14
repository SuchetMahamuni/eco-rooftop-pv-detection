from google_image_fetcher import fetch_google_image
import os

API_KEY = "AIzaSyAF71xKeFF13D1A8ZHV8foB1upZhRPR7oE"

lat,lon = "18.470436, 73.862138".split(', ')

img_path, meta, success = fetch_google_image(
    lat=float(lat),
    lon=float(lon),
    sample_id="test_sadguru_hostel",
    out_dir= os.path.join(os.getcwd(),"artefacts"),
    api_key=API_KEY
)

print("Success:", success)
print("Image path:", img_path)
print("Metadata:", meta)
