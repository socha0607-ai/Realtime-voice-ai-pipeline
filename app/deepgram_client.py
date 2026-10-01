import json
import os
import asyncio
from typing import AsyncGenerator
import websockets
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
DEEPGRAM_WS_URL = (
    "wss://api.deepgram.com/v1/listen"
    "?model=nova-2"
    "&encoding=linear16"
    "&sample_rate=16000"
    "&channels=1"
    "&interim_results=true"
    "&punctuate=true"
)


class DeepgramLiveClient:
    def __init__(self, api_key: str = DEEPGRAM_API_KEY):
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is not set.")
        self.api_key = api_key
        self.headers = {"Authorization": f"Token {self.api_key}"}

    async def stream_audio_and_receive(
        self, audio_queue: asyncio.Queue
    ) -> AsyncGenerator[str, None]:
        """
        Connects to Deepgram's WebSocket API.
        Reads audio chunks from `audio_queue`, streams them to Deepgram,
        and yields real-time transcription results.
        """
        async with websockets.connect(
            DEEPGRAM_WS_URL, extra_headers=self.headers
        ) as dg_ws:

            async def sender():
                """Task to read audio chunks from the client queue and send to Deepgram."""
                try:
                    while True:
                        chunk = await audio_queue.get()
                        if chunk is None:  # Sentinel value signaling end of stream
                            # Send empty byte buffer to indicate stream end to Deepgram
                            await dg_ws.send(json.dumps({"type": "CloseStream"}))
                            break
                        await dg_ws.send(chunk)
                        audio_queue.task_done()
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"[Deepgram Sender Error]: {e}")

            # Spawn the sender task in background
            sender_task = asyncio.create_task(sender())

            try:
                async for message in dg_ws:
                    data = json.loads(message)
                    # Parse transcription payload from Deepgram response
                    channel = data.get("channel", {})
                    alternatives = channel.get("alternatives", [])
                    if alternatives:
                        transcript = alternatives[0].get("transcript", "")
                        is_final = data.get("is_final", False)
                        if transcript.strip():
                            yield json.dumps(
                                {"transcript": transcript, "is_final": is_final}
                            )
            except websockets.exceptions.ConnectionClosed:
                print("[Deepgram WS Connection Closed]")
            finally:
                sender_task.cancel()
                await asyncio.gather(sender_task, return_exceptions=True)
