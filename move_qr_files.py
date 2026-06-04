import os
import shutil

# Paths
base_dir = os.path.dirname(__file__)
qr_folder = os.path.join(base_dir, "QR")
os.makedirs(qr_folder, exist_ok=True)

# Move all *_qr.png files to QR folder
for file in os.listdir(base_dir):
    if file.endswith("_qr.png"):
        old_path = os.path.join(base_dir, file)
        new_path = os.path.join(qr_folder, file)
        shutil.move(old_path, new_path)
        print(f"Moved: {file} → {qr_folder}")

print("✅ All QR files moved successfully!")
