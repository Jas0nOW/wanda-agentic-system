"""
WANDA Local Voice Gateway - Main Entry Point
=============================================
This is the local service that handles Voice Input -> Processing -> CLI Injection.
"""

import asyncio
import sys
from pathlib import Path

# Local modules
from src.vad import SileroVAD
from src.stt import FasterWhisperSTT
from src.gateway import OllamaGateway
from src.tts import TTSEngine
from src.safety import SafetyChecker
from src.cli_injector import CLIInjector


class WandaLocalGateway:
    """The main orchestrator for the local voice pipeline."""

    def __init__(self, config_path: Path = None):
        self.vad = SileroVAD(latency_target_ms=200)
        self.stt = FasterWhisperSTT(model="large-v3-turbo", device="cuda")
        self.gateway = OllamaGateway(model="brainstorm-36b")
        self.tts = TTSEngine(profile="premium")  # XTTS-v2
        self.safety = SafetyChecker()
        self.cli = CLIInjector()

    async def run_pipeline(self, audio_bytes: bytes) -> str:
        """
        The core pipeline: Audio -> Text -> Refined Prompt -> Execution.
        """
        # 1. STT: Convert audio to text
        transcript = await self.stt.transcribe(audio_bytes)
        print(f"[STT] Transcript: {transcript}")

        # 2. Gateway: Refine prompt and get routing info
        gateway_response = await self.gateway.process(transcript)
        print(f"[Gateway] Response: {gateway_response}")

        # 3. Safety Check
        if gateway_response.get("safety_flag"):
            confirmation = await self._request_confirmation(
                gateway_response["confirmation_message"]
            )
            if not confirmation:
                return "Cancelled by user."

        # 4. Inject into CLI
        result = await self.cli.inject(
            target=gateway_response["target_cli"],
            prompt=gateway_response["refined_prompt"],
            agent=gateway_response["target_agent"],
        )

        # 5. Summarize and report via TTS
        summary = f"Done. {result.get('summary', 'Task completed.')}"
        await self.tts.speak(summary)

        return result

    async def _request_confirmation(self, message: str) -> bool:
        """
        Ask user for confirmation via TTS and wait for input.
        [ENTER] send | [e] edit | [c] cancel
        """
        await self.tts.speak(f"Warning: {message}. Press Enter to confirm or C to cancel.")
        user_input = input("[ENTER] Confirm | [c] Cancel: ")
        return user_input.lower() != "c"

    async def listen_loop(self):
        """
        Main listen loop: Continuously listen for voice input.
        """
        print("[WANDA] Voice Gateway Active. Say 'Hey Wanda' or press Enter to start.")
        while True:
            # Wait for VAD to detect speech
            audio_bytes = await self.vad.listen()
            if audio_bytes:
                await self.run_pipeline(audio_bytes)


async def main():
    gateway = WandaLocalGateway()
    await gateway.listen_loop()


if __name__ == "__main__":
    asyncio.run(main())
