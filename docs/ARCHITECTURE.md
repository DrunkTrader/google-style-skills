# Architecture

## Design goals

The pack has four independent language skills, progressive disclosure, and a conservative installation surface. A user can install `google-python-style` without copying or loading the other three skills. The skills contain no runtime code and no network-dependent behavior.

## Repository layers

```text
google-*-style/SKILL.md       activation, precedence, workflow, reference map
google-*/references/*.md      detailed paraphrased rules and source records
docs/                         installation, usage, maintenance, coverage
scripts/install.py             explicit copy/uninstall plan and execution
scripts/validate.py            deterministic repository checks
tests/                         installer/structure tests and scenario fixtures
```

## Progressive disclosure

Hosts load frontmatter descriptions first, then the short `SKILL.md`, then references only when an agent needs a particular topic. `SKILL.md` files intentionally avoid reproducing the complete official guides. Reference files are organized by actual guide sections rather than forcing identical topics across languages.

## Precedence model

The skills explicitly tell agents to use this order:

1. User instructions.
2. Project-specific instructions/contribution guidelines.
3. Established local conventions and supported toolchain.
4. Compatible Google guidance.

This prevents a style skill from becoming an excuse for broad reformatting or an architecture rewrite.

## Installer model

`install.py` resolves one of three destination modes:

- An explicit `--destination` root.
- A documented agent path for `--scope project` or `--scope user`.
- A detected agent list when `--auto-detect` is requested.

It plans all source/destination pairs before modifying files, prints them, stages each copy in a temporary sibling, refuses conflicts by default, writes a provenance marker for safe local uninstall, rejects overlap with packaged source directories, and bounds uninstall to the configured root. Each individual operation is atomic-ish with rollback on replacement failure; a batch is not transactional. It uses only Python's standard library.

## Validation model

`validate.py` performs structural and link checks without requiring a YAML package or live agent. `tests/test_installer.py` uses isolated temporary directories and subprocesses. The fixture scenarios document representative language-model evaluations; deterministic tests do not prove that every LLM will follow every rule.

## Compatibility boundary

The standard Agent Skills structure is portable, but discovery paths and optional metadata differ. This repository supports and documents a verified path subset for Claude Code, Codex, OpenCode, Cursor, and Gemini CLI. Other agents can use the same skill directories through their own documented install path or an explicit custom destination.
