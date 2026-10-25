from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
FIXTURES = ROOT / "tests" / "fixtures"


def run_installer(
    *args: str, cwd: Optional[Path] = None, home: Optional[Path] = None
):
    env = os.environ.copy()
    if home is not None:
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
    return subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        cwd=str(cwd or ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class InstallerTests(unittest.TestCase):
    def test_list_contains_all_skills_and_agents(self):
        result = run_installer("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        for value in (
            "google-cpp-style",
            "google-rust-style",
            "google-python-style",
            "google-typescript-style",
            "claude-code",
            "codex",
        ):
            self.assertIn(value, result.stdout)

    def test_dry_run_does_not_modify_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = run_installer(
                "install",
                "--skill",
                "google-python-style",
                "--destination",
                str(destination),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Dry run", result.stdout)
            self.assertFalse(destination.exists())

    def test_selected_install_is_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = run_installer(
                "install",
                "--skill",
                "google-rust-style",
                "--destination",
                str(destination),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "google-rust-style" / "SKILL.md").is_file())
            self.assertFalse((destination / "google-python-style").exists())

    def test_all_skills_install(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = run_installer(
                "install", "--all", "--destination", str(destination)
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for skill in (
                "google-cpp-style",
                "google-rust-style",
                "google-python-style",
                "google-typescript-style",
            ):
                self.assertTrue((destination / skill / "SKILL.md").is_file())

    def test_project_agent_path_is_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            result = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--agent",
                "codex",
                "--scope",
                "project",
                "--project-root",
                str(project),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(project / ".agents" / "skills"), result.stdout)

    def test_shared_project_agent_roots_are_deduplicated(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            result = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--agent",
                "codex",
                "--agent",
                "opencode",
                "--scope",
                "project",
                "--project-root",
                str(project),
                "--dry-run",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.count("google-cpp-style:"), 1)

    def test_user_agent_paths_resolve_for_all_agents(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            home.mkdir()
            expected = {
                "claude-code": home / ".claude" / "skills",
                "codex": home / ".agents" / "skills",
                "opencode": home / ".config" / "opencode" / "skills",
                "cursor": home / ".cursor" / "skills",
                "gemini-cli": home / ".gemini" / "skills",
            }
            for agent, path in expected.items():
                result = run_installer(
                    "install",
                    "--skill",
                    "google-cpp-style",
                    "--agent",
                    agent,
                    "--scope",
                    "user",
                    "--dry-run",
                    home=home,
                )
                self.assertEqual(result.returncode, 0, (agent, result.stderr))
                self.assertIn(str(path), result.stdout)

    def test_all_documented_agent_mappings_resolve(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            for agent in ("claude-code", "codex", "opencode", "cursor", "gemini-cli"):
                result = run_installer(
                    "install",
                    "--skill",
                    "google-cpp-style",
                    "--agent",
                    agent,
                    "--scope",
                    "project",
                    "--project-root",
                    str(project),
                    "--dry-run",
                )
                self.assertEqual(result.returncode, 0, (agent, result.stderr))

    def test_conflicts_are_not_overwritten_without_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = run_installer(
                "install", "--skill", "google-cpp-style", "--destination", str(destination)
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            marker = destination / "google-cpp-style" / "operator-marker.txt"
            marker.write_text("keep me", encoding="utf-8")
            second = run_installer(
                "install", "--skill", "google-cpp-style", "--destination", str(destination)
            )
            self.assertEqual(second.returncode, 3)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")

    def test_replace_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            first = run_installer(
                "install", "--skill", "google-cpp-style", "--destination", str(destination)
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            marker = destination / "google-cpp-style" / "operator-marker.txt"
            marker.write_text("old", encoding="utf-8")
            second = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--destination",
                str(destination),
                "--replace",
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse(marker.exists())

    def test_replace_handles_existing_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            destination.mkdir()
            existing = destination / "google-cpp-style"
            existing.write_text("not a skill", encoding="utf-8")
            result = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--destination",
                str(destination),
                "--replace",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((existing / "SKILL.md").is_file())
            self.assertNotIn("Traceback", result.stderr)

    def test_uninstall_is_bounded_and_removes_exact_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            outside = Path(directory) / "outside.txt"
            outside.write_text("safe", encoding="utf-8")
            installed = run_installer(
                "install", "--skill", "google-rust-style", "--destination", str(destination)
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            removed = run_installer(
                "uninstall", "--skill", "google-rust-style", "--destination", str(destination)
            )
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertFalse((destination / "google-rust-style").exists())
            self.assertEqual(outside.read_text(encoding="utf-8"), "safe")

    def test_uninstall_refuses_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "skills"
            outside = Path(directory) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "important.txt").write_text("safe", encoding="utf-8")
            (root / "google-cpp-style").symlink_to(outside, target_is_directory=True)
            result = run_installer(
                "uninstall", "--skill", "google-cpp-style", "--destination", str(root)
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue((outside / "important.txt").exists())

    def test_uninstall_refuses_packaged_source(self):
        result = run_installer(
            "uninstall",
            "--skill",
            "google-cpp-style",
            "--destination",
            str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((ROOT / "google-cpp-style" / "SKILL.md").exists())

    def test_uninstall_refuses_destination_root_inside_any_packaged_source(self):
        destination = ROOT / "google-cpp-style"
        result = run_installer(
            "uninstall",
            "--skill",
            "google-rust-style",
            "--destination",
            str(destination),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((ROOT / "google-cpp-style" / "SKILL.md").exists())

    def test_uninstall_refuses_forged_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            target = destination / "google-cpp-style"
            target.mkdir(parents=True)
            (target / ".google-style-skills-install.json").write_text(
                json.dumps({"skill": "google-cpp-style"}), encoding="utf-8"
            )
            result = run_installer(
                "uninstall", "--skill", "google-cpp-style", "--destination", str(destination)
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(target.exists())

    def test_uninstall_refuses_non_object_marker_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            target = destination / "google-cpp-style"
            target.mkdir(parents=True)
            (target / ".google-style-skills-install.json").write_text(
                "null", encoding="utf-8"
            )
            result = run_installer(
                "uninstall", "--skill", "google-cpp-style", "--destination", str(destination)
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)

    def test_install_refuses_destination_inside_packaged_source(self):
        destination = ROOT / "google-cpp-style" / ".test-destination"
        result = run_installer(
            "install",
            "--skill",
            "google-rust-style",
            "--destination",
            str(destination),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())

    def test_uninstall_preflights_missing_targets_before_deleting(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            installed = run_installer(
                "install", "--skill", "google-rust-style", "--destination", str(destination)
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            result = run_installer(
                "uninstall",
                "--skill",
                "google-rust-style",
                "--skill",
                "google-python-style",
                "--destination",
                str(destination),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue((destination / "google-rust-style").exists())

    def test_invalid_skill_and_scope_fail_usefully(self):
        with tempfile.TemporaryDirectory() as directory:
            unknown = run_installer(
                "install",
                "--skill",
                "not-a-skill",
                "--destination",
                str(Path(directory) / "skills"),
            )
            self.assertEqual(unknown.returncode, 2)
            self.assertIn("Unknown skill", unknown.stderr)
            bad_scope = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--scope",
                "machine",
                "--agent",
                "codex",
            )
            self.assertEqual(bad_scope.returncode, 2)

    def test_destination_parent_error_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            parent_file = Path(directory) / "not-a-directory"
            parent_file.write_text("file", encoding="utf-8")
            result = run_installer(
                "install",
                "--skill",
                "google-cpp-style",
                "--destination",
                str(parent_file / "skills"),
            )
            self.assertEqual(result.returncode, 7)
            self.assertIn("destination root", result.stderr.lower())


class FixtureScenarioTests(unittest.TestCase):
    def test_all_language_scenarios_have_valid_and_invalid_fixtures(self):
        scenarios = json.loads(
            (FIXTURES / "style-scenarios.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(scenarios), 4)
        for scenario in scenarios:
            self.assertIn(scenario["skill"], {
                "google-cpp-style",
                "google-rust-style",
                "google-python-style",
                "google-typescript-style",
            })
            self.assertTrue((FIXTURES / scenario["valid_fixture"]).is_file())
            self.assertTrue((FIXTURES / scenario["invalid_fixture"]).is_file())
            self.assertGreaterEqual(len(scenario["signals"]), 3)
            self.assertTrue(scenario["non_style_boundary"])

    def test_skill_descriptions_are_language_scoped(self):
        contents = {
            skill: (ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
            for skill in (
                "google-cpp-style",
                "google-rust-style",
                "google-python-style",
                "google-typescript-style",
            )
        }
        self.assertIn("C++", contents["google-cpp-style"])
        self.assertIn("Rust", contents["google-rust-style"])
        self.assertIn("Python", contents["google-python-style"])
        self.assertIn("TypeScript", contents["google-typescript-style"])
        self.assertNotIn("Apply this skill only for Python", contents["google-cpp-style"])


if __name__ == "__main__":
    unittest.main()
