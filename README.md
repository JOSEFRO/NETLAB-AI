# NETLAB AI

<p align="center"><img src="https://d8j0ntlcm91z4.cloudfront.net/user_3MJ8xX039ib9919oo3CFVd7NjMx/hf_20261119_141651_aa8abd62-3c82-434a-b8d9-9b5d4a5e0d60.webp" alt="Ilustración conceptual del laboratorio de redes y automatización NETLAB AI" width="100%"></p>

> **Arte conceptual de presentación generado para este repositorio.** No es una captura real de la aplicación ni demuestra una integración Packet Tracer/MCP ya operativa.

**Asistente de laboratorios de redes en español** para analizar prácticas, organizar preguntas e instrucciones, trabajar con Cisco Packet Tracer mediante MCP, recopilar evidencias y generar informes.

> Estado: prototipo inicial en desarrollo. La integración con Packet Tracer debe configurarse y probarse localmente; no se afirma que el despliegue automático esté validado todavía.

## Objetivos

- Leer prácticas en PDF, DOCX, TXT y Markdown; OCR opcional para imágenes.
- Separar preguntas e instrucciones y conservar la página cuando sea posible.
- Mantener seguimiento por actividad.
- Conectarse a un servidor MCP por stdio y descubrir sus herramientas disponibles.
- Guardar capturas devueltas por MCP o usar captura de escritorio como respaldo opcional.
- Generar informes PDF y datos JSON.
- Ofrecer una interfaz de escritorio en español con un panel central de laboratorio.

## Requisitos

- Windows 11 (objetivo principal).
- Python 3.11 o superior.
- Cisco Packet Tracer 9 para pruebas de integración.
- Servidor MCP-Packet-Tracer y extensión configurados según la documentación upstream.
- `uvx` disponible en PATH si se utiliza la configuración predeterminada.

## Instalación en Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item config\settings.example.json config\settings.json
python main.py
```

## Configuración MCP

Edita `config/settings.json` y ajusta `mcp.command`, `mcp.args` y, si corresponde, las variables de entorno. La configuración de ejemplo usa:

```json
{
  "command": "uvx",
  "args": ["--from", "packet-tracer-mcp[ui]", "packet-tracer-mcp", "--stdio"]
}
```

Confirma el comando y los argumentos con la versión actual del proyecto MCP que instales. El cliente lista las herramientas disponibles en tiempo de conexión.

## OCR

Para imágenes o PDF escaneados instala Tesseract OCR, el paquete `pytesseract` y los datos de idioma español. Activa `ocr.enabled` y configura `tesseract_cmd` en `settings.json`.

## Estructura

- `netlab_ai/documents.py`: extracción de documentos.
- `netlab_ai/parser.py`: detección heurística de preguntas e instrucciones numeradas.
- `netlab_ai/mcp_client.py`: cliente MCP stdio.
- `netlab_ai/evidence.py`: evidencias y capturas.
- `netlab_ai/reports.py`: exportación JSON/PDF.
- `netlab_ai/ui.py`: interfaz Tkinter.

## Límites conocidos

La extracción y clasificación inicial son heurísticas; no garantizan detectar todas las preguntas, especialmente en documentos con columnas, diagramas o formato libre. Este primer corte no genera respuestas inteligentes ni ejecuta configuraciones de red por sí solo. Esas funciones requieren el siguiente módulo de resolución, mapeo de herramientas MCP y pruebas reales en Packet Tracer. Ningún resultado debe marcarse como completado sin verificación.

## Licencia

Pendiente de selección. Hasta que se añada una licencia, no se concede automáticamente permiso de reutilización.
