"""Module contains helper functions for LifeRecorder class."""

from datetime import datetime
from typing import Union


def get_timestamp() -> str:
    """Function returns the timestamp."""

    return datetime.now().strftime("%d-%b-%Y %H:%M")


def generate_record_string(tag: str, content: str):
    """Returns formatted life log."""

    timestamp = get_timestamp()
    return f"{timestamp}; {tag}; {content}"


def write_headers(file_object) -> None:
    """Writes headers to the file."""

    file_object.write("timestamp; tag; content\n")


def print_line_of_record(identifier: str, record: str) -> None:
    """Prints a record with provided identifier (id)."""

    print(f"{identifier} | {record}")


def get_identifier(row_num: int) -> Union[str, int]:
    """Returns the identifier of the given row"""

    if row_num == 0:
        return "+"
    return row_num
