"""Module contains class that adds new records to the database."""

from typing import Dict, Tuple

from .import life_recorder, helper


class UpdateLifeRecorder(life_recorder.LifeRecorder):
    """Implements adding life records to the database."""

    def act(self, identifier: int = None) -> None:
        """Add a new life record to database."""

        old_record = helper.get_record(self.records, str(identifier))
        assert isinstance(old_record['id'], int)

        print(
            f"Current record: #{old_record['id']}: {old_record['tag']} - {old_record['content']}")
        print('If you want to keep any value untouched, press "Enter".')

        tag, content = self.get_record_details()
        record = self.construct_record_dict(old_record["id"], old_record["timestamp"],
                                            tag, content)

        updated_database = helper.update_database(self.database, record)
        self.save_records(updated_database)

        print(
            f"Updated life record: #{record['id']}: {record['tag']} - {record['content']}")

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

    @staticmethod
    def construct_record_dict(identifier: str, timestamp: str, tag: str, content: str) -> Dict:
        """Returns dictionary of record."""

        return {
            "id": identifier,
            "timestamp": timestamp,
            "tag": tag,
            "content": content
        }


if __name__ == "__main__":
    print(__doc__)
    life = UpdateLifeRecorder()
    life.act(3)
