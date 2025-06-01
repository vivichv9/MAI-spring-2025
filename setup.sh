docker compose up -d

docker exec -it superset_app superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@superset.com \
  --password admin

docker exec -it superset_app superset db upgrade
docker exec -it superset_app superset init