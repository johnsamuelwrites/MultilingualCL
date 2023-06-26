#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
import unittest
from multilingualcl.language import Language


class LanguageTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_language(self):
        l = Language("@1")
        l.add_name("en")
        l.add_name("en")
        l.add_name("English")
        assert "en" in l.get_all_names()
        assert "English" in l.get_all_names()
        assert l.get_identifier("English") == "@1"


if __name__ == "__main__":
    unittest.main()
