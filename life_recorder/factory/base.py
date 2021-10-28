"""
This module contains LifeRecorder class which is used to work with records.
"""


import json


class Commands():
    """Class contains commands an strings which can be used to perform this command."""

    def __init__(self):
        self.create = ["create", "c", "C"]
        self.read = ["read", "r", "R"]
        self.update = ["update", "u", "U"]
        self.delete = ["delete", "d", "D"]

    def get_type(self, command):
        """
        Method returns the command type, i.e. number that represents identifier
        requirement of a command.

        0: requires no identifier
        1: requires identifier
        2: identifier is optional or it's hybrid

        """
        if command in self._no_identifier_commands:
            status = 0
        elif command in self._only_with_identifier:
            status = 1
        elif command in self._hybrid_commands:
            status = 2

        return status

    @property
    def _no_identifier_commands(self):
        return [*self.create]

    @property
    def _only_with_identifier(self):
        return [*self.update, *self.delete]

    @property
    def _hybrid_commands(self):
        return [*self.read]

    @property
    def all_commands(self):
        return [*self.create, *self.read, *self.update, *self.delete]


COMMANDS = Commands()


class LifeRecorder:
    """Class that implements writing and reading of life records."""

    _file_name = "life_records.json"

    def __init__(self):
        self._database = self.load_database()
        self.input_messages = {}

    def act(self, identifier: str = None):
        """This method implements main purpose of current class."""

        raise NotImplementedError()

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
            with open(self._file_name, "r") as file:
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

        with open(self.file_name, "w") as output:
            json.dump(records, output)

    @staticmethod
    def get_empty_database():
        """Function returns an empty database to start saving data."""

        return {
            "last_id": 0,
            "records": {}
        }


if __name__ == "__main__":
    print(__doc__)
