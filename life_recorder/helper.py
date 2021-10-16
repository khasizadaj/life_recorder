"""Module contains helper functions for LifeRecorder class."""

from datetime import datetime
from typing import Union, Dict


def get_timestamp() -> str:
    """Function returns the timestamp."""

    return datetime.now().strftime("%d-%b-%Y %H:%M")

def update_records(records: Dict, new_record: Dict) -> Dict:
    """Function adds record to the records dictionary"""

    records[new_record["id"]] = new_record

    return records

def print_pretty_record(record: str) -> None:
    """Prints a record with provided identifier (id)."""

    print(f"#{record['id']} {record['tag']} - {record['content']}")


def get_identifier(row_num: int) -> Union[str, int]:
    """Returns the identifier of the given row"""

    if row_num == 0:
        return "+"
    return row_num
