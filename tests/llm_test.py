#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from multilingualcl.llm import (
    is_ollama_available, _extract_json, LLMEngine, _OLLAMA_AVAILABLE,
)


class LLMTestSuite(unittest.TestCase):

    def test_ollama_available_returns_bool(self):
        """is_ollama_available() should return a bool without crashing."""
        result = is_ollama_available()
        self.assertIsInstance(result, bool)

    def test_llm_engine_init(self):
        """LLMEngine can be instantiated regardless of Ollama availability."""
        engine = LLMEngine()
        self.assertEqual(engine.model_name, "mistral")

    def test_llm_engine_custom_model(self):
        engine = LLMEngine(model_name="llama2")
        self.assertEqual(engine.model_name, "llama2")

    def test_extract_json_raw(self):
        """Parse a raw JSON object from text."""
        text = 'Here is the result: {"action": "create", "resource": "file"}'
        result = _extract_json(text)
        self.assertIsNotNone(result)
        self.assertEqual(result["action"], "create")
        self.assertEqual(result["resource"], "file")

    def test_extract_json_code_fence(self):
        """Parse JSON from a markdown code fence."""
        text = '```json\n{"action": "delete", "resource": "directory"}\n```'
        result = _extract_json(text)
        self.assertIsNotNone(result)
        self.assertEqual(result["action"], "delete")

    def test_extract_json_invalid(self):
        """Return None for text with no valid JSON."""
        text = "no json here at all"
        result = _extract_json(text)
        self.assertIsNone(result)

    def test_extract_json_malformed(self):
        """Return None for malformed JSON."""
        text = '{"action": "create", resource: file}'
        result = _extract_json(text)
        self.assertIsNone(result)

    def test_detect_language_without_ollama(self):
        """detect_language returns None when Ollama is unavailable."""
        engine = LLMEngine()
        if not _OLLAMA_AVAILABLE:
            result = engine.detect_language("hello world")
            self.assertIsNone(result)

    def test_explain_command_without_ollama(self):
        """explain_command returns None when Ollama is unavailable."""
        engine = LLMEngine()
        if not _OLLAMA_AVAILABLE:
            result = engine.explain_command("ls -la")
            self.assertIsNone(result)
