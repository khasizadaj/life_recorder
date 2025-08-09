"""
This module contains LifeRecorder class which is used to work with records.
"""


from enum import Enum
import json
import os

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from life_recorder.helper import get_data_dir


class Commands(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

    def __eq__(self, other):
        return self.value == other


class LifeRecorder(ABC):
    """Class that implements writing and reading of life records."""

    _file_name = "life_records.json"
    _data_dir = get_data_dir()

    def __init__(self):
        self._database = self.load_database()
        self.input_messages = {}

    @abstractmethod
    def act(self, identifier: Union[str, None] = None):
        """This method implements main purpose of current class."""

        pass

    @property
    def database(self):
        """Function return database attribute of the class."""

        return self._database

    @property
    def records(self):
        """Function returns records saved so far."""

        return self._database["records"]

    @property
    def file_name(self):
        """Function returns the file name variable."""

        return self._file_name

    def load_database(self):
        """This property return a dictionary of records."""

        try:
            with open(self.path_to_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return self.get_empty_database()

    def get_input_message(self, input_type: str):
        """Function returns the input message for the given input type."""

        if input_type not in self.input_messages.keys():
            raise KeyError(f"There is no such input type: {input_type}")

        return self.input_messages[input_type]

    def save_records(self, records: str) -> None:
        """Writes life log to file."""

        with open(self.path_to_file, "w") as output:
            json.dump(records, output)

    @property
    def path_to_file(self) -> str:
        """Property method that returns the path to the file."""

        return self.get_path_to_file()

    def get_path_to_file(self):
        """
        Method returns the path to the file. 
        If there is `.data` directory,it will make new one and return it.
        """

        data_dir = Path(self._data_dir)
        is_dir = os.path.isdir(data_dir)
        if is_dir:
            pass
        else:
            os.mkdir(data_dir)

        data_dir = Path.joinpath(data_dir, self.file_name)
        return data_dir

    @staticmethod
    def get_empty_database():
        """Function returns an empty database to start saving data."""

        return {
            "last_id": 0,
            "records": {}
        }


if __name__ == "__main__":
    print(__doc__)
