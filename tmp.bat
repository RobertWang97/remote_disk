@echo off
wmic process where "name='python.exe'" get name | find "python.exe" >nul
if errorlevel 1 (
    start python.exe
) else (
    echo python is already running.
)
pause