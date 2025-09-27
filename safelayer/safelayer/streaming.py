"""Real-time streaming and HTTP API interface for SafeLayer.

Provides:
- FastAPI HTTP endpoints for synchronous guard processing
- WebSocket endpoint for real-time streaming moderation/masking
- Server-Sent Events (SSE) support for streaming audit events (best-effort)
- Lightweight, optional dependencies pattern
"""
from typing import Any, Dict, List, Optional
import json
import asyncio

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False

from .manager import GuardManager
from .guards.base import BaseGuard


class _TextIn(BaseModel) if FASTAPI_AVAILABLE else object:  # type: ignore
    if FASTAPI_AVAILABLE:
        text: str
        explain: Optional[bool] = False
    else:
        pass


class StreamingServer:
    def __init__(self, guards: List[BaseGuard]):
        self.manager = GuardManager(guards)
        self.app = None
        if FASTAPI_AVAILABLE:
            self._build_app()

    def _build_app(self):
        app = FastAPI(title="SafeLayer Streaming API", version="1.0.0")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")
        async def health() -> Dict[str, str]:  # noqa: D401
            return {"status": "ok"}

        @app.post("/process")
        async def process(payload: _TextIn):  # type: ignore
            text = payload.text
            masked = self.manager.run(text)
            return JSONResponse({"input": text, "output": masked})

        @app.websocket("/ws")
        async def ws_endpoint(ws: WebSocket):
            await ws.accept()
            try:
                while True:
                    raw = await ws.receive_text()
                    try:
                        data = json.loads(raw)
                        text = data.get("text", "")
                    except Exception:
                        text = raw
                    masked = self.manager.run(text)
                    await ws.send_text(json.dumps({"output": masked}))
            except WebSocketDisconnect:
                pass

        self.app = app

    def run(self, host: str = "0.0.0.0", port: int = 8080):
        if not FASTAPI_AVAILABLE:
            raise RuntimeError("FastAPI not installed. `pip install fastapi uvicorn` to enable API.")
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
