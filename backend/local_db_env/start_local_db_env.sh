echo "> init db"
docker network create dont-remember
docker-compose down
docker-compose build
docker-compose up -d

sleep 5

echo "> insert init data"
python3 ./init_data.py
echo "> URI: postgresql://dont-remember-user:dont-remember-pwd@localhost:5432/dont_remember"