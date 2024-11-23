from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import RabbitMessage
from faststream import FastStream
import json
from config import RABBITMQ_HOST, TRANSLATION_QUEUE


broker = RabbitBroker(url=f"amqp://{RABBITMQ_HOST}")
app = FastStream(broker)

@broker.publisher(TRANSLATION_QUEUE)
async def send_to_translation_queue(publish, transcription_text: str):
    """
    Publish transcription to the translation queue.
    """
    message = {"text": transcription_text}
    await publish(message)  # FastStream handles message sending

    print("Sent transcription to translation queue:", transcription_text)

if __name__ == "__main__":
    app.run()
