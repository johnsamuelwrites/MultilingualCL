import os
import re
import json
import yaml


def _default_resource_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "..", "resources")


def load_command_map_from_directory(directory):
    """
    Load command map from YAML files in the specified directory.

    Args:
        directory (str): The directory path containing the YAML files.

    Returns:
        dict: A dictionary representing the loaded command map.

    """
    command_map = {}
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                file_commands = yaml.safe_load(file)
                command_map.update(file_commands)
    return command_map


def load_command_map():
    """
    Loads a command map from the specified directory.

    :return: A dictionary representing the command map.
    """
    command_map_directory = os.path.join(_default_resource_dir(), "yaml")

    command_map = load_command_map_from_directory(command_map_directory)
    return command_map


def load_actions_json(resource_dir=None):
    """Load resources/actions.json -- action-to-resource mappings per locale."""
    if resource_dir is None:
        resource_dir = _default_resource_dir()
    path = os.path.join(resource_dir, "actions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_commandline_json(resource_dir=None):
    """Load resources/commandline.json -- CLI terminology and resource labels."""
    if resource_dir is None:
        resource_dir = _default_resource_dir()
    path = os.path.join(resource_dir, "commandline.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_commands_yaml(locale="en", resource_dir=None):
    """Load resources/{locale}/commands.yaml or commandes.yaml.

    Returns the raw parsed content (a nested dict/list structure).
    """
    if resource_dir is None:
        resource_dir = _default_resource_dir()
    lang_code = locale[:2] if len(locale) > 2 else locale
    locale_dir = os.path.join(resource_dir, lang_code)
    if os.path.isdir(locale_dir):
        for fname in os.listdir(locale_dir):
            if fname.endswith(".yaml"):
                path = os.path.join(locale_dir, fname)
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
    return {}


def load_actions_md(locale="en", resource_dir=None):
    """Parse resources/{locale}/actions.md into {canonical_action: [synonyms]}.

    The file format uses markdown headers like '* Create:' followed by
    indented bullet items like '    - create'.
    """
    if resource_dir is None:
        resource_dir = _default_resource_dir()
    lang_code = locale[:2] if len(locale) > 2 else locale
    path = os.path.join(resource_dir, lang_code, "actions.md")
    if not os.path.isfile(path):
        return {}

    actions = {}
    current_category = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            # Match category header: '* Create:' or '* Delete/Remove:'
            cat_match = re.match(r'^\*\s+(.+?):', line)
            if cat_match:
                raw_category = cat_match.group(1)
                # Take the first word (lowercased) as the canonical action
                # e.g., 'Delete/Remove' -> 'delete'
                canonical = raw_category.split('/')[0].strip().lower()
                current_category = canonical
                if current_category not in actions:
                    actions[current_category] = []
                continue

            # Match synonym entry: '    - create' or '    - wipe out'
            syn_match = re.match(r'^\s+-\s+(.+)', line)
            if syn_match and current_category is not None:
                synonym = syn_match.group(1).strip().lower()
                if synonym not in actions[current_category]:
                    actions[current_category].append(synonym)

    return actions


def load_resources_md(locale="en", resource_dir=None):
    """Parse resources/{locale}/resources.md into {category: [terms]}.

    The file format uses '* Category:' headers with indented '    - term' items.
    """
    if resource_dir is None:
        resource_dir = _default_resource_dir()
    lang_code = locale[:2] if len(locale) > 2 else locale
    path = os.path.join(resource_dir, lang_code, "resources.md")
    if not os.path.isfile(path):
        return {}

    resources = {}
    current_category = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            cat_match = re.match(r'^\*\s+(.+?):', line)
            if cat_match:
                current_category = cat_match.group(1).strip().lower()
                if current_category not in resources:
                    resources[current_category] = []
                continue

            term_match = re.match(r'^\s+-\s+(.+)', line)
            if term_match and current_category is not None:
                term = term_match.group(1).strip().lower()
                if term not in resources[current_category]:
                    resources[current_category].append(term)

    return resources
