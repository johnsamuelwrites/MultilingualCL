#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import os
from dataclasses import dataclass, field


@dataclass
class MultilingualCLConfig:
    # LLM settings
    ollama_model: str = "mistral"
    ollama_enabled: bool = True
    ollama_timeout: float = 10.0

    # Safety settings
    safety_enabled: bool = True
    auto_execute_safe: bool = True

    # REPL settings
    show_command_preview: bool = True
    locale_override: str = ""

    # Paths
    resource_dir: str = field(default_factory=lambda: os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "resources"
    ))


def load_config():
    config = MultilingualCLConfig()

    env_map = {
        "MULTILINGUALCL_OLLAMA_MODEL": ("ollama_model", str),
        "MULTILINGUALCL_OLLAMA_ENABLED": ("ollama_enabled", lambda v: v.lower() in ("1", "true", "yes")),
        "MULTILINGUALCL_OLLAMA_TIMEOUT": ("ollama_timeout", float),
        "MULTILINGUALCL_SAFETY_ENABLED": ("safety_enabled", lambda v: v.lower() in ("1", "true", "yes")),
        "MULTILINGUALCL_SHOW_PREVIEW": ("show_command_preview", lambda v: v.lower() in ("1", "true", "yes")),
        "MULTILINGUALCL_LOCALE": ("locale_override", str),
    }

    for env_var, (attr, converter) in env_map.items():
        value = os.environ.get(env_var)
        if value is not None:
            setattr(config, attr, converter(value))

    return config
