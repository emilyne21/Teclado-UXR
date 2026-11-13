@echo off
cd /d "%~dp0"
echo Creando entorno virtual en .venv ...
py -3.9 -m venv .venv || py -3 -m venv .venv || python -m venv .venv
if not exist .venv\Scripts\python.exe (
  echo No se pudo crear el entorno. Instala Python 3.9 o superior desde python.org
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
echo.
echo Listo. Ahora abre iniciar_mouse.bat o iniciar_tobii.bat
pause
