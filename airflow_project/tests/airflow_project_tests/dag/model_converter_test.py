import os

import pandas as pd
import pytest
from airflow_project_tests.util.project_path import ProjectPath

from airflow_project.plugins.custom_operator.model_converter import ModelConverter


# pylint: disable=W0621: redefined-outer-name
@pytest.fixture
def csv_cleaned_file_path():
    return os.path.join(ProjectPath.get(), "tests/data/cleaned-user-data.csv")


@pytest.fixture
def task(csv_cleaned_file_path):
    csv_file_path = os.path.join(ProjectPath.get(), "tests/data/user-data.csv")
    task = ModelConverter(
        task_id="task",
        csv_file_path=csv_file_path,
        csv_cleaned_file_path=csv_cleaned_file_path,
    )
    return task


def test_conversion(task, csv_cleaned_file_path):
    if os.path.exists(csv_cleaned_file_path):
        os.remove(csv_cleaned_file_path)

    task.execute(context={})

    df = pd.read_csv(csv_cleaned_file_path)
    assert df.columns.tolist() == ["Age", "name"]
    assert df["name"].tolist() == ["A B", "C D"]
    assert df["Age"].tolist() == [30, 35]

    os.remove(csv_cleaned_file_path)
