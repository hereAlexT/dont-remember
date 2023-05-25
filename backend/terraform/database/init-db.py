import json
import psycopg2
import sys

db_host = sys.argv[1]
db_name = sys.argv[2]
db_user = sys.argv[3]
db_password = sys.argv[4]

# extract the last four digit after ':' of db_host as the db_host
db_host = db_host.split(":")[0]

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    dbname=db_name,
    user=db_user,
    password=db_password
)

with conn.cursor() as cursor:
    with open("./database/init-db.sql", "r") as f:
        cursor.execute(f.read())
    conn.commit()
