from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import RabbitMessage
from faststream import FastStream
from services.asr_service import ASRService
from asr_handler import process_audio
from config import RABBITMQ_HOST, ASR_QUEUE, TRANSLATION_QUEUE, MODEL_PATH

# Initialize FastStream broker
broker = RabbitBroker(url=f"amqp://{RABBITMQ_HOST}")
app = FastStream(broker)

@broker.subscriber(ASR_QUEUE)
async def process_audio_message(message: RabbitMessage):
    """
    Process audio data received from the ASR queue.
    """
    print("Received new audio data for ASR processing.")
    body = message.body
    transcription_text = process_audio(body)

    message = {"text": transcription_text}
    await send_to_translation(message)
    print("Sent Transcrip to translation service.")

async def send_to_translation(message):
    broker.connect()
    await broker.publish(
        message=message,
        routing_key=TRANSLATION_QUEUE
    )

# Main entry point: Run FastStream app asynchronously
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Run the async main function
