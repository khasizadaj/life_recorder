# We are using TDD to build new LifeRecorder class that performs
# common CRUD and search operations on life records. We should have single
# responsibility for each method and keep them small and focused in single
# class.

import json
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

from src.life_recorder.base import LifeRecorder


class TestLifeRecorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path_to_empty_db = "./tests/fixtures/empty_db.json"
        with open(cls.path_to_empty_db, "r") as f:
            cls.empty_db = json.load(f)
        cls.path_to_db = "./tests/fixtures/db.json"
        with open(cls.path_to_db, "r") as f:
            cls.db = json.load(f)

    def setUp(self) -> None:
        self.path_to_temp_db = shutil.copy(self.path_to_db, "test_db.json")
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(self.path_to_temp_db):
            os.remove(self.path_to_temp_db)
        return super().tearDown()

    def test_class_has_mandatory_methods(self):
        life_recorder = LifeRecorder()
        self.assertTrue(hasattr(life_recorder, "read"))

    def test_class_has_public_access_to_db(self):
        life_recorder = LifeRecorder()
        self.assertTrue(hasattr(life_recorder, "db"))

    def test_loading_empty_db(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_empty_db)
        self.assertEqual(life_recorder.records, {})
        self.assertEqual(life_recorder.db["last_id"], 0)

    def test_loading_db_with_records(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_db)
        self.assertEqual(life_recorder.records, self.db["records"])
        self.assertDictEqual(life_recorder.db, self.db)

    @patch("src.life_recorder.base.get_data_dir")
    def test_path_to_db(self, mock_get_data_dir):
        path_to_data_dir = "./mock"
        mock_get_data_dir.return_value = path_to_data_dir
        life_recorder = LifeRecorder()
        self.assertEqual(
            str(life_recorder.path_to_db),
            str(Path("./mock/life_records.json")),
        )

        shutil.rmtree(path_to_data_dir)

    def test_path_to_db_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            LifeRecorder(path_to_db="non_existent.json")

    def test_path_to_db_exists(self):
        path_to_db = "test.json"
        with open(path_to_db, "w") as f:
            f.write('{"last_id": 0, "records": {}}')

        life_recorder = LifeRecorder(path_to_db=path_to_db)
        self.assertEqual(str(life_recorder.path_to_db), str(Path(path_to_db)))

        os.remove(path_to_db)

    def test_create(self):
        new_note = {
            "tag": "test",
            "title": "Test Record",
            "content": "This is a test record.",
        }
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        result = life_recorder.create(new_note)
        self.assertIn("lr-4", life_recorder.records)
        self.assertCountEqual(
            list(result.keys()), ["id", "timestamp"] + list(new_note.keys())
        )
        for key, value in new_note.items():
            self.assertEqual(life_recorder.records["lr-4"][key], value)
        self.assertEqual(life_recorder.db["last_id"], 4)

        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        self.assertIn("lr-4", life_recorder.records)
        self.assertEqual(result, life_recorder.records["lr-4"])
        for key, value in new_note.items():
            self.assertEqual(life_recorder.records["lr-4"][key], value)

    def test_create_pass_invalid_input(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        with self.assertRaises(TypeError):
            life_recorder.create("invalid_input")  # type: ignore

        with self.assertRaises(TypeError):
            life_recorder.create(None)  # type: ignore

        with self.assertRaises(TypeError):
            life_recorder.create(1)  # type: ignore

        with self.assertRaises(ValueError):
            life_recorder.create({})

        with self.assertRaises(ValueError):
            life_recorder.create({"wrong_key": "test"})

    def test_read_all(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_db)
        records = life_recorder.read()
        self.assertEqual(records, self.db["records"])

    def test_read_one(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_db)
        record = life_recorder.read_one("lr-1")
        assert record is not None
        self.assertDictEqual(record, self.db["records"]["lr-1"])

        record = life_recorder.read_one("non_existent")
        self.assertIsNone(record)

    def test_delete(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        life_recorder.delete("lr-1")
        self.assertNotIn("lr-1", life_recorder.records)

        # Create a new LifeRecorder instance to verify that the deletion
        # persists in the database file.
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        self.assertNotIn("lr-1", life_recorder.records)

    def test_delete_raises_error_with_incorrect_key(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        with self.assertRaises(ValueError):
            life_recorder.delete("non_existent")

    def test_delete_raises_error_with_non_string_identifier(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_temp_db)
        with self.assertRaises(TypeError):
            life_recorder.delete(12345)  # type: ignore


if __name__ == "__main__":
    unittest.main()
