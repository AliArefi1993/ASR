import os
from services.asr_service import ASRService
from config import AUDIO_TEMP_PATH, MODEL_PATH
asr_service = ASRService(model_path=MODEL_PATH)
import logging


logger = logging.getLogger(__name__)


def process_audio(audio_data):
    """
    This function receives the audio data, saves it temporarily, and processes it with the ASR service.
    """
    try:
        file_path = os.path.join(AUDIO_TEMP_PATH, "audio.wav")
        
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        asr_service.transcribe_audio(file_path)
        transcription_text = asr_service.results.get('transcription')

        return transcription_text
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
