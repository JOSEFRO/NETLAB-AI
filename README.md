<div align="center">

<img src="https://d8j0ntlcm91z4.cloudfront.net/user_3MJ8xX039ib9919oo3CFVd7NjMx/hf_20261119_141651_aa8abd62-3c82-434a-b8d9-9b5d4a5e0d60.webp" alt="Arte conceptual de NETLAB AI" width="100%">

# NETLAB AI

**Asistente de laboratorio para prácticas de redes, evidencias e informes en español.**

![Estado](https://img.shields.io/badge/estado-prototipo%20en%20desarrollo-orange)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)
![MCP](https://img.shields.io/badge/integraci%C3%B3n-MCP-6B5CE7)
![Plataforma](https://img.shields.io/badge/objetivo-Windows-0078D6?logo=windows)

[Repositorio](https://github.com/JOSEFRO/NETLAB-AI) · [Incidencias](https://github.com/JOSEFRO/NETLAB-AI/issues) · [Historial](https://github.com/JOSEFRO/NETLAB-AI/commits/main)

</div>

## 1. Descripción

NETLAB AI es un prototipo de aplicación de escritorio orientado a organizar prácticas de redes, extraer instrucciones de documentos, conectarse a herramientas MCP y recopilar evidencias para generar informes.

El proyecto está pensado para acompañar laboratorios controlados y actividades educativas. Las operaciones de red deben realizarse únicamente en equipos, simuladores y entornos para los que exista autorización.

## 2. Objetivos funcionales

- Leer documentos PDF, DOCX, TXT y Markdown.
- Aplicar OCR opcional a documentos escaneados.
- Identificar preguntas e instrucciones mediante análisis heurístico.
- Organizar actividades y tareas.
- Conectarse a un servidor MCP mediante stdio.
- Descubrir herramientas disponibles durante la conexión.
- Recopilar capturas y evidencias de prácticas.
- Exportar informes PDF y datos JSON.
- Presentar una interfaz de escritorio en español.

La extracción heurística puede omitir contenido en documentos complejos. Los resultados requieren revisión humana.

## 3. Arquitectura del proyecto

| Módulo | Responsabilidad |
|---|---|
| `documents.py` | Extracción de texto de documentos. |
| `parser.py` | Detección heurística de preguntas e instrucciones. |
| `mcp_client.py` | Comunicación con servidor MCP por stdio. |
| `evidence.py` | Gestión de evidencias y capturas. |
| `reports.py` | Generación de informes y exportación. |
| `ui.py` | Interfaz de escritorio Tkinter. |

## 4. Tecnologías y protocolos

- Python 3.11 o superior.
- Tkinter para interfaz de escritorio.
- PyMuPDF y python-docx para documentos.
- Tesseract OCR opcional.
- ReportLab para generación de PDF.
- MCP (Model Context Protocol) para comunicación con herramientas.
- Transporte stdio para el proceso MCP configurado.

MCP no implica acceso automático a Packet Tracer: se requiere un servidor compatible, configuración local y pruebas de integración.

## 5. Requisitos

- Windows 11 como plataforma objetivo principal.
- Python 3.11 o superior.
- Cisco Packet Tracer instalado para pruebas de integración.
- Servidor MCP compatible y configurado.
- `uvx` disponible en PATH si se utiliza el comando de ejemplo.
- Tesseract OCR opcional para documentos escaneados.

## 6. Instalación

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item config\settings.example.json config\settings.json
python main.py
```

## 7. Configuración MCP

Edita `config/settings.json` y revisa el comando, argumentos y variables de entorno del servidor que hayas instalado.

Configuración de referencia:

```json
{
  "command": "uvx",
  "args": [
    "--from",
    "packet-tracer-mcp[ui]",
    "packet-tracer-mcp",
    "--stdio"
  ]
}
```

Verifica la sintaxis y compatibilidad con la versión del servidor MCP utilizada. No copies credenciales ni secretos en archivos versionados.

## 8. OCR

Para procesar documentos escaneados:

1. Instala Tesseract OCR.
2. Instala los datos de idioma español.
3. Configura la ruta del ejecutable en `settings.json`.
4. Activa la opción `ocr.enabled`.
5. Compara el texto extraído con el documento original.

## 9. Seguridad y uso responsable

- Utiliza Packet Tracer y laboratorios propios o autorizados.
- Revisa las instrucciones antes de ejecutar cualquier operación.
- No ejecutes automáticamente configuraciones no revisadas.
- Mantén las credenciales fuera de archivos versionados.
- Valida las rutas de entrada y salida de documentos.
- Limita permisos del proceso y acceso a archivos.
- Registra errores sin almacenar información sensible innecesaria.
- Conserva evidencia suficiente para auditar el resultado.

## 10. Limitaciones actuales

La extracción y clasificación son heurísticas y pueden fallar con columnas, diagramas o formatos complejos. El prototipo no debe considerarse un motor autónomo de resolución de prácticas ni un sistema que configure redes sin supervisión. La integración MCP debe probarse localmente con las herramientas realmente disponibles.

## 11. Validación y próximos pasos

- Pruebas unitarias para extracción y clasificación.
- Documentos de ejemplo con resultados esperados.
- Pruebas de conexión, desconexión y errores MCP.
- Validación de capturas y rutas de evidencias.
- Pruebas de generación y apertura de informes PDF.
- Registro de versiones y herramientas MCP detectadas.

## 12. Licencia

No se ha incorporado una licencia de reutilización. El código y los recursos permanecen reservados a su titular salvo autorización expresa.
