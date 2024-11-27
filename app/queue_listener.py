from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import RabbitMessage
from faststream import FastStream
from asr_handler import process_audio
from config import RABBITMQ_HOST, ASR_QUEUE,  RABBITMQ_USER, RABBITMQ_PASSWORD
from send_task_queue import send_to_translation
import asyncio
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize FastStream broker
broker = RabbitBroker(url=f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}")
app = FastStream(broker)

@broker.subscriber(ASR_QUEUE)
async def process_audio_message(message: RabbitMessage):
    """
    Process audio data received from the ASR queue.
    """
    import json
    logger.info("Received new audio data for ASR processing.")
    body = message.body
    message_data = json.loads(body)
    audio_data = message_data.get("audio_data").encode('latin1') 
    chain = message_data.get("chain")
    request_id = message_data.get("request_id")
    transcription_text = process_audio(audio_data)

    message = {"text": transcription_text, "chain": chain, "request_id": request_id}
    logger.info(f"transcription text is : {transcription_text}")
    await send_to_translation(broker, message)
    logger.info("Sent Transcrip to translation service.")

# Main entry point: Run FastStream app asynchronously
async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function
