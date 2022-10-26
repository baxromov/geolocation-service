from fastapi import FastAPI
import logging
import psycopg2

app = FastAPI()
from config.settings import DATABASE, get_settings
from models.geolocation import LocationModelProducer

log = logging.getLogger("uvicorn")
connection = psycopg2.connect(
    database=DATABASE.get('db').get('database'),
    user=DATABASE.get('db').get('username'),
    password=DATABASE.get('db').get('password'),
    host=DATABASE.get('db').get('host'),
    port=DATABASE.get('db').get('port')
)


@app.get('/')
async def root(skip: int = 0, limit: int = 10):
    query = f"select * from geolocation limit {limit} offset {skip}"
    cursor = connection.cursor()
    cursor.execute(query)
    data = [dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()]
    return {
        "skip": skip,
        "limit": limit,
        'results': data
    }
