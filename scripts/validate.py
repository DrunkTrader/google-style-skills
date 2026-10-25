#!/usr/bin/env python3
"""Run deterministic structural checks for the Google style skill pack."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from pathlib import PureWindowsPath


SKILLS = (
    "google-cpp-style",
    "google-rust-style",
    "google-python-style",
    "google-typescript-style",
)
REQUIRED_FRONTMATTER = ("name", "description")
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
URL_SCHEMES = {"http", "https"}


class ValidationError(Exception):
    pass


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("{}: frontmatter must start on the first line".format(path))
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        raise ValidationError("{}: frontmatter has no closing ---".format(path))
    values = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            raise ValidationError("{}: invalid frontmatter line: {}".format(path, line))
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values, "\n".join(lines[end + 1 :])


def validate_frontmatter(skill_dir: Path) -> None:
    path = skill_dir / "SKILL.md"
    values, body = parse_frontmatter(path)
    for key in REQUIRED_FRONTMATTER:
        if not values.get(key):
            raise ValidationError("{}: missing required frontmatter field {}".format(path, key))
    name = values["name"]
    if not NAME_RE.fullmatch(name) or "--" in name or len(name) > 64:
        raise ValidationError("{}: invalid Agent Skills name {!r}".format(path, name))
    if name != skill_dir.name:
        raise ValidationError("{}: name {!r} does not match directory".format(path, name))
    if not 1 <= len(values["description"]) <= 1024:
        raise ValidationError("{}: description length is outside 1..1024".format(path))
    if len(body.strip()) == 0:
        raise ValidationError("{}: skill body is empty".format(path))
    if "references/" not in body:
        raise ValidationError("{}: body must point to local references".format(path))


def validate_links(path: Path, root: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(" ", 1)[0].strip("<>")
        if not target or target.startswith("#"):
            continue
        parsed = urlparse(target)
        if parsed.scheme:
            if parsed.scheme not in URL_SCHEMES or not parsed.netloc:
                raise ValidationError("{}: invalid external URL {!r}".format(path, target))
            continue
        local_target = target.split("#", 1)[0].split("?", 1)[0]
        if not local_target:
            continue
        if Path(local_target).is_absolute() or PureWindowsPath(local_target).is_absolute():
            raise ValidationError("{}: absolute local link is not allowed: {}".format(path, target))
        try:
            local = (path.parent / local_target).resolve(strict=False)
            pack_root = root.resolve(strict=False)
        except RuntimeError as exc:
            raise ValidationError(
                "{}: could not resolve local link {}: {}".format(path, target, exc)
            )
        try:
            local.relative_to(pack_root)
        except ValueError:
            raise ValidationError(
                "{}: local link escapes the pack root: {}".format(path, target)
            )
        if not local.exists():
            raise ValidationError("{}: relative link does not exist: {}".format(path, target))


def validate_source_records(root: Path) -> None:
    for skill in SKILLS:
        references = root / skill / "references"
        record = references / "source-and-license.md"
        if not record.is_file():
            raise ValidationError("{}: missing source attribution record".format(record))
        text = record.read_text(encoding="utf-8")
        for marker in ("google.github.io/styleguide/", "CC BY 3.0", "Apache 2.0", "independently maintained"):
            if marker not in text:
                raise ValidationError("{}: missing attribution marker {!r}".format(record, marker))
        if len(list(references.glob("*.md"))) < 2:
            raise ValidationError("{}: expected detailed reference files".format(references))


def validate_mapping(root: Path) -> None:
    mapping = root / "docs" / "SOURCE_MAPPING.md"
    if not mapping.is_file():
        raise ValidationError("Missing {}".format(mapping))
    text = mapping.read_text(encoding="utf-8")
    for marker in ("## C++", "## Rust", "## Python", "## TypeScript", "Status", "Covered"):
        if marker not in text:
            raise ValidationError("{}: missing coverage marker {!r}".format(mapping, marker))
    if re.search(r"\|\s*Not yet covered\s*\|", text):
        raise ValidationError("{}: unexplained Not yet covered entry remains".format(mapping))


def validate(root: Path) -> None:
    for skill in SKILLS:
        skill_dir = root / skill
        if not skill_dir.is_dir():
            raise ValidationError("Missing skill directory {}".format(skill_dir))
        validate_frontmatter(skill_dir)
        for markdown in skill_dir.rglob("*.md"):
            validate_links(markdown, root)
    for markdown in (root / "README.md", root / "NOTICE.md"):
        validate_links(markdown, root)
    for markdown in (root / "docs").glob("*.md"):
        validate_links(markdown, root)
    validate_source_records(root)
    validate_mapping(root)
    print("Validation passed for {}.".format(root))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="pack root")
    args = parser.parse_args(argv)
    try:
        validate(Path(args.root).expanduser().resolve())
    except (OSError, RuntimeError, ValidationError) as exc:
        print("Validation failed: {}".format(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
