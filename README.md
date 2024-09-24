# Airflow project

### Install dependencies
`poerty install`

### Command to run docker containers via docker compose
```AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> MINIO_ROOT_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) docker-compose up --detach```

Open `http://localhost:8080` Airflow webserver to check whether the dag is imported correctly.

