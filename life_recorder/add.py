"""Module contains class that adds new records to the database."""

from typing import Dict

from . import helper, life_recorder


class AddLifeRecorder(life_recorder.LifeRecorder):
    """Implements adding life records to the database."""

    def act(self, identifier: str = None) -> None:
        """Add a new life record to database."""

        if identifier is not None:
            raise Exception(
                "It's not needed have an identifier when adding a life record.")

        record = self.get_record_details()
        updated_database = helper.update_database(self.database, record)
        self.save_records(updated_database)

        print(
            f"Added life record: #{record['id']}: {record['tag']} - {record['content']}")

    def get_record_details(self) -> Dict:
        """Function gets inputs from user and returns new record."""

        # ask for tag of record
        input_message = self.get_input_message("tag")
        tag = input(input_message)

        # ask for content of record
        input_message = self.get_input_message("content")
        content = input(input_message)

        # create and return a life record
        return self.construct_record_dict(tag, content)

    def construct_record_dict(self, tag: str, content: str):
        """Returns dictionary of record."""

        identifier = self.get_identifier()
        timestamp = helper.get_timestamp()

        return {
            "id": identifier,
            "timestamp": timestamp,
            "tag": tag,
            "content": content
        }

    def get_identifier(self) -> int:
        """Function updates and returns the identifier for next record."""

        self.update_last_id()
        return self.last_id

    def update_last_id(self) -> None:
        """Updates last id of the database."""

        self.database["last_id"] += 1

    @property
    def last_id(self):
        """Returns the last id used in the database."""
        return int(self.database["last_id"])


if __name__ == "__main__":
    print(__doc__)
