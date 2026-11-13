# Arquitectura inicial

NETLAB AI separa la aplicación de escritorio, el análisis documental, el flujo de prácticas, la capa MCP y las evidencias.

## Módulos

- `documents.py`: extracción de PDF, DOCX, texto e imágenes OCR opcional.
- `parser.py`: detección heurística de instrucciones y preguntas numeradas.
- `models.py`: modelo común de práctica y actividades.
- `mcp_client.py`: cliente MCP por stdio y descubrimiento dinámico de herramientas.
- `evidence.py`: almacenamiento de capturas devueltas por MCP o captura local opcional.
- `reports.py`: exportación JSON y PDF.
- `ui.py`: interfaz de escritorio Tkinter en español.

## Flujo previsto

1. Importar un documento.
2. Extraer el texto y conservar referencias de página cuando existan.
3. Dividir el documento en actividades.
4. Preparar una solución y un plan técnico estructurado.
5. Solicitar confirmación antes de desplegar cambios en Packet Tracer.
6. Ejecutar herramientas MCP y guardar sus resultados.
7. Verificar cada requisito y adjuntar evidencias.
8. Generar el informe final.

## Límites del primer corte

El analizador es heurístico y no garantiza detectar toda pregunta en documentos con formato libre, columnas o diagramas. El cliente MCP requiere configurar y probar el comando del servidor y la extensión en Packet Tracer. No se afirma compatibilidad funcional hasta realizar pruebas en Windows con Packet Tracer 9.
