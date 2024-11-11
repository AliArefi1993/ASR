import pika
import json
from app.asr_handler import process_audio
from app.config import RABBITMQ_HOST, ASR_QUEUE, TRANSLATION_QUEUE

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

def listen_for_audio_tasks():
    """
    This function listens to the ASR queue and processes audio when a new task is added.
    """
    # Set up connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the ASR queue (make sure it exists)
    channel.queue_declare(queue=ASR_QUEUE)

    def callback(ch, method, properties, body):
        """
        This callback is triggered whenever a new message is received in the queue.
        """
        print("Received new audio data for ASR processing.")
        
        # Process the audio data (no need for request ID anymore)
        process_audio(body)

        # Acknowledge the message to remove it from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up the consumer (message listener)
    channel.basic_consume(queue=ASR_QUEUE, on_message_callback=callback)

    # Start listening for messages
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    listen_for_audio_tasks()
