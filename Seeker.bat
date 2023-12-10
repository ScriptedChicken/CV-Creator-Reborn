@echo off
cd /d %~dp0

rem Assuming your virtual environment is in a folder named "venv" within the script's directory
call venv\Scripts\activate

python app.py

rem Deactivate the virtual environment after running the script
deactivate
