"""Module contains creation part of factory pattern."""

# factories
from life_recorder.life_recorder import LifeRecorder
from life_recorder.create import CreateLifeRecorder
from life_recorder.read import ReadLifeRecorder
from life_recorder.update import UpdateLifeRecorder
from life_recorder.delete import DeleteLifeRecorder


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
