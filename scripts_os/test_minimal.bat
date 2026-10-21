@echo off
cd /d "%~dp0\.."
python src\main.py --vfs "vfs_examples/minimal" --script "scripts/stage3_error.txt"