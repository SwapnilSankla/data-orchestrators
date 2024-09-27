import os

import pytest
from _pytest.monkeypatch import MonkeyPatch
from airflow.models import DagBag
from airflow_project_tests.util.project_path import ProjectPath


# pylint: disable=W0621: redefined-outer-name
@pytest.fixture
def dag_bag():
    monkeypatch = MonkeyPatch()
    monkeypatch.setenv("AWS_CONN_ID", "test_aws_conn_id", "")
    monkeypatch.setenv("S3_BUCKET_NAME", "test", "")
    monkeypatch.setenv("PARQUET_FILE_NAME", "test-data.parquet", "")
    monkeypatch.setenv("CSV_FILE_PATH", "test-data.csv", "")
    monkeypatch.setenv("CLEANED_CSV_FILE_PATH", "test-data-cleaned.csv", "")

    dag_folder_path = os.path.join(ProjectPath.get(), "src/airflow_project/dags", "")
    return DagBag(dag_folder=dag_folder_path, include_examples=False)


@pytest.fixture
def dag(dag_bag):
    return dag_bag.get_dag(dag_id="download_parquet_from_s3_push_to_postgres")


def __get_downstream_task_ids(dag, task_id):
    task = dag.get_task(task_id)
    return list(map(lambda t: t.task_id, task.downstream_list))


def test_dag_schedule_interval(dag):
    assert dag.schedule_interval == "@daily"


def test_dag_retries(dag):
    assert dag.default_args["retries"] == 5


def test_dag_retry_delay(dag):
    assert dag.default_args["retry_delay"].total_seconds() == 300


def test_dag_catchup(dag):
    assert dag.default_args["catchup"] is False


def test_dag_owner(dag):
    assert dag.default_args["owner"] == "airflow"


def test_number_of_tasks(dag):
    assert len(dag.tasks) == 6


def test_dependencies_is_parquet_file_available(dag):
    task = "is_parquet_file_available"
    expected_task_dependencies = ["download_parquet_from_s3"]
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_dependencies_download_parquet_from_s3(dag):
    task = "download_parquet_from_s3"
    expected_task_dependencies = ["convert_parquet_to_csv"]
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_dependencies_convert_parquet_to_csv(dag):
    task = "convert_parquet_to_csv"
    expected_task_dependencies = ["convert_to_model"]
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_dependencies_convert_to_model(dag):
    task = "convert_to_model"
    expected_task_dependencies = ["create_table_if_not_exists"]
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_dependencies_create_table_if_not_exists(dag):
    task = "create_table_if_not_exists"
    expected_task_dependencies = ["insert_into_table"]
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_dependencies_insert_into_postgres(dag):
    task = "insert_into_table"
    expected_task_dependencies = []
    assert __get_downstream_task_ids(dag, task) == expected_task_dependencies


def test_is_parquet_file_available_task_configuration(dag):
    task = dag.get_task("is_parquet_file_available")
    assert task.aws_conn_id == "test_aws_conn_id"
    assert task.bucket_name == "test"
    assert task.bucket_key == "test-data.parquet"


def test_download_parquet_from_s3_task_configuration(dag):
    task = dag.get_task("download_parquet_from_s3")
    assert task.op_kwargs["aws_conn_id"] == "test_aws_conn_id"
    assert task.op_kwargs["bucket_name"] == "test"
    assert task.op_kwargs["bucket_key"] == "test-data.parquet"


def test_convert_parquet_to_csv_task_configuration(dag):
    task = dag.get_task("convert_parquet_to_csv")
    assert task.csv_file_path == "test-data.csv"


def test_convert_to_model_task_configuration(dag):
    task = dag.get_task("convert_to_model")
    assert task.csv_file_path == "test-data.csv"
    assert task.csv_cleaned_file_path == "test-data-cleaned.csv"
