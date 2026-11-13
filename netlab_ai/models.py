from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

@dataclass
class Activity:
    number: int
    kind: str
    text: str
    page: int | None = None
    answer: str = ""
    status: str = "Pendiente"
    evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

@dataclass
class Practice:
    source_file: str
    title: str
    extracted_text: str
    activities: list[Activity] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def total(self) -> int:
        return len(self.activities)

    @property
    def completed(self) -> int:
        return sum(a.status == "Completada" for a in self.activities)
