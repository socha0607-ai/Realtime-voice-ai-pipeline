import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from app.deepgram_client import DeepgramLiveClient

app = FastAPI(
    title="Real-Time Voice AI Pipeline",
    description="Low-latency live speech-to-text server using FastAPI & Deepgram Nova-2",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint used by Docker container health check."""
    return JSONResponse(status_code=200, content={"status": "healthy"})


@app.websocket("/ws/listen")
async def websocket_audio_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time full-duplex audio streaming.
    Receives raw PCM/WAV binary audio chunks from the client, passes them
    to Deepgram, and streams transcribed text back in real-time.
    """
    await websocket.accept()

    audio_queue: asyncio.Queue = asyncio.Queue(maxsize=100)  # Backpressure queue
    dg_client = DeepgramLiveClient()

    async def receive_audio_from_client():
        """Reads incoming audio chunks over WebSocket from the client."""
        try:
            while True:
                # Expecting raw binary audio frames (PCM 16-bit, 16kHz)
                message = await websocket.receive()
                if "bytes" in message and message["bytes"]:
                    # Put audio into queue; backpressure handled by maxsize
                    await audio_queue.put(message["bytes"])
                elif "text" in message and message["text"] == "EOF":
                    await audio_queue.put(None)
                    break
        except WebSocketDisconnect:
            print("[Client Disconnected]")
            await audio_queue.put(None)
        except Exception as e:
            print(f"[Client Receiver Error]: {e}")
            await audio_queue.put(None)

    async def send_transcripts_to_client():
        """Streams live transcripts from Deepgram back to the connected client."""
        try:
            async for transcript_json in dg_client.stream_audio_and_receive(
                audio_queue
            ):
                await websocket.send_text(transcript_json)
        except Exception as e:
            print(f"[Transcript Forwarder Error]: {e}")

    # Run receiver and transcription forwarder concurrently
    try:
        await asyncio.gather(
            receive_audio_from_client(),
            send_transcripts_to_client(),
            return_exceptions=True,
        )
    finally:
        await websocket.close()
