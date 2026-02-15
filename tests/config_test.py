#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import os
import unittest
from multilingualcl.config import MultilingualCLConfig, load_config


class ConfigTestSuite(unittest.TestCase):

    def test_default_config(self):
        config = MultilingualCLConfig()
        self.assertEqual(config.ollama_model, "mistral")
        self.assertTrue(config.ollama_enabled)
        self.assertTrue(config.safety_enabled)
        self.assertTrue(config.show_command_preview)
        self.assertEqual(config.locale_override, "")
        self.assertEqual(config.ollama_timeout, 10.0)

    def test_resource_dir_exists(self):
        config = MultilingualCLConfig()
        self.assertTrue(os.path.isdir(config.resource_dir))

    def test_load_config_defaults(self):
        config = load_config()
        self.assertEqual(config.ollama_model, "mistral")
        self.assertTrue(config.safety_enabled)

    def test_custom_config(self):
        config = MultilingualCLConfig(
            ollama_model="llama2",
            ollama_enabled=False,
            safety_enabled=False,
        )
        self.assertEqual(config.ollama_model, "llama2")
        self.assertFalse(config.ollama_enabled)
        self.assertFalse(config.safety_enabled)
