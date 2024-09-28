# Airflow project

## Local setup

### Setup Airflow home directory
- Change directory to airflow_project
- Run `export AIRFLOW_HOME=${pwd}`

### Run tests
- Change directory to airflow_project
- Run `poetry run tox`

### Command to run docker containers via docker compose
- Change directory to airflow_project
- Create empty folders `docker_compose_postgres_data` and `docker_compose_s3_data` 
- Run ```VAULT_DEV_ROOT_TOKEN_ID=<> AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) MINIO_ROOT_PASSWORD=<> docker-compose up --detach```
- Follow the commands mentioned in vault-script.sh to set up Vault. Copy the secret_id from the config and rerun docker-compose up command with the secret_id as an environment variable. ```VAULT_SECRET_ID=<> VAULT_DEV_ROOT_TOKEN_ID=<> AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) MINIO_ROOT_PASSWORD=<> docker-compose up --detach```
- Open `http://localhost:8080` Airflow webserver to check whether the dag is imported correctly.

### Minio setup
- Login to minio using `http://localhost:9001` with username as minio and password mentioned as `MINIO_ROOT_PASSWORD` while running docker compose
- Upload the file `sample_data/user-data.parquet` to the bucket
