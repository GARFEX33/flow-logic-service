import asyncio
import json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
import structlog
from src.config.settings import BROKER_URL
from src.domain.models import Evento

logger = structlog.get_logger()

async def start_kafka_consumer():
    try:
        consumer = AIOKafkaConsumer(
            'event_topic',
            bootstrap_servers=BROKER_URL,
            group_id="flow-logic-group",
            auto_offset_reset="earliest"
        )
        await consumer.start()
        logger.info("Kafka consumer connected successfully")

        try:
            async for message in consumer:
                event_data = json.loads(message.value.decode('utf-8'))
                evento = Evento(**event_data)
                logger.info("Received event", event=event_data)
                # Process the event
        finally:
            await consumer.stop()
    except KafkaError as e:
        logger.error("Kafka connection error", error=str(e))

async def main():
    await start_kafka_consumer()

if __name__ == "__main__":
    asyncio.run(main())