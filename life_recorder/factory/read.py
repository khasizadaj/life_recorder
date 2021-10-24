"""Module contains class that reads record(s) from the database."""

import sys
from typing import Dict

from life_recorder import helper as h
from .base import LifeRecorder


class ReadLifeRecorder(LifeRecorder):
    """Implements reading life records from the database."""

    def act(self, identifier: int = None) -> None:
        """
        Function reads records from the database. 
        If identifier is specified, it will return only one record.
        """

        if identifier is not None:
            record = h.get_record(self.records, identifier)
            if record is None:
                message = "Provided identifier didn't match with any record."
                h.add_breakline(print, func_args=[message], both=True)
                sys.exit()

            h.add_breakline(h.print_pretty_record,
                            func_args=[record], after=True)
            return

        for record in self.get_all_records():
            h.add_breakline(h.print_pretty_record,
                            func_args=[record], after=True)

    def get_all_records(self) -> Dict:
        """Function return all records from the database."""

        return self.records.values()


if __name__ == "__main__":
    print(__doc__)
