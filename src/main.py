import shlex
import tkinter as tk
from tkinter import scrolledtext


VFS_NAME = "virtual_fs"


def parse_command(command_line):
    """Разделяет строку на команду и аргументы с учетом кавычек."""
    try:
        return shlex.split(command_line, posix=True)
    except ValueError as error:
        raise ValueError(f"Ошибка разбора команды: {error}") from error


def execute_command(parts):
    """Выполняет команду или возвращает сообщение об ошибке."""
    command = parts[0]
    arguments = parts[1:]

    if command in ("ls", "cd"):
        if len(arguments) > 1:
            raise ValueError(
                f"{command}: слишком много аргументов"
            )
        return f"Команда: {command}\nАргументы: {arguments}"

    if command == "exit":
        if arguments:
            raise ValueError("exit: аргументы не поддерживаются")
        return None

    raise ValueError(f"{command}: команда не найдена")


class ShellEmulator:
    """Графический эмулятор командной оболочки."""

    def __init__(self, root):
        self.root = root
        self.root.title(f"Shell Emulator - {VFS_NAME}")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#171717",
            fg="#F0F0F0",
            insertbackground="white",
            state=tk.DISABLED
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        self.command_entry = tk.Entry(
            root,
            font=("Consolas", 12)
        )
        self.command_entry.pack(
            fill=tk.X, padx=10, pady=(0, 10)
        )
        self.command_entry.bind("<Return>", self.on_enter)
        self.command_entry.focus_set()

        self.write_output("Shell Emulator запущен.")
        self.write_output("Доступные команды: ls, cd, exit.\n")

    def write_output(self, text):
        """Добавляет текст в область вывода."""
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def on_enter(self, event):
        """Обрабатывает команду после нажатия Enter."""
        command_line = self.command_entry.get()
        self.command_entry.delete(0, tk.END)

        if not command_line.strip():
            return

        self.write_output(f"{VFS_NAME}:~$ {command_line}")

        try:
            parts = parse_command(command_line)
            if not parts:
                return

            result = execute_command(parts)

            if result is None:
                self.root.destroy()
                return

            self.write_output(result)

        except ValueError as error:
            self.write_output(f"Ошибка: {error}")


def main():
    """Создает окно и запускает эмулятор."""
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()