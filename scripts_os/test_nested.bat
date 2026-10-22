@echo off
cd /d "%~dp0\.."
python src\shell_emulator.py --vfs "vfs_examples/nested" --script "scripts/stage3_error.txt"
