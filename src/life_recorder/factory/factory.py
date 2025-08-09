"""Module contains creation part of factory pattern."""

# factories
from .base import LifeRecorder, Commands
from .create import CreateLifeRecorder
from .read import ReadLifeRecorder
from .update import UpdateLifeRecorder
from .delete import DeleteLifeRecorder


def action_factory(command: str) -> LifeRecorder:
    """Factory that decides which action to perform based on the command."""

    if command == Commands.CREATE:
        return CreateLifeRecorder()
    elif command == Commands.READ:
        return ReadLifeRecorder()
    elif command == Commands.UPDATE:
        return UpdateLifeRecorder()
    elif command == Commands.DELETE:
        return DeleteLifeRecorder()
    else:
        raise ValueError("Command doesn't exist.")
