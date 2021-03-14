#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
import unittest
from multilingualcl.model import Command, PositionalArgument, OptionalArgument


class ModelTestSuite(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic_model(self):
        pa = PositionalArgument("n", "number", int, "+")
        oa = OptionalArgument("s", "sum", None)
        c = Command("add", "addition of integers", [pa, oa])


if __name__ == '__main__':
    unittest.main()
