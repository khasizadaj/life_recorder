"""Module contains class that adds new records to the database."""

import sys
from typing import Tuple, Dict

from . import life_recorder, helper


class UpdateLifeRecorder(life_recorder.LifeRecorder):
    """Implements adding life records to the database."""

    def act(self, identifier: int = None) -> None:
        """Add a new life record to database."""

        if identifier is None:
            print("In order to update any record, you need to specify an identifier.")
            print()
            sys.exit()

        old_record = helper.get_record(self.records, str(identifier))

        if old_record is None:
            print("Provided identifier didn't match with any record.")
            print()
            sys.exit()

        print(
            f"Current record: #{old_record['id']}: {old_record['tag']} - {old_record['content']}"
        )
        print('If you want to keep any value untouched, press "Enter".')

        tag, content = self.check_new_tag_and_content(
            old_record, *self.get_record_details())

        record = helper.construct_record_dict(old_record["id"], old_record["timestamp"],
                                              tag, content)

        updated_database = helper.update_database(self.database, record)
        self.save_records(updated_database)

        print(
            f"Updated life record: #{record['id']}: {record['tag']} - {record['content']}")

    def check_new_tag_and_content(self, old_record: Dict, tag: str, content: str):
        """
        Check if provided tag and content are really new ones. 
        If empty value is provide, it means that user doesn't wanna change it.
        """

        if tag == "":
            tag = old_record['tag']

        if content == "":
            content = old_record['content']

        return tag, content

    def get_record_details(self) -> Tuple:
        """Function gets and returns inputs from user."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # return user inputs
        return tag, content


if __name__ == "__main__":
    print(__doc__)
    life = UpdateLifeRecorder()
    life.act(3)
