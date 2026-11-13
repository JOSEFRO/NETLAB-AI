from __future__ import annotations
from pathlib import Path
from .config import load_config
from .documents import read_document
from .parser import analyze_text
from .reports import export_json, export_pdf

class PracticeWorkflow:
    def __init__(self):
        self.config = load_config()

    def analyze(self, source: str):
        text = read_document(
            source,
            ocr_enabled=bool(self.config.get("ocr", {}).get("enabled")),
            tesseract_cmd=self.config.get("ocr", {}).get("tesseract_cmd", "")
        )
        return analyze_text(text, source)

    def export(self, practice):
        workspace = Path(self.config["workspace"]) / Path(practice.source_file).stem
        workspace.mkdir(parents=True, exist_ok=True)
        export_json(practice, workspace / "practice.json")
        export_pdf(practice, workspace / "informe.pdf")
        return workspace
