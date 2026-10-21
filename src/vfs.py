import hashlib
import shutil
from pathlib import Path


class VirtualFileSystem:
    """Виртуальная файловая система, хранящая данные в памяти."""

    def __init__(self, path):
        """Создаёт VFS и загружает файлы из указанной директории."""
        self.path = Path(path)
        self.name = self.path.name
        self.files = {}

        self.load()

    def load(self):
        """Загружает файлы и каталоги VFS в память."""
        if not self.path.exists():
            raise FileNotFoundError(
                f"VFS не найдена: {self.path}"
            )

        if not self.path.is_dir() or self.path.is_symlink():
            raise ValueError(
                f"Некорректная директория VFS: {self.path}"
            )

        files = {}

        for item in sorted(self.path.rglob("*")):
            relative_path = item.relative_to(self.path).as_posix()

            if item.is_symlink():
                raise ValueError(
                    f"Символическая ссылка запрещена: {relative_path}"
                )

            if item.is_dir():
                files[relative_path] = None
            elif item.is_file():
                files[relative_path] = item.read_bytes()
            else:
                raise ValueError(
                    f"Неподдерживаемый элемент: {relative_path}"
                )

        self.files = files

    def get_hash(self):
        """Вычисляет SHA-256 виртуальной файловой системы."""
        hasher = hashlib.sha256()

        for path in sorted(self.files):
            content = self.files[path]
            path_bytes = path.encode("utf-8")

            hasher.update(len(path_bytes).to_bytes(8, "big"))
            hasher.update(path_bytes)

            if content is None:
                hasher.update(b"D")
            else:
                hasher.update(b"F")
                hasher.update(len(content).to_bytes(8, "big"))
                hasher.update(content)

        return hasher.hexdigest()

    def reset(self):
        """Сбрасывает рабочую VFS к пустому состоянию."""
        work_root = (
                Path(__file__).resolve().parents[1] / "vfs_work"
        ).resolve()

        current_path = self.path.resolve()

        if current_path.parent != work_root:
            raise ValueError(
                "vfs-init разрешена только для VFS из vfs_work"
            )

        if not current_path.is_dir():
            raise ValueError("Директория VFS не найдена")

        for item in current_path.iterdir():
            if item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        self.files.clear()