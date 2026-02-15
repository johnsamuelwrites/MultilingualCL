#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re
import difflib
from dataclasses import dataclass, field
from multilingualcl.command_map import (
    load_actions_json,
    load_actions_md,
    load_resources_md,
    load_commands_yaml,
    load_commandline_json,
)


@dataclass
class IntentResult:
    action: str = ""
    resource: str = ""
    modifiers: list = field(default_factory=list)
    confidence: float = 0.0
    source: str = "semantic"


# Common modifier words that map to command flags
MODIFIER_MAP = {
    "force": "-f",
    "forcefully": "-f",
    "forcibly": "-f",
    "recursive": "-r",
    "recursively": "-r",
    "all": "-a",
    "verbose": "-v",
    "verbosely": "-v",
    "quiet": "-q",
    "quietly": "-q",
    "hidden": "-a",
    "long": "-l",
    "detailed": "-l",
}


class SemanticIndex:
    """Loads and indexes all semantic resource files at startup."""

    def __init__(self, resource_dir=None):
        self.resource_dir = resource_dir
        # synonym -> canonical action (e.g., "erase" -> "delete")
        self.action_verbs = {}
        # canonical action -> [synonyms]
        self.action_synonyms = {}
        # term -> canonical resource category (e.g., "file" -> "file management")
        self.resource_types = {}
        # canonical resource category -> [terms]
        self.resource_terms = {}
        # action -> [valid resource terms] from actions.json
        self.action_resources = {}
        # (action, resource_domain) -> [(description, linux_command)]
        self.command_catalog = {}

    def load(self):
        self._load_action_verbs()
        self._load_resource_types()
        self._load_action_resources()
        self._load_command_catalog()

    def _load_action_verbs(self):
        """Parse actions.md to build verb synonym index.

        When a synonym appears in multiple categories (e.g., "erase" in both
        "delete" and "uninstall"), the first category wins.
        """
        actions = load_actions_md("en", self.resource_dir)
        for canonical, synonyms in actions.items():
            self.action_synonyms[canonical] = synonyms
            for synonym in synonyms:
                # First category to claim a synonym wins
                if synonym not in self.action_verbs:
                    self.action_verbs[synonym] = canonical
            # Also map the canonical name to itself
            if canonical not in self.action_verbs:
                self.action_verbs[canonical] = canonical

    def _load_resource_types(self):
        """Parse resources.md to build resource type index."""
        resources = load_resources_md("en", self.resource_dir)
        for category, terms in resources.items():
            self.resource_terms[category] = terms
            for term in terms:
                self.resource_types[term] = category
            # Map category name itself
            if category not in self.resource_types:
                self.resource_types[category] = category

    def _load_action_resources(self):
        """Load actions.json to know which actions apply to which resources.

        Also registers action names and aliases from actions.json as verbs
        in the action_verbs index (first-claim rule applies).
        """
        data = load_actions_json(self.resource_dir)
        # actions.json has locale keys: {"en_US": {"create": {"option": [...]}}}
        for locale_data in data.values():
            for action, details in locale_data.items():
                options = details.get("option", [])
                aliases = details.get("alias", [])
                if action not in self.action_resources:
                    self.action_resources[action] = []
                for opt in options:
                    if opt not in self.action_resources[action]:
                        self.action_resources[action].append(opt)

                # Register action and aliases as verbs
                if action not in self.action_verbs:
                    self.action_verbs[action] = action
                if action not in self.action_synonyms:
                    self.action_synonyms[action] = [action]
                for alias in aliases:
                    if alias not in self.action_verbs:
                        self.action_verbs[alias] = action
                    if alias not in self.action_synonyms[action]:
                        self.action_synonyms[action].append(alias)

    def _load_command_catalog(self):
        """Parse commands.yaml to build (action, resource_domain) -> command mappings.

        The YAML structure is:
            Action Category:        (e.g., "Create/Create New:")
              Resource Domain:      (e.g., "File Management:")
                - description: linux_command
        """
        raw = load_commands_yaml("en", self.resource_dir)
        if not raw:
            return

        for action_category, domains in raw.items():
            if not isinstance(domains, dict):
                continue
            # Extract canonical action from category
            # e.g., "Create/Create New" -> "create"
            canonical_action = action_category.split('/')[0].strip().lower()

            for domain_name, entries in domains.items():
                if not isinstance(entries, list):
                    continue
                canonical_domain = domain_name.strip().lower()
                key = (canonical_action, canonical_domain)
                if key not in self.command_catalog:
                    self.command_catalog[key] = []

                for entry in entries:
                    if isinstance(entry, str):
                        # Entry like "- vi/vim" (no colon mapping)
                        # Store as both description and command
                        self.command_catalog[key].append(
                            (entry.strip(), entry.strip().split('/')[0].strip())
                        )
                    elif isinstance(entry, dict):
                        # Should not happen with this YAML format
                        for desc, cmd in entry.items():
                            self.command_catalog[key].append((str(desc), str(cmd)))

        # Also parse entries that are strings with "description: command" format
        # The YAML loader treats "- description: command" as a dict entry
        # But "- create file/new file: touch filename" is loaded as a dict
        # Re-parse the raw data to handle this correctly
        self.command_catalog.clear()
        self._parse_commands_yaml_raw()

    def _parse_commands_yaml_raw(self):
        """Parse commands.yaml handling the dict-entry format correctly.

        The YAML loader parses entries like '- create file: touch filename'
        as a dict {\"create file\": \"touch filename\"} within a list.
        Entries like '- vi/vim' become plain strings.
        """
        raw = load_commands_yaml("en", self.resource_dir)
        if not raw:
            return

        for action_category, domains in raw.items():
            if not isinstance(domains, dict):
                continue
            canonical_action = action_category.split('/')[0].strip().lower()

            for domain_name, entries in domains.items():
                if not isinstance(entries, list):
                    continue
                canonical_domain = domain_name.strip().lower()
                key = (canonical_action, canonical_domain)
                if key not in self.command_catalog:
                    self.command_catalog[key] = []

                for entry in entries:
                    if isinstance(entry, dict):
                        for desc, cmd in entry.items():
                            cmd_str = str(cmd).strip()
                            # Extract just the base command (first word)
                            base_cmd = cmd_str.split()[0] if cmd_str else ""
                            self.command_catalog[key].append(
                                (str(desc).strip().lower(), base_cmd, cmd_str)
                            )
                    elif isinstance(entry, str):
                        # Plain string entry like "vi/vim"
                        base = entry.strip().split('/')[0].strip()
                        self.command_catalog[key].append(
                            (entry.strip().lower(), base, base)
                        )


def extract_intent_rulebased(user_input, index, locale="en_US"):
    """Rule-based intent extraction using token matching against the semantic index.

    Algorithm:
    1. Tokenize input (split on whitespace, normalize case)
    2. Match tokens against action_verbs index -> find canonical action
    3. Match remaining tokens against resource_types index -> find resource
    4. Remaining unmatched tokens become modifiers
    5. Return IntentResult with confidence based on match quality
    """
    tokens = user_input.lower().split()
    if not tokens:
        return IntentResult(confidence=0.0)

    action = None
    action_tokens_used = 0
    resource = None
    modifiers = []
    remaining_tokens = []

    # Try matching 1 or 2 tokens as an action verb
    # Try 2-token match first (e.g., "wipe out", "set up")
    if len(tokens) >= 2:
        two_word = tokens[0] + " " + tokens[1]
        if two_word in index.action_verbs:
            action = index.action_verbs[two_word]
            action_tokens_used = 2

    # Try 1-token match
    if action is None and tokens[0] in index.action_verbs:
        action = index.action_verbs[tokens[0]]
        action_tokens_used = 1

    # Try fuzzy match on first token if no exact match
    if action is None:
        close = difflib.get_close_matches(
            tokens[0], index.action_verbs.keys(), n=1, cutoff=0.7
        )
        if close:
            action = index.action_verbs[close[0]]
            action_tokens_used = 1

    if action is None:
        return IntentResult(confidence=0.0)

    # Process remaining tokens for resource and modifiers
    for token in tokens[action_tokens_used:]:
        if token in MODIFIER_MAP:
            modifiers.append(token)
        elif token in index.resource_types:
            resource = token
        elif resource is None:
            # Try fuzzy match for resource
            close = difflib.get_close_matches(
                token, index.resource_types.keys(), n=1, cutoff=0.7
            )
            if close:
                resource = close[0]
            else:
                remaining_tokens.append(token)
        else:
            remaining_tokens.append(token)

    # Calculate confidence
    confidence = 0.0
    if action:
        confidence += 0.5
    if resource:
        confidence += 0.3
        # Bonus if action+resource is a valid combination in actions.json
        if action in index.action_resources:
            if resource in index.action_resources[action]:
                confidence += 0.2

    return IntentResult(
        action=action or "",
        resource=resource or "",
        modifiers=modifiers,
        confidence=confidence,
        source="semantic",
    )


def resolve_command(intent, index):
    """Look up the Linux command for a given intent from the command catalog.

    Searches command_catalog entries for matching (action, resource) pairs.
    Returns the full command template string, or None if no match found.
    """
    if not intent.action:
        return None

    # Build modifier flags
    flags = []
    for mod in intent.modifiers:
        if mod in MODIFIER_MAP:
            flags.append(MODIFIER_MAP[mod])

    # Search command_catalog for entries matching the action
    best_match = None
    best_score = 0.0

    for (cat_action, cat_domain), entries in index.command_catalog.items():
        # Check if the catalog action matches our intent action
        if cat_action != intent.action:
            # Try if our action is a synonym of the catalog action
            cat_canonical = cat_action.split('/')[0].strip().lower()
            if cat_canonical != intent.action:
                continue

        for entry in entries:
            if len(entry) == 3:
                desc, base_cmd, full_cmd = entry
            else:
                desc, base_cmd = entry[0], entry[1]
                full_cmd = base_cmd

            # Score based on resource match in the domain name or description
            score = 0.5  # Base score for action match

            if intent.resource:
                if intent.resource in cat_domain:
                    score += 0.3
                if intent.resource in desc:
                    score += 0.2

            if score > best_score:
                best_score = score
                best_match = base_cmd
                if flags:
                    best_match = base_cmd + " " + " ".join(flags)

    return best_match
