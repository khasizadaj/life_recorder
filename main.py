"""Module is used to run LifeRecorder class and record some memories."""
import sys
from typing import List
from loguru import logger

from life_recorder.life_recorder import AddLifeRecorder, ReadLifeRecorder


@logger.catch
def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""

    action_arg = args[1]
    try:
        identifier = args[2]
    except IndexError:
        identifier = None

    action = action_factory(action_arg)

    if identifier is None:
        action().act()
    else:
        action().act(identifier)


def action_factory(action: str):
    """Factory that decides which action to perform."""

    if action == "add":
        return AddLifeRecorder
    elif action == "read":
        return ReadLifeRecorder
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    # get action arg from command line
    arguments = sys.argv
    main(arguments)
