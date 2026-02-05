"""REST API for WANDA Voice Core (aiohttp)."""

from __future__ import annotations
import asyncio
import json
import time
from typing import Optional

from wanda_voice_core.config import VoiceCoreConfig
from wanda_voice_core.engine import WandaVoiceEngine
from wanda_voice_core.schemas import UtteranceRequest, ValidationError

try:
    from aiohttp import web
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False


class WandaAPI:
    """REST API server for WANDA Voice Core."""

    def __init__(self, engine: WandaVoiceEngine, config: Optional[VoiceCoreConfig] = None):
        self.engine = engine
        self.config = config or engine.config
        self._start_time = time.time()

    def create_app(self) -> web.Application:
        if not AIOHTTP_AVAILABLE:
            raise ImportError("aiohttp required: pip install aiohttp")

        app = web.Application()
        app.router.add_post("/v1/utterance", self.handle_utterance)
        app.router.add_get("/v1/health", self.handle_health)
        app.router.add_get("/v1/status", self.handle_status)
        app.router.add_get("/v1/stream", self.handle_stream)
        return app

    async def handle_utterance(self, request: web.Request) -> web.Response:
        """POST /v1/utterance - Process text utterance."""
        try:
            body = await request.json()
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)

        try:
            req = UtteranceRequest(
                text=body.get("text", ""),
                mode=body.get("mode", "text"),
                context=body.get("context"),
            )
            req.validate()
        except ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        result = await self.engine.process_text(
            req.text, skip_confirmation=True
        )

        return web.json_response({
            "final_text": result.improved_text or result.transcript,
            "response_text": result.response_text,
            "actions": [],
            "events_summary": [
                e.event_type for e in self.engine.event_bus.get_events_for_run(result.run_id or "")
            ],
            "run_id": result.run_id,
            "error": result.error,
        })

    async def handle_health(self, request: web.Request) -> web.Response:
        """GET /v1/health - Health check."""
        return web.json_response({
            "status": "ok",
            "uptime_s": round(time.time() - self._start_time, 1),
        })

    async def handle_status(self, request: web.Request) -> web.Response:
        """GET /v1/status - Current engine status."""
        provider_name = "none"
        provider_available = False
        if self.engine._primary_provider:
            provider_name = self.engine._primary_provider.name
            provider_available = self.engine._primary_provider.is_available()

        return web.json_response({
            "state": "running",
            "provider": {
                "name": provider_name,
                "available": provider_available,
            },
            "config_profile": self.config.get("profile", "gui"),
            "recent_events": [
                e.to_dict() for e in self.engine.event_bus.get_recent_events(10)
            ],
        })

    async def handle_stream(self, request: web.Request) -> web.StreamResponse:
        """GET /v1/stream - SSE for real-time events."""
        resp = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
        await resp.prepare(request)

        queue: asyncio.Queue = asyncio.Queue()

        def on_event(event):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass

        self.engine.event_bus.subscribe("*", on_event)

        try:
            while True:
                event = await asyncio.wait_for(queue.get(), timeout=30)
                data = json.dumps(event.to_dict(), ensure_ascii=False)
                await resp.write(f"data: {data}\n\n".encode())
        except (asyncio.TimeoutError, ConnectionResetError):
            pass
        finally:
            self.engine.event_bus.unsubscribe("*", on_event)

        return resp


def run_api(config: Optional[VoiceCoreConfig] = None) -> None:
    """Start the API server."""
    if not AIOHTTP_AVAILABLE:
        print("[API] aiohttp not installed. Install with: pip install aiohttp")
        return

    config = config or VoiceCoreConfig()
    engine = WandaVoiceEngine(config)

    # Auto-setup providers
    from wanda_voice_core.providers.gemini_cli import GeminiCLIProvider
    primary = GeminiCLIProvider(
        model=config.get("providers.gemini_model", "flash"),
        timeout=config.get("providers.gemini_timeout", 90),
    )
    engine.set_providers(primary)

    api = WandaAPI(engine, config)
    app = api.create_app()

    host = config.get("api.host", "127.0.0.1")
    port = config.get("api.port", 8370)
    print(f"[API] Starting on {host}:{port}")
    web.run_app(app, host=host, port=port, print=None)


if __name__ == "__main__":
    run_api()
