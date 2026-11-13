from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "settings.json"
DEFAULTS: dict[str, Any] = {
    "language": "es",
    "workspace": str(ROOT / "laboratorios"),
    "mcp": {
        "enabled": False,
        "command": "uvx",
        "args": ["--from", "packet-tracer-mcp[ui]", "packet-tracer-mcp", "--stdio"],
        "env": {},
        "connect_timeout_seconds": 30
    },
    "capture": {"enabled": True, "fallback_screenshot": True},
    "ocr": {"enabled": False, "tesseract_cmd": ""}
}

def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    if not path.exists():
        return DEFAULTS.copy()
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return DEFAULTS.copy()
    return _merge(DEFAULTS, loaded)

def _merge(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result
