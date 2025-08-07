"""Module contains functions to check arguments provided for program."""

from typing import List
from .factory.base import COMMANDS


def get_identifier_status(args: List[str]) -> bool:
    """Checks if the identifier is among provided arguments and valid."""

    if len(args) < 2:
        return 1

    if not args[1].isdigit():
        return 2

    return 0


def check_requires_identifier(command: str) -> int:
    """Function checks whether command is required to have an identifier."""

    command_type = COMMANDS.get_type(command)

    if command_type == 0:
        return False

    return True


def check_command(command) -> bool:
    """Check if the command is valid."""

    if command not in COMMANDS.all_commands:
        print('Error: Unknown command. Unfortunately we don\'t have such command.')
        print('Usage: You can utilize these COMMANDS: create, read, update, '
              'delete.')
        print(f'Info: You tried this command: "{command}".')
        return False

    return True


def print_no_identifier(command: str):
    """Prints an error message and usage in case the identifier is missing."""

    print('Error: Identifier is not provided for command')
    print('Usage: You need to provide an identifier for the command '
          f'to perform. For example, "{command} 3"')


def print_not_number(command: str):
    """
    Prints an error message and usage in case the identifier is not a number.
    """

    print('Error: Identifier is not a number')
    print('Usage: You need to provide a number as an identifier for the command '
          f'to perform. For example, "{command} 3"')


# this dictionary contains status type and functions for each status. Right now,
# it only contains error functions.
STATUS_FUNCS = {1: print_no_identifier, 2: print_not_number}
