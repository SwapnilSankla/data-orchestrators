import os
import pytest
from airflow.models import DagBag

from airflow_project_tests.util.project_path import ProjectPath


# pylint: disable=W0621: redefined-outer-name
@pytest.fixture
def dag_bag():
    dag_folder_path = os.path.join(ProjectPath.get(), "src/airflow_project/dags")
    return DagBag(dag_folder=dag_folder_path, include_examples=False)


def test_dag_loaded(dag_bag):
    assert len(dag_bag.import_errors) == 0
