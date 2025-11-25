import boto3, os, concurrent.futures
from pathlib import Path
from botocore.exceptions import ClientError

bucket_name = "quantum-clinical-optimization-us-west-2"
local_root = Path.home() / "datasets" / "clinical-trials" / "unzipped"
prefix = "clinical-trials-data/raw/"
s3 = boto3.client("s3")

def log(msg):
    print(msg, flush=True)

def file_exists_in_s3(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise

def upload_file(local_path, s3_key):
    try:
        s3.upload_file(str(local_path), bucket_name, s3_key)
        return True
    except Exception as e:
        log(f"⚠️ Failed: {s3_key} ({e})")
        return False
