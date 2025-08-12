# We are using TDD to build new LifeRecorder class that performs
# common CRUD and search operations on life records. We should have single
# responsibility for each method and keep them small and focused in single
# class.

import json
import json
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

from life_recorder.base import LifeRecorder


class TestLifeRecorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path_to_empty_db = "./tests/fixtures/empty_db.json"
        with open(cls.path_to_empty_db, "r") as f:
            cls.empty_db = json.load(f)
        cls.path_to_db = "./tests/fixtures/db.json"
        with open(cls.path_to_db, "r") as f:
            cls.db = json.load(f)

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

    @patch("life_recorder.base.get_data_dir")
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

    def test_read_all(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_db)
        records = life_recorder.read()
        self.assertEqual(records, self.db["records"])

    def test_read_one(self):
        life_recorder = LifeRecorder(path_to_db=self.path_to_db)
        record = life_recorder.read_one("lr-1")
        self.assertDictEqual(record, self.db["records"]["lr-1"])

        record = life_recorder.read_one("non_existent")
        self.assertIsNone(record)


if __name__ == "__main__":
    unittest.main()
