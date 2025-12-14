import math

IMAGE_CENTER = (320, 320)  # for 640x640 images
METERS_PER_PIXEL = 0.3    # approx for Google zoom ~20


def sqft_to_radius_px(buffer_sqft):
    buffer_sqm = buffer_sqft * 0.092903
    radius_m = math.sqrt(buffer_sqm / math.pi)
    return radius_m / METERS_PER_PIXEL


def bbox_area(bbox):
    x1, y1, x2, y2 = bbox
    return abs(x2 - x1) * abs(y2 - y1)


def bbox_points(bbox):
    x1, y1, x2, y2 = bbox
    return [
        (x1, y1), (x2, y1), (x2, y2), (x1, y2),      # corners
        ((x1+x2)/2, y1), ((x1+x2)/2, y2),            # mid top/bottom
        (x1, (y1+y2)/2), (x2, (y1+y2)/2)             # mid left/right
    ]


def point_inside_circle(point, center, radius):
    px, py = point
    cx, cy = center
    return math.hypot(px - cx, py - cy) <= radius


def bbox_intersects_circle(bbox, radius_px):
    for p in bbox_points(bbox):
        if point_inside_circle(p, IMAGE_CENTER, radius_px):
            return True
    return False


def bbox_fully_inside_circle(bbox, radius_px):
    for p in bbox_points(bbox)[:4]:  # only corners
        if not point_inside_circle(p, IMAGE_CENTER, radius_px):
            return False
    return True


def select_panel_with_buffer_logic(detections, conf_thresh=0.4):
    """
    Implements official buffer logic:
    - Try 1200 sqft
    - Escalate to 2400 sqft if needed
    """

    # Filter by confidence
    detections = [d for d in detections if d["confidence"] >= conf_thresh]

    if not detections:
        return None, None  # no solar at all

    # ---------- 1200 sqft ----------
    r1200 = sqft_to_radius_px(1200)

    inside_1200 = []
    boundary_crossing = []

    for d in detections:
        if bbox_fully_inside_circle(d["bbox"], r1200):
            inside_1200.append(d)
        elif bbox_intersects_circle(d["bbox"], r1200):
            boundary_crossing.append(d)

    # Case 1 & 2
    if inside_1200:
        best = max(inside_1200, key=lambda d: bbox_area(d["bbox"]))
        return best, 1200

    # Case 3
    if boundary_crossing:
        best = max(boundary_crossing, key=lambda d: bbox_area(d["bbox"]))
        return best, 2400

    # ---------- 2400 sqft ----------
    r2400 = sqft_to_radius_px(2400)

    inside_2400 = [
        d for d in detections if bbox_intersects_circle(d["bbox"], r2400)
    ]

    if inside_2400:
        best = max(inside_2400, key=lambda d: bbox_area(d["bbox"]))
        return best, 2400

    # Case 4
    return None, None
