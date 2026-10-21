@echo off
cd /d "%~dp0\.."
python src\main.py --vfs "vfs_examples/several_files" --script "scripts/stage3_error.txt"