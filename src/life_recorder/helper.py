"""Module contains helper functions for LifeRecorder class."""

from datetime import datetime
import os
import click
from rich import print
from typing import Dict, List

from . import config


def get_timestamp() -> str:
    """Function returns the timestamp."""

    return datetime.now().strftime("%d-%b-%Y %H:%M")


def update_database(database: Dict, record: Dict) -> Dict:
    """Function updates database."""
    cp_database = database.copy()

    cp_database["records"][str(record["id"])] = record

    return cp_database


def construct_record_dict(identifier: str, timestamp: str, tag: str, title: str,
                          content: str) -> Dict:
    """Returns dictionary of record."""

    return {
        "id": identifier,
        "timestamp": timestamp,
        "tag": tag,
        "title": title,
        "content": content
    }


def delete_record(database: Dict, identifier: str) -> Dict:
    """Function deletes record from database with given identifier."""

    cp_database = database.copy()
    del cp_database["records"][identifier]
    return cp_database


def get_record(records: Dict, identifier: str) -> Dict:
    """Returns dictionary of single record that matches given identifier."""

    return records.get(identifier, None)


def add_breakline(func, func_args: List, before: bool = False,
                  after: bool = False, both: bool = False) -> None:
    """Function adding breaklines depending on arguments provided."""

    if before:
        print()
        func(*func_args)

    elif after:
        func(*func_args)
        print()
    elif both:
        print()
        func(*func_args)
        print()

def pretty_record(record: dict) -> str:
    """Returns a pretty-printed string of a record."""

    return (
        f"{click.style('Id:', fg='white')} #{record['id']} \n"
        f"{click.style('Timestamp:', fg='white')} {record['timestamp']} \n"
        f"{click.style('Tag:', fg='white')} {record['tag']} \n"
        f"{click.style('Title:', fg='white')} {record['title']} \n"
        f"{click.style('Content:', fg='white')} {record['content']}"
    )


def print_pretty_record(record: dict) -> None:
    click.echo(pretty_record(record))


def get_user() -> str:
    """Function returns the user name."""

    path = os.path.expanduser("~")
    return os.path.basename(path)


def get_data_dir() -> str:
    """Function returns the data directory of the program."""

    if config.DEBUG:
        return "./data"

    return os.path.join(os.path.expanduser('~'), '.data')
