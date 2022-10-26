import json
import logging

import psycopg2
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from config.settings import DATABASE, get_settings
from models.geolocation import LocationModelProducer

log = logging.getLogger("uvicorn")


def create_consumer() -> AIOKafkaConsumer:
    print(get_settings().kafka_instance)
    return AIOKafkaConsumer(
        get_settings().kafka_topics,
        bootstrap_servers=get_settings().kafka_instance,
    )


app = FastAPI()
consumer = create_consumer()


async def consume():
    while True:
        async for msg in consumer:
            consume_data = json.loads(msg.value.decode())
            location_model = LocationModelProducer(**consume_data)
            connection = psycopg2.connect(
                database=DATABASE.get('db').get('database'),
                user=DATABASE.get('db').get('username'),
                password=DATABASE.get('db').get('password'),
                host=DATABASE.get('db').get('host'),
                port=DATABASE.get('db').get('port')
            )
            query = f"insert into geolocation (latitude, longitude, address, guid) " \
                    f"values ({location_model.latitude}, {location_model.longitude}, '{location_model.address}', '{location_model.guid}')"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()


@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""

    log.info("Starting up...")
    await consumer.start()
    await consume()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for FastAPI application."""

    log.info("Shutting down...")
    await consumer.stop()
