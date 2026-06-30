from pathlib import Path
import pandas as pd
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

IMAGE_ROOT = Path("data/raw/images")

results = []

for channel in IMAGE_ROOT.iterdir():

    if not channel.is_dir():
        continue

    print(f"\nProcessing {channel.name}")

    for image in channel.glob("*.jpg"):

        try:
            print(f"Processing {image}")
            prediction = model(str(image), verbose=False)
        except Exception as e:
            print(f"Skipping {image.name}: {e}")
            continue

        classes = []
        confidences = []

        for r in prediction:
            for box in r.boxes:

                cls = model.names[int(box.cls[0])]
                conf = float(box.conf[0])

                classes.append(cls)
                confidences.append(conf)

        has_person = "person" in classes

        has_product = any(
            c in ["bottle", "cup", "box", "vase"]
            for c in classes
        )

        if has_person and has_product:
            category = "promotional"

        elif has_product:
            category = "product_display"

        elif has_person:
            category = "lifestyle"

        else:
            category = "other"

        results.append({

            "message_id": int(image.stem),

            "channel_name": channel.name,

            "detected_class": ",".join(classes),

            "confidence_score":
                max(confidences) if confidences else None,

            "image_category": category

        })

df = pd.DataFrame(results)

df.to_csv("data/detections.csv", index=False)

print("\nFinished!")
print(df.head())
print(f"\nSaved {len(df)} rows to data/detections.csv")