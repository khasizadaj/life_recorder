"""Module is used to run LifeRecorder class and record some memories."""

import sys
from typing import List, Tuple
from loguru import logger

from life_recorder.life_recorder import LifeRecorder
from life_recorder.create import CreateLifeRecorder
from life_recorder.read import ReadLifeRecorder
from life_recorder.update import UpdateLifeRecorder
from life_recorder.delete import DeleteLifeRecorder


def action_factory(command: str) -> LifeRecorder:
    """Factory that decides which action to perform based on the command."""

    if command == "create":
        return CreateLifeRecorder
    elif command == "read":
        return ReadLifeRecorder
    elif command == "update":
        return UpdateLifeRecorder
    elif command == "delete":
        return DeleteLifeRecorder


def check_arguments(args: List[str]) -> Tuple[bool]:
    """Function checks whether arguments are valid."""

    command = args[0]
    is_command = check_command(command)

    if not is_command:
        sys.exit()

    # False means that identifier is not needed for this command.
    is_identifier = False
    requires_identifier = check_requires_identifier(command)
    if requires_identifier:
        is_identifier = check_identifier(args)

    if not is_identifier:
        sys.exit()

    return is_command, is_identifier


def check_identifier(args: List[str]) -> bool:
    """Checks if the identifier is among provided arguments and valid."""

    if len(args) < 2:
        command = args[0]

        print('Error: Identifier is not provided for command')
        print('Usage: You need to provide an identifier for the command '
              f'to perform. For example, "{command} 3"')
        return False

    if not args[1].isdigit():
        command = args[0]

        print('Error: Identifier is not a number')
        print('Usage: You need to provide an identifier for the command '
              f'to perform. For example, "{command} 3"')
        return False

    return True


def check_requires_identifier(command: str):
    """Checks if the identifier requires an identifier."""

    # as "read" command can be used in both ways, it is not included
    id_required_actions = ["update", "delete"]
    return command in id_required_actions


def check_command(command):
    """Check if the command is valid."""

    commands = ["create", "read", "update", "delete"]

    if command not in commands:
        print('Error: Unknown command. Unfortunately we don\'t have such command.')
        print('Usage: You can utilize these commands: create, read, update, '
              'delete.')
        print(f'Info: You tried this command: "{command}".')
        return False

    return True


@logger.catch
def main(args: List[str]) -> None:
    """Functions gets the record and writes it to the file."""

    is_command, is_identifier = check_arguments(args)
    if is_command:
        command = args[0]

    if is_identifier:
        identifier = args[1]
    else:
        identifier = None

    action = action_factory(command)
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
