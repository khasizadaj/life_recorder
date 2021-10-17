"""
This module contains LifeRecorder class which is used to work with records.
"""


import json


class LifeRecorder:
    """Class that implements writing and reading of life records."""

    _file_name = "life_records.json"
    input_messages = {
        "tag": "What is the tag of this record?: ",
        "content": "What do you want to remember? ",
        "read": "How many rows do you want to read?",
        "action": "What do you want to do, read (r) or write (w)? ",
        "delete": "Are you sure you want to delete this record? [Y(y) / N(n)] ",

    }

    def __init__(self):
        self._database = self.load_database()

    def act(self, identifier: str = None):
        """This method implements main purpose of current class."""
        raise NotImplementedError()

    @property
    def database(self):
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


if __name__ == "__main__":
    print(__doc__)
