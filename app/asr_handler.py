import os
from app.services.asr_service import ASRService
from app.config import AUDIO_TEMP_PATH

# Assuming your ASRService is already implemented
asr_service = ASRService(model_path="app/models/vosk-model-en-us-0.22-lgraph")

def process_audio(audio_data):
    """
    This function receives the audio data, saves it temporarily, and processes it with the ASR service.
    """
    try:
        # Save the incoming audio data to a temporary file
        file_path = os.path.join(AUDIO_TEMP_PATH, "audio.wav")  # Use a constant name since only one request at a time
        
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        transcription = asr_service.transcribe_audio(file_path)
        
        # Send the transcription to a result queue or store it as needed
        print(f"Transcription: {transcription}")
        print(f"asr_service.results after: {asr_service.results}")
        
        # Here you would send the transcription back to a translation service or return it
        # For example, you could call a function to push the result to a translation queue or return the result.

    except Exception as e:
        print(f"Error processing audio: {e}")
        # You can log this error or handle it as needed
