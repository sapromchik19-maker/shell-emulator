@echo off
cd /d "%~dp0\.."
python src\shell_emulator.py --script "scripts/start.txt"
