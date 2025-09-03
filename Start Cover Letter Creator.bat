@echo off
cd /d %~dp0
call venv\Scripts\activate
python cv_creator\app.py
