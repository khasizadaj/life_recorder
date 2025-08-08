"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import List, Tuple
from loguru import logger
import click

import life_recorder.check as ch
import life_recorder.factory.factory as fac


@click.command("main")
@click.argument(
    "command", type=click.Choice(["create", "read", "update", "delete"])
)
@click.argument("identifier", required=False, type=click.STRING)
@click.version_option(version="0.1.0", prog_name="life_recorder")
@logger.catch
def main(command: str, identifier: str) -> None:
    """
    Utility to record life events.
    """

    click.echo(f"Command: {command}")
    click.echo(f"Identifier: {identifier}")

    action = fac.action_factory(command)
    action.act(identifier)
    sys.exit()


if __name__ == "__main__":
    main()
