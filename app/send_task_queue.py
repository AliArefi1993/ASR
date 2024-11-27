from config import TRANSLATION_QUEUE
import asyncio


async def send_to_translation(broker, message):
    max_retries=10
    for attempt in range(1, max_retries + 1):
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
            if attempt < max_retries:
                await asyncio.sleep(delay)
                delay *= 2  
            else:
                print(f"Max retries reached ({max_retries}). Failed to send the message.")
                raise 