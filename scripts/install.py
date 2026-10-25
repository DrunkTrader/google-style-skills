#!/usr/bin/env python3
"""Install the portable Google style Agent Skills.

This installer intentionally uses only the Python standard library. It plans
all operations before writing, refuses conflicts by default, stages copies, and
keeps uninstall bounded to the resolved destination root.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


SKILLS = (
    "google-cpp-style",
    "google-rust-style",
    "google-python-style",
    "google-typescript-style",
)

# These paths are documented by the Agent Skills compatibility reference and,
# for Claude Code/Codex, by their product documentation. Project paths are
# relative to the selected project root. Global paths are relative to HOME.
AGENT_PATHS = {
    "claude-code": {"project": ".claude/skills", "user": ".claude/skills"},
    "codex": {"project": ".agents/skills", "user": ".agents/skills"},
    "opencode": {"project": ".agents/skills", "user": ".config/opencode/skills"},
    "cursor": {"project": ".agents/skills", "user": ".cursor/skills"},
    "gemini-cli": {"project": ".agents/skills", "user": ".gemini/skills"},
}

AGENT_COMMANDS = {
    "claude-code": "claude",
    "codex": "codex",
    "opencode": "opencode",
    "cursor": "cursor",
    "gemini-cli": "gemini",
}

EXIT_USAGE = 2
EXIT_CONFLICT = 3
EXIT_UNSUPPORTED = 4
EXIT_PERMISSION = 5
EXIT_PARTIAL = 6
EXIT_IO = 7
INSTALL_MARKER = ".google-style-skills-install.json"
INSTALLER_VERSION = "1"


class InstallerError(Exception):
    """An expected, actionable installer error."""

    def __init__(self, message: str, code: int = EXIT_USAGE) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Operation:
    skill: str
    source: Path
    destination_root: Path
    destination: Path
    agent: str
    scope: str


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def validate_skill_name(name: str) -> None:
    if name not in SKILLS:
        raise InstallerError(
            "Unknown skill {!r}. Choose one of: {}".format(
                name, ", ".join(SKILLS)
            ),
            EXIT_USAGE,
        )


def select_skills(values: Optional[Sequence[str]], install_all: bool) -> List[str]:
    selected = list(values or [])
    if install_all and selected:
        raise InstallerError("Use --all or --skill, not both.")
    if install_all:
        return list(SKILLS)
    if not selected:
        raise InstallerError("Select at least one skill with --skill or --all.")
    for name in selected:
        validate_skill_name(name)
    if len(set(selected)) != len(selected):
        raise InstallerError("Each skill may be selected only once.")
    return selected


def path_exists_for_agent(agent: str, scope: str, project_root: Path) -> bool:
    config = AGENT_PATHS[agent]
    home = Path.home()
    base = home if scope == "user" else project_root
    path_exists = (base / config[scope]).exists()
    return (
        path_exists
        or shutil.which(AGENT_COMMANDS[agent]) is not None
    )


def detect_agents(scope: str, project_root: Path) -> List[str]:
    return [
        agent
        for agent in AGENT_PATHS
        if path_exists_for_agent(agent, scope, project_root)
    ]


def normalize_root(path: Path) -> Path:
    try:
        return path.expanduser().resolve(strict=False)
    except RuntimeError as exc:
        raise InstallerError(
            "Could not resolve path {} because it contains a symlink loop: {}".format(
                path, exc
            ),
            EXIT_USAGE,
        )


def resolve_agent_root(agent: str, scope: str, project_root: Path) -> Path:
    if agent not in AGENT_PATHS:
        raise InstallerError(
            "Unsupported agent {!r}. Supported agents: {}. Use --destination "
            "for a compatible agent with a different documented path.".format(
                agent, ", ".join(AGENT_PATHS)
            ),
            EXIT_UNSUPPORTED,
        )
    relative = Path(AGENT_PATHS[agent][scope])
    if scope == "user":
        return normalize_root(Path.home() / relative)
    return normalize_root(project_root / relative)


def select_destinations(args: argparse.Namespace) -> List[Tuple[str, str, Path]]:
    explicit_destination = args.destination is not None
    explicit_agents = list(args.agent or [])
    if explicit_destination and args.auto_detect:
        raise InstallerError("Do not combine --destination with --auto-detect.")
    if explicit_destination and len(explicit_agents) > 1:
        raise InstallerError(
            "An explicit --destination is a single destination; select at most one agent."
        )
    if explicit_destination:
        label = explicit_agents[0] if explicit_agents else "custom"
        if explicit_agents and explicit_agents[0] not in AGENT_PATHS:
            raise InstallerError(
                "Unknown agent {!r}; omit --agent for a custom destination or "
                "choose one of: {}".format(label, ", ".join(AGENT_PATHS)),
                EXIT_UNSUPPORTED,
            )
        return [(label, "custom", normalize_root(Path(args.destination)))]

    project_root = normalize_root(Path(args.project_root))
    if args.auto_detect and explicit_agents:
        raise InstallerError("Do not combine --auto-detect with --agent.")
    if args.auto_detect:
        explicit_agents = detect_agents(args.scope, project_root)
        if not explicit_agents:
            raise InstallerError(
                "No supported agents were detected. Specify --agent or an explicit "
                "--destination.",
                EXIT_UNSUPPORTED,
            )
    if not explicit_agents:
        raise InstallerError(
            "Specify --agent, --auto-detect, or --destination."
        )

    destinations = []
    seen_roots = set()
    for agent in explicit_agents:
        if agent not in AGENT_PATHS:
            raise InstallerError(
                "Unsupported agent {!r}. Supported agents: {}. Use --destination "
                "for a compatible agent with a different documented path.".format(
                    agent, ", ".join(AGENT_PATHS)
                ),
                EXIT_UNSUPPORTED,
            )
        destination_root = resolve_agent_root(agent, args.scope, project_root)
        key = (args.scope, destination_root)
        if key not in seen_roots:
            destinations.append((agent, args.scope, destination_root))
            seen_roots.add(key)
    return destinations


def build_operations(
    skills: Iterable[str], destinations: Iterable[Tuple[str, str, Path]]
) -> List[Operation]:
    root = repository_root()
    operations = []
    for agent, scope, destination_root in destinations:
        for skill in skills:
            source = root / skill
            if not source.is_dir() or not (source / "SKILL.md").is_file():
                raise InstallerError(
                    "Source skill is missing or incomplete: {}".format(source)
                )
            destination = destination_root / skill
            operations.append(
                Operation(
                    skill=skill,
                    source=source,
                    destination_root=destination_root,
                    destination=destination,
                    agent=agent,
                    scope=scope,
                )
            )
    return operations


def same_path(left: Path, right: Path) -> bool:
    return left.resolve(strict=False) == right.resolve(strict=False)


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def source_skill_paths() -> List[Path]:
    root = repository_root()
    return [root / skill for skill in SKILLS]


def reject_source_overlap(path: Path, label: str) -> None:
    for source in source_skill_paths():
        if path_is_within(path, source):
            raise InstallerError(
                "Refusing to {} inside a packaged source skill: {}. Choose an "
                "agent path or a separate destination.".format(label, path),
                EXIT_CONFLICT,
            )


def remove_path(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        path.unlink()
    else:
        shutil.rmtree(path)


def write_install_marker(staged: Path, operation: Operation) -> None:
    marker = staged / INSTALL_MARKER
    marker.write_text(
        json.dumps(
            {
                "installer": "google-style-skills",
                "installer_version": INSTALLER_VERSION,
                "skill": operation.skill,
                "source": str(operation.source),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check_common_operation(operation: Operation, replace: bool) -> None:
    destination_root = operation.destination_root
    if same_path(destination_root, repository_root()):
        raise InstallerError(
            "Refusing to install into the repository root; choose an agent path "
            "or a separate --destination."
        )
    reject_source_overlap(destination_root, "install")
    if same_path(operation.destination, operation.source):
        raise InstallerError(
            "Source and destination are identical for {}: {}".format(
                operation.skill, operation.destination
            )
        )
    if operation.destination.exists() or operation.destination.is_symlink():
        if not replace:
            raise InstallerError(
                "Destination already exists: {}. Inspect it or rerun with "
                "--replace after explicitly approving replacement.".format(
                    operation.destination
                ),
                EXIT_CONFLICT,
            )


def print_operations(operations: Sequence[Operation], action: str, replace: bool) -> None:
    print("{} plan ({} operation{}):".format(action.capitalize(), len(operations), "" if len(operations) == 1 else "s"))
    for operation in operations:
        suffix = " [replace]" if replace and operation.destination.exists() else ""
        print("  {}: {} -> {}{}".format(operation.skill, operation.source, operation.destination, suffix))


def copy_staged(operation: Operation, replace: bool) -> None:
    parent = operation.destination_root
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except PermissionError as exc:
        raise InstallerError(
            "Permission denied while creating destination root {}: {}".format(
                parent, exc
            ),
            EXIT_PERMISSION,
        )
    except OSError as exc:
        raise InstallerError(
            "Could not create destination root {}: {}".format(parent, exc),
            EXIT_IO,
        )
    stage_parent = None
    backup = None
    try:
        try:
            stage_parent = Path(
                tempfile.mkdtemp(prefix=".google-style-stage-", dir=str(parent))
            )
        except PermissionError as exc:
            raise InstallerError(
                "Permission denied while staging {}: {}".format(parent, exc),
                EXIT_PERMISSION,
            )
        except OSError as exc:
            raise InstallerError(
                "Could not create a staging directory in {}: {}".format(parent, exc),
                EXIT_IO,
            )

        staged = stage_parent / operation.skill
        shutil.copytree(operation.source, staged, symlinks=True)
        write_install_marker(staged, operation)
        if operation.destination.exists() or operation.destination.is_symlink():
            if not replace:
                raise InstallerError(
                    "Destination changed after planning: {}".format(
                        operation.destination
                    ),
                    EXIT_CONFLICT,
                )
            backup = parent / (".{}-backup-{}".format(operation.skill, uuid.uuid4().hex))
            os.replace(str(operation.destination), str(backup))
        os.replace(str(staged), str(operation.destination))
        if backup is not None and backup.exists():
            try:
                remove_path(backup)
            except OSError as exc:
                raise InstallerError(
                    "Installed {} but could not remove the previous backup {}: {}".format(
                        operation.skill, backup, exc
                    ),
                    EXIT_PARTIAL,
                )
    except InstallerError as exc:
        if backup is not None and backup.exists() and not operation.destination.exists():
            try:
                os.replace(str(backup), str(operation.destination))
            except OSError as restore_exc:
                raise InstallerError(
                    "{} Recovery also failed while restoring {}: {}".format(
                        exc, operation.destination, restore_exc
                    ),
                    EXIT_PARTIAL,
                )
        raise
    except PermissionError as exc:
        if backup is not None and not operation.destination.exists() and backup.exists():
            try:
                os.replace(str(backup), str(operation.destination))
            except OSError as restore_exc:
                raise InstallerError(
                    "Permission denied while installing {} to {}: {}. Recovery also "
                    "failed: {}".format(
                        operation.skill, operation.destination, exc, restore_exc
                    ),
                    EXIT_PARTIAL,
                )
        raise InstallerError(
            "Permission denied while installing {} to {}: {}".format(
                operation.skill, operation.destination, exc
            ),
            EXIT_PERMISSION,
        )
    except OSError as exc:
        if backup is not None and not operation.destination.exists() and backup.exists():
            try:
                os.replace(str(backup), str(operation.destination))
            except OSError as restore_exc:
                raise InstallerError(
                    "Could not install {} to {}: {}. Recovery also failed: {}".format(
                        operation.skill, operation.destination, exc, restore_exc
                    ),
                    EXIT_PARTIAL,
                )
        raise InstallerError(
            "Could not install {} to {}: {}".format(
                operation.skill, operation.destination, exc
            ),
            EXIT_IO,
        )
    finally:
        if stage_parent is not None:
            shutil.rmtree(stage_parent, ignore_errors=True)


def install(operations: Sequence[Operation], dry_run: bool, replace: bool) -> int:
    for operation in operations:
        check_common_operation(operation, replace)
    print_operations(operations, "installation", replace)
    if dry_run:
        print("Dry run: no files were modified.")
        return 0

    completed = []
    for operation in operations:
        try:
            copy_staged(operation, replace)
        except InstallerError as exc:
            if completed:
                print(
                    "Partial installation: completed {}. The failed operation was {}. "
                    "Inspect the listed destination and rerun only after resolving "
                    "the error.".format(", ".join(completed), operation.destination),
                    file=sys.stderr,
                )
                raise InstallerError(str(exc), max(exc.code, EXIT_PARTIAL))
            raise
        completed.append(operation.skill + " @ " + str(operation.destination))
    print("Installed {} skill{}.".format(len(operations), "" if len(operations) == 1 else "s"))
    return 0


def check_uninstall_target(operation: Operation) -> None:
    root = operation.destination_root.resolve(strict=False)
    target = operation.destination
    if target.parent.resolve(strict=False) != root:
        raise InstallerError(
            "Unsafe uninstall target outside destination root: {}".format(target),
            EXIT_USAGE,
        )
    for source in source_skill_paths():
        if path_is_within(root, source) or path_is_within(target, source):
            raise InstallerError(
                "Refusing to uninstall inside a packaged source skill: {}".format(
                    target
                ),
                EXIT_CONFLICT,
            )
    if target.is_symlink():
        raise InstallerError(
            "Refusing to uninstall a symlink; inspect it manually so an external "
            "target cannot be removed: {}".format(target),
            EXIT_CONFLICT,
        )
    if target.exists() and target.resolve(strict=False).parent != root:
        raise InstallerError(
            "Unsafe uninstall target resolves outside destination root: {}".format(target),
            EXIT_CONFLICT,
        )
    if not target.exists():
        return
    if not target.is_dir():
        raise InstallerError(
            "Refusing to uninstall a non-directory target: {}".format(target),
            EXIT_CONFLICT,
        )
    marker = target / INSTALL_MARKER
    if not marker.is_file():
        raise InstallerError(
            "Refusing to uninstall an unowned skill directory without {}: {}".format(
                INSTALL_MARKER, target
            ),
            EXIT_CONFLICT,
        )
    try:
        metadata = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InstallerError(
            "Refusing to uninstall a skill with an invalid install marker {}: {}".format(
                marker, exc
            ),
            EXIT_CONFLICT,
        )
    if not isinstance(metadata, dict):
        raise InstallerError(
            "Install marker must contain a JSON object: {}".format(marker),
            EXIT_CONFLICT,
        )
    if metadata.get("installer") != "google-style-skills":
        raise InstallerError(
            "Install marker is not owned by this installer: {}".format(marker),
            EXIT_CONFLICT,
        )
    if metadata.get("installer_version") != INSTALLER_VERSION:
        raise InstallerError(
            "Install marker version is unsupported: {}".format(marker),
            EXIT_CONFLICT,
        )
    if metadata.get("source") != str(operation.source):
        raise InstallerError(
            "Install marker source does not match {}: {}".format(
                operation.skill, marker
            ),
            EXIT_CONFLICT,
        )
    if metadata.get("skill") != operation.skill:
        raise InstallerError(
            "Install marker does not match {}: {}".format(operation.skill, marker),
            EXIT_CONFLICT,
        )


def uninstall(operations: Sequence[Operation], dry_run: bool) -> int:
    for operation in operations:
        check_uninstall_target(operation)
    print_operations(operations, "uninstall", False)
    missing = [str(operation.destination) for operation in operations if not operation.destination.exists()]
    if missing:
        raise InstallerError(
            "Skill was not installed at: {}".format(", ".join(missing)),
            EXIT_CONFLICT,
        )
    if dry_run:
        print("Dry run: no files were modified.")
        return 0
    for operation in operations:
        target = operation.destination
        try:
            remove_path(target)
        except PermissionError as exc:
            raise InstallerError(
                "Permission denied while uninstalling {}: {}".format(target, exc),
                EXIT_PERMISSION,
            )
        except OSError as exc:
            raise InstallerError(
                "Could not uninstall {}: {}".format(target, exc),
                EXIT_IO,
            )
    if missing:
        raise InstallerError(
            "Skill was not installed at: {}".format(", ".join(missing)),
            EXIT_CONFLICT,
        )
    print("Uninstalled {} skill{}.".format(len(operations), "" if len(operations) == 1 else "s"))
    return 0


def print_list() -> int:
    print("Available skills:")
    for skill in SKILLS:
        print("  {}".format(skill))
    print("\nSupported agent path mappings:")
    for agent, paths in AGENT_PATHS.items():
        print("  {}: project ./{}, user ~/{}".format(agent, paths["project"], paths["user"]))
    project_root = normalize_root(Path.cwd())
    detected = detect_agents("project", project_root)
    print("\nDetected agents in this environment: {}".format(", ".join(detected) if detected else "none"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="list skills, agent mappings, and detection results")

    def add_target_args(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--skill", action="append", help="skill name; repeat for multiple skills")
        subparser.add_argument("--all", action="store_true", help="select all four skills")
        subparser.add_argument("--agent", action="append", help="supported agent name; repeat for multiple agents")
        subparser.add_argument("--auto-detect", action="store_true", help="detect supported agents with known local paths")
        subparser.add_argument("--scope", choices=("project", "user"), default="project")
        subparser.add_argument("--project-root", default=str(Path.cwd()), help="project root for project scope")
        subparser.add_argument("--destination", help="explicit destination root for one custom installation")
        subparser.add_argument("--dry-run", action="store_true", help="print the plan without modifying files")

    install_parser = subparsers.add_parser("install", help="install selected skills")
    add_target_args(install_parser)
    install_parser.add_argument("--replace", action="store_true", help="replace existing exact skill directories")

    uninstall_parser = subparsers.add_parser("uninstall", help="remove selected installed skills")
    add_target_args(uninstall_parser)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            return print_list()
        skills = select_skills(args.skill, args.all)
        destinations = select_destinations(args)
        operations = build_operations(skills, destinations)
        if args.command == "install":
            return install(operations, args.dry_run, args.replace)
        return uninstall(operations, args.dry_run)
    except InstallerError as exc:
        print("Error: {}".format(exc), file=sys.stderr)
        return exc.code
    except KeyboardInterrupt:
        print("Interrupted; no further operations were attempted.", file=sys.stderr)
        return EXIT_PARTIAL


if __name__ == "__main__":
    sys.exit(main())
