"""Application state management for UI (Settings, History, Pins)."""

import json
from pathlib import Path
from typing import Any, Dict, List

_STATE_FILE = Path.home() / ".neurafind" / "ui_state.json"

class AppState:
    def __init__(self):
        self.settings: Dict[str, Any] = {
            "theme": "dark",
            "language": "en",
            "result_limit": 50,
            "semantic_threshold": 0.65,
            "cache_controls": True,
        }
        self.search_history: List[str] = []
        self.pinned_results: List[str] = []
        self._load()

    def _load(self):
        if not _STATE_FILE.exists():
            return
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.settings.update(data.get("settings", {}))
                self.search_history = data.get("search_history", [])
                self.pinned_results = data.get("pinned_results", [])
        except Exception:
            pass

    def save(self):
        _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "settings": self.settings,
                    "search_history": self.search_history,
                    "pinned_results": self.pinned_results,
                }, f, indent=2)
        except Exception:
            pass

    def add_search_history(self, query: str):
        if not query:
            return
        if query in self.search_history:
            self.search_history.remove(query)
        self.search_history.insert(0, query)
        self.search_history = self.search_history[:20]  # Keep last 20
        self.save()

    def remove_search_history(self, query: str):
        if query in self.search_history:
            self.search_history.remove(query)
            self.save()

    def toggle_pin(self, path: str):
        if path in self.pinned_results:
            self.pinned_results.remove(path)
        else:
            self.pinned_results.append(path)
        self.save()

    def is_pinned(self, path: str) -> bool:
        return path in self.pinned_results

# Global singleton
state = AppState()
