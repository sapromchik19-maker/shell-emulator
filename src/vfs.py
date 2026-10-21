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
        """Загружает структуру каталогов и файлы в память."""
        if not self.path.exists():
            raise FileNotFoundError(
                f"VFS не найдена: {self.path}"
            )

        if not self.path.is_dir():
            raise ValueError(
                f"Путь VFS не является директорией: {self.path}"
            )

        self.files.clear()

        for item in sorted(self.path.rglob("*")):
            relative_path = item.relative_to(self.path).as_posix()

            if item.is_dir():
                self.files[relative_path] = None
            elif item.is_file():
                self.files[relative_path] = item.read_bytes()
            else:
                raise ValueError(
                    f"Неподдерживаемый элемент VFS: {relative_path}"
                )
    def get_hash(self):
        """Вычисляет SHA-256 виртуальной файловой системы."""
        hasher = hashlib.sha256()

        for path in sorted(self.files):
            content = self.files[path]

            hasher.update(path.encode("utf-8"))

            if content is None:
                hasher.update(b"DIRECTORY")
            else:
                hasher.update(b"FILE")
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