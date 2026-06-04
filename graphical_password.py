# graphical_password.py
import sqlite3
import os
import random

DB = "users.db"
IMAGE_FOLDER = "image"  # folder where your 100 images are stored


def choose_graphical_password(username):
    """Let user choose 5 images during registration."""
    images = os.listdir(IMAGE_FOLDER)
    images = [img for img in images if img.lower().endswith((".png", ".jpg", ".jpeg"))]

    if len(images) < 5:
        print("❌ Not enough images in folder for graphical password.")
        return False

    print("\n--- Graphical Password Registration ---")
    print("Select 5 images from the list below:")

    for i, img in enumerate(images, start=1):
        print(f"{i}. {img}")

    selected = []
    for i in range(5):
        choice = int(input(f"Enter image number {i+1}: "))
        if 1 <= choice <= len(images):
            selected.append(images[choice-1])
        else:
            print("Invalid choice. Try again.")
            return False

    # Save as comma-separated string in DB
    graphical_password = ",".join(selected)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE users SET graphical_password=? WHERE username=?", (graphical_password, username))
    conn.commit()
    conn.close()

    print("✅ Graphical password set successfully!")
    return True


def verify_graphical_password(username):
    """Verify graphical password during login using randomized 3x3 grid."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT graphical_password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row or not row[0]:
        print("❌ No graphical password set for this user.")
        return False

    user_images = row[0].split(",")  # 5 chosen images
    all_images = os.listdir(IMAGE_FOLDER)
    all_images = [img for img in all_images if img.lower().endswith((".png", ".jpg", ".jpeg"))]

    # Pick 1 correct image randomly from user's set
    correct_image = random.choice(user_images)

    # Pick 8 random decoys (not from user's set)
    decoys = random.sample([img for img in all_images if img not in user_images], 8)

    # Combine and shuffle into 3x3 grid
    grid = decoys + [correct_image]
    random.shuffle(grid)

    print("\n--- Graphical Password Verification ---")
    print("Identify your registered image from the 3x3 grid:")

    # Display grid in 3x3 format
    for i, img in enumerate(grid, start=1):
        print(f"{i}. {img}", end="\t")
        if i % 3 == 0:
            print()

    choice = int(input("Enter the number of your registered image: "))
    if 1 <= choice <= 9 and grid[choice-1] == correct_image:
        print("✅ Graphical password verified!")
        return True
    else:
        print("❌ Graphical password incorrect!")
        return False
