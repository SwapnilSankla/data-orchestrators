# Airflow project

## Local setup

### Setup Airflow home directory
- Change directory to airflow_project
- Run `export AIRFLOW_HOME=${pwd}`

### Install dependencies
`poerty install`

### Lint
- Change directory to airflow_project
- Run `pylint --fail-under=9 .`

### Run Unit tests
- Change directory to airflow_project
- Start Poetry shell with `poetry shell`
- From the root folder run `airflow db init && poetry run pytest`

### Command to run docker containers via docker compose
- Change directory to airflow_project
- Create empty folders `docker_compose_postgres_data` and `docker_compose_s3_data` 
- Run ```AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> MINIO_ROOT_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) docker-compose up --detach```
- Open `http://localhost:8080` Airflow webserver to check whether the dag is imported correctly.

### Minio connection setup
Add `aws_minio` connection with `AWS Access Key ID` as `minio username`, `AWS Secret Access Key` as `minio password`. And under `Extra` add `{ "host": "http://minio:9000"}`
