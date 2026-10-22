@echo off
cd /d "%~dp0\.."
python src\shell_emulator.py --vfs "vfs_examples/minimal" --script "scripts/stage3_error.txt"
