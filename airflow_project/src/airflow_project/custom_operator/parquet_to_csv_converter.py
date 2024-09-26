from airflow.models import BaseOperator


class ParquetToCsvOperator(BaseOperator):
    def __init__(self, csv_file_path, **kwargs):
        super().__init__(**kwargs)
        self.csv_file_path = csv_file_path

    def execute(self, context):
        import pandas as pd
        self.parquet_file_path = context['ti'].xcom_pull(task_ids='download_parquet_from_s3')
        df = pd.read_parquet(self.parquet_file_path)
        df.to_csv(self.csv_file_path, index=False)