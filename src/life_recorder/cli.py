"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import Union
from loguru import logger
import click

from life_recorder.base import LifeRecorder
from life_recorder import helper as h
import life_recorder.factory.factory as fac


@click.group()
@click.version_option(version="0.1.0", prog_name="life_recorder")
@logger.catch
def main() -> None:
    """
    Utility to record life events.
    """
    pass


@main.command()
@logger.catch
def create() -> None:
    """Creates the new record."""

    action = fac.action_factory("create")
    action.act()
    sys.exit()


@main.command()
@click.argument("identifier", required=False, type=click.STRING)
@logger.catch
def read(identifier: Union[str, None]) -> None:
    """
    Reads the record.

    IDENTIFIER is id of the record. If not provided, it will read all records.
    """
    life_recorder = LifeRecorder()
    if identifier is not None:
        record = life_recorder.read_one(identifier)
        if record is None:
            message = "Provided identifier didn't match with any record."
            h.add_breakline(print, func_args=[message], both=True)
            sys.exit()

        h.add_breakline(h.print_pretty_record,
                        func_args=[record], after=True)
        sys.exit()

    for record  in life_recorder.read().values():
        h.add_breakline(h.print_pretty_record,
                        func_args=[record], after=True)
    sys.exit()


@main.command()
@click.argument("identifier", required=True, type=click.STRING)
@logger.catch
def update(identifier: Union[str, None]) -> None:
    """
    Updates the record.

    IDENTIFIER is id of the record.
    """
    action = fac.action_factory("update")
    action.act(identifier=identifier)
    sys.exit()


@main.command()
@click.argument("identifier", required=True, type=click.STRING)
@logger.catch
def delete(identifier: Union[str, None]) -> None:
    """
    Deletes the record.

    IDENTIFIER is id of the record.
    """
    action = fac.action_factory("delete")
    action.act(identifier=identifier)
    sys.exit()


if __name__ == "__main__":
    main()
