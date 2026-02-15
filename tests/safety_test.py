#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from multilingualcl.safety import classify_risk, RiskLevel


class SafetyTestSuite(unittest.TestCase):

    def test_ls_is_safe(self):
        result = classify_risk("ls -la")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_pwd_is_safe(self):
        result = classify_risk("pwd")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_cat_is_safe(self):
        result = classify_risk("cat file.txt")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_git_status_is_safe(self):
        result = classify_risk("git status")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_git_log_is_safe(self):
        result = classify_risk("git log")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_grep_is_safe(self):
        result = classify_risk("grep pattern file.txt")
        self.assertEqual(result.risk_level, RiskLevel.SAFE)

    def test_mkdir_is_moderate(self):
        result = classify_risk("mkdir newdir")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_touch_is_moderate(self):
        result = classify_risk("touch file.txt")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_git_commit_is_moderate(self):
        result = classify_risk("git commit -m 'message'")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_cp_is_moderate(self):
        result = classify_risk("cp file1 file2")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_mv_is_moderate(self):
        result = classify_risk("mv old new")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_rm_is_dangerous(self):
        result = classify_risk("rm file.txt")
        self.assertEqual(result.risk_level, RiskLevel.DANGEROUS)

    def test_chmod_is_dangerous(self):
        result = classify_risk("chmod 777 file.txt")
        self.assertEqual(result.risk_level, RiskLevel.DANGEROUS)

    def test_kill_is_dangerous(self):
        result = classify_risk("kill 1234")
        self.assertEqual(result.risk_level, RiskLevel.DANGEROUS)

    def test_sudo_is_dangerous(self):
        result = classify_risk("sudo apt install pkg")
        self.assertEqual(result.risk_level, RiskLevel.DANGEROUS)

    def test_rm_rf_root_is_destructive(self):
        result = classify_risk("rm -rf /")
        self.assertEqual(result.risk_level, RiskLevel.DESTRUCTIVE)

    def test_mkfs_is_destructive(self):
        result = classify_risk("mkfs.ext4 /dev/sda1")
        self.assertEqual(result.risk_level, RiskLevel.DESTRUCTIVE)

    def test_shutdown_is_destructive(self):
        result = classify_risk("shutdown now")
        self.assertEqual(result.risk_level, RiskLevel.DESTRUCTIVE)

    def test_safe_does_not_require_confirm(self):
        result = classify_risk("ls")
        self.assertFalse(result.requires_confirm)

    def test_moderate_does_not_require_confirm(self):
        result = classify_risk("mkdir foo")
        self.assertFalse(result.requires_confirm)

    def test_dangerous_requires_confirm(self):
        result = classify_risk("rm file.txt")
        self.assertTrue(result.requires_confirm)

    def test_destructive_requires_confirm(self):
        result = classify_risk("rm -rf /")
        self.assertTrue(result.requires_confirm)

    def test_unknown_command_defaults_to_moderate(self):
        result = classify_risk("some_unknown_tool --flag")
        self.assertEqual(result.risk_level, RiskLevel.MODERATE)

    def test_result_has_explanation(self):
        result = classify_risk("ls")
        self.assertIsInstance(result.explanation, str)
        self.assertGreater(len(result.explanation), 0)

    def test_result_has_command(self):
        result = classify_risk("ls -la")
        self.assertEqual(result.command, "ls -la")
