import unittest
from airflow.models import DagBag

class TestDownloadParquetFromS3PushToPostgresDagValidation(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag(dag_folder='src/airflow_project/dags', include_examples=False)
        self.dag = self.dagbag.get_dag(dag_id='download_parquet_from_s3_push_to_postgres')

    def test_dag_schedule_interval(self):
        self.assertEqual(self.dag.schedule_interval, '@daily')

    def test_dag_retries(self):
        self.assertEqual(self.dag.default_args['retries'], 5)

    def test_dag_retry_delay(self):
        self.assertEqual(self.dag.default_args['retry_delay'].total_seconds(), 300)
    
    def test_dag_catchup(self):
        self.assertEqual(self.dag.default_args['catchup'], False)

    def test_dag_owner(self):
        self.assertEqual(self.dag.default_args['owner'], 'airflow')

    def test_number_of_tasks(self):
        self.assertEqual(len(self.dag.tasks), 1)

    def test_dependencies_insert_into_postgres_table(self):
        task = 'is_parquet_file_available'
        expected_task_dependencies = []
        self.assertEqual(self.__get_downstream_task_ids(task), expected_task_dependencies)

    def test_is_parquet_file_available_task_configuration(self):
        task = self.dag.get_task('is_parquet_file_available')
        self.assertEqual(task.aws_conn_id, 'aws_minio')
        self.assertEqual(task.bucket_name, 'data')
        self.assertEqual(task.bucket_key, 'user-data.parquet')

    def __get_downstream_task_ids(self, task_id):
        task = self.dag.get_task(task_id)
        return list(map(lambda task: task.task_id, task.downstream_list))        
