import os
import io
import json
import boto3
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# === CONFIG ===
AWS_REGION = "us-east-1"
S3_BUCKET = "mairo-g"
S3_KEY = "transactions/synthetic_fraud_data.csv"

SNOWFLAKE_ACCOUNT = os.environ["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = os.environ["SNOWFLAKE_USER"]
SNOWFLAKE_PASSWORD = os.environ["SNOWFLAKE_PASSWORD"]
SNOWFLAKE_DATABASE = "FRAUD_ANALYTICS"
SNOWFLAKE_SCHEMA = "RAW"
SNOWFLAKE_TABLE = "FRAUD_TRANSACTIONS"
SNOWFLAKE_WAREHOUSE = os.environ["SNOWFLAKE_WAREHOUSE"]
SNOWFLAKE_ROLE = "ACCOUNTADMIN"

# === STEP 1: Read CSV from S3 ===
s3 = boto3.client("s3", region_name=AWS_REGION)

def read_csv_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read()
    return pd.read_csv(io.BytesIO(data))

df = read_csv_from_s3(S3_BUCKET, S3_KEY)

# === STEP 2: Normalize column names ===
df.columns = [col.lower() for col in df.columns]

# === STEP 3: Clean non-scalar values ===
def clean_non_scalar_columns(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
            print(f"⚠️ Column '{col}' contains non-scalar values. Converting them to strings.")
            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x)

        # Optional: force numeric conversion if Snowflake expects a numeric type
        # (e.g. 'amount', 'distance_from_home', etc.)
        if col in ['amount', 'distance_from_home', 'transaction_hour', 'velocity_last_hour', 'num_transactions', 'total_amount', 'max_single_amount']:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                print(f"⚠️ Could not convert column '{col}' to numeric: {e}")
    return df


df = clean_non_scalar_columns(df)

print(f"✅ Loaded {len(df)} rows from S3")
print(f"🧪 Columns: {df.columns.tolist()}")

# === STEP 4: Connect to Snowflake ===
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

with conn.cursor() as cur:
    cur.execute(f"DESC TABLE {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE}")
    snowflake_columns = [row[0] for row in cur.fetchall()]
    print("Columns in Snowflake table:", snowflake_columns)

    cur.execute(f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE}")
    print(f"🧑‍💻 Using warehouse: {SNOWFLAKE_WAREHOUSE}")

# === STEP 5: Truncate Table ===
with conn.cursor() as cur:
    cur.execute(f"TRUNCATE TABLE {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE}")
    print(f"🧹 Table {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE} truncated.")

# === STEP 6: Upload to Snowflake ===
success, nchunks, nrows, _ = write_pandas(
    conn,
    df,
    table_name=SNOWFLAKE_TABLE,
    quote_identifiers=True
)

print(f"🚀 Uploaded {nrows} rows to Snowflake table {SNOWFLAKE_TABLE}")

# === Cleanup ===
conn.close()