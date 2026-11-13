# Integración MCP-Packet-Tracer

La integración se configura en `config/settings.json` (copia `config/settings.example.json`).

El cliente consulta `list_tools()` para descubrir las herramientas que realmente ofrece la versión instalada. No debe asumir que una herramienta existe solo por su nombre.

## Capturas

NETLAB AI puede guardar imágenes embebidas que devuelva una herramienta MCP. Si el servidor devuelve solo una ruta o texto, la aplicación debe registrar ese resultado y resolver la ruta de acuerdo con el entorno local. La captura de escritorio con PyAutoGUI es un respaldo opcional y captura la pantalla del equipo, no sustituye una captura específica del panel lógico.

## Seguridad

- No ejecutar comandos IOS arbitrarios extraídos de un documento sin revisión.
- Mostrar el plan antes de desplegar cambios.
- Registrar la herramienta, argumentos no sensibles, resultado y errores.
- No marcar una actividad como completada sin verificación.
- No almacenar credenciales en el repositorio.
