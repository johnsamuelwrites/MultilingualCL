#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

class Command:
    '''
      Class for a command
    '''

    def __init__(self, name, description=None, arguments=None):
        self.name = name
        self.description = name
        self.arguments = arguments


class Argument:
    '''Command line argument'''

    def __init__(self, short_name, long_name, datatype=None, values=None):
        self.short_name = short_name
        self.long_name = long_name
        self.datatype = datatype
        self.values = values


class PositionalArgument (Argument):
    '''Positional argument of a command or a subcommand'''

    def __init__(self, short_name, long_name, datatype=None, count=1):
        super().__init__(short_name, long_name, datatype, None)
        self.count = count


class OptionalArgument (Argument):
    '''Optional argument of a command or a subcommand'''

    def __init__(self, short_name, long_name, datatype=None, values=None):
        super().__init__(short_name, long_name, datatype, values)


class SubCommand (PositionalArgument):
    '''Subcommand'''

    def __init__(self, short_name, long_name):
        super().__init__(short_name, long_name)
