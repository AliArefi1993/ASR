import pika
import json
from app.config import RABBITMQ_HOST, TRANSLATION_QUEUE

def send_to_translation_queue(transcription_text):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=TRANSLATION_QUEUE)

    message = {
        "text": transcription_text  
    }
    
    channel.basic_publish(
        exchange="",
        routing_key=TRANSLATION_QUEUE,
        body=json.dumps(message) 
    )

    print("Sent transcription to translation queue:", transcription_text)

    connection.close()
