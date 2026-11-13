from __future__ import annotations
from pathlib import Path
from .models import Practice

def export_json(practice: Practice, output: Path) -> Path:
    import json
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(practice.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return output

def export_pdf(practice: Practice, output: Path) -> Path:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallMuted", parent=styles["BodyText"], textColor=colors.HexColor("#64748b"), fontSize=8))
    story = [Paragraph("NETLAB AI — Informe de práctica", styles["Title"]), Paragraph(practice.title, styles["Heading2"]), Spacer(1, 0.4*cm)]
    story.append(Paragraph(f"Actividades detectadas: {practice.total} | Completadas: {practice.completed}", styles["BodyText"]))
    for activity in practice.activities:
        story.extend([Spacer(1, 0.35*cm), Paragraph(f"{activity.number}. {activity.kind.title()}", styles["Heading3"]), Paragraph(_esc(activity.text), styles["BodyText"])])
        if activity.answer:
            story.append(Paragraph("<b>Respuesta:</b> " + _esc(activity.answer), styles["BodyText"]))
        story.append(Paragraph(f"Estado: {_esc(activity.status)}", styles["SmallMuted"]))
        for evidence in activity.evidence:
            path = Path(evidence)
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                try:
                    story.append(Image(str(path), width=15*cm, height=8.4*cm, kind="proportional"))
                except Exception:
                    pass
    SimpleDocTemplate(str(output), pagesize=A4, rightMargin=1.8*cm, leftMargin=1.8*cm, topMargin=1.8*cm, bottomMargin=1.8*cm).build(story)
    return output

def _esc(value: str) -> str:
    from xml.sax.saxutils import escape
    return escape(value).replace("\n", "<br/>")
