# Airflow mini project

## Problem statement

When file on S3 bucket is uploaded we need to fetch the file do some post processing and store into the Postgres Db.

## Description

CSV file format on S3:
First name, last name, Age
John, Doe, 30
Arun, Sen, 35

Postgres table schema:
id   integer
name varchar
age  integer

Python processing:
Need to combine first name and last name before putting it into the db

## Tech details

- Command for running docker compose locally
  ```AIRFLOW_PASSWORD=<> POSTGRES_PASSWORD=<> MINIO_ROOT_PASSWORD=<> UID=$(id -u) GID=$(id -g) AIRFLOW_UID=$(id -u) docker-compose up --detach```
- For generating user-data.parquet go to utils and run `python3 CSVToPaquetConverter.py`. Then manually upload it to Minio
- Create Postgres connection and minio connection from Airflow connections tab (For minio select Amazon web services as connection type)