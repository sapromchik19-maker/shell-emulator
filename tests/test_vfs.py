import sys
import unittest
import hashlib
import tempfile
import shutil
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vfs import VirtualFileSystem


class TestVFS(unittest.TestCase):
    """Проверки загрузки виртуальной файловой системы."""

    def test_minimal(self):
        vfs = VirtualFileSystem("vfs_examples/minimal")

        self.assertEqual(vfs.name, "minimal")
        self.assertIn("readme.txt", vfs.files)

    def test_several_files(self):
        vfs = VirtualFileSystem("vfs_examples/several_files")

        self.assertEqual(len(vfs.files), 3)
        self.assertIn("first.txt", vfs.files)

    def test_nested(self):
        vfs = VirtualFileSystem("vfs_examples/nested")

        self.assertIn("documents", vfs.files)
        self.assertIn("documents/university", vfs.files)
        self.assertIn(
            "documents/university/practice/report.txt",
            vfs.files
        )

    def test_missing_directory(self):
        with self.assertRaises(FileNotFoundError):
            VirtualFileSystem("vfs_examples/missing")

    def test_hash(self):
        """Проверяет правильность формата SHA-256."""
        vfs = VirtualFileSystem("vfs_examples/minimal")

        result = vfs.get_hash()

        self.assertEqual(len(result), 64)
        self.assertTrue(
            all(char in "0123456789abcdef" for char in result)
        )

    def test_hash_repeat(self):
        """Проверяет, что хеш не меняется без изменений VFS."""
        vfs = VirtualFileSystem("vfs_examples/nested")

        first_hash = vfs.get_hash()
        second_hash = vfs.get_hash()

        self.assertEqual(first_hash, second_hash)

    def test_hash_changes(self):
        """Проверяет изменение хеша при изменении данных в памяти."""
        vfs = VirtualFileSystem("vfs_examples/minimal")

        old_hash = vfs.get_hash()
        vfs.files["new.txt"] = b"New file"

        self.assertNotEqual(old_hash, vfs.get_hash())

    def test_reset_protection(self):
        """Проверяет защиту исходной VFS от удаления."""
        vfs = VirtualFileSystem("vfs_examples/minimal")

        with self.assertRaises(ValueError):
            vfs.reset()

        self.assertIn("readme.txt", vfs.files)

    def test_reset_success(self):
        """Проверяет успешный сброс рабочей VFS."""
        work_root = Path(__file__).resolve().parents[1] / "vfs_work"
        test_path = work_root / f"test_{uuid.uuid4().hex}"

        test_path.mkdir(parents=True)

        try:
            (test_path / "file.txt").write_text("Test", encoding="utf-8")

            vfs = VirtualFileSystem(test_path)
            self.assertIn("file.txt", vfs.files)

            vfs.reset()

            self.assertEqual(vfs.files, {})
            self.assertEqual(list(test_path.iterdir()), [])
        finally:
            shutil.rmtree(test_path, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()