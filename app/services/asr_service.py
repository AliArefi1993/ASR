from vosk import Model, KaldiRecognizer
import wave
import json
import os

class ASRService:
    def __init__(self, model_path: str):
        self.model = Model(model_path)
        self.results = {"status": "pending", "transcription": None}

    def transcribe_audio(self, file_path: str):
        try:
            with wave.open(file_path, "rb") as wf:
                
                recognizer = KaldiRecognizer(self.model, wf.getframerate())
                transcription = ""

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        transcription += result.get("text", "")
                
                final_result = json.loads(recognizer.FinalResult())
                transcription += final_result.get("text", "")

            self.results["status"] = "completed"
            self.results["transcription"] = transcription
        finally:
            os.remove(file_path)

    def reset_results(self):
        self.results = {"status": "pending", "transcription": None}

    def get_transcription_status(self):
        return self.results
