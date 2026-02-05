# Wanda Voice Assistant - Push Notifications
"""Push notifications via ntfy.sh for mobile alerts."""

import requests
import threading
from typing import Optional, Dict
from datetime import datetime


class WandaNotifier:
    """
    Push notifications for Wanda events.
    Uses ntfy.sh (free, open source, works on iOS/Android).
    """
    
    # Notification types with emojis
    TYPES = {
        "task_complete": "✅",
        "task_failed": "❌",
        "idea_captured": "💡",
        "project_created": "📁",
        "reminder": "⏰",
        "message": "💬"
    }
    
    def __init__(
        self,
        topic: str = "wanda-jannis",
        server: str = "https://ntfy.sh",
        enabled: bool = True
    ):
        """
        Initialize notifier.
        
        Args:
            topic: Your unique ntfy topic (keep secret!)
            server: ntfy.sh server URL (or self-hosted)
            enabled: Enable/disable notifications
        """
        self.topic = topic
        self.server = server.rstrip("/")
        self.enabled = enabled
        self.url = f"{self.server}/{self.topic}"
        
        if enabled:
            print(f"[Notifier] Ready: {self.url}")
    
    def send(
        self,
        message: str,
        title: str = "Wanda",
        priority: int = 3,
        tags: str = "",
        notification_type: str = "message",
        click_url: Optional[str] = None
    ) -> bool:
        """
        Send push notification.
        
        Args:
            message: Notification body
            title: Notification title
            priority: 1-5 (min to max)
            tags: Comma-separated emoji tags
            notification_type: Type for emoji prefix
            click_url: URL to open on click
        
        Returns:
            True if sent successfully
        """
        if not self.enabled:
            return False
        
        # Add type emoji
        emoji = self.TYPES.get(notification_type, "💬")
        title = f"{emoji} {title}"
        
        # Build headers
        headers = {
            "Title": title,
            "Priority": str(priority),
        }
        
        if tags:
            headers["Tags"] = tags
        
        if click_url:
            headers["Click"] = click_url
        
        try:
            response = requests.post(
                self.url,
                data=message.encode("utf-8"),
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[Notifier] Error: {e}")
            return False
    
    def task_complete(self, task_name: str, result: str = ""):
        """Notify task completion."""
        message = f"Task abgeschlossen: {task_name}"
        if result:
            message += f"\n\n{result[:200]}"
        
        self.send(
            message=message,
            title="Task fertig!",
            priority=4,
            notification_type="task_complete"
        )
    
    def task_failed(self, task_name: str, error: str = ""):
        """Notify task failure."""
        message = f"Task fehlgeschlagen: {task_name}"
        if error:
            message += f"\n\n{error[:200]}"
        
        self.send(
            message=message,
            title="Task Fehler",
            priority=5,
            notification_type="task_failed"
        )
    
    def idea_captured(self, idea: str):
        """Notify idea capture."""
        self.send(
            message=f"Neue Idee gespeichert:\n\n{idea[:300]}",
            title="Idee erfasst",
            priority=3,
            notification_type="idea_captured"
        )
    
    def project_created(self, project_name: str, path: str):
        """Notify project creation."""
        self.send(
            message=f"Projekt erstellt: {project_name}\n\nPfad: {path}",
            title="Projekt angelegt",
            priority=4,
            notification_type="project_created"
        )
    
    def send_async(self, *args, **kwargs):
        """Send notification asynchronously."""
        threading.Thread(
            target=self.send,
            args=args,
            kwargs=kwargs,
            daemon=True
        ).start()


if __name__ == "__main__":
    # Test
    notifier = WandaNotifier(topic="wanda-test")
    notifier.send(
        message="Wanda Notifier funktioniert!",
        title="Test",
        priority=3
    )
    print("Notification sent!")
