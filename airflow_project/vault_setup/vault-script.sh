# Exec into vault container and execute the below commands

vault login # Login to vault with root token

vault auth enable approle #Enables approle auth method

# Create airflow_policy to allow read and list access to secret/* path
vault policy write airflow_policy - <<EOF
 path "airflow/*" {
 capabilities = ["read", "list"]
 }
EOF

#Create a role named airflow_role with policies as airflow_policy
vault write auth/approle/role/airflow_role \
  role_id=airflow_role \
  secret_id_ttl=0 \
  secret_id_num_uses=0 \
  token_num_uses=0 \
  token_ttl=24h \
  token_max_ttl=24h \
  token_policies=airflow_policy

#Run the below command to get the secret_id. Use it while configuring the airflow connection
vault write -f auth/approle/role/airflow_role/secret-id

#Run the below command to enable the kv secrets engine at airflow path
vault secrets enable -path=airflow -version=2 kv

#Run the below command to write the minio connection uri to vault
vault kv put -mount=airflow connections/aws_minio @aws_minio.json

# Run the below command to write the postgres connection uri to vault
vault kv put -mount=airflow connections/postgres_localhost conn_uri="postgresql://airflow:<POSTGRES_PASSWORD>@db:5432/airflow"
