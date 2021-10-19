"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import List, Optional
from loguru import logger

from life_recorder.life_recorder import LifeRecorder
from life_recorder.create import CreateLifeRecorder
from life_recorder.read import ReadLifeRecorder
from life_recorder.update import UpdateLifeRecorder
from life_recorder.delete import DeleteLifeRecorder


def action_factory(action: str) -> Optional[LifeRecorder]:
    """Factory that decides which action to perform."""

    if action == "create":
        return CreateLifeRecorder
    elif action == "read":
        return ReadLifeRecorder
    elif action == "update":
        return UpdateLifeRecorder
    elif action == "delete":
        return DeleteLifeRecorder
    else:
        print(
            f'Unfortunately we don\'t have such an action. \nTried action was "{action}"\nWe support these actions: create, read, read <id>, update, delete.'
        )
        return None


@logger.catch
def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""

    action_arg = args[1]
    try:
        identifier = args[2]
    except IndexError:
        identifier = None

    action = action_factory(action_arg)

    try:
        action().act(identifier)
    except TypeError:
        sys.exit()


if __name__ == '__main__':
    # get action arg from command line
    arguments = sys.argv
    main(arguments)
