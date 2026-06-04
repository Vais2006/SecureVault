import os
import shutil

# Base project folder (where your Python files are)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source = main folder (where stray images are downloaded)
SOURCE_FOLDER = BASE_DIR  

# Destination = image folder
DEST_FOLDER = os.path.join(BASE_DIR, "image")

# Make sure "image" folder exists
os.makedirs(DEST_FOLDER, exist_ok=True)

# Image extensions we care about
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def move_images():
    moved_files = []
    for file in os.listdir(SOURCE_FOLDER):
        if file.lower().endswith(IMAGE_EXTENSIONS):
            src = os.path.join(SOURCE_FOLDER, file)
            dst = os.path.join(DEST_FOLDER, file)
            if os.path.isfile(src):
                shutil.move(src, dst)
                moved_files.append(file)

    if moved_files:
        print("✅ Moved images:", ", ".join(moved_files))
        print(f"📂 All images are now inside: {DEST_FOLDER}")
    else:
        print("ℹ️ No images found in main folder.")

if __name__ == "__main__":
    move_images()
