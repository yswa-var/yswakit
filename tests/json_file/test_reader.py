import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from yswakit.json_file import JsonFileReader, JsonRootTypeError


class JsonFileReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = JsonFileReader()

    def test_reads_json_object_as_dictionary(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(
                '{"host": "localhost", "port": 8123, "flags": ["fast"]}',
                encoding="utf-8",
            )

            result = self.reader.read(path)

        self.assertEqual(
            result,
            {"host": "localhost", "port": 8123, "flags": ["fast"]},
        )

    def test_rejects_non_object_root(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "items.json"
            path.write_text('["one", "two"]', encoding="utf-8")

            with self.assertRaisesRegex(JsonRootTypeError, "got list"):
                self.reader.read(path)

    def test_invalid_json_raises_decode_error(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text('{"missing": true', encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                self.reader.read(path)

    def test_missing_file_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.reader.read("does-not-exist.json")

    def test_empty_encoding_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "encoding must not be empty"):
            JsonFileReader(encoding="")


if __name__ == "__main__":
    unittest.main()
