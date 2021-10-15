"""This module contains LifeRecorder class which is used to work with records."""

from life_recorder.helper import (generate_life_record_string, get_identifier,
                                  print_line_of_record, write_headers)


class LifeRecorder:
    """Class that implements writing and reading of life records."""

    input_messages = {
        "tag": "What is the tag of this record?: ",
        "content": "What do you want to remember? ",
        "read": "How many rows do you want to read?",
        "action": "What do you want to do, read (r) or write (w)? ",
    }

    def __init__(self, file_name):
        self._file_name = file_name

    def get_input_message(self, input_type: str):
        """Function returns the input message for the given input type."""

        if input_type not in self.input_messages.keys():
            raise KeyError(f"There is no such input type: {input_type}")

        return self.input_messages[input_type]

    def add_life_record(self) -> None:
        """Add a new life record to file"""

        record = self.get_life_record()
        self.write_life_record(record)

    def get_life_record(self):
        """Function adds new log to the file and returns the last added log."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # create life record
        record = generate_life_record_string(tag, content)

        return record

    def write_life_record(self, record: str) -> None:
        """Writes life log to file."""

        records_exist = self.check_for_record()
        with open(self.file_name, 'a+') as file_object:
            if records_exist is False:
                write_headers(file_object)
            file_object.write(f"{record}\n")

        print(f"Last life log: {record}")

    def read_records(self, row_count: int = None) -> None:
        """
        Function reads given amount (`row_count`) of records from the beginning
        of the file. If row_count is not specified it reads the whole document.

        Header of the file is not taken into account as a record.
        """

        if row_count is None:
            # it represents infinite number of records
            row_count = 100_000

        with open(self.file_name, 'r') as file_object:
            for i in range(row_count + 1):
                identifier = get_identifier(i)
                curr_record = file_object.readline().strip("\n")
                if curr_record == "":
                    return None
                print_line_of_record(identifier, curr_record)

        return None

    @property
    def file_name(self):
        """Function returns the file name variable."""
        return self._file_name

    def check_for_record(self) -> bool:
        """
        Function returns the boolean value indicating whether there is any
        records in the file.
        """
        try:
            with open(self.file_name, 'r') as file_object:
                return file_object.read() != ""
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    print(__doc__)
