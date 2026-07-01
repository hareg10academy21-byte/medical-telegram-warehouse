from ultralytics import YOLO
import pandas as pd
from pathlib import Path
import cv2

print("Loading YOLOv8 model...")

model = YOLO("yolov8n.pt")

IMAGE_ROOT = Path("data/raw/images")

results_data = []

PRODUCT_OBJECTS = {
    "bottle",
    "cup",
    "box",
    "book",
    "cell phone"
}

print("Scanning images...")

for image_file in IMAGE_ROOT.rglob("*"):

    if image_file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    print(f"Processing: {image_file}")

    # -------------------------------------------------------
    # Skip empty image files
    # -------------------------------------------------------

    try:
        if image_file.stat().st_size == 0:
            print(f"Skipping empty image: {image_file}")
            continue
    except Exception:
        continue

    # -------------------------------------------------------
    # Read image safely
    # -------------------------------------------------------

    try:
        image = cv2.imread(str(image_file))

        if image is None:
            print(f"Skipping unreadable image: {image_file}")
            continue

    except Exception as e:
        print(f"Skipping corrupted image: {image_file}")
        print(e)
        continue

    # -------------------------------------------------------
    # Run YOLO
    # -------------------------------------------------------

    try:
        results = model(image)

    except Exception as e:
        print(f"YOLO failed on {image_file}")
        print(e)
        continue

    detected = []
    confidence = []

    for r in results:

        for box in r.boxes:

            cls = int(box.cls)

            label = model.names[cls]

            conf = float(box.conf)

            detected.append(label)

            confidence.append(conf)

    has_person = "person" in detected

    has_product = any(obj in detected for obj in PRODUCT_OBJECTS)

    if has_person and has_product:

        category = "promotional"

    elif has_product:

        category = "product_display"

    elif has_person:

        category = "lifestyle"

    else:

        category = "other"

    results_data.append({

        "message_id": int(image_file.stem),

        "channel_name": image_file.parent.name,

        "detected_class": ",".join(detected),

        "confidence_score": max(confidence) if confidence else 0,

        "image_category": category

    })

print()

print("Creating CSV...")

df = pd.DataFrame(results_data)

Path("data/processed").mkdir(parents=True, exist_ok=True)

output = "data/processed/detection_results.csv"

df.to_csv(output, index=False)

print(df.head())

print()

print(f"Processed {len(df)} images.")

print(f"Saved to {output}")