import boto3
import json

bucket = "quantum-clinical-optimization-us-west-2"
prefix = "clinical-trials-data/raw/"

s3 = boto3.client("s3")

keys = []
continuation_token = None

print("📁 Fetching existing S3 keys...")

while True:
    if continuation_token:
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            ContinuationToken=continuation_token
        )
    else:
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix
        )

    contents = response.get("Contents", [])
    for obj in contents:
        keys.append(obj["Key"])

    if response.get("IsTruncated"):
        continuation_token = response["NextContinuationToken"]
    else:
        break

print(f"Total keys fetched: {len(keys)}")

# Save list
with open("existing_keys.json", "w") as f:
    json.dump(keys, f)

print("Saved to existing_keys.json")
