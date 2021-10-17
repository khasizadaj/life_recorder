"""Module contains helper functions for LifeRecorder class."""

from datetime import datetime
from typing import Dict


def get_timestamp() -> str:
    """Function returns the timestamp."""

    return datetime.now().strftime("%d-%b-%Y %H:%M")


def update_database(database: Dict, record: Dict) -> Dict:
    """Function updates database."""
    cp_database = database.copy()

    cp_database["records"][str(record["id"])] = record

    return cp_database


def delete_record(database: Dict, identifier: str) -> Dict:
    """Function deletes record from database with given identifier."""

    cp_database = database.copy()
    del cp_database["records"][identifier]
    return cp_database


def get_record(records: Dict, identifier: str) -> Dict:
    """Returns dictionary of single record that matches given identifier."""

    return records.get(identifier, None)


def print_pretty_record(record: str) -> None:
    """Prints a record with provided identifier (id)."""

    print(f"#{record['id']} {record['tag']} - {record['content']}")
