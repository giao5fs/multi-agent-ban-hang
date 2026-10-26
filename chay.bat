@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
echo Chon bai muon chay:
echo   1 - Mot agent
echo   2 - Nhieu agent + do thi (tu viet)
echo   3 - Nhieu agent voi LangGraph
set /p BAI=Nhap so (1/2/3): 
if "%BAI%"=="1" .venv\Scripts\python bai1_mot_agent.py
if "%BAI%"=="2" .venv\Scripts\python bai2_do_thi_tu_viet.py
if "%BAI%"=="3" .venv\Scripts\python bai3_langgraph.py
pause
