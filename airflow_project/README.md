# Airflow project

### Install dependencies
`poerty install`

### Minio connection setup
Add `aws_minio` connection with `AWS Access Key ID` as `minio username`, `AWS Secret Access Key` as `minio password`. And under `Extra` add `{ "host": "http://minio:9000"}`

### Run Unit tests
Start Poetry shell with `poetry shell`
From the root folder run `airflow db init && poetry run pytest`

### Command to run docker containers via docker compose
```AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> MINIO_ROOT_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) docker-compose up --detach```

Open `http://localhost:8080` Airflow webserver to check whether the dag is imported correctly.

