#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re
import json
import time

_OLLAMA_AVAILABLE = False
try:
    import ollama
    _OLLAMA_AVAILABLE = True
except ImportError:
    pass

# Cache for server availability check
_ollama_check_cache = {"available": False, "timestamp": 0.0}
_CACHE_TTL = 30.0  # seconds


def is_ollama_available():
    """Check both library availability AND running server.

    Caches result for 30 seconds to avoid repeated network checks.
    """
    if not _OLLAMA_AVAILABLE:
        return False

    now = time.time()
    if now - _ollama_check_cache["timestamp"] < _CACHE_TTL:
        return _ollama_check_cache["available"]

    try:
        ollama.list()
        _ollama_check_cache["available"] = True
    except Exception:
        _ollama_check_cache["available"] = False

    _ollama_check_cache["timestamp"] = now
    return _ollama_check_cache["available"]


def _extract_json(text):
    """Extract a JSON object from LLM output, handling markdown fences."""
    # Try to find JSON in code fence
    fence_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find raw JSON object
    brace_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


class LLMEngine:
    """Manages Ollama interactions for intent extraction and language detection."""

    def __init__(self, model_name="mistral"):
        self.model_name = model_name

    def detect_language(self, text):
        """Detect the language of user input.

        Returns a locale code like 'en_US', 'fr_FR', or None on failure.
        """
        if not is_ollama_available():
            return None

        prompt = (
            "Detect the language of the following text and return ONLY the "
            "locale code (e.g., en_US, fr_FR, de_DE, es_ES, zh_CN, ar_SA, "
            "hi_IN, ja_JP, ko_KR, pt_BR). Return nothing else.\n\n"
            f"Text: {text}\n\nLocale code:"
        )

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            result = response.get("response", "").strip()
            # Validate it looks like a locale code
            if re.match(r'^[a-z]{2}_[A-Z]{2}$', result):
                return result
        except Exception:
            pass

        return None

    def extract_intent(self, user_input, locale, semantic_index):
        """Use LLM for intent extraction with constrained output.

        The prompt includes action verb list and resource types from the
        SemanticIndex as context, constraining the LLM to output a valid
        (action, resource, modifiers) tuple.
        """
        if not is_ollama_available():
            return None

        from multilingualcl.semantic import IntentResult

        # Build context from semantic index
        actions = list(semantic_index.action_synonyms.keys())[:30]
        resources = list(semantic_index.resource_types.keys())[:30]

        prompt = (
            "You are a command-line intent parser. Given user input, extract "
            "the intent as a JSON object.\n\n"
            f"Valid actions: {', '.join(actions)}\n"
            f"Valid resources: {', '.join(resources)}\n\n"
            "Return ONLY a JSON object with these fields:\n"
            '- "action": one of the valid actions\n'
            '- "resource": one of the valid resources\n'
            '- "modifiers": list of qualifier words (e.g., ["force", "recursive"])\n\n'
            f"User input: {user_input}\n\n"
            "JSON:"
        )

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            result_text = response.get("response", "")
            parsed = _extract_json(result_text)

            if parsed and "action" in parsed:
                action = parsed.get("action", "").lower()
                resource = parsed.get("resource", "").lower()
                modifiers = parsed.get("modifiers", [])

                # Validate action against our index
                if action in semantic_index.action_verbs:
                    action = semantic_index.action_verbs[action]
                elif action not in semantic_index.action_synonyms:
                    return None

                return IntentResult(
                    action=action,
                    resource=resource,
                    modifiers=modifiers if isinstance(modifiers, list) else [],
                    confidence=0.8,
                    source="llm",
                )
        except Exception:
            pass

        return None

    def explain_command(self, command, locale="en_US"):
        """Generate a human-readable explanation of what a command does."""
        if not is_ollama_available():
            return None

        prompt = (
            f"Explain in one short sentence what this Linux command does: "
            f"{command}"
        )

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response.get("response", "").strip()
        except Exception:
            return None
