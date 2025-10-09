import pytsk3
import sys
import os

# Set the path to the storage device (e.g., '\\\\.\\E:' on Windows or '/dev/sdb1' on Linux)
DEVICE_PATH = r'\\.\E:'  # Change this to your drive letter or device path
OUTPUT_DIR = 'recovered_files'

# Common file extensions to recover
RECOVER_EXTS = ['.txt', '.jpg', '.pdf', '.docx']

def is_deleted(entry):
    """Check if a file entry is deleted."""
    return entry.info.meta and entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC

def has_valid_ext(filename):
    """Check if file has a recoverable extension."""
    return any(filename.lower().endswith(ext) for ext in RECOVER_EXTS)

def recover_files(fs, directory, output_dir, log):
    """Recursively scan and recover deleted files."""
    for entry in directory:
        if not hasattr(entry, 'info') or not hasattr(entry.info, 'name'):
            continue
        name = entry.info.name.name.decode('utf-8', errors='ignore')
        if name in [".", ".."]:
            continue

        # If entry is a directory, recurse
        if entry.info.meta and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            try:
                subdir = entry.as_directory()
                recover_files(fs, subdir, output_dir, log)
            except Exception:
                continue

        # If entry is a deleted file with a valid extension, recover it
        elif is_deleted(entry) and has_valid_ext(name):
            try:
                filedata = entry.read_random(0, entry.info.meta.size)
                out_path = os.path.join(output_dir, name)
                # Avoid overwriting files
                base, ext = os.path.splitext(out_path)
                count = 1
                while os.path.exists(out_path):
                    out_path = f"{base}_{count}{ext}"
                    count += 1
                with open(out_path, 'wb') as f:
                    f.write(filedata)
                log.append(f"Recovered: {name} -> {out_path}")
            except Exception as e:
                log.append(f"Failed to recover {name}: {e}")

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    log = []

    # Open the disk image/device
    try:
        img = pytsk3.Img_Info(DEVICE_PATH)
        fs = pytsk3.FS_Info(img)
    except Exception as e:
        print(f"Error opening device: {e}")
        sys.exit(1)

    # Start recovery from root directory
    root_dir = fs.open_dir(path="/")
    recover_files(fs, root_dir, OUTPUT_DIR, log)

    # Print recovery log
    print("Recovery Log:")
    for entry in log:
        print(entry)

if __name__ == "__main__":
    main()
