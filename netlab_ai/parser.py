from __future__ import annotations
import re
from .models import Activity, Practice

QUESTION_RE = re.compile(r"(?im)^\s*(?:pregunta\s*)?(\d{1,3})[.)\-:]\s+(.+?)(?=\n\s*(?:pregunta\s*)?\d{1,3}[.)\-:]|\Z)", re.S)
QUESTION_WORDS = re.compile(r"(?i)\b(qué|que|cuál|cual|cuáles|cuales|cómo|como|por qué|porque|explique|mencione|defina|describa|indique|compare|calcule|configure|cree|realice|verifique|demuestre|conecte|diseñe)\b")

def analyze_text(text: str, source_file: str = "practica") -> Practice:
    activities: list[Activity] = []
    seen: set[tuple[str, str]] = set()
    for match in QUESTION_RE.finditer(text):
        body = " ".join(match.group(2).split())
        kind = "pregunta" if re.search(r"(?i)\?|\b(qué|que|cuál|cómo|por qué|defina|explique|mencione)\b", body) else "instrucción"
        key = (kind, body.casefold())
        if body and key not in seen:
            seen.add(key)
            activities.append(Activity(number=len(activities) + 1, kind=kind, text=body, page=_page_before(text, match.start())))
    if not activities:
        for line in text.splitlines():
            line = line.strip(" •\t-")
            if len(line) > 12 and QUESTION_WORDS.search(line):
                kind = "pregunta" if "?" in line or re.search(r"(?i)\b(defina|explique|mencione|qué|cuál|cómo)\b", line) else "instrucción"
                key = (kind, line.casefold())
                if key not in seen:
                    seen.add(key)
                    activities.append(Activity(number=len(activities) + 1, kind=kind, text=line, page=_page_before(text, text.find(line))))
    practice = Practice(source_file=source_file, title=_title(source_file), extracted_text=text, activities=activities)
    return practice

def _page_before(text: str, offset: int) -> int | None:
    markers = list(re.finditer(r"\[PÁGINA (\d+)\]", text[:offset], re.I))
    return int(markers[-1].group(1)) if markers else None

def _title(source: str) -> str:
    from pathlib import Path
    return Path(source).stem.replace("_", " ").replace("-", " ").title()
