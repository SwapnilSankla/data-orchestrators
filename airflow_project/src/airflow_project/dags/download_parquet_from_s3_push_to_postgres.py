import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 24),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

dag = DAG('download_parquet_from_s3_push_to_postgres', 
          default_args=default_args, 
          description='This DAG downloads parquet file from S3 and pushes it to Postgres', 
          schedule='@daily', 
          start_date=datetime(2024, 9, 11))    

is_parquet_file_available = S3KeySensor(
    task_id='is_parquet_file_available',
    aws_conn_id=os.getenv('AWS_CONN_ID', 'aws_minio'),
    bucket_name=os.getenv('S3_BUCKET_NAME', 'data'),
    bucket_key= os.getenv('PARQUET_FILE_NAME', 'user-data.parquet'),
    dag=dag)