"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import Union
from loguru import logger
import click
from rich import print

from life_recorder.base import LifeRecorder
from life_recorder import helper as h


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

    life_recorder = LifeRecorder()

    # Get user inputs
    tag = input("What is the tag of this record? (optional): ")
    
    title = input("What is the title of this record?: ")
    while title == "":
        title = input("Please enter a title; it can't be blank: ")

    content = input("What is the content of this record?: ")
    while content == "":
        content = input("Please enter a content; it can't be blank: ")

    # Create the record
    record_data = {
        "tag": tag,
        "title": title,
        "content": content
    }
    
    new_record = life_recorder.create(record_data)
    h.add_breakline(h.print_pretty_record, func_args=[new_record], both=True)
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

        h.add_breakline(h.print_pretty_record, func_args=[record], after=True)
        sys.exit()

    for record in life_recorder.read().values():
        h.add_breakline(h.print_pretty_record, func_args=[record], after=True)
    sys.exit()


@main.command()
@click.argument("identifier", required=True, type=click.STRING)
@logger.catch
def update(identifier: str) -> None:
    """
    Updates the record.

    IDENTIFIER is id of the record.
    """
    life_recorder = LifeRecorder()
    
    # Get the existing record
    old_record = life_recorder.read_one(identifier)
    if old_record is None:
        message = "Provided identifier didn't match with any record."
        h.add_breakline(print, func_args=[message], both=True)
        sys.exit()

    # Show current record to user
    print("Current record:")
    h.add_breakline(h.print_pretty_record, func_args=[old_record], after=True)

    print('Usage: Add new detail for respective field. If you want to keep '
          'any value untouched, press "Enter".')

    # Get user inputs for updating
    tag = input("What is the updated tag? (optional): ")
    title = input("What is the updated title?: ")
    content = input("What is the updated content?: ")

    # Use existing values if user didn't provide new ones
    if tag == "":
        tag = old_record['tag']
    if title == "":
        title = old_record['title']
    if content == "":
        content = old_record['content']

    # Create updated record
    updated_record = {
        "tag": tag,
        "title": title,
        "content": content
    }

    # Update the record using the base class method
    life_recorder.update(identifier, updated_record)

    message = f"Record with #{identifier} is updated."
    h.add_breakline(print, func_args=[message], after=True)
    sys.exit()


@main.command()
@click.argument("identifier", required=True, type=click.STRING)
@logger.catch
def delete(identifier: str) -> None:
    """
    Deletes the record.

    IDENTIFIER is id of the record.
    """

    life_recorder = LifeRecorder()
    record = life_recorder.read_one(identifier)
    if record is None:
        message = "There is no record with the given identifier."
        h.add_breakline(print, func_args=[message], both=True)
        sys.exit()

    # message = "Record you want to delete is:"
    # h.add_breakline(print, func_args=[message], after=True)

    click.echo(click.style("\nRecord you want to delete is:\n", fg="green"))
    click.echo(f"{h.pretty_record(record)}\n")

    if (
        click.confirm(
            click.style(
                "Are you sure you want to delete this record?", fg="red"
            ),
            default=None,
        )
        is False
    ):
        message = "Every record matters! I am glad that you didn't delete it!"
        click.echo(click.style(message, fg="green"))
        sys.exit()

    life_recorder.delete(identifier)

    message = "Deleting record ... Don't stop adding new records!"
    click.echo(click.style(message, fg="white"))

    message = "Successfully deleted record."
    click.echo(click.style(message, fg="green"))

    sys.exit()


if __name__ == "__main__":
    main()
