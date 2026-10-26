@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [1/3] Tao moi truong Python rieng (.venv)...
python -m venv .venv || (echo Loi: chua cai Python. Xem README buoc 1. & pause & exit /b)
echo [2/3] Cai thu vien...
.venv\Scripts\python -m pip install -r requirements.txt
echo [3/3] Tao file .env...
if not exist .env copy .env.example .env >nul
echo.
echo XONG! Bay gio chay: chay.bat
pause
