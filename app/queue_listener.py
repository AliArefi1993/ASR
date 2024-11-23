from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import RabbitMessage
from faststream import FastStream
from asr_handler import send_to_translation_queue
from config import RABBITMQ_HOST, ASR_QUEUE, TRANSLATION_QUEUE

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
    await send_to_translation_queue(body)  # Ensure `process_audio` supports async if necessary
    print("Audio processing completed.")

@broker.publisher(TRANSLATION_QUEUE)
async def send_to_translation_queue(publish, transcription_text: str):
    """
    Publish transcription to the translation queue.
    """
    message = {"text": transcription_text}
    await publish(message)
    print(f"Sent transcription to translation queue: {transcription_text}")

# Main entry point: Run FastStream app asynchronously
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Run the async main function
