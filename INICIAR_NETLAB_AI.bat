@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 (
    echo No se pudo crear el entorno. Instala Python 3.11 o superior.
    pause
    exit /b 1
  )
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist "config\settings.json" copy "config\settings.example.json" "config\settings.json" >nul
python main.py
if errorlevel 1 pause
