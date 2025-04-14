from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

default_args = {
    'owner': 'mairo',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'fraud_data_pipeline',
    default_args=default_args,
    description='Orchestrates the fraud detection pipeline',
    schedule_interval='@daily',
    catchup=False
)

# 1. Run Spark Job
run_spark = BashOperator(
    task_id='run_spark_transformation',
    bash_command='spark-submit /Project/spark_jobs/transform_transaction.py',
    dag=dag,
)

# 2. Batch Ingestion into Snowflake
def load_to_snowflake():
    from ingestion.batch_ingestion import main
    main()

load_data = PythonOperator(
    task_id='load_transformed_data',
    python_callable=load_to_snowflake,
    dag=dag,
)

# 3. (Optional) Run SQL Models or KPIs
run_sql = BashOperator(
    task_id='run_kpi_queries',
    bash_command='snowsql -c my_conn -f /path/to/sql/kpi_queries.sql',
    dag=dag,
)

# Set Task Dependencies
run_spark >> load_data >> run_sql
