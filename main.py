"""Module is used to run LifeRecorder class and record some memories."""
import sys
from typing import Callable, List

from life_recorder.life_recorder import LifeRecorder


def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""
    
    life_recorder = LifeRecorder()

    action_arg = args[1]
    action_func = action_factory(action_arg, life_recorder)
    action_func()


def action_factory(action: str, life_recorder: LifeRecorder) -> Callable:
    """Factory that decides which action to perform."""

    if action == "add":
        return life_recorder.add_record
    elif action == "read":
        return life_recorder.read_records


if __name__ == '__main__':
    # get action arg from command line
    arguments = sys.argv
    main(arguments)
