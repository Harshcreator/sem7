import os
import hashlib
import exifread
from PIL import Image
import json

# -----------------------------
# Function: Extract EXIF metadata
# -----------------------------
def extract_exif(image_path):
    exif_data = {}
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            for tag in tags:
                exif_data[tag] = str(tags[tag])
    except Exception as e:
        exif_data['error'] = str(e)
    return exif_data

# -----------------------------
# Function: Generate SHA256 hash
# -----------------------------
def generate_hash(image_path):
    hasher = hashlib.sha256()
    try:
        with open(image_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# Function: Basic image analysis
# -----------------------------
def analyze_image(image_path):
    info = {}
    try:
        img = Image.open(image_path)
        info['width'], info['height'] = img.size
        info['format'] = img.format
        info['mode'] = img.mode
    except Exception as e:
        info['error'] = str(e)
    return info

# -----------------------------
# Function: Forensic report for a single image
# -----------------------------
def forensic_report(image_path):
    report = {
        'file_name': os.path.basename(image_path),
        'file_path': os.path.abspath(image_path),
        'hash': generate_hash(image_path),
        'exif': extract_exif(image_path),
        'image_info': analyze_image(image_path)
    }
    return report

# -----------------------------
# Function: Process all images in a folder
# -----------------------------
def batch_process(folder_path, save_json=True):
    supported_formats = ('.jpg', '.jpeg', '.png', '.tiff', '.bmp')
    reports = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_path = os.path.join(root, file)
                report = forensic_report(image_path)
                reports.append(report)
                print(f"Processed: {file}")

    if save_json:
        output_file = os.path.join(folder_path, 'forensic_report.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=4)
        print(f"\nForensic report saved as {output_file}")

    return reports

# -----------------------------
# Main execution
# -----------------------------
if __name__ == "__main__":
    print("=== Digital Image Forensics Tool ===")
    folder_path = input("Enter the folder path containing images: ")
    
    if not os.path.exists(folder_path):
        print("Error: Folder does not exist.")
    else:
        reports = batch_process(folder_path)
        print("\n=== Summary ===")
        for rep in reports:
            print(f"File: {rep['file_name']}, Hash: {rep['hash'][:16]}..., Format: {rep['image_info'].get('format', 'N/A')}")
