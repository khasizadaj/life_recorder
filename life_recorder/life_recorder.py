"""This module contains LifeRecorder class which is used to work with records.
TODO Adding unique identifier for each record. (get_identifier method)"""

from abc import ABC, abstractmethod
from typing import Dict
import json

from life_recorder import helper


class LifeRecorder(ABC):
    """Class that implements writing and reading of life records."""

    _file_name = "life_records.json"
    input_messages = {
        "tag": "What is the tag of this record?: ",
        "content": "What do you want to remember? ",
        "read": "How many rows do you want to read?",
        "action": "What do you want to do, read (r) or write (w)? ",
    }

    def __init__(self):
        self._records = self.get_records()

    @abstractmethod
    def act(self):
        """Implement main purpose of the current class."""

    @property
    def records(self):
        """Function returns records saved so far."""

        return self._records

    def get_records(self):
        """This property return a dictionary of records."""

        try:
            with open(self._file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def get_input_message(self, input_type: str):
        """Function returns the input message for the given input type."""

        if input_type not in self.input_messages.keys():
            raise KeyError(f"There is no such input type: {input_type}")

        return self.input_messages[input_type]

    def save_records(self, records: str) -> None:
        """Writes life log to file."""

        with open(self.file_name, "w") as output:
            json.dump(records, output)

    @property
    def file_name(self):
        """Function returns the file name variable."""
        return self._file_name


class AddLifeRecorder(LifeRecorder):
    """Implements adding life records to the file."""

    def act(self) -> None:
        """Add a new life record to file"""

        record = self.get_record()
        curr_records = helper.update_records(self.records, record)
        self.save_records(curr_records)

        print(
            f"Last life record: #{record['id']}: {record['tag']} - {record['content']}")

    def get_record(self):
        """Function adds new log to the file and returns the last added log."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # create life record
        record = self.create_record_dict(tag, content)

        return record

    def get_identifier(self, i):
        return i

    def create_record_dict(self, tag: str, content: str):
        """Returns dictionary of record."""
        identifier = self.get_identifier("5")
        timestamp = helper.get_timestamp()

        return {
            "id": identifier,
            "timestamp": timestamp,
            "tag": tag,
            "content": content
        }


class ReadLifeRecorder(LifeRecorder):
    """Implements reading life records from the file."""

    def act(self, identifier: int = None) -> None:
        """
        Function reads given amount of records (`row_count`) from the beginning
        of the file. If row_count is not specified it reads the whole document.

        Header of the file is not taken into account as a record.
        """

        if identifier is not None:
            record = self.get_single_record(identifier)
            helper.print_pretty_record(record)
            return

        for record in self.get_all_records():
            helper.print_pretty_record(record)
        return

    def get_all_records(self):
        """Function return all records that saved so far."""

        return self.records.values()

    def get_single_record(self, identifier) -> Dict:
        """Returns dictionary of single record that matches given identifier."""

        return self.records[identifier]


if __name__ == "__main__":
    print(__doc__)
