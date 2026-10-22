@echo off
cd /d "%~dp0\.."
python src\shell_emulator.py --vfs "vfs_examples/several_files" --script "scripts/stage3_error.txt"
