import unittest
from airflow.models import DagBag

class TestDagValidation(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag(dag_folder="dags", include_examples=False)

    def test_dag_loaded(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            f"DAG import failures: {self.dagbag.import_errors}",
        )

    