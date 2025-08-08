import unittest

from life_recorder.factory.factory import action_factory
from life_recorder.factory.base import LifeRecorder
from life_recorder.factory.create import CreateLifeRecorder
from life_recorder.factory.delete import DeleteLifeRecorder


class TestActionFactory(unittest.TestCase):
    """
    Test factory functions.
    """
    def test_action_factory_returns_correct_type(self):
        """
        Test that action factory returns correct action type.
        """
        action = action_factory("create")
        self.assertIsInstance(action, LifeRecorder)
        self.assertIsInstance(action, CreateLifeRecorder)

        action = action_factory("delete")
        self.assertIsInstance(action, LifeRecorder)
        self.assertIsInstance(action, DeleteLifeRecorder)

    def test_action_factory_raises_error(self):
        """
        Test that action factory raises error when command doesn't exist.
        """
        with self.assertRaises(ValueError):
            action_factory("wrong_command")


if __name__ == "__main__":
    unittest.main()
