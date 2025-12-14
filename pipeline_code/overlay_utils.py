import cv2
import math

IMAGE_CENTER = (320, 320)

def draw_overlay(image_path, detection, buffer_sqft, out_path):
    img = cv2.imread(image_path)

    if img is None:
        return

    # Draw bounding box
    if detection:
        x1, y1, x2, y2 = map(int, detection["bbox"])
        conf = detection["confidence"]

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            img,
            f"Solar ({conf:.2f})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    # Draw buffer circle
    radius = int(math.sqrt((buffer_sqft * 0.092903) / math.pi) / 0.3)
    cv2.circle(img, IMAGE_CENTER, radius, (255, 0, 0), 2)

    cv2.imwrite(out_path, img)
