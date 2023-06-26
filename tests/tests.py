#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from tests.languagetest import *
from tests.modeltest import *
from tests.command_map_test import *
from tests.parsertest import *
from tests.commandtest import *
from tests.repltest import *

if __name__ == "__main__":
    languagetests = LanguageTestSuite()
    modeltests = ModelTestSuite()
    language_map_tests = CommandMapTestSuite()
    parser_tests = ParseUserCommandTestSuite()
    command_tests = CommandTestSuite()
    repl_tests = ReplTestSuite()
    tests = unittest.TestSuite(
        [
            languagetests,
            modeltests,
            language_map_tests,
            parser_tests,
            command_tests,
            repl_tests,
        ]
    )
    unittest.main()
