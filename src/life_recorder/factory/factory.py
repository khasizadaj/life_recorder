"""Module contains creation part of factory pattern."""

# factories
from .base import LifeRecorder, Commands
from .create import CreateLifeRecorder
from .update import UpdateLifeRecorder


def action_factory(command: str) -> LifeRecorder:
    """Factory that decides which action to perform based on the command."""

    if command == Commands.CREATE:
        return CreateLifeRecorder()
    elif command == Commands.UPDATE:
        return UpdateLifeRecorder()
    else:
        raise ValueError("Command doesn't exist.")
