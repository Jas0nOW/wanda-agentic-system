# Wanda Voice Assistant - Autonomous Mode
"""Vollautomatischer Mode - Wanda arbeitet selbstständig."""

import threading
import time
import queue
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AutonomousTask:
    """A task in autonomous mode."""
    id: str
    description: str
    tool: str  # gemini, opencode, claude
    prompt: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    subtasks: List['AutonomousTask'] = None
    
    def __post_init__(self):
        if self.subtasks is None:
            self.subtasks = []


class AutonomousController:
    """
    Controls fully autonomous operation.
    - Breaks down tasks
    - Delegates to CLI tools
    - Monitors progress
    - Provides updates
    """
    
    def __init__(
        self,
        cli_proxy,  # CLIProxy instance
        ollama=None,  # OllamaAdapter for planning
        on_progress: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None
    ):
        self.cli_proxy = cli_proxy
        self.ollama = ollama
        self.on_progress = on_progress  # For TTS updates
        self.on_complete = on_complete
        
        self.active = False
        self.current_task: Optional[AutonomousTask] = None
        self.task_queue: queue.Queue = queue.Queue()
        self.worker_thread: Optional[threading.Thread] = None
    
    def start(self, initial_task: str) -> str:
        """Start autonomous mode with initial task."""
        if self.active:
            return "Bereits im autonomen Modus."
        
        self.active = True
        self._notify("Vollautonom-Modus aktiviert. Ich analysiere die Aufgabe.")
        
        # Plan the task
        tasks = self._plan_tasks(initial_task)
        
        for task in tasks:
            self.task_queue.put(task)
        
        # Start worker
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        return f"Starte mit {len(tasks)} Teilaufgaben."
    
    def stop(self) -> str:
        """Stop autonomous mode."""
        self.active = False
        self._notify("Autonomer Modus beendet.")
        return "Autonomer Modus gestoppt."
    
    def _plan_tasks(self, description: str) -> List[AutonomousTask]:
        """Plan tasks using Ollama or simple parsing."""
        tasks = []
        
        # Use Ollama for planning if available
        if self.ollama and self.ollama.available:
            plan = self.ollama.generate(
                f"Zerlege diese Aufgabe in max. 3 konkrete Schritte: {description}\n"
                "Format: Nummerierte Liste, kurz und präzise."
            )
            
            if plan:
                lines = [l.strip() for l in plan.split("\n") if l.strip()]
                for i, line in enumerate(lines[:5]):
                    # Clean numbering
                    clean = line.lstrip("0123456789.-) ")
                    if clean:
                        tool = self._decide_tool(clean)
                        tasks.append(AutonomousTask(
                            id=f"task_{i}",
                            description=clean,
                            tool=tool,
                            prompt=clean
                        ))
        
        # Fallback: single task
        if not tasks:
            tool = self._decide_tool(description)
            tasks.append(AutonomousTask(
                id="task_0",
                description=description,
                tool=tool,
                prompt=description
            ))
        
        return tasks
    
    def _decide_tool(self, description: str) -> str:
        """Decide which tool to use."""
        desc_lower = description.lower()
        
        if self.ollama and self.ollama.available:
            return self.ollama.decide_delegation(description)
        
        # Simple keyword matching
        if any(kw in desc_lower for kw in ["code", "projekt", "datei", "fix", "implement"]):
            return "opencode"
        elif any(kw in desc_lower for kw in ["research", "erkläre", "analysiere"]):
            return "claude"
        
        return "gemini"
    
    def _worker_loop(self):
        """Process tasks in queue."""
        while self.active:
            try:
                task = self.task_queue.get(timeout=1)
                self._execute_task(task)
            except queue.Empty:
                if self.task_queue.empty():
                    self._notify("Alle Aufgaben erledigt.")
                    self.active = False
                    if self.on_complete:
                        self.on_complete(self._get_summary())
                    break
    
    def _execute_task(self, task: AutonomousTask):
        """Execute a single task."""
        self.current_task = task
        task.status = TaskStatus.RUNNING
        
        self._notify(f"Arbeite an: {task.description[:50]}...")
        
        try:
            # Optimize prompt if Ollama available
            prompt = task.prompt
            if self.ollama and self.ollama.available:
                prompt = self.ollama.optimize_prompt(prompt, task.tool)
            
            # Send to CLI
            result = self.cli_proxy.send_to_cli(prompt, task.tool)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            
            # Short progress update
            self._notify(f"Fertig: {task.description[:30]}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = str(e)
            self._notify(f"Fehler bei: {task.description[:30]}")
    
    def _notify(self, message: str):
        """Send progress notification."""
        print(f"[Autonomous] {message}")
        if self.on_progress:
            self.on_progress(message)
    
    def _get_summary(self) -> str:
        """Get summary of completed work."""
        return "Autonome Session beendet. Alle Aufgaben abgearbeitet."
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "active": self.active,
            "current_task": self.current_task.description if self.current_task else None,
            "queue_size": self.task_queue.qsize()
        }


if __name__ == "__main__":
    print("Autonomous Mode module loaded")
