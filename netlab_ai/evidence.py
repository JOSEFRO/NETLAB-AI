from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
import re
import shutil

def create_evidence_dir(workspace: str | Path, practice_name: str) -> Path:
    folder = Path(workspace) / _safe(practice_name) / "evidencias"
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def save_mcp_capture(result: Any, folder: Path, label: str) -> list[str]:
    """Copia una imagen embebida o una captura indicada por ruta en la respuesta MCP."""
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
            for candidate in _extract_paths(text):
                source = Path(candidate)
                if source.is_file() and source.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                    target = folder / f"{_safe(label)}_{index}{source.suffix.lower()}"
                    if source.resolve() != target.resolve():
                        shutil.copy2(source, target)
                    saved.append(str(target))
    return saved

def _extract_paths(text: str) -> list[str]:
    candidates = re.findall(r"(?:[A-Za-z]:\\[^\r\n\"']+|/[^\r\n\"']+\.(?:png|jpe?g))", text, flags=re.I)
    cleaned = []
    for value in candidates:
        value = value.strip().rstrip(" .,:;)")
        if value:
            cleaned.append(value)
    return cleaned

def desktop_capture(folder: Path, label: str) -> str | None:
    try:
        import pyautogui
        target = folder / f"{_safe(label)}_{datetime.now():%Y%m%d_%H%M%S}.png"
        pyautogui.screenshot().save(target)
        return str(target)
    except Exception:
        return None

def _safe(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return cleaned[:70] or "captura"
