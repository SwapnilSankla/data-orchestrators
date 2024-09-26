import os
import unittest

from airflow.models import DagBag

from airflow_project_test.util.project_path import ProjectPath


class TestDagValidation(unittest.TestCase):
    def setUp(self):
        dag_folder_path = os.path.join(ProjectPath.get(), 'src/airflow_project/dags')
        self.dagBag = DagBag(dag_folder=dag_folder_path, include_examples=False)

    def test_dag_loaded(self):
        self.assertFalse(
            len(self.dagBag.import_errors),
            f"DAG import failures: {self.dagBag.import_errors}",
        )
