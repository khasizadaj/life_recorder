"""Module contains creation part of factory pattern."""

# factories
from .base import LifeRecorder
from .create import CreateLifeRecorder
from .read import ReadLifeRecorder
from .update import UpdateLifeRecorder
from .delete import DeleteLifeRecorder


def action_factory(command: str) -> LifeRecorder:
    """Factory that decides which action to perform based on the command."""

    if command == "create":
        fac = CreateLifeRecorder
    elif command == "read":
        fac = ReadLifeRecorder
    elif command == "update":
        fac = UpdateLifeRecorder
    elif command == "delete":
        fac = DeleteLifeRecorder

    return fac
