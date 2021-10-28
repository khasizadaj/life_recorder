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
        fac = CreateLifeRecorder
    elif command in COMMANDS.read:
        fac = ReadLifeRecorder
    elif command in COMMANDS.update:
        fac = UpdateLifeRecorder
    elif command in COMMANDS.delete:
        fac = DeleteLifeRecorder

    return fac
