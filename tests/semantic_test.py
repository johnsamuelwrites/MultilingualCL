#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from multilingualcl.semantic import (
    SemanticIndex, IntentResult,
    extract_intent_rulebased, resolve_command,
)


class SemanticIndexTestSuite(unittest.TestCase):

    def setUp(self):
        self.index = SemanticIndex()
        self.index.load()

    def test_action_verbs_loaded(self):
        """Verify actions.md parsed -- synonyms map to canonical actions."""
        self.assertIn("erase", self.index.action_verbs)
        self.assertEqual(self.index.action_verbs["erase"], "delete")
        self.assertIn("remove", self.index.action_verbs)
        self.assertEqual(self.index.action_verbs["remove"], "delete")

    def test_action_create_synonyms(self):
        self.assertIn("create", self.index.action_verbs)
        self.assertEqual(self.index.action_verbs["create"], "create")
        self.assertIn("build", self.index.action_verbs)
        self.assertEqual(self.index.action_verbs["build"], "create")

    def test_action_synonyms_dict(self):
        """Verify reverse mapping: canonical -> [synonyms]."""
        self.assertIn("create", self.index.action_synonyms)
        self.assertIn("create", self.index.action_synonyms["create"])

    def test_resource_types_loaded(self):
        """Verify resources.md parsed correctly."""
        self.assertGreater(len(self.index.resource_types), 0)
        self.assertIn("file", self.index.resource_types)
        self.assertIn("process", self.index.resource_types)

    def test_resource_terms_dict(self):
        """Verify resource category -> [terms] mapping."""
        self.assertGreater(len(self.index.resource_terms), 0)

    def test_action_resources_loaded(self):
        """Verify actions.json loaded -- 'create' can target 'file'."""
        self.assertIn("create", self.index.action_resources)
        self.assertIn("file", self.index.action_resources["create"])
        self.assertIn("directory", self.index.action_resources["create"])

    def test_command_catalog_loaded(self):
        """Verify commands.yaml parsed into catalog entries."""
        self.assertGreater(len(self.index.command_catalog), 0)

    def test_extract_intent_create_file(self):
        intent = extract_intent_rulebased("create file", self.index, "en_US")
        self.assertEqual(intent.action, "create")
        self.assertEqual(intent.resource, "file")
        self.assertGreater(intent.confidence, 0.5)
        self.assertEqual(intent.source, "semantic")

    def test_extract_intent_delete_directory(self):
        intent = extract_intent_rulebased("delete directory", self.index, "en_US")
        self.assertEqual(intent.action, "delete")
        self.assertEqual(intent.resource, "directory")
        self.assertGreater(intent.confidence, 0.5)

    def test_extract_intent_synonym(self):
        """'erase file' should resolve to delete+file."""
        intent = extract_intent_rulebased("erase file", self.index, "en_US")
        self.assertEqual(intent.action, "delete")

    def test_extract_intent_list_process(self):
        intent = extract_intent_rulebased("list process", self.index, "en_US")
        self.assertEqual(intent.action, "list")
        self.assertEqual(intent.resource, "process")

    def test_extract_intent_with_modifier(self):
        intent = extract_intent_rulebased("delete file force", self.index, "en_US")
        self.assertEqual(intent.action, "delete")
        self.assertIn("force", intent.modifiers)

    def test_extract_intent_empty_input(self):
        intent = extract_intent_rulebased("", self.index, "en_US")
        self.assertEqual(intent.confidence, 0.0)

    def test_extract_intent_unknown_input(self):
        intent = extract_intent_rulebased("xyzzy plugh", self.index, "en_US")
        self.assertEqual(intent.confidence, 0.0)

    def test_resolve_command_create_file(self):
        intent = IntentResult(
            action="create", resource="file",
            modifiers=[], confidence=1.0, source="semantic"
        )
        command = resolve_command(intent, self.index)
        self.assertIsNotNone(command)
        self.assertIn("touch", command)

    def test_resolve_command_delete_file(self):
        intent = IntentResult(
            action="delete", resource="file",
            modifiers=[], confidence=1.0, source="semantic"
        )
        command = resolve_command(intent, self.index)
        self.assertIsNotNone(command)
        self.assertIn("rm", command)

    def test_resolve_command_list_file(self):
        intent = IntentResult(
            action="list", resource="file",
            modifiers=[], confidence=1.0, source="semantic"
        )
        command = resolve_command(intent, self.index)
        self.assertIsNotNone(command)
        self.assertIn("ls", command)

    def test_resolve_command_with_modifier(self):
        intent = IntentResult(
            action="delete", resource="file",
            modifiers=["force"], confidence=1.0, source="semantic"
        )
        command = resolve_command(intent, self.index)
        self.assertIsNotNone(command)
        self.assertIn("-f", command)

    def test_resolve_command_no_action(self):
        intent = IntentResult(
            action="", resource="file",
            modifiers=[], confidence=0.0, source="semantic"
        )
        command = resolve_command(intent, self.index)
        self.assertIsNone(command)
