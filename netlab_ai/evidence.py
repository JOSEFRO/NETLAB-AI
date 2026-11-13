from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any

def create_evidence_dir(workspace: str | Path, practice_name: str) -> Path:
    folder = Path(workspace) / _safe(practice_name) / "evidencias"
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def save_mcp_capture(result: Any, folder: Path, label: str) -> list[str]:
    """Guarda contenido de imagen devuelto por MCP si viene embebido; registra texto/rutas."""
    saved: list[str] = []
    content = getattr(result, "content", None) or []
    for index, item in enumerate(content, 1):
        mime = getattr(item, "mimeType", "") or getattr(item, "mime_type", "")
        data = getattr(item, "data", None)
        if data and str(mime).startswith("image/"):
            import base64
            ext = ".png" if "png" in mime else ".jpg"
            target = folder / f"{_safe(label)}_{index}{ext}"
            target.write_bytes(base64.b64decode(data))
            saved.append(str(target))
        text = getattr(item, "text", None)
        if text:
            saved.append(str(text))
    return saved

def desktop_capture(folder: Path, label: str) -> str | None:
    try:
        import pyautogui
        target = folder / f"{_safe(label)}_{datetime.now():%Y%m%d_%H%M%S}.png"
        pyautogui.screenshot().save(target)
        return str(target)
    except Exception:
        return None

def _safe(value: str) -> str:
    import re
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return cleaned[:70] or "captura"
