# Wanda Voice Assistant - Remote Project Initializer
"""Initialize projects in Work-OS from mobile voice commands."""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple


class ProjectInitializer:
    """
    Initialize JD-compliant projects in Work-OS from voice commands.
    
    Example:
        "Erstelle Projekt SmartWidget" → 
        Work-OS/20_Playground/21_Experiments/SmartWidget/
    """
    
    # Base paths (Johnny.Decimal compliant)
    WORK_OS_ROOT = Path.home() / "Schreibtisch" / "Work-OS"
    PLAYGROUND = WORK_OS_ROOT / "20_Playground"
    EXPERIMENTS = PLAYGROUND / "21_Experiments"
    VENTURES = PLAYGROUND / "22_Ventures"
    
    # Project template
    README_TEMPLATE = '''# {name}

**Erstellt**: {date}  
**Status**: 🟡 In Progress  
**Typ**: {project_type}

## Beschreibung
{description}

## Ziele
{goals}

## Nächste Schritte
- [ ] {next_step}

---
*Automatisch erstellt von Wanda*
'''
    
    PLAN_TEMPLATE = '''# {name} - Projektplan

## Vision
{description}

## Phasen

### Phase 1: Research & Planning
- [ ] Machbarkeit prüfen
- [ ] Technologien auswählen
- [ ] MVP definieren

### Phase 2: Implementation
- [ ] Grundstruktur aufbauen
- [ ] Core Features implementieren
- [ ] Tests schreiben

### Phase 3: Polish
- [ ] UI/UX verfeinern
- [ ] Dokumentation
- [ ] Launch vorbereiten

## Ressourcen
- Budget: TBD
- Zeitrahmen: TBD

---
*Automatisch erstellt von Wanda*
'''
    
    def __init__(self, ollama=None, notifier=None):
        """
        Initialize project initializer.
        
        Args:
            ollama: OllamaAdapter for AI-enhanced descriptions
            notifier: WandaNotifier for push notifications
        """
        self.ollama = ollama
        self.notifier = notifier
        
        # Ensure base directories exist
        self.EXPERIMENTS.mkdir(parents=True, exist_ok=True)
        self.VENTURES.mkdir(parents=True, exist_ok=True)
    
    def create_project(
        self,
        name: str,
        description: str = "",
        project_type: str = "experiment",
        goals: str = "",
        init_git: bool = True
    ) -> Tuple[bool, str]:
        """
        Create a new project in Playground.
        
        Args:
            name: Project name (will be sanitized)
            description: Brief description
            project_type: 'experiment' or 'venture'
            goals: Project goals
            init_git: Initialize git repo
        
        Returns:
            Tuple of (success, path_or_error)
        """
        # Sanitize name
        safe_name = self._sanitize_name(name)
        
        # Choose base path
        if project_type == "venture":
            # Get next JD ID for ventures
            jd_id = self._get_next_venture_id()
            base = self.VENTURES
            folder_name = f"{jd_id}_{safe_name}"
        else:
            base = self.EXPERIMENTS
            folder_name = safe_name
        
        project_path = base / folder_name
        
        # Check if exists
        if project_path.exists():
            return False, f"Projekt existiert bereits: {project_path}"
        
        try:
            # Create directory
            project_path.mkdir(parents=True)
            
            # Enhance description with Ollama if available
            if self.ollama and self.ollama.available and not description:
                description = self._generate_description(name)
            
            if not description:
                description = f"Projekt basierend auf der Idee: {name}"
            
            if not goals:
                goals = "- Kernfunktionalität implementieren\n- MVP fertigstellen"
            
            # Create README
            readme_content = self.README_TEMPLATE.format(
                name=name,
                date=datetime.now().strftime("%Y-%m-%d"),
                project_type="Experiment" if project_type == "experiment" else "Venture",
                description=description,
                goals=goals,
                next_step="Projekt-Setup abschließen"
            )
            (project_path / "README.md").write_text(readme_content, encoding="utf-8")
            
            # Create PLAN.md
            plan_content = self.PLAN_TEMPLATE.format(
                name=name,
                description=description
            )
            (project_path / "PLAN.md").write_text(plan_content, encoding="utf-8")
            
            # Create basic structure
            (project_path / "src").mkdir()
            (project_path / "docs").mkdir()
            (project_path / "tests").mkdir()
            
            # Git init
            if init_git:
                self._git_init(project_path)
            
            # Notify
            if self.notifier:
                self.notifier.project_created(name, str(project_path))
            
            return True, str(project_path)
            
        except Exception as e:
            return False, f"Fehler: {e}"
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize project name for filesystem."""
        # Remove special chars, keep alphanumeric and underscores
        safe = re.sub(r'[^\w\s-]', '', name)
        safe = re.sub(r'[\s]+', '_', safe)
        return safe[:50]  # Limit length
    
    def _get_next_venture_id(self) -> str:
        """Get next available JD ID for ventures (22.XX)."""
        existing = list(self.VENTURES.glob("22.*"))
        if not existing:
            return "22.05"
        
        # Find highest ID
        max_id = 4
        for folder in existing:
            match = re.match(r'22\.(\d+)', folder.name)
            if match:
                max_id = max(max_id, int(match.group(1)))
        
        return f"22.{max_id + 1:02d}"
    
    def _generate_description(self, name: str) -> str:
        """Generate description using Ollama."""
        try:
            prompt = f"""Erstelle eine kurze Projektbeschreibung (2-3 Sätze) für ein Softwareprojekt namens "{name}".
Fokussiere auf den Nutzen und Hauptfeatures. Antworte nur mit der Beschreibung, ohne Überschriften."""
            
            return self.ollama.generate(prompt, max_tokens=150)
        except:
            return ""
    
    def _git_init(self, project_path: Path):
        """Initialize git repository."""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                capture_output=True,
                timeout=5
            )
            
            # Create .gitignore
            gitignore = """# Python
__pycache__/
*.py[cod]
venv/
.env

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
"""
            (project_path / ".gitignore").write_text(gitignore)
            
            # Initial commit
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                capture_output=True,
                timeout=5
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit by Wanda"],
                cwd=project_path,
                capture_output=True,
                timeout=5
            )
        except Exception as e:
            print(f"[ProjectInit] Git error: {e}")
    
    def capture_idea(self, idea: str) -> str:
        """
        Quick idea capture without full project creation.
        Saves to IDEAS.md in Experiments.
        """
        ideas_file = self.EXPERIMENTS / "IDEAS.md"
        
        # Create if not exists
        if not ideas_file.exists():
            ideas_file.write_text("# 💡 Ideen-Sammlung\n\nGesammelt von Wanda unterwegs.\n\n---\n\n")
        
        # Append idea
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"## {timestamp}\n\n{idea}\n\n---\n\n"
        
        with open(ideas_file, "a", encoding="utf-8") as f:
            f.write(entry)
        
        # Notify
        if self.notifier:
            self.notifier.idea_captured(idea)
        
        return f"Idee gespeichert in {ideas_file}"
    
    def parse_command(self, text: str) -> Optional[Dict]:
        """
        Parse voice command for project creation.
        
        Examples:
            "Erstelle Projekt SmartWidget"
            "Neue Idee: App für Zeiterfassung"
            "Starte Venture CryptoTracker"
        """
        text_lower = text.lower()
        
        # Project creation patterns
        project_patterns = [
            r"erstelle\s+projekt\s+(.+)",
            r"neues\s+projekt\s+(.+)",
            r"projekt\s+erstellen\s+(.+)",
            r"create\s+project\s+(.+)",
            r"starte\s+projekt\s+(.+)",
        ]
        
        for pattern in project_patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).strip()
                return {"action": "create_project", "name": name, "type": "experiment"}
        
        # Venture patterns
        venture_patterns = [
            r"starte\s+venture\s+(.+)",
            r"neues\s+venture\s+(.+)",
            r"venture\s+erstellen\s+(.+)",
        ]
        
        for pattern in venture_patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).strip()
                return {"action": "create_project", "name": name, "type": "venture"}
        
        # Idea patterns
        idea_patterns = [
            r"neue\s+idee[:\s]+(.+)",
            r"idee[:\s]+(.+)",
            r"notiere[:\s]+(.+)",
            r"merke\s+dir[:\s]+(.+)",
        ]
        
        for pattern in idea_patterns:
            match = re.search(pattern, text_lower)
            if match:
                idea = match.group(1).strip()
                return {"action": "capture_idea", "idea": idea}
        
        return None


if __name__ == "__main__":
    init = ProjectInitializer()
    
    # Test parsing
    tests = [
        "Erstelle Projekt SmartWidget",
        "Neue Idee: Eine App für Zeiterfassung",
        "Starte Venture CryptoTracker",
    ]
    
    for test in tests:
        result = init.parse_command(test)
        print(f"'{test}' → {result}")
