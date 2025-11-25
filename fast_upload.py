import os
import json
import boto3
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
bucket = "quantum-clinical-optimization-us-west-2"
prefix = "clinical-trials-data/raw/"
local_root = Path.home() / "datasets" / "clinical-trials" / "unzipped"

# -----------------------------
# Load existing S3 keys
# -----------------------------
print("📂 Loading existing_keys.json...")
with open("existing_keys.json", "r") as f:
    existing_keys = set(json.load(f))

print(f"Existing keys loaded: {len(existing_keys)}")

# -----------------------------
# AWS client
# -----------------------------
s3 = boto3.client("s3")

# -----------------------------
# Upload function
# -----------------------------
def upload(local_file, s3_key):
    try:
        s3.upload_file(str(local_file), bucket, s3_key)
        print(f"⬆️  Uploaded: {s3_key}")
        return True
    except Exception as e:
        print(f"⚠️ Upload failed: {s3_key} — {e}")
        return False

# -----------------------------
# Main upload loop
# -----------------------------
uploaded = 0
skipped = 0
checked = 0

print("\n🚀 Starting FAST upload pass...\n")

for root, _, files in os.walk(local_root):
    for name in files:
        checked += 1

        local_file = Path(root) / name
        rel = local_file.relative_to(local_root)
        s3_key = f"{prefix}{rel.as_posix()}"

        # skip instantly if in keyset
        if s3_key in existing_keys:
            skipped += 1
        else:
            if upload(local_file, s3_key):
                uploaded += 1

        # progress tick every 1000
        if checked % 1000 == 0:
            print(f"Progress: checked {checked} → uploaded {uploaded}, skipped {skipped}")

print("\n🎉 FAST upload pass complete!")
print(f"Total checked: {checked}")
print(f"Uploaded: {uploaded}")
print(f"Skipped: {skipped}")
