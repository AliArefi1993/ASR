import os
from app.services.asr_service import ASRService
from app.config import AUDIO_TEMP_PATH, MODEL_PATH
from app.send_task_queue import send_to_translation_queue
asr_service = ASRService(model_path=MODEL_PATH)

def process_audio(audio_data):
    """
    This function receives the audio data, saves it temporarily, and processes it with the ASR service.
    """
    try:
        file_path = os.path.join(AUDIO_TEMP_PATH, "audio.wav")
        
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        transcription = asr_service.transcribe_audio(file_path)
        print(f"Transcription: {transcription}")
        transcription_text = asr_service.results.get('transcription')
        send_to_translation_queue(transcription_text)
        
    except Exception as e:
        print(f"Error processing audio: {e}")
