"""Module contains functions to check arguments provided for program."""

from typing import List

COMMANDS_ALL = {0: ["create"], 1: ["update", "delete"], 2: ["read"]}


def check_identifier(args: List[str]) -> bool:
    """Checks if the identifier is among provided arguments and valid."""

    if len(args) < 2:
        return 1

    if not args[1].isdigit():
        return 2

    return 0


def check_requires_identifier(command: str) -> int:
    """Checks if the identifier requires an identifier."""

    comms_no_identifier = COMMANDS_ALL[0]
    comms_only_with_identifier = COMMANDS_ALL[1]
    comms_hybrid = COMMANDS_ALL[2]

    if command in comms_no_identifier:
        status = 0
    elif command in comms_only_with_identifier:
        status = 1
    elif command in comms_hybrid:
        status = 2

    return status


def check_command(command) -> bool:
    """Check if the command is valid."""

    commands = [comm for comm_list in COMMANDS_ALL.values()
                for comm in comm_list]

    if command not in commands:
        print('Error: Unknown command. Unfortunately we don\'t have such command.')
        print('Usage: You can utilize these commands: create, read, update, '
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


IDENTIFIER_CHECK_STATUSES = {1: print_no_identifier, 2: print_not_number}
