"""
Transcription API
POST /transcribe → upload audio, get job_id
GET  /jobs/{id}  → get transcription result
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from transcribe import run_pipeline
import uuid
import os
import shutil

app = FastAPI(
    title="Transcription Pipeline",
    description="Audio → text with timestamps per segment",
    version="1.0.0"
)

jobs = {}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED = (".mp3", ".wav", ".m4a", ".mp4", ".ogg", ".flac", ".aac")


def process_job(job_id: str, file_path: str):
    try:
        jobs[job_id] = {"status": "processing"}
        result = run_pipeline(file_path)
        result["job_id"] = job_id
        jobs[job_id] = result
    except Exception as e:
        jobs[job_id] = {"status": "failed", "error": str(e)}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/transcribe")
async def transcribe_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Audio file upload karo, job_id milega"""
    if not file.filename:
        raise HTTPException(400, "No file provided")

    if not file.filename.lower().endswith(ALLOWED):
        raise HTTPException(
            400,
            f"Unsupported format. Allowed: {', '.join(ALLOWED)}"
        )

    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    jobs[job_id] = {"status": "queued"}
    background_tasks.add_task(process_job, job_id, file_path)

    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Job ka status aur result lo"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return jobs[job_id]


@app.get("/health")
async def health():
    return {"status": "ok"}