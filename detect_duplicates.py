import sys
import os
from PIL import Image
import imagehash

def detect_duplicates(directory="images", threshold=2):
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist. Skipping duplicate check.")
        return 0
    # Get list of image files
    images = [f for f in os.listdir(directory) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))]
    hashes = {}
    duplicate_found = False
    for img_name in images:
        path = os.path.join(directory, img_name)
        try:
            with Image.open(path) as img:
                dhash = imagehash.dhash(img)
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
            continue
        for existing_img, existing_hash in hashes.items():
            if dhash - existing_hash <= threshold:
                print(f"Duplicate detected: {img_name} and {existing_img}")
                duplicate_found = True
        hashes[img_name] = dhash
    if duplicate_found:
        print("Duplicates found.")
        return 1
    else:
        print("No duplicates detected.")
        return 0

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else "images"
    exit_code = detect_duplicates(directory)
    sys.exit(exit_code)
