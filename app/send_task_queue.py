from config import TRANSLATION_QUEUE
import asyncio
import logging


logger = logging.getLogger(__name__)

async def send_to_translation(broker, message):
    try:
        await broker.publish(
            message=message,
            routing_key=TRANSLATION_QUEUE
        )
        logger.info("Message published successfully.")
    except asyncio.CancelledError:
        logger.error("Publish task was cancelled.")
        raise 
    except Exception as e:
        logger.error(f"An error occurred while publishing: {e}")
