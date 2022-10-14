import logging
import psycopg2
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from config import get_settings

log = logging.getLogger("uvicorn")

connection = psycopg2.connect()


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
            print(
                "consumed: ",
                f"topic: {msg.topic},",
                f"partition: {msg.partition},",
                f"offset: {msg.offset},",
                f"key: {msg.key},",
                f"timestamp: {msg.timestamp}",
            )


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

