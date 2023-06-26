import unittest
from multilingualcl.parser import parse_user_command, load_command_map
from multilingualcl.command_map import load_command_map


class ParseUserCommandTestSuite(unittest.TestCase):
    def test_parse_user_command(self):
        command_map = load_command_map()
        current_locale = "en_US"
        user_input = "ls -l"

        # Actual value
        actual_parsed_args, actual_options_map = parse_user_command(
            command_map, current_locale, user_input
        )

        # Assert
        self.assertNotEqual(actual_parsed_args, None)
        self.assertNotEqual(actual_options_map, None)


if __name__ == "__main__":
    unittest.main()
