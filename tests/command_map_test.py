import unittest
from multilingualcl.command_map import load_command_map, load_command_map_from_directory
import os


class CommandMapTestSuite(unittest.TestCase):
    def setUp(self):
        self.command_map_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../resources/yaml"
        )

    def test_load_command_map(self):
        command_map = load_command_map()

        # Assert
        self.assertNotEqual(command_map, None)

    def test_load_command_map_from_directory(self):
        command_map = load_command_map_from_directory(self.command_map_directory)

        # Assert
        self.assertNotEqual(command_map, None)


if __name__ == "__main__":
    unittest.main()
