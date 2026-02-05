"""Run artifact manager for WANDA Voice Core."""

from __future__ import annotations
import json
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from wanda_voice_core.schemas import RunEvent


class RunManager:
    """Manages run artifacts: events, summaries, audio files."""

    def __init__(self, runs_dir: Optional[Path] = None):
        if runs_dir is None:
            runs_dir = Path.home() / ".wanda" / "voice_runs"
        self.runs_dir = runs_dir
        self._current_run: Optional[str] = None
        self._run_start: float = 0.0
        self._events: list[dict[str, Any]] = []

    def start_run(self) -> str:
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        self._current_run = run_id
        self._run_start = time.time()
        self._events = []
        return run_id

    @property
    def current_run(self) -> Optional[str]:
        return self._current_run

    def log_event(self, event: RunEvent) -> None:
        if not self._current_run:
            return
        entry = event.to_dict()
        self._events.append(entry)
        events_file = self.runs_dir / self._current_run / "events.jsonl"
        try:
            with open(events_file, "a") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def save_artifact(self, name: str, data: Any) -> Optional[Path]:
        if not self._current_run:
            return None
        artifact_path = self.runs_dir / self._current_run / name
        try:
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(data, (dict, list)):
                with open(artifact_path, "w") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif isinstance(data, bytes):
                with open(artifact_path, "wb") as f:
                    f.write(data)
            else:
                with open(artifact_path, "w") as f:
                    f.write(str(data))
            return artifact_path
        except OSError:
            return None

    def save_audio(
        self, audio_data: bytes, filename: str = "audio.wav"
    ) -> Optional[Path]:
        return self.save_artifact(filename, audio_data)

    def end_run(self, summary: Optional[dict[str, Any]] = None) -> None:
        if not self._current_run:
            return
        duration = time.time() - self._run_start
        summary_data = {
            "run_id": self._current_run,
            "duration_s": round(duration, 2),
            "event_count": len(self._events),
            "started_at": self._run_start,
            **(summary or {}),
        }
        summary_path = self.runs_dir / self._current_run / "summary.json"
        try:
            with open(summary_path, "w") as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass
        self._current_run = None
        self._events = []

    def cleanup_old_runs(self, max_runs: int = 50) -> None:
        """Remove oldest runs if over limit."""
        if not self.runs_dir.exists():
            return
        runs = sorted(self.runs_dir.iterdir(), key=lambda p: p.stat().st_mtime)
        while len(runs) > max_runs:
            oldest = runs.pop(0)
            try:
                import shutil

                shutil.rmtree(oldest)
            except OSError:
                pass
