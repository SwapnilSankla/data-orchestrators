import pandas
from airflow.models import BaseOperator


class ModelConverter(BaseOperator):
    def __init__(self, csv_file_path, csv_cleaned_file_path, **kwargs):
        super().__init__(**kwargs)
        self.csv_file_path = csv_file_path
        self.csv_cleaned_file_path = csv_cleaned_file_path

    def execute(self, context):
        df = pandas.read_csv(self.csv_file_path)
        df["name"] = df["First name"] + " " + df["last name"]
        df.drop(columns=["First name", "last name"], inplace=True)
        df.to_csv(self.csv_cleaned_file_path, index=False)
