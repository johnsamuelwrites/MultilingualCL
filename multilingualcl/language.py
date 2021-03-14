#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
import re


class Language:
    def __init__(self, identifier):
        if re.match("@[0-9]+", identifier):
            self.identifier = identifier
            self.names = set()
        else:
            print("Invalid language identifier: " + identifier)
            exit(1)

    def add_name(self, name):
        self.names.add(name)

    def get_all_names(self):
        return list(self.names)

    def get_identifier(self, name):
        if name in self.names:
            return self.identifier
        return None


class LanguageMap:
    def __init__(self):
        self.languageIDDict = {}
        self.IDlanguageDict = {}

    def addLanguage(self, identifier, language):
        if(type(language) == str and
           type(identifier) == str):
            self.IDlanguageDict[identifier].add(language)
            self.languageIDDict[language] = identifier
        else:
            print("Unable to add the language. Incorrect data type.")
