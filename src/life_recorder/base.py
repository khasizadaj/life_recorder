"""
Module that provides `LifeRecorder` class for life record management.
"""

import json
import os
from pathlib import Path

from .helper import get_data_dir
from . import config


class LifeRecorder:
    def __init__(self, path_to_db: str | None = None):
        if path_to_db:
            self.path_to_db = Path(path_to_db)
            if not self.path_to_db.exists():
                raise FileNotFoundError(
                    f"Database file not found: {self.path_to_db}"
                )
        else:
            init_path_to_db = Path(
                os.path.join(get_data_dir(), "life_records.json")
            )
            if not init_path_to_db.exists():
                self._init_db(init_path_to_db)
            self.path_to_db = init_path_to_db
        self._db = self._load_database()

    def read(self):
        """Read all life records."""
        return self.records

    def read_one(self, identifier: str) -> dict[str, str] | None:
        """Read a single life record by its identifier."""
        return self.records.get(identifier, None)

    def delete(self, identifier: str):
        """Delete a life record by its identifier."""

        if isinstance(identifier, str) is False:
            raise TypeError("Identifier must be a string.")

        if identifier in self.records:
            del self.records[identifier]
            self._save_database()
        else:
            raise ValueError(f"No record found with identifier: {identifier}")

    def _load_database(self):
        """Load the database from the JSON file."""
        with open(self.path_to_db, "r") as f:
            return json.load(f)

    def _save_database(self):
        """Save the current state of the database to the JSON file."""
        with open(self.path_to_db, "w") as f:
            if config.DEBUG:
                json.dump(self._db, f, indent=4)
            else:
                json.dump(self._db, f)

    def _init_db(self, init_path_to_db: Path) -> None:
        """Initialize the database with default values."""
        init_path_to_db.parent.mkdir(parents=True, exist_ok=True)
        init_path_to_db.touch()
        with open(init_path_to_db, "w") as f:
            json.dump({"last_id": 0, "records": {}}, f)

    @property
    def db(self):
        """Return the database dictionary."""
        return self._db

    @property
    def records(self):
        """Return the records dictionary."""
        return self._db.get("records", {})
