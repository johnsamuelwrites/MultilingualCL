import unittest
from multilingualcl.command import obtain_command_from_translation
from multilingualcl.command_map import load_command_map

class CommandTestSuite(unittest.TestCase):

    def test_parse_user_command(self):
        command_map = load_command_map()
        current_locale = "en_US"
        user_input = "ls -l"

        # Actual value
        actual_command = obtain_command_from_translation(command_map, current_locale, user_input)

        # Assert
        self.assertEqual(actual_command, user_input)

    def test_parse_user_command_long_option(self):
        command_map = load_command_map()
        current_locale = "en_US"
        user_input = "ls --long"

        # Actual value
        actual_command = obtain_command_from_translation(command_map, current_locale, user_input)

        # Assert
        expected_command = "ls -l"
        self.assertEqual(actual_command, expected_command)

if __name__ == '__main__':
    unittest.main()

