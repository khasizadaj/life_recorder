"""Module contains class that deletes records from the database."""

import sys
from typing import Dict, Union

from life_recorder import helper as h
from .base import LifeRecorder


class DeleteLifeRecorder(LifeRecorder):
    """Implements adding life records to the database."""

    def __init__(self):
        super().__init__()
        self.input_messages[
            "delete"] = "Are you sure you want to delete this record? [Y(y) / N(n)]: "

    def act(self, identifier: Union[str, None] = None):
        """Add a new life record to database."""

        if identifier is None:
            message = "In order to delete any record, you need to specify an identifier."
            h.add_breakline(print, func_args=[message], both=True)
            sys.exit()

        old_record = h.get_record(self.records, str(identifier))
        if old_record is None:
            message = "There is no record with the given identifier."
            h.add_breakline(print, func_args=[message], both=True)
            sys.exit()

        self.print_old_record(old_record)

        decision = self.get_decision()
        if decision:
            message = "Deleting record ... Don't stop adding new records!"
            h.add_breakline(print, func_args=[message], before=True)

            updated_database = h.delete_record(self.database, identifier)
            self.save_records(updated_database)

            message = "Successfully deleted record."
            h.add_breakline(print, func_args=[message], after=True)
        else:
            message = "Every record matters! I am glad that you didn't delete it!"
            h.add_breakline(print, func_args=[message], both=True)
            return

    def print_old_record(self, old_record: Dict) -> None:
        """Prints the old record for user."""

        message = "Record you want to delete is:"
        h.add_breakline(print, func_args=[message], before=True)

        h.add_breakline(h.print_pretty_record,
                        func_args=[old_record], after=True)

    def get_decision(self) -> bool:
        """Returns the decision of user about deletion of record."""

        decision = input(self.get_input_message("delete"))

        if decision.lower() == 'y':
            return True
        return False


if __name__ == "__main__":
    print(__doc__)
