"""Module contains class that deletes records from the database."""

import sys
from typing import Dict

from life_recorder import helper
from .base import LifeRecorder


class DeleteLifeRecorder(LifeRecorder):
    """Implements adding life records to the database."""

    def act(self, identifier: int = None) -> None:
        """Add a new life record to database."""

        if identifier is None:
            print(
                "In order to delete any record, you need to specify an identifier."
            )
            print()
            sys.exit()

        old_record = helper.get_record(self.records, str(identifier))
        self.print_old_record(old_record)

        decision = self.get_decision()
        if decision:
            print("Deleting record ... Don't stop adding new records!")

            updated_database = helper.delete_record(self.database, identifier)
            self.save_records(updated_database)

            print("Successfully deleted record.")
        else:
            print("Every record matters! I am glad that you didn't delete it!")
            return

    def print_old_record(self, old_record: Dict) -> None:
        """Prints the old record for user."""

        print("Record you want to delete is:")
        helper.print_pretty_record(old_record)
        print("")

    def get_decision(self) -> bool:
        """Returns the decision of user about deletion of record."""

        decision = input(self.get_input_message("delete"))

        if decision.lower() == 'y':
            return True
        return False


if __name__ == "__main__":
    print(__doc__)
