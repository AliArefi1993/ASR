
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

ASR_QUEUE = "asr_task_queue"
TRANSLATION_QUEUE = "translation_task_queue"
RESPONSE_QUEUE = "response_queue"

AUDIO_TEMP_PATH="app/temp/"
MODEL_PATH="app/models/vosk-model-en-us-0.22-lgraph"