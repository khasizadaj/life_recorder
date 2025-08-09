import unittest
from life_recorder import config
from life_recorder.helper import get_data_dir, get_user
from unittest.mock import patch


class TestHelper(unittest.TestCase):
    def setUp(self):
        config.DEBUG = False

    @patch("platform.system")
    @patch("os.path.expanduser")
    def test_get_data_dir(self, mox_expanduser, mock_platform):
        mox_expanduser.return_value = "C:\\Users\\life_user"
        mock_platform.return_value = "Windows"
        self.assertEqual(get_data_dir(), "C:\\\\Users\\life_user\\.data")

    @patch("platform.system")
    @patch("os.path.expanduser")
    def test_get_user_linux(self, mock_expanduser, mock_platform):
        mock_platform.return_value = "Linux"
        mock_expanduser.return_value = "/home/life_user"
        self.assertEqual(get_user(), "life_user")

    @patch("platform.system")
    @patch("os.path.expanduser")
    def test_get_user_windows(self, mock_expanduser, mock_platform):
        mock_platform.return_value = "Windows"
        mock_expanduser.return_value = "C:\\Users\\life_user"
        self.assertEqual(get_user(), "life_user")

    @patch("platform.system")
    def test_get_user_unknown(self, mock_platform):
        mock_platform.return_value = "unknown"

        with self.assertRaises(NotImplementedError):
            get_user()


if __name__ == "__main__":
    unittest.main()
