"""Module contains creation part of factory pattern."""

# factories
from .base import LifeRecorder, Commands
from .create import CreateLifeRecorder
from .update import UpdateLifeRecorder


def action_factory(command: str) -> LifeRecorder | None:
    """Factory that decides which action to perform based on the command."""
    if command not in Commands.__members__.values():
        raise ValueError(
            f"Unsupported command '{command}'. Supported commands are: {', '.join(Commands.__members__.keys())}."
        )

    if command == Commands.CREATE:
        return CreateLifeRecorder()
    elif command == Commands.UPDATE:
        return UpdateLifeRecorder()
