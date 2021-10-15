"""This module contains LifeRecorder class which is used to work with records."""

from life_recorder.helper import (generate_record_string, get_identifier,
                                  print_line_of_record, write_headers)


class LifeRecorder:
    """Class that implements writing and reading of life records."""

    _file_name = "life_records.csv"
    input_messages = {
        "tag": "What is the tag of this record?: ",
        "content": "What do you want to remember? ",
        "read": "How many rows do you want to read?",
        "action": "What do you want to do, read (r) or write (w)? ",
    }

    def get_input_message(self, input_type: str):
        """Function returns the input message for the given input type."""

        if input_type not in self.input_messages.keys():
            raise KeyError(f"There is no such input type: {input_type}")

        return self.input_messages[input_type]

    def add_record(self) -> None:
        """Add a new life record to file"""

        record = self.get_record()
        self.write_record(record)

    def get_record(self):
        """Function adds new log to the file and returns the last added log."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # create life record
        record = generate_record_string(tag, content)

        return record

    def write_record(self, record: str) -> None:
        """Writes life log to file."""

        records_exist = self.check_for_record()
        with open(self.file_name, 'a+') as file_object:
            if records_exist is False:
                write_headers(file_object)
            file_object.write(f"{record}\n")

        print(f"Last life log: {record}")

    def get_all_records(self):
        with open(self.file_name, 'r') as file_object:
            return file_object.read().split("\n")

    def get_single_record(self, identifier: int) -> str:
        raise NotImplementedError()

    def read_records(self, identifier: int = None) -> None:
        """
        Function reads given amount (`row_count`) of records from the beginning
        of the file. If row_count is not specified it reads the whole document.

        Header of the file is not taken into account as a record.
        """

        if identifier is not None:
            record = self.get_single_record(identifier)
            print(record)

        for record in self.get_all_records():
            print(record)
        
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
