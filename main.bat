@echo off
wmic process where "name='python.exe'" get name | find "python.exe" >nul
if errorlevel 1 (
    start python C:\self-learning\remote_disk\main.py -seconds 5 -s C:\self-learning\uucopy\source -t C:\self-learning\uucopy\target -dir %~dp0
) else (
    echo python is already running.
)