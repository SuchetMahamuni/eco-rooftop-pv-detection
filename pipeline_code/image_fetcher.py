import os
import math
import requests
from datetime import datetime

ESRI_TILE_URL = (
    "https://services.arcgisonline.com/ArcGIS/rest/services/"
    "World_Imagery/MapServer/tile/{z}/{y}/{x}"
)

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int(
        (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)
        / 2.0 * n
    )
    return x_tile, y_tile


def fetch_esri_image(lat, lon, sample_id, out_dir="../artefacts", zoom=19):
    """
    Fetch ESRI World Imagery tile for given lat/lon
    """

    os.makedirs(out_dir, exist_ok=True)

    try:
        x, y = latlon_to_tile(lat, lon, zoom)
        url = ESRI_TILE_URL.format(z=zoom, x=x, y=y)

        print(f"Requesting from url: {url}")

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        image_path = os.path.join(out_dir, f"{sample_id}_esri.png")
        with open(image_path, "wb") as f:
            f.write(response.content)

        metadata = {
            "source": "ESRI World Imagery (Tile)",
            "fetch_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "zoom": zoom,
            "tile_x": x,
            "tile_y": y
        }

        return image_path, metadata, True

    except Exception as e:
        print(f"[ERROR] ESRI tile fetch failed: {e}")
        return None, None, False
