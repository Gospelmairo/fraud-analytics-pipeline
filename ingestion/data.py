import kagglehub
import pandas as pd
import os
import boto3
import io

# ------------------------------
# ✅ CONFIGURATION - UPDATE THESE
# ------------------------------
S3_BUCKET_NAME = "mairo-g"
S3_FOLDER_NAME = "transactions"
ROWS_TO_LOAD = 500_000

# ------------------------------
# ✅ Upload DataFrame directly to S3 (no local file)
# ------------------------------
def upload_df_to_s3(df, bucket, key):
    s3 = boto3.client('s3')
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    try:
        s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket, Key=key)
        print(f"✅ Uploaded to s3://{bucket}/{key}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

# ------------------------------
# ✅ Step 1: Download dataset from KaggleHub
# ------------------------------
print("⬇️ Downloading dataset from KaggleHub...")
dataset_path = kagglehub.dataset_download("ismetsemedov/transactions")
print("📁 Dataset downloaded to:", dataset_path)

# ------------------------------
# ✅ Step 2: Stream each file to S3
# ------------------------------
csv_files = [f for f in os.listdir(dataset_path) if f.endswith(".csv")]

for csv_file in csv_files:
    file_path = os.path.join(dataset_path, csv_file)

    print(f"📄 Reading {ROWS_TO_LOAD} rows from {csv_file}...")
    df = pd.read_csv(file_path, nrows=ROWS_TO_LOAD)

    # Build S3 key and upload
    s3_key = f"{S3_FOLDER_NAME}/{csv_file}"
    upload_df_to_s3(df, S3_BUCKET_NAME, s3_key)
