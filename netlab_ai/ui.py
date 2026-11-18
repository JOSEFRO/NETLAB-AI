from __future__ import annotations
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from .workflow import PracticeWorkflow
from .config import load_config
from .mcp_client import MCPBridge
from .evidence import desktop_capture, save_mcp_capture, create_evidence_dir

BG = "#070b14"
PANEL = "#101b2c"
PANEL2 = "#15263b"
TEXT = "#f1f5fb"
MUTED = "#91a8bd"
ACCENT = "#79e2e8"
GREEN = "#78e2b7"

class NetLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NETLAB AI | Centro de operaciones")
        self.geometry("1440x900")
        self.minsize(1120, 720)
        self.configure(bg=BG)
        self.workflow = PracticeWorkflow()
        self.practice = None
        self.mcp: MCPBridge | None = None
        self._topology_phase = 0.0
        self._topology_job = None
        self._pulse_items = []
        self._style()
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL, rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background=PANEL2, foreground=TEXT, relief="flat")
        style.map("Treeview", background=[("selected", "#164e63")], foreground=[("selected", "white")])
        style.configure("TProgressbar", troughcolor=PANEL2, background=GREEN, bordercolor=PANEL2)

    def _build(self):
        top = tk.Frame(self, bg=BG, height=66)
        top.pack(fill="x", padx=18, pady=(14, 10))
        tk.Label(top, text="NETLAB", bg=BG, fg=TEXT, font=("Segoe UI", 21, "bold")).pack(side="left")
        tk.Label(top, text="AI  /  NETWORK LAB AUTOMATION", bg=BG, fg=ACCENT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=12, pady=(12, 0))
        self.connection = tk.Label(top, text="● MCP desconectado", bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self.connection.pack(side="right")
        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=18, pady=(0, 12))
        self._button(actions, "Importar práctica", self.import_file).pack(side="left")
        self._button(actions, "Exportar informe", self.export_report, secondary=True).pack(side="left", padx=8)
        self._button(actions, "Conectar MCP", self.connect_mcp, secondary=True).pack(side="left")
        self._button(actions, "Capturar pantalla", self.capture_screen, secondary=True).pack(side="left", padx=8)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        left = self._panel(body, 250); left.pack(side="left", fill="y", padx=(0, 10))
        center = self._panel(body); center.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = self._panel(body, 270); right.pack(side="right", fill="y")

        self._heading(left, "DOCUMENTO Y ACTIVIDADES")
        self.file_label = tk.Label(left, text="Ninguna práctica cargada", bg=PANEL, fg=MUTED, wraplength=220, justify="left")
        self.file_label.pack(fill="x", padx=14, pady=10)
        self.activity_list = tk.Listbox(left, bg=PANEL2, fg=TEXT, selectbackground="#155e75", relief="flat", highlightthickness=0, font=("Segoe UI", 9))
        self.activity_list.pack(fill="both", expand=True, padx=10, pady=8)
        self.activity_list.bind("<<ListboxSelect>>", self.show_activity)

        self._heading(center, "ESPACIO DE TRABAJO · TOPOLOGÍA")
        self.canvas = tk.Canvas(center, bg="#081321", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12, pady=12)
        self.canvas.bind("<Configure>", lambda _e: self._draw_placeholder())
        self._draw_placeholder()

        self._heading(right, "DETALLES Y RESPUESTA")
        self.detail_title = tk.Label(right, text="Selecciona una actividad", bg=PANEL, fg=TEXT, font=("Segoe UI", 11, "bold"), wraplength=235, justify="left")
        self.detail_title.pack(anchor="w", padx=14, pady=(12, 6))
        self.detail = tk.Text(right, height=16, bg=PANEL2, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=("Segoe UI", 9))
        self.detail.pack(fill="both", expand=True, padx=12, pady=8)
        self.detail.insert("1.0", "Aquí aparecerán la instrucción original, la respuesta y las evidencias.")
        self.detail.configure(state="disabled")
        self.progress = ttk.Progressbar(right, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=14, pady=(10, 4))
        self.progress_label = tk.Label(right, text="0 actividades", bg=PANEL, fg=MUTED, font=("Segoe UI", 8))
        self.progress_label.pack(anchor="w", padx=14, pady=(0, 12))
        self.status = tk.Label(self, text="Listo · Importa un PDF, DOCX o imagen para comenzar", bg="#07101c", fg=MUTED, anchor="w", padx=18)
        self.status.pack(fill="x", side="bottom")

    def _panel(self, parent, width=None):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground="#29465d", highlightthickness=1, width=width or 0)
        if width: frame.pack_propagate(False)
        return frame

    def _heading(self, parent, text):
        tk.Label(parent, text=text, bg=PANEL, fg=ACCENT, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(14, 4))

    def _button(self, parent, text, command, secondary=False):
        return tk.Button(parent, text=text, command=command, bg=PANEL2 if secondary else "#a93850", fg=TEXT, activebackground="#d64b65", activeforeground="white", relief="flat", bd=0, padx=14, pady=9, font=("Segoe UI", 9, "bold"), cursor="hand2")

    def _draw_placeholder(self):
        if self._topology_job:
            try:
                self.after_cancel(self._topology_job)
            except tk.TclError:
                pass
            self._topology_job = None
        self.canvas.delete("all")
        self._pulse_items = []
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 50 or h < 50:
            return
        # Decorative standby topology only. Live devices must come from MCP data.
        points = [
            (w * .16, h * .50, "ROUTER"),
            (w * .39, h * .27, "SW-01"),
            (w * .39, h * .73, "SW-02"),
            (w * .68, h * .27, "HOST-01"),
            (w * .68, h * .73, "HOST-02"),
            (w * .86, h * .50, "SERVER"),
        ]
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]
        for x in range(24, int(w), 34):
            self.canvas.create_line(x, 0, x, h, fill="#0d2436", tags=("grid",))
        for y in range(20, int(h), 34):
            self.canvas.create_line(0, y, w, y, fill="#0d2436", tags=("grid",))
        for edge_index, (a, b) in enumerate(edges):
            x1, y1, _ = points[a]
            x2, y2, _ = points[b]
            self.canvas.create_line(x1, y1, x2, y2, fill="#28506a", width=2, tags=("network-edge",))
            pulse = self.canvas.create_oval(x1-4, y1-4, x1+4, y1+4, fill=ACCENT, outline="", tags=("network-pulse",))
            self._pulse_items.append((pulse, x1, y1, x2, y2, edge_index / max(1, len(edges))))
        for index, (x, y, label) in enumerate(points):
            self.canvas.create_oval(x-19, y-19, x+19, y+19, fill="#102b40", outline="#4c91aa", width=2)
            self.canvas.create_oval(x-7, y-7, x+7, y+7, fill="#8fe8e7" if index == 0 else "#80b9d0", outline="")
            self.canvas.create_text(x, y+31, text=label, fill="#b7d4e2", font=("Segoe UI", 8, "bold"))
        self.canvas.create_text(18, 18, anchor="nw", text="VISTA ILUSTRATIVA · MCP SIN CONEXIÓN", fill="#d7b77f", font=("Segoe UI", 8, "bold"))
        self.canvas.create_text(w/2, h-24, text="La topología real aparecerá cuando la integración MCP entregue dispositivos y enlaces.", fill=MUTED, font=("Segoe UI", 8))
        self._animate_topology()

    def _animate_topology(self):
        if not self.winfo_exists():
            return
        self._topology_phase = (self._topology_phase + 0.018) % 1.0
        for item, x1, y1, x2, y2, offset in self._pulse_items:
            t = (self._topology_phase + offset) % 1.0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            self.canvas.coords(item, x-4, y-4, x+4, y+4)
        self._topology_job = self.after(55, self._animate_topology)

    def import_file(self):
        path = filedialog.askopenfilename(title="Seleccionar práctica", filetypes=[("Documentos", "*.pdf *.docx *.txt *.md *.png *.jpg *.jpeg"), ("Todos", "*.*")])
        if not path: return
        try:
            self.practice = self.workflow.analyze(path)
            self.file_label.configure(text=Path(path).name)
            self.activity_list.delete(0, "end")
            for item in self.practice.activities:
                self.activity_list.insert("end", f"{item.number:02d} · {item.kind.title()} · {item.text[:42]}")
            self.progress_label.configure(text=f"{self.practice.total} actividades detectadas")
            self.status.configure(text=f"Documento analizado: {len(self.practice.extracted_text)} caracteres")
            self.progress.configure(value=0)
            if not self.practice.activities:
                messagebox.showwarning("Análisis", "Se extrajo el texto, pero no se detectaron actividades numeradas. Revisa el documento.")
        except Exception as exc:
            messagebox.showerror("No se pudo leer el documento", str(exc))

    def show_activity(self, _event=None):
        if not self.practice: return
        selection = self.activity_list.curselection()
        if not selection: return
        item = self.practice.activities[selection[0]]
        self.detail_title.configure(text=f"{item.number}. {item.kind.title()}")
        self.detail.configure(state="normal"); self.detail.delete("1.0", "end")
        self.detail.insert("1.0", f"{item.text}\n\nRespuesta:\n{item.answer or 'Pendiente de resolver.'}\n\nEstado: {item.status}\n\nEvidencias:\n" + "\n".join(item.evidence))
        self.detail.configure(state="disabled")

    def connect_mcp(self):
        cfg = load_config().get("mcp", {})
        command = cfg.get("command", "uvx")
        args = cfg.get("args", [])
        self.status.configure(text="Conectando con el servidor MCP…")
        self.connection.configure(text="● Conectando…", fg="#fbbf24")
        def worker():
            try:
                bridge = MCPBridge(command, args, cfg.get("env") or None)
                tools = bridge.connect(timeout=int(cfg.get("connect_timeout_seconds", 30)))
                self.after(0, lambda: self._mcp_connected(bridge, tools))
            except Exception as exc:
                self.after(0, lambda error=str(exc): self._mcp_failed(error))
        threading.Thread(target=worker, daemon=True).start()

    def _mcp_connected(self, bridge, tools):
        self.mcp = bridge
        self.connection.configure(text=f"● MCP conectado · {len(tools)} herramientas", fg=GREEN)
        self.status.configure(text="Servidor MCP conectado. Herramientas descubiertas dinámicamente.")
        names = ", ".join(t["name"] for t in tools[:8])
        self.detail.configure(state="normal"); self.detail.delete("1.0", "end")
        self.detail.insert("1.0", "Herramientas MCP detectadas:\n" + names + ("…" if len(tools) > 8 else ""))
        self.detail.configure(state="disabled")

    def _mcp_failed(self, error):
        self.connection.configure(text="● MCP sin conexión", fg="#f87171")
        self.status.configure(text=f"Error de conexión MCP: {error}")
        messagebox.showerror("No se pudo conectar", error)

    def capture_screen(self):
        cfg = load_config()
        workspace = Path(cfg["workspace"])
        name = Path(self.practice.source_file).stem if self.practice else "capturas"
        folder = create_evidence_dir(workspace, name)
        self.status.configure(text="Solicitando captura…")
        def worker():
            saved = []
            errors = []
            if self.mcp and self.mcp.connected:
                candidates = [t for t in self.mcp.tools if any(k in t["name"].lower() for k in ("screenshot", "ui_capture", "capture"))]
                for tool in candidates:
                    schema = tool.get("inputSchema") or {}
                    required = (schema.get("required") or [])
                    if required: continue
                    try:
                        result = self.mcp.call_tool(tool["name"], {})
                        saved.extend(save_mcp_capture(result, folder, tool["name"]))
                        if saved: break
                    except Exception as exc:
                        errors.append(str(exc))
            if not saved and cfg.get("capture", {}).get("fallback_screenshot", True):
                fallback = desktop_capture(folder, "pantalla_packet_tracer")
                if fallback: saved.append(fallback)
            self.after(0, lambda: self._capture_done(saved, errors))
        threading.Thread(target=worker, daemon=True).start()

    def _capture_done(self, saved, errors):
        if saved:
            if self.practice and self.practice.activities:
                self.practice.activities[0].evidence.extend(saved)
            self.status.configure(text=f"Captura/evidencia guardada: {saved[0]}")
            messagebox.showinfo("Evidencia guardada", "\n".join(saved[:4]))
        else:
            self.status.configure(text="No se obtuvo captura. Revisa la conexión y permisos.")
            messagebox.showwarning("Captura", "No se pudo obtener una imagen. " + ("; ".join(errors[:2]) if errors else "Verifica la configuración MCP y PyAutoGUI."))

    def export_report(self):
        if not self.practice:
            messagebox.showwarning("Informe", "Primero importa una práctica."); return
        try:
            folder = self.workflow.export(self.practice)
            self.status.configure(text=f"Informe generado en {folder}")
            messagebox.showinfo("Informe generado", str(folder / "informe.pdf"))
        except Exception as exc:
            messagebox.showerror("Error al generar informe", str(exc))

    def _close(self):
        if self._topology_job:
            try:
                self.after_cancel(self._topology_job)
            except tk.TclError:
                pass
            self._topology_job = None
        if self.mcp:
            self.mcp.disconnect()
        self.destroy()
