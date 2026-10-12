import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from yswakit.json_file import JsonFileStore


class JsonFileStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = JsonFileStore()

    def test_updates_selected_keys_and_preserves_others(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(
                '{"host": "localhost", "port": 8123, "debug": false}',
                encoding="utf-8",
            )

            result = self.store.update(path, {"port": 9000, "debug": True})
            saved = json.loads(path.read_text(encoding="utf-8"))

        expected = {"host": "localhost", "port": 9000, "debug": True}
        self.assertEqual(result, expected)
        self.assertEqual(saved, expected)

    def test_update_is_shallow(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(
                '{"database": {"host": "old", "port": 8123}}',
                encoding="utf-8",
            )

            result = self.store.update(path, {"database": {"host": "new"}})

        self.assertEqual(result, {"database": {"host": "new"}})

    def test_write_creates_json_object_file(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "new.json"

            result = self.store.write(path, {"enabled": True})

            self.assertEqual(result, {"enabled": True})
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                {"enabled": True},
            )

    def test_serialization_failure_preserves_original_file(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            original = '{"host": "localhost"}\n'
            path.write_text(original, encoding="utf-8")

            with self.assertRaises(TypeError):
                self.store.update(path, {"unsupported": object()})

            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_updating_missing_file_raises_file_not_found(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            with self.assertRaises(FileNotFoundError):
                self.store.update(path, {"enabled": True})


if __name__ == "__main__":
    unittest.main()
