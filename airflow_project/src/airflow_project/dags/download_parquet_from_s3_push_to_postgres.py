import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 24),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

def download_file(aws_conn_id, bucket_name, bucket_key):
    return S3Hook(aws_conn_id).download_file(key=bucket_key, bucket_name=bucket_name, local_path='.')

dag = DAG('download_parquet_from_s3_push_to_postgres', 
          default_args=default_args, 
          description='This DAG downloads parquet file from S3 and pushes it to Postgres', 
          schedule='@daily', 
          start_date=datetime(2024, 9, 11))    

is_parquet_file_available = S3KeySensor(
    task_id='is_parquet_file_available',
    aws_conn_id=os.getenv('AWS_CONN_ID'),
    bucket_name=os.getenv('S3_BUCKET_NAME'),
    bucket_key= os.getenv('PARQUET_FILE_NAME'),
    dag=dag)

download_parquet_from_s3 = PythonOperator(
    task_id='download_parquet_from_s3',
    python_callable=download_file,
    op_kwargs={
        'aws_conn_id': os.getenv('AWS_CONN_ID'),
        'bucket_name': os.getenv('S3_BUCKET_NAME'),
        'bucket_key': os.getenv('PARQUET_FILE_NAME')
    },
    dag=dag)

is_parquet_file_available >> download_parquet_from_s3