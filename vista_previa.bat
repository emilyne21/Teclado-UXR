@echo off
cd /d "%~dp0"
.venv\Scripts\python.exe main.py --preview
echo Imagenes guardadas en la carpeta previews
pause
