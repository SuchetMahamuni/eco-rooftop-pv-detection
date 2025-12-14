import os
import requests
from datetime import datetime

def fetch_google_image(lat, lon, sample_id, api_key, out_dir="artefacts", zoom=20):
    """
    Fetch satellite image from Google Static Maps API
    """

    os.makedirs(out_dir, exist_ok=True)

    url = "https://maps.googleapis.com/maps/api/staticmap"

    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": "640x640",
        "maptype": "satellite",
        "key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        image_path = os.path.join(out_dir, f"{sample_id}_google.png")
        with open(image_path, "wb") as f:
            f.write(response.content)

        metadata = {
            "source": "Google Static Maps (Satellite)",
            "fetch_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "zoom": zoom,
            "image_size": "640x640"
        }

        return image_path, metadata, True

    except Exception as e:
        print(f"[ERROR] Google image fetch failed: {e}")
        return None, None, False
