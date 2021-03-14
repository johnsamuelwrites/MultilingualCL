#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from tests.languagetest import *

if __name__ == '__main__':
    languagetests = LanguageTestSuite()
    tests = unittest.TestSuite([languagetests])
    unittest.main()
