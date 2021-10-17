"""Module is used to run LifeRecorder class and record some memories."""
import sys
from typing import List
from loguru import logger

from life_recorder.read import ReadLifeRecorder
from life_recorder.add import AddLifeRecorder
from life_recorder.update import UpdateLifeRecorder
from life_recorder.delete import DeleteLifeRecorder


def life_factory(action: str):
    """Factory that decides which action to perform."""

    if action == "add":
        return AddLifeRecorder
    elif action == "read":
        return ReadLifeRecorder
    elif action == "update":
        return UpdateLifeRecorder
    elif action == "delete":
        return DeleteLifeRecorder
    else:
        print(
            f'Unfortunately we don\'t have such an action. \nTried action was "{action}"\nWe support these actions: add, read, read <id>, update, delete.')


@logger.catch
def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""

    action_arg = args[1]
    try:
        identifier = args[2]
    except IndexError:
        identifier = None

    action = life_factory(action_arg)

    try:
        action().act(identifier)
    except TypeError:
        sys.exit()


if __name__ == '__main__':
    # get action arg from command line
    arguments = sys.argv
    # arguments = ["", "read", "8"]
    main(arguments)
