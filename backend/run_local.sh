echo "removing previous environment..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune --force


echo "build docker network 'dont-remember'"
docker network create dont-remember

ENV_FILE=local.env
echo ">> Starting Postgres Service..."
cd local_db_env || exit
docker-compose up -d
cd ..


echo ">> Starting users Service..."
cd ./users ||  exit
docker build -t users .
docker-compose build
docker-compose up -d
cd ..

echo ">> Starting words Service..."
cd ./words ||  exit
docker build -t words .
docker-compose build
docker-compose up -d
cd ..

echo "Done."


