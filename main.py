"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import List, Tuple
from loguru import logger

import life_recorder.check as ch
import life_recorder.factory as fac


def get_arguments(args: List[str]) -> Tuple[bool]:
    """Function checks whether arguments are valid."""

    command = args[0]
    is_command = ch.check_command(command)

    if not is_command:
        sys.exit()

    # `None` is defualt value for variable, which means that identifier is not
    # required for this command. if it's required but not provided, respective
    # message will be printed.
    identifier = None

    requires_identifier: int = ch.check_requires_identifier(command)
    if requires_identifier in [1, 2]:
        identifier_status = ch.check_identifier(args)

        func = ch.IDENTIFIER_CHECK_STATUSES.get(identifier_status, None)
        if func is not None:
            if identifier_status == 1 and requires_identifier == 2:
                pass
            else:
                func(command)

        if identifier_status != 0:
            if identifier_status == 1 and requires_identifier == 2:
                pass
            else:
                sys.exit()

        try:
            identifier = args[1]
        except IndexError:
            pass

    return command, identifier


@logger.catch
def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""

    # get arguments
    command, identifier = get_arguments(args)

    # get factory
    action = fac.action_factory(command)

    # perform the action
    action().act(identifier)


if __name__ == '__main__':
    # get action arg from command line
    arguments = sys.argv[1:]
    if len(arguments) < 1:
        print('Error: You haven\'t provided any arguments for program to perform '
              'action.')
        print('Usage: Add commands to use this program. Supported commands: '
              'create, read, read <identifier>, update <identifier>, '
              'delete <identifier>')

        sys.exit()

    main(arguments)
    sys.exit()
