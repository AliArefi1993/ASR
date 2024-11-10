from fastapi import APIRouter, UploadFile, BackgroundTasks, HTTPException
from fastapi import FastAPI, UploadFile, File
from app.services.asr_service import ASRService

router = APIRouter()
asr_service = ASRService(model_path="app/models/vosk-model-en-us-0.22-lgraph")

@router.post("/asr/")
async def asr_endpoint(file: UploadFile, background_tasks: BackgroundTasks):
    file_path = f"app/temp/{file.filename}"
    with open(file_path, "wb") as temp_file:
        temp_file.write(await file.read())
    asr_service.reset_results()
    background_tasks.add_task(asr_service.transcribe_audio, file_path)

    return {"status": "Processing started"}

@router.get("/asr_result/")
async def get_transcription_result():
    result = asr_service.get_transcription_status()
    if result["status"] == "completed":
        return {"status": "completed", "transcription": result["transcription"]}
    elif result["status"] == "pending":
        return {"status": "processing"}
    else:
        raise HTTPException(status_code=500, detail="Unknown error occurred")
