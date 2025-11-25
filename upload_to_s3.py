import os
import boto3
import time
from pathlib import Path
from botocore.exceptions import ClientError

# --- CONFIGURATION ----------------------------------------------------------
bucket_name = "quantum-clinical-optimization-us-west-2"
local_root = Path.home() / "datasets" / "clinical-trials" / "unzipped"
prefix = "clinical-trials-data/raw/"
batch_size = 500  # files per log update
max_retries = 3   # retry failed uploads

s3 = boto3.client("s3")

# --- HELPER FUNCTIONS -------------------------------------------------------
def log(msg):
    print(msg, flush=True)

def file_exists_in_s3(s3_client, bucket, key):
    """Check if an object already exists in S3."""
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise

def upload_file(local_path, s3_key):
    """Upload file with simple retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            s3.upload_file(str(local_path), bucket_name, s3_key)
            return True
        except Exception as e:
            log(f"⚠️ Attempt {attempt} failed for {s3_key}: {e}")
            time.sleep(2 * attempt)
    return False

# --- MAIN UPLOAD LOOP -------------------------------------------------------
uploaded = 0
skipped = 0
all_files = []

for root, _, files in os.walk(local_root):
    for f in files:
        local_path = Path(root) / f
        rel_path = local_path.relative_to(local_root)
        s3_key = f"{prefix}{rel_path.as_posix()}"
        all_files.append((local_path, s3_key))

total_files = len(all_files)
log(f"Found {total_files} files under {local_root}")

for i, (local_path, s3_key) in enumerate(all_files, 1):
    try:
        if file_exists_in_s3(s3, bucket_name, s3_key):
            skipped += 1
        else:
            if upload_file(local_path, s3_key):
                uploaded += 1
            else:
                log(f"❌ Failed after retries: {s3_key}")
    except Exception as e:
        log(f"⚠️ Skipped {s3_key}: {e}")

    if i % batch_size == 0 or i == total_files:
        log(f"📦 Progress: {i}/{total_files} files checked → {uploaded} uploaded, {skipped} skipped")

log(f"\n✅ Upload complete.\nTotal files scanned: {total_files}\nUploaded: {uploaded}\nSkipped: {skipped}")
