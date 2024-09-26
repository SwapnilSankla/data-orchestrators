import os
import unittest

from airflow.models import DagBag


class TestDagValidation(unittest.TestCase):
    def setUp(self):
        # TODO: Need cleaner way to get project path
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        dag_folder_path = os.path.join(project_path, 'src/airflow_project/dags')
        self.dagbag = DagBag(dag_folder=dag_folder_path, include_examples=False)

    def test_dag_loaded(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            f"DAG import failures: {self.dagbag.import_errors}",
        )

    