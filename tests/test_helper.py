import unittest
from unittest.mock import patch

from src.life_recorder import config
from src.life_recorder.helper import get_user


class TestHelper(unittest.TestCase):
    def setUp(self):
        config.DEBUG = False

    @patch("platform.system")
    @patch("os.path.expanduser")
    def test_get_user_linux(self, mock_expanduser, mock_platform):
        mock_platform.return_value = "Linux"
        mock_expanduser.return_value = "/home/life_user"
        self.assertEqual(get_user(), "life_user")


if __name__ == "__main__":
    unittest.main()
