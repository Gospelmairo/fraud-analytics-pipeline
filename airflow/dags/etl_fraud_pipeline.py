from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.empty import EmptyOperator

import os
import boto3
from kaggle.api.kaggle_api_extended import KaggleApi

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

dag = DAG(
    'fraud_detection_etl_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='ETL pipeline for real-time fraud analytics',
)

# 📥 Download Kaggle data & upload to S3
def download_and_upload_kaggle_data():
    dataset = 'arjunbhasin2013/cc-fraud-detection'
    file_name = 'transactions.csv'
    local_path = f'/tmp/{file_name}'
    s3_bucket = 'mairo-g'
    s3_key = 'kaggle/transactions/transactions.csv'

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path='/tmp', unzip=True)

    s3 = boto3.client('s3')
    s3.upload_file(local_path, s3_bucket, s3_key)
    print(f"✅ Uploaded to s3://{s3_bucket}/{s3_key}")

# 👨‍🏭 Spark transformation
spark_transform = BashOperator(
    task_id='spark_transform',
    bash_command='spark-submit /Users/user/Desktop/Project/spark_jobs/transform_transaction.py',
    dag=dag,
)

# 🧪 Batch ingestion to Snowflake using your script
ingest_to_snowflake = BashOperator(
    task_id='ingest_to_snowflake',
    bash_command='python3 /Users/user/Desktop/Project/ingestion/batch_ingestion.py',
    dag=dag,
)

# 🧠 SQL transformations in Snowflake (if needed as a separate script)
def run_sql_transforms():
    import snowflake.connector
    conn = snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        database='FRAUD_ANALYTICS',
        schema='RAW',
        role='ACCOUNTADMIN'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM FRAUD_TRANSACTIONS;")
    print("✅ Total transactions:", cursor.fetchone())

    cursor.close()
    conn.close()

sql_transform = PythonOperator(
    task_id='sql_transform',
    python_callable=run_sql_transforms,
    dag=dag,
)

# 🧩 DAG Flow
start = EmptyOperator(task_id='start', dag=dag)
end = EmptyOperator(task_id='end', dag=dag)

download_upload = PythonOperator(
    task_id='download_and_upload_kaggle',
    python_callable=download_and_upload_kaggle_data,
    dag=dag,
)

start >> download_upload >> spark_transform >> ingest_to_snowflake >> sql_transform >> end
