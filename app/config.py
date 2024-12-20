
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")

ASR_QUEUE = "asr_task_queue"
TRANSLATION_QUEUE = "translation_task_queue"
RESPONSE_QUEUE = "response_queue"

AUDIO_TEMP_PATH="app/"
MODEL_PATH="/app/app/models/"
MODEL_NAME="vosk-model-en-us-0.22-lgraph"
