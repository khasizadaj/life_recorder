"""Module contains creation part of factory pattern."""

# factories
from .base import LifeRecorder, COMMANDS
from .create import CreateLifeRecorder
from .read import ReadLifeRecorder
from .update import UpdateLifeRecorder
from .delete import DeleteLifeRecorder


def action_factory(command: str) -> LifeRecorder:
    """Factory that decides which action to perform based on the command."""

    if command in COMMANDS.create:
        return CreateLifeRecorder()
    elif command in COMMANDS.read:
        return ReadLifeRecorder()
    elif command in COMMANDS.update:
        return UpdateLifeRecorder()
    elif command in COMMANDS.delete:
        return DeleteLifeRecorder()
    else:
        raise ValueError("Command doesn't exist.")
