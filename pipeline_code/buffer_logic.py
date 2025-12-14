import math

def sqft_to_pixel_radius(buffer_sqft, image_size_px=640, meters_per_pixel=0.3):
    """
    Convert buffer area (sqft) to pixel radius.
    Assumes approx meters per pixel (Google zoom ~20 ≈ 0.3 m/px)
    """
    buffer_sqm = buffer_sqft * 0.092903
    radius_m = math.sqrt(buffer_sqm / math.pi)
    radius_px = radius_m / meters_per_pixel
    return radius_px


def bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def bbox_area(bbox):
    x1, y1, x2, y2 = bbox
    return abs(x2 - x1) * abs(y2 - y1)


def select_panel_by_buffer(
    detections,
    image_center=(320, 320),
    buffer_sqft=1200
):
    """
    detections: list of dicts
      { 'bbox': [x1,y1,x2,y2], 'confidence': float }

    Returns:
      selected_detection or None
    """

    buffer_radius_px = sqft_to_pixel_radius(buffer_sqft)

    best_det = None
    best_score = 0

    cx, cy = image_center

    for det in detections:
        bx, by = bbox_center(det["bbox"])
        dist = math.sqrt((bx - cx) ** 2 + (by - cy) ** 2)

        if dist <= buffer_radius_px:
            area = bbox_area(det["bbox"])
            if area > best_score:
                best_score = area
                best_det = det

    return best_det
