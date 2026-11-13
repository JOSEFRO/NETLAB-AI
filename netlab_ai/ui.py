from __future__ import annotations
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from .workflow import PracticeWorkflow
from .config import load_config

BG = "#0b1220"
PANEL = "#111c2e"
PANEL2 = "#17243a"
TEXT = "#e5edf8"
MUTED = "#91a3bb"
ACCENT = "#38bdf8"
GREEN = "#34d399"

class NetLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NETLAB AI | Centro de operaciones")
        self.geometry("1440x900")
        self.minsize(1120, 720)
        self.configure(bg=BG)
        self.workflow = PracticeWorkflow()
        self.practice = None
        self._style()
        self._build()

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
        left = self._panel(body, 250)
        left.pack(side="left", fill="y", padx=(0, 10))
        center = self._panel(body)
        center.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = self._panel(body, 270)
        right.pack(side="right", fill="y")

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
        frame = tk.Frame(parent, bg=PANEL, highlightbackground="#24364e", highlightthickness=1, width=width or 0)
        if width:
            frame.pack_propagate(False)
        return frame

    def _heading(self, parent, text):
        tk.Label(parent, text=text, bg=PANEL, fg=ACCENT, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(14, 4))

    def _button(self, parent, text, command, secondary=False):
        return tk.Button(parent, text=text, command=command, bg=PANEL2 if secondary else "#075985", fg=TEXT, activebackground="#0e7490", activeforeground="white", relief="flat", bd=0, padx=14, pady=9, font=("Segoe UI", 9, "bold"), cursor="hand2")

    def _draw_placeholder(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 50 or h < 50:
            return
        self.canvas.create_text(w/2, h/2-40, text="ÁREA CENTRAL DE TOPOLOGÍA", fill=ACCENT, font=("Segoe UI", 15, "bold"))
        self.canvas.create_text(w/2, h/2, text="Conecta MCP y abre un laboratorio para visualizar Packet Tracer.", fill=MUTED, font=("Segoe UI", 10))
        self.canvas.create_text(w/2, h/2+34, text="El panel central es una vista de trabajo; la topología real vive en Packet Tracer.", fill="#64748b", font=("Segoe UI", 8))

    def import_file(self):
        path = filedialog.askopenfilename(title="Seleccionar práctica", filetypes=[("Documentos", "*.pdf *.docx *.txt *.md *.png *.jpg *.jpeg"), ("Todos", "*.*")])
        if not path:
            return
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
                messagebox.showwarning("Análisis", "Se extrajo el texto, pero no se detectaron preguntas o instrucciones numeradas. Revisa el documento.")
        except Exception as exc:
            messagebox.showerror("No se pudo leer el documento", str(exc))

    def show_activity(self, _event=None):
        if not self.practice:
            return
        selection = self.activity_list.curselection()
        if not selection:
            return
        item = self.practice.activities[selection[0]]
        self.detail_title.configure(text=f"{item.number}. {item.kind.title()}")
        self.detail.configure(state="normal")
        self.detail.delete("1.0", "end")
        self.detail.insert("1.0", f"{item.text}\n\nRespuesta:\n{item.answer or 'Pendiente de resolver.'}\n\nEstado: {item.status}\n\nEvidencias:\n" + "\n".join(item.evidence))
        self.detail.configure(state="disabled")

    def connect_mcp(self):
        messagebox.showinfo("Conexión MCP", "La conexión MCP se configura en config/settings.json. Este primer corte incluye la interfaz y el analizador; el adaptador de ejecución se está preparando.")
        self.connection.configure(text="● MCP por configurar", fg="#fbbf24")

    def capture_screen(self):
        from .evidence import desktop_capture
        from pathlib import Path
        cfg = load_config()
        folder = Path(cfg["workspace"]) / (Path(self.practice.source_file).stem if self.practice else "capturas") / "evidencias"
        folder.mkdir(parents=True, exist_ok=True)
        result = desktop_capture(folder, "pantalla")
        if result:
            if self.practice:
                self.practice.activities[0].evidence.append(result) if self.practice.activities else None
            self.status.configure(text=f"Captura guardada: {result}")
            messagebox.showinfo("Captura guardada", result)
        else:
            messagebox.showwarning("Captura", "No se pudo capturar la pantalla. Comprueba los permisos y PyAutoGUI.")

    def export_report(self):
        if not self.practice:
            messagebox.showwarning("Informe", "Primero importa una práctica.")
            return
        try:
            folder = self.workflow.export(self.practice)
            self.status.configure(text=f"Informe generado en {folder}")
            messagebox.showinfo("Informe generado", str(folder / "informe.pdf"))
        except Exception as exc:
            messagebox.showerror("Error al generar informe", str(exc))
