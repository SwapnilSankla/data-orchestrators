import os
import unittest
import pandas as pd
from airflow_project_test.util.project_path import ProjectPath
from airflow_project.dags.download_parquet_from_s3_push_to_postgres import ModelConverter


class ModelConverterTest(unittest.TestCase):
    def test_conversion(self):
        csv_file_path = os.path.join(ProjectPath.get(), 'test/data/user-data.csv')
        csv_cleaned_file_path = os.path.join(ProjectPath.get(), 'test/data/cleaned-user-data.csv')
        if os.path.exists(csv_cleaned_file_path):
            os.remove(csv_cleaned_file_path)

        task = ModelConverter(task_id='task', csv_file_path=csv_file_path, csv_cleaned_file_path=csv_cleaned_file_path)
        task.execute(context={})

        df = pd.read_csv(csv_cleaned_file_path)
        self.assertEqual(df.columns.tolist(), ['Age', 'name'])
        self.assertEqual(df['name'].tolist(), ['A B', 'C D'])
        self.assertEqual(df['Age'].tolist(), [30, 35])

        os.remove(csv_cleaned_file_path)
