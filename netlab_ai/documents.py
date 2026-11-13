from __future__ import annotations
from pathlib import Path

SUPPORTED = {".pdf", ".docx", ".txt", ".md", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

class DocumentError(RuntimeError):
    pass

def read_document(path: str | Path, *, ocr_enabled: bool = False, tesseract_cmd: str = "") -> str:
    file = Path(path)
    if not file.exists():
        raise DocumentError(f"No existe el archivo: {file}")
    suffix = file.suffix.lower()
    if suffix not in SUPPORTED:
        raise DocumentError(f"Formato no admitido: {suffix}")
    if suffix == ".pdf":
        return _read_pdf(file)
    if suffix == ".docx":
        return _read_docx(file)
    if suffix in {".txt", ".md"}:
        return file.read_text(encoding="utf-8", errors="replace")
    if ocr_enabled:
        return _ocr_image(file, tesseract_cmd)
    raise DocumentError("Es una imagen. Activa OCR e instala Tesseract para extraer su texto.")

def _read_pdf(path: Path) -> str:
    try:
        import fitz
        pages = []
        with fitz.open(path) as doc:
            for index, page in enumerate(doc, 1):
                text = page.get_text("text").strip()
                pages.append(f"\n[PÁGINA {index}]\n{text}")
        result = "\n".join(pages).strip()
        if not result:
            raise DocumentError("El PDF no contiene texto seleccionable. Requiere OCR.")
        return result
    except ImportError as exc:
        raise DocumentError("Falta PyMuPDF. Instala las dependencias del proyecto.") from exc

def _read_docx(path: Path) -> str:
    try:
        from docx import Document
        doc = Document(path)
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells))
        return "\n".join(parts)
    except ImportError as exc:
        raise DocumentError("Falta python-docx. Instala las dependencias del proyecto.") from exc

def _ocr_image(path: Path, tesseract_cmd: str = "") -> str:
    try:
        from PIL import Image
        import pytesseract
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        return pytesseract.image_to_string(Image.open(path), lang="spa+eng")
    except Exception as exc:
        raise DocumentError(f"No se pudo ejecutar OCR: {exc}") from exc
