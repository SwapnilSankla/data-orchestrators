import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import BaseOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas


class ParquetToCsvOperator(BaseOperator):
    def __init__(self, parquet_file_path_provider_task_id, csv_file_path, **kwargs):
        super().__init__(**kwargs)
        self.csv_file_path = csv_file_path
        self.parquet_file_path_provider_task_id = parquet_file_path_provider_task_id

    def execute(self, context):
        parquet_file_path = context['ti'].xcom_pull(task_ids=self.parquet_file_path_provider_task_id)
        df = pandas.read_parquet(parquet_file_path)
        df.to_csv(self.csv_file_path, index=False)


class ModelConverter(BaseOperator):
    def __init__(self, csv_file_path, csv_cleaned_file_path, **kwargs):
        super().__init__(**kwargs)
        self.csv_file_path = csv_file_path
        self.csv_cleaned_file_path = csv_cleaned_file_path

    def execute(self, context):
        df = pandas.read_csv(self.csv_file_path)
        df['name'] = df['First name'] + ' ' + df['last name']
        df.drop(columns=['First name', 'last name'], inplace=True)
        df.to_csv(self.csv_cleaned_file_path, index=False)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 24),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}


def __download_file(aws_conn_id, bucket_name, bucket_key):
    return S3Hook(aws_conn_id).download_file(key=bucket_key, bucket_name=bucket_name, local_path='.')


def __insert(csv_cleaned_file_path):
    insert_into_postgres_table = PostgresHook(postgres_conn_id=os.getenv('POSTGRES_CONN_ID'), schema='airflow')
    connection = insert_into_postgres_table.get_conn()
    cursor = connection.cursor()
    transformed_data = []
    with open(csv_cleaned_file_path, 'r', encoding='utf-8') as f:
        f.readlines().pop(0)
        for line in f.readlines():
            transformed_data.append(tuple(line.strip().split(',')))

    for record in transformed_data:
        cursor.execute('INSERT INTO user_data(age, Name) VALUES (%s, %s)', record)

    connection.commit()
    cursor.close()
    connection.close()


dag = DAG('download_parquet_from_s3_push_to_postgres',
          default_args=default_args,
          description='This DAG downloads parquet file from S3 and pushes it to Postgres',
          schedule='@daily',
          start_date=datetime(2024, 9, 11))

is_parquet_file_available = S3KeySensor(
    task_id='is_parquet_file_available',
    aws_conn_id=os.getenv('AWS_CONN_ID'),
    bucket_name=os.getenv('S3_BUCKET_NAME'),
    bucket_key=os.getenv('PARQUET_FILE_NAME'),
    dag=dag)

download_parquet_from_s3 = PythonOperator(
    task_id='download_parquet_from_s3',
    python_callable=__download_file,
    op_kwargs={
        'aws_conn_id': os.getenv('AWS_CONN_ID'),
        'bucket_name': os.getenv('S3_BUCKET_NAME'),
        'bucket_key': os.getenv('PARQUET_FILE_NAME')
    },
    dag=dag)

convert_parquet_to_csv = ParquetToCsvOperator(
    task_id='convert_parquet_to_csv',
    parquet_file_path_provider_task_id='download_parquet_from_s3',
    csv_file_path=os.getenv('CSV_FILE_PATH'),
    dag=dag)

model_converter = ModelConverter(
    task_id='convert_to_model',
    csv_file_path=os.getenv('CSV_FILE_PATH'),
    csv_cleaned_file_path=os.getenv('CLEANED_CSV_FILE_PATH'),
    dag=dag)

create_table_if_not_exists = SQLExecuteQueryOperator(
    task_id='create_table_if_not_exists',
    conn_id=os.getenv('POSTGRES_CONN_ID'),
    sql='''
        CREATE TABLE IF NOT EXISTS user_data (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT)
    ''',
    dag=dag)

insert_into_table = PythonOperator(
    task_id='insert_into_table',
    python_callable=__insert,
    op_args=[os.getenv('CLEANED_CSV_FILE_PATH')],
    dag=dag)

# pylint: disable=W0104
is_parquet_file_available >> download_parquet_from_s3 >> convert_parquet_to_csv >> model_converter
model_converter >> create_table_if_not_exists >> insert_into_table
