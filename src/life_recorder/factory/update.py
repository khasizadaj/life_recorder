"""Module contains class that adds new records to the database."""

import sys
from typing import Tuple, Dict, Union

from life_recorder import helper as h
from .base import LifeRecorder


class UpdateLifeRecorder(LifeRecorder):
    """Implements adding life records to the database."""

    def __init__(self):
        super().__init__()
        self.input_messages["tag"] = "What is the updated tag? (optional): "
        self.input_messages["title"] = "What is the updated title?: "
        self.input_messages["content"] = "What is the updated content?: "

    def act(self, identifier: Union[str, None] = None):
        """Add a new life record to database."""

        if identifier is None:
            message = "In order to update any record, you need to specify an identifier."
            h.add_breakline(print, func_args=[message], both=True)
            sys.exit()

        old_record = h.get_record(self.records, str(identifier))

        if old_record is None:
            message = "Provided identifier didn't match with any record."
            h.add_breakline(print, func_args=[message], after=True)
            sys.exit()

        print("Current record:")
        h.add_breakline(h.print_pretty_record, func_args=[
                        old_record], after=True)

        print('Usage: Add new detail for respective field. If you want to keep '
              'any value untouched, press "Enter".')

        tag, title, content = self.compare_new_details(
            old_record, *self.get_record_details())

        record = h.construct_record_dict(old_record["id"], old_record["timestamp"],
                                         tag, title, content)

        updated_database = h.update_database(self.database, record)
        self.save_records(updated_database)

        message = f"Record with #{record['id']} is updated."
        h.add_breakline(print, func_args=[message], after=True)

    @staticmethod
    def compare_new_details(old_record: Dict, tag: str, title: str, content: str):
        """
        Check if provided tag and content are really new ones. 
        If empty value is provide, it means that user doesn't wanna change it.
        """

        if tag == "":
            tag = old_record['tag']

        if title == "":
            title = old_record['title']

        if content == "":
            content = old_record['content']

        return tag, title, content

    def get_record_details(self) -> Tuple:
        """Function gets and returns inputs from user."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        input_message = self.get_input_message("title")
        title = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # return user inputs
        return tag, title, content


if __name__ == "__main__":
    print(__doc__)
