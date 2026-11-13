from __future__ import annotations
import asyncio
import shutil
import threading
from typing import Any

class MCPBridge:
    """Cliente MCP stdio con un event loop persistente en segundo plano."""
    def __init__(self, command: str = "uvx", args: list[str] | None = None, env: dict[str, str] | None = None):
        self.command = command
        self.args = args or []
        self.env = env
        self._loop: asyncio.AbstractEventLoop | None = None
        self._session: Any = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()
        self._closed = threading.Event()
        self._error: Exception | None = None
        self.tools: list[dict[str, Any]] = []

    @property
    def connected(self) -> bool:
        return self._session is not None and self._thread is not None and self._thread.is_alive()

    def connect(self, timeout: int = 30) -> list[dict[str, Any]]:
        if self.connected:
            return self.tools
        self._ready.clear()
        self._closed.clear()
        self._error = None
        self._thread = threading.Thread(target=self._thread_main, daemon=True, name="NETLAB-MCP")
        self._thread.start()
        if not self._ready.wait(timeout):
            self.disconnect()
            raise TimeoutError("Tiempo agotado al conectar con el servidor MCP.")
        if self._error:
            raise RuntimeError(str(self._error)) from self._error
        return self.tools

    def _thread_main(self) -> None:
        asyncio.run(self._serve())

    async def _serve(self) -> None:
        self._loop = asyncio.get_running_loop()
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            executable = shutil.which(self.command) or self.command
            params = StdioServerParameters(command=executable, args=self.args, env=self.env)
            async with stdio_client(params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    self._session = session
                    await session.initialize()
                    response = await session.list_tools()
                    self.tools = [
                        {"name": tool.name, "description": tool.description or "", "inputSchema": tool.inputSchema}
                        for tool in response.tools
                    ]
                    self._ready.set()
                    while not self._closed.is_set():
                        await asyncio.sleep(0.15)
        except Exception as exc:
            self._error = exc
            self._ready.set()
        finally:
            self._session = None
            self._loop = None

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None, timeout: int = 90) -> Any:
        if not self.connected or self._loop is None or self._session is None:
            raise RuntimeError("El puente MCP no está conectado.")
        coroutine = self._session.call_tool(name, arguments or {})
        future = asyncio.run_coroutine_threadsafe(coroutine, self._loop)
        return future.result(timeout=timeout)

    def disconnect(self) -> None:
        self._closed.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        self._session = None
