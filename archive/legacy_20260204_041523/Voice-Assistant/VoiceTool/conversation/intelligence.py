# Wanda Voice Assistant - Workflow Engine
"""Executes multi-step workflows like project initialization."""

import subprocess
import os
from typing import Optional, Dict, Any
from pathlib import Path


class WorkflowEngine:
    """Executes automated workflows."""
    
    WORKFLOW_KEYWORDS = {
        "init_project": ["initiiere", "erstelle projekt", "neues projekt", "projekt anlegen"],
        "git_commit": ["committe", "git commit", "änderungen speichern"],
    }
    
    def detect_workflow(self, text: str) -> Optional[str]:
        """Detect if text triggers a workflow."""
        text_lower = text.lower()
        
        for workflow, keywords in self.WORKFLOW_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return workflow
        
        return None
    
    def extract_params(self, text: str, workflow: str) -> Dict[str, Any]:
        """Extract parameters from text for workflow."""
        params = {}
        text_lower = text.lower()
        
        if workflow == "init_project":
            # Try to extract project name
            words = text.split()
            for i, word in enumerate(words):
                if word.lower() in ["projekt", "project", "namens", "genannt"]:
                    if i + 1 < len(words):
                        params["name"] = words[i + 1].strip('.,!?')
                        break
            
            # Detect project type
            if "python" in text_lower:
                params["type"] = "python"
            elif "node" in text_lower or "javascript" in text_lower:
                params["type"] = "node"
            else:
                params["type"] = "python"  # default
        
        return params
    
    def execute(self, workflow: str, params: Dict[str, Any], cwd: Optional[str] = None) -> str:
        """Execute workflow."""
        cwd = cwd or os.getcwd()
        
        if workflow == "init_project":
            return self._init_project(params, cwd)
        elif workflow == "git_commit":
            return self._git_commit(params, cwd)
        
        return f"❌ Unknown workflow: {workflow}"
    
    def _init_project(self, params: Dict[str, Any], cwd: str) -> str:
        """Initialize new project."""
        name = params.get("name", "new-project")
        project_type = params.get("type", "python")
        project_path = Path(cwd) / name
        
        steps = []
        
        # Create directory
        try:
            project_path.mkdir(exist_ok=True)
            steps.append(f"✅ Created {name}/")
        except Exception as e:
            return f"❌ Failed to create directory: {e}"
        
        # Git init
        try:
            subprocess.run(["git", "init"], cwd=project_path, capture_output=True)
            steps.append("✅ Git initialized")
        except:
            steps.append("⚠️ Git init failed")
        
        # Python venv
        if project_type == "python":
            try:
                subprocess.run(["python3", "-m", "venv", "venv"], cwd=project_path, capture_output=True)
                steps.append("✅ Python venv created")
            except:
                steps.append("⚠️ Venv creation failed")
        
        # README
        readme = project_path / "README.md"
        readme.write_text(f"# {name}\n\nProject created by Wanda.\n")
        steps.append("✅ README.md created")
        
        # .gitignore
        gitignore = project_path / ".gitignore"
        gitignore.write_text("venv/\n__pycache__/\n*.pyc\n.env\n")
        steps.append("✅ .gitignore created")
        
        return "\n".join(steps) + f"\n\n✅ Project {name} ready at {project_path}"
    
    def _git_commit(self, params: Dict[str, Any], cwd: str) -> str:
        """Git add and commit."""
        message = params.get("message", "Update via Wanda")
        
        try:
            subprocess.run(["git", "add", "-A"], cwd=cwd, capture_output=True)
            result = subprocess.run(
                ["git", "commit", "-m", message], 
                cwd=cwd, capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"✅ Committed: {message}"
            else:
                return f"⚠️ {result.stderr.strip()}"
        except Exception as e:
            return f"❌ Git commit failed: {e}"


if __name__ == "__main__":
    engine = WorkflowEngine()
    
    # Test detection
    tests = [
        "Initiiere ein Python-Projekt namens test123",
        "Erstelle Projekt MeinApp",
        "Das ist ein normaler Satz",
    ]
    for text in tests:
        workflow = engine.detect_workflow(text)
        if workflow:
            params = engine.extract_params(text, workflow)
            print(f"'{text}' -> {workflow} with {params}")
        else:
            print(f"'{text}' -> No workflow")
