"""Module contains class that reads record(s) from the database."""

from typing import Dict, Optional

from .life_recorder import LifeRecorder
from . import helper


class ReadLifeRecorder(LifeRecorder):
    """Implements reading life records from the database."""

    def act(self, identifier: int = None) -> None:
        """
        Function reads records from the database. 
        If identifier is specified, it will return only one record.
        """

        if identifier is not None:
            record = helper.get_record(self.records, identifier)
            if record is None:
                print("Provided identifier didn't match with any record.")
                return

            helper.print_pretty_record(record)
            return

        for record in self.get_all_records():
            helper.print_pretty_record(record)

    def get_all_records(self):
        """Function return all records from the database."""

        return self.records.values()


if __name__ == "__main__":
    print(__doc__)