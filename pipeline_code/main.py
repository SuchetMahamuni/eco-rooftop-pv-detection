import os
import json
import pandas as pd

from google_image_fetcher import fetch_google_image
from inference import SolarPanelDetector
from buffer_logic import select_panel_with_buffer_logic, bbox_area
from overlay_utils import draw_overlay
# ---------------- CONFIG ---------------- #

MODEL_PATH = "trained_model/solar_yolov8.pt"   # adjust if name differs
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # IMPORTANT
OUTPUT_DIR = "prediction_files"
ARTEFACT_DIR = "artefacts"

CONF_THRESHOLD = 0.35

# ---------------------------------------- #


def estimate_area_sqm(bbox, meters_per_pixel=0.3):
    """
    Estimate PV area in square meters from bbox (pixel space)
    """
    pixel_area = bbox_area(bbox)
    sqm = pixel_area * (meters_per_pixel ** 2)
    return round(sqm, 2)


def process_sample(detector, sample):
    sample_id = sample["sample_id"]
    lat = sample["latitude"]
    lon = sample["longitude"]

    # 1. Fetch image
    image_path, image_meta, success = fetch_google_image(
        lat, lon, sample_id, api_key=API_KEY, out_dir=ARTEFACT_DIR
    )

    if not success:
        print(f"Image {sample_id} fetching unsuccessful")
        return {
            "sample_id": sample_id,
            "lat": lat,
            "lon": lon,
            "has_solar": False,
            "confidence": 0.0,
            "pv_area_sqm_est": 0.0,
            "buffer_radius_sqft": 2400,
            "qc_status": "NOT_VERIFIABLE",
            "bbox_or_mask": None,
            "image_metadata": {}
        }

    # 2. Run inference
    detections = detector.predict(image_path)

    selected, buffer_used = select_panel_with_buffer_logic(detections)

    if selected is None:
        has_solar = False
        buffer_used = 2400

    overlay_path = f"{ARTEFACT_DIR}/{sample_id}_overlay.png"
    draw_overlay(image_path, selected, buffer_used, overlay_path)

    if selected is None:
        print(f"Image {sample_id} SELECTION unsuccessful")
        return {
            "sample_id": sample_id,
            "lat": lat,
            "lon": lon,
            "has_solar": False,
            "confidence": 0.0,
            "pv_area_sqm_est": 0.0,
            "buffer_radius_sqft": buffer_used,
            "qc_status": "VERIFIABLE",
            "bbox_or_mask": None,
            "image_metadata": image_meta
        }

    # 3. Area estimation
    area_sqm = estimate_area_sqm(selected["bbox"])

    qc_status = "VERIFIABLE"
    if selected["confidence"] < 0.4:
        qc_status = "NOT_VERIFIABLE"

    return {
        "sample_id": sample_id,
        "lat": lat,
        "lon": lon,
        "has_solar": True,
        "confidence": round(selected["confidence"], 3),
        "pv_area_sqm_est": area_sqm,
        "buffer_radius_sqft": buffer_used,
        "qc_status": qc_status,
        "bbox_or_mask": selected["bbox"],
        "image_metadata": image_meta
    }


def main(input_excel):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_excel(input_excel)

    detector = SolarPanelDetector(
        model_path=MODEL_PATH,
        conf_threshold=CONF_THRESHOLD
    )

    results = []

    for _, row in df.iterrows():
        result = process_sample(detector, row)

        results.append(result)

    output_path = os.path.join(OUTPUT_DIR, "predictions.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[DONE] Results saved to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_excel>")
    else:
        main(sys.argv[1])
