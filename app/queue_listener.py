from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import RabbitMessage
from faststream import FastStream
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
    import json
    print("Received new audio data for ASR processing.")
    body = message.body
    message_data = json.loads(body)
    audio_data = message_data.get("audio_data").encode('latin1') 
    chain = message_data.get("chain")
    request_id = message_data.get("request_id")
    transcription_text = process_audio(audio_data)

    message = {"text": transcription_text, "chain": chain, "request_id": request_id}
    print(f"transcription text is : {transcription_text}")
    await send_to_translation(broker, message)
    print("Sent Transcrip to translation service.")

async def send_to_translation(broker, message):
    try:
        await broker.publish(
            message=message,
            routing_key=TRANSLATION_QUEUE
        )
        print("Message published successfully.")
    except asyncio.CancelledError:
        print("Publish task was cancelled.")
        raise 
    except Exception as e:
        print(f"An error occurred while publishing: {e}")

# Main entry point: Run FastStream app asynchronously
async def main():
    await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Run the async main function
