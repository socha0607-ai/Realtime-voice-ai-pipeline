# Real-Time Voice AI Pipeline & Audio Streaming Server

A low-latency, full-duplex audio streaming pipeline built using **Python, FastAPI, Asyncio, and WebSockets**, integrated with **Deepgram Nova-2 API** for real-time speech-to-text (STT) transcription.

## Features
- **Full-Duplex Streaming:** Asynchronous WebSocket server capable of processing raw audio streams (PCM/WAV).
- **Sub-250ms Latency:** High-throughput streaming leveraging Python's `asyncio` event loop.
- **Deepgram Nova-2 Integration:** Real-time speech recognition via live transcription callbacks.
- **Backpressure & Resiliency:** Robust handling of incoming chunk buffers and network variations.
- **Dockerized Deployment:** Fully containerized setup with dynamic health checks.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI, Uvicorn
- **Concurrency:** Asyncio, WebSockets
- **Speech API:** Deepgram Nova-2 (STT)
- **Containerization:** Docker

## Repository Structure

realtime-voice-ai-pipeline/
├── app/
│   ├── init.py
│   ├── main.py
│   ├── websocket_handler.py
│   └── deepgram_client.py
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
├── commands.md
└── README.md


## Quick Start

### Prerequisites
- Docker or Python 3.11+
- Deepgram API Key ([Get one here](https://console.deepgram.com/))

### Environment Setup
Create a `.env` file in the root directory:
```env
DEEPGRAM_API_KEY=your_deepgram_api_key_here
HOST=0.0.0.0
PORT=8000


Run Locally (Python)
Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Run with Docker
Bash

docker build -t realtime-voice-ai-pipeline .
docker run -d -p 8000:8000 --env-file .env --name voice-pipeline realtime-voice-ai-pipeline

Resumé Highlights

    Built an asynchronous, full-duplex WebSocket server using FastAPI & Asyncio to stream raw PCM/WAV audio chunks with end-to-end latency under 250ms.

    Integrated Deepgram Nova-2 API for real-time speech recognition, handling dynamic chunk buffering and live transcription callbacks.

    Optimized network throughput by implementing backpressure handling and audio packet re-sequencing over WebSockets.

    Containerized the service with Docker and configured automated health checks, reducing deployment friction and service restarts.

License

MIT License
