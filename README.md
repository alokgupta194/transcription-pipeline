
# Transcription Pipeline

A Python-based audio transcription tool that converts audio files into text with timestamps for each speech segment. Built using [faster-whisper](https://github.com/SYSTRAN/faster-whisper), FFmpeg, and FastAPI.

## Features

- Supports MP3, WAV, M4A, OGG, FLAC, MP4, and AAC.
- Converts speech to text with segment-level timestamps.
- Automatically detects the spoken language.
- Uses Voice Activity Detection (VAD) to handle silence in long recordings.
- Provides CLI and REST API interfaces.
- Supports asynchronous transcription jobs.
- Runs locally after the initial model download.

## Tech Stack

- Python
- faster-whisper
- FFmpeg
- FastAPI
- Uvicorn

## Architecture

```text
Audio Upload
     |
     v
FFmpeg Preprocessing
     |
     v
faster-whisper Transcription
     |
     v
Text and Timestamp Processing
     |
     v
Structured JSON Output
```

## Installation

### 1. Install FFmpeg

**Windows:** Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add its `bin` directory to your system PATH.

**macOS:**

```bash
brew install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
```

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/transcription-pipeline.git
cd transcription-pipeline
```

### 3. Set Up the Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### CLI

Check the available commands:

```bash
python transcribe.py --help
```

### REST API

Start the server:

```bash
uvicorn app:app --reload --port 8000
```

Upload an audio file:

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@sample.mp3"
```

Example response:

```json
{
  "job_id": "abc-123",
  "status": "queued"
}
```

Retrieve the transcription result:

```bash
curl "http://localhost:8000/jobs/abc-123"
```

Interactive API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Example Output

```json
{
  "text": "Hi, this is AJ with another effortless English podcast.",
  "language": "en",
  "duration": 480,
  "segments": [
    {
      "start": 2.26,
      "end": 8.38,
      "text": "Hi, this is AJ with another effortless English podcast."
    },
    {
      "start": 8.38,
      "end": 13.06,
      "text": "So today is Monday and I'm here in San Francisco."
    }
  ],
  "status": "completed",
  "model": "faster-whisper-base"
}
```

## Performance and Testing

Tested with an 8-minute English audio recording on a CPU-only Windows machine.

| Metric | Result |
|---|---|
| Audio duration | 8 minutes |
| Model | faster-whisper base |
| CPU | 4 cores, 2.30 GHz |
| RAM | 8 GB |
| GPU | None |
| Output | Text with segment timestamps |

## Project Structure

```text
transcription-pipeline/
├── transcribe.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample.mp3
```

## License

No license has been added yet.

---

Built with Python, faster-whisper, FFmpeg, and FastAPI.
