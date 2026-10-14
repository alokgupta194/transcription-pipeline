"""
Transcription Pipeline
Audio file → text with timestamps per segment

Flow:
  1. Preprocess (ffmpeg → 16kHz mono WAV)
  2. Transcribe (faster-whisper)
  3. Post-process (clean text)
  4. Return JSON with timestamps
"""

import subprocess
import tempfile
import json
import sys
import uuid
from datetime import datetime
from faster_whisper import WhisperModel


# Model ek baar load karo (startup pe)
print("Loading model...")
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=4)
print("Model ready ✅\n")


def preprocess(audio_path: str) -> str:
    """
    Kisi bhi audio format ko 16kHz mono WAV me convert karo.
    Supports: MP3, WAV, M4A, OGG, FLAC, MP4, AAC, etc.
    """
    wav_path = tempfile.mktemp(suffix=".wav")
    cmd = [
        "ffmpeg", "-y",
        "-i", audio_path,
        "-ac", "1",           # mono
        "-ar", "16000",       # 16kHz
        "-c:a", "pcm_s16le",  # WAV codec
        wav_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return wav_path


def transcribe(wav_path: str) -> dict:
    """
    Audio → text with timestamps per segment.
    vad_filter=True handles long audio by skipping silence.
    """
    segments, info = model.transcribe(
        wav_path,
        beam_size=1,
        vad_filter=True,
        word_timestamps=False
    )

    seg_list = []
    texts = []

    for seg in segments:
        seg_list.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        })
        texts.append(seg.text.strip())

    return {
        "text": " ".join(texts),
        "language": info.language,
        "duration": round(info.duration, 2),
        "segments": seg_list
    }


def run_pipeline(audio_path: str) -> dict:
    """Poora transcription flow"""
    print(f"1. Preprocessing: {audio_path}")
    wav = preprocess(audio_path)

    print("2. Transcribing...")
    result = transcribe(wav)

    print("3. Cleaning text")
    result["text"] = " ".join(result["text"].split())

    result.update({
        "job_id": str(uuid.uuid4()),
        "status": "completed",
        "model": "faster-whisper-base",
        "created_at": datetime.utcnow().isoformat()
    })

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file>")
        sys.exit(1)

    result = run_pipeline(sys.argv[1])
    print("\n--- RESULT ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))