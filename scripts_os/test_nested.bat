@echo off
cd /d "%~dp0\.."
python src\main.py --vfs "vfs_examples/nested" --script "scripts/stage3_error.txt"