from airflow.models import BaseOperator


class ParquetToCsvOperator(BaseOperator):
    def __init__(self, parquet_file_path_provider_task_id, csv_file_path, **kwargs):
        super().__init__(**kwargs)
        self.csv_file_path = csv_file_path
        self.parquet_file_path_provider_task_id = parquet_file_path_provider_task_id

    def execute(self, context):
        import pandas as pd
        parquet_file_path = context['ti'].xcom_pull(task_ids=self.parquet_file_path_provider_task_id)
        df = pd.read_parquet(parquet_file_path)
        df.to_csv(self.csv_file_path, index=False)