import unittest
from unittest.mock import patch, mock_open
from termcolor import colored
from multilingualcl.repl import (
    load_history,
    save_history,
    get_suggestions,
    highlight_match,
    evaluate_command,
)
from multilingualcl.command_map import load_command_map


class ReplTestSuite(unittest.TestCase):
    def test_get_suggestions(self):
        # Arrange
        text = "cmmand1"
        options = ["command1", "command2", "command3", "cmnd1", "cmnd2", "cmnd3"]
        expected_matches = ["command1", "cmnd1"]

        # Act
        actual_matches = get_suggestions(text, options)

        # Assert
        self.assertEqual(actual_matches, expected_matches)

    def test_highlight_match(self):
        # Arrange
        text = "This is a sample text."
        match = "sample"
        expected_highlighted_text = "This is a " + colored(match, "yellow") + " text."

        # Act
        actual_highlighted_text = highlight_match(text, match)

        # Assert
        self.assertEqual(actual_highlighted_text, expected_highlighted_text)

    def test_evaluate_command(self):
        # Arrange
        command = "ls"
        current_locale = "en_US"
        command_map = load_command_map()

        # Run without error
        actual_result = evaluate_command(command, command_map, current_locale)


if __name__ == "__main__":
    unittest.main()
