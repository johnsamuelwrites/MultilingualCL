#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re
from enum import Enum
from dataclasses import dataclass


class RiskLevel(Enum):
    SAFE = "safe"
    MODERATE = "moderate"
    DANGEROUS = "dangerous"
    DESTRUCTIVE = "destructive"


@dataclass
class SafetyResult:
    risk_level: RiskLevel
    command: str
    explanation: str
    requires_confirm: bool


# Patterns checked from most dangerous to least dangerous.
# Each pattern is a regex matched against the full command string.
RISK_PATTERNS = {
    RiskLevel.DESTRUCTIVE: [
        r'^rm\s+.*-[a-zA-Z]*r[a-zA-Z]*f.*\s*/',
        r'^rm\s+.*-[a-zA-Z]*f[a-zA-Z]*r.*\s*/',
        r'^rm\s+-rf\s',
        r'^rm\s+-fr\s',
        r'^mkfs\b',
        r'^dd\b',
        r'^fdisk\b',
        r'^parted\b',
        r'>\s*/dev/',
        r'^shutdown\b',
        r'^reboot\b',
        r'^poweroff\b',
    ],
    RiskLevel.DANGEROUS: [
        r'^rm\b',
        r'^chmod\b',
        r'^chown\b',
        r'^kill\b',
        r'^killall\b',
        r'^sudo\b',
        r'^userdel\b',
        r'^groupdel\b',
        r'^git\s+push\s+.*--force',
        r'^git\s+push\s+-f\b',
        r'^git\s+reset\s+--hard',
    ],
    RiskLevel.MODERATE: [
        r'^git\s+commit\b',
        r'^git\s+add\b',
        r'^git\s+push\b',
        r'^mkdir\b',
        r'^touch\b',
        r'^mv\b',
        r'^cp\b',
        r'^tar\b',
        r'^gzip\b',
        r'^gunzip\b',
        r'^zip\b',
        r'^unzip\b',
        r'^useradd\b',
        r'^groupadd\b',
        r'^usermod\b',
        r'^groupmod\b',
    ],
    RiskLevel.SAFE: [
        r'^ls\b',
        r'^pwd\b',
        r'^cat\b',
        r'^head\b',
        r'^tail\b',
        r'^whoami\b',
        r'^date\b',
        r'^uname\b',
        r'^hostname\b',
        r'^uptime\b',
        r'^free\b',
        r'^df\b',
        r'^du\b',
        r'^who\b',
        r'^w\b',
        r'^ps\b',
        r'^wc\b',
        r'^file\b',
        r'^echo\b',
        r'^printf\b',
        r'^history\b',
        r'^git\s+status\b',
        r'^git\s+log\b',
        r'^git\s+diff\b',
        r'^git\s+branch\b',
        r'^grep\b',
        r'^find\b',
        r'^diff\b',
        r'^sort\b',
        r'^uniq\b',
        r'^lspci\b',
        r'^lsusb\b',
        r'^lsblk\b',
        r'^top\b',
        r'^htop\b',
        r'^jobs\b',
        r'^fg\b',
        r'^nslookup\b',
        r'^ifconfig\b',
        r'^ip\b',
        r'^netstat\b',
        r'^ss\b',
    ],
}

RISK_EXPLANATIONS = {
    RiskLevel.SAFE: "This command is read-only and safe to execute.",
    RiskLevel.MODERATE: "This command modifies files or system state.",
    RiskLevel.DANGEROUS: "This command can delete data or change permissions.",
    RiskLevel.DESTRUCTIVE: "This command can cause irreversible damage.",
}


def classify_risk(command):
    """Classify a command's risk level using regex patterns.

    Checks patterns from most dangerous to least dangerous.
    Unknown commands default to MODERATE.
    """
    command = command.strip()

    # Check from most dangerous to least
    for risk_level in [RiskLevel.DESTRUCTIVE, RiskLevel.DANGEROUS,
                       RiskLevel.MODERATE, RiskLevel.SAFE]:
        for pattern in RISK_PATTERNS[risk_level]:
            if re.search(pattern, command):
                requires_confirm = risk_level in (
                    RiskLevel.DANGEROUS, RiskLevel.DESTRUCTIVE
                )
                return SafetyResult(
                    risk_level=risk_level,
                    command=command,
                    explanation=RISK_EXPLANATIONS[risk_level],
                    requires_confirm=requires_confirm,
                )

    # Unknown commands default to MODERATE
    return SafetyResult(
        risk_level=RiskLevel.MODERATE,
        command=command,
        explanation="Unknown command -- treating as moderate risk.",
        requires_confirm=False,
    )


def confirm_execution(safety_result):
    """Interactive confirmation based on risk level.

    SAFE: no prompt needed
    MODERATE: no prompt needed
    DANGEROUS: require 'y' to proceed
    DESTRUCTIVE: require typing 'yes' to proceed
    """
    if safety_result.risk_level == RiskLevel.DESTRUCTIVE:
        print(f"\n  WARNING: {safety_result.explanation}")
        print(f"  Command: {safety_result.command}")
        response = input("  Type 'yes' to confirm: ")
        return response.strip().lower() == "yes"

    if safety_result.risk_level == RiskLevel.DANGEROUS:
        print(f"\n  Warning: {safety_result.explanation}")
        print(f"  Command: {safety_result.command}")
        response = input("  Proceed? [y/N]: ")
        return response.strip().lower() in ("y", "yes")

    return True
