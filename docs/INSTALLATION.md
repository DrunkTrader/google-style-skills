# Installation

This pack uses the open [Agent Skills specification](https://agentskills.io/specification): each skill is a directory containing `SKILL.md` plus optional `references/` files. Installation is explicit; no command in this repository installs an agent, edits shell startup files, executes downloaded code, or silently writes to a home directory.

## Supported paths used by this repository

The paths below are verified from the current Agent Skills compatibility reference and the official product documentation available on October 24, 2026.

| Agent | Project-local skills | User-global skills | Evidence/status |
| --- | --- | --- | --- |
| Claude Code (`claude-code`) | `.claude/skills/` | `~/.claude/skills/` | Verified from [Claude Code skills docs](https://code.claude.com/docs/en/skills); installer-tested in temporary directories. |
| OpenAI Codex (`codex`) | `.agents/skills/` | `~/.agents/skills/` | Verified from [OpenAI Codex skill docs](https://developers.openai.com/codex/skills); installer-tested in temporary directories. |
| OpenCode (`opencode`) | `.agents/skills/` | `~/.config/opencode/skills/` | Path listed by the maintained [skills CLI agent compatibility reference](https://github.com/vercel-labs/skills/blob/main/docs/agents.md); installer-tested as a path mapping, not in a live OpenCode session. |
| Cursor (`cursor`) | `.agents/skills/` | `~/.cursor/skills/` | Path listed by the maintained compatibility reference; installer-tested as a path mapping, not in a live Cursor session. |
| Gemini CLI (`gemini-cli`) | `.agents/skills/` | `~/.gemini/skills/` | Path listed by the maintained compatibility reference; installer-tested as a path mapping, not in a live Gemini session. |

The repository installer supports these five names. Other Agent Skills-compatible agents can use the standard structure through their own documented paths or the standard CLI; use `--destination` when a custom path is known and safe.

## Method A: standard `skills` CLI

The currently maintained ecosystem CLI documents `npx skills add` and supports GitHub shorthands, URLs, local paths, selected skills, selected agents, project/global scope, copies, dry-run-like listing, and all-agent installation. The exact source commands below are tested for syntax against the current CLI documentation, but the `DrunkTrader/google-style-skills` commands are **not executable until this repository is published**.

```bash
# Published repository placeholder: list available skills.
npx skills add DrunkTrader/google-style-skills --list

# One language, global Claude Code installation.
npx skills add DrunkTrader/google-style-skills --skill google-cpp-style --agent claude-code -g -y

# Several languages, project-local Codex installation.
npx skills add DrunkTrader/google-style-skills \
  --skill google-python-style \
  --skill google-typescript-style \
  --agent codex -y

# All four skills to all detected agents.
npx skills add DrunkTrader/google-style-skills --skill '*' --agent '*' -y

# Copy instead of symlink.
npx skills add DrunkTrader/google-style-skills --skill google-rust-style --agent codex --copy -y
```

The CLI's documented default is project scope; `-g/--global` selects user scope. Run `npx skills --help` and consult the CLI's current [command reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) before using a newer option. The standard CLI can discover more agents than this repository's local installer; this pack does not claim live testing for every listed agent.

### Local checkout with the standard CLI

The CLI accepts a local path, so a checkout can be used without publishing:

```bash
npx skills add /absolute/path/to/google_style_skills \
  --skill google-python-style --agent claude-code --copy -y
```

This command is documented by the CLI and is the preferred local integration test when Node.js 22.20+ and `npx` are available. It writes to the selected agent's project/global path, so use a disposable test project or `--list` first.

## Method B: repository-provided installer

The standard-library installer is useful when Node.js is unavailable, when an agent has a custom path, or when an operator wants an explicit plan before writing.

```bash
# Discover skills and supported path mappings.
python3 scripts/install.py list

# Preview a project-local install for one agent.
python3 scripts/install.py install \
  --skill google-python-style \
  --agent codex \
  --scope project \
  --dry-run

# Apply it after inspecting the proposed source/destination.
python3 scripts/install.py install \
  --skill google-python-style \
  --agent codex \
  --scope project

# Install all languages globally for Claude Code.
python3 scripts/install.py install --all --agent claude-code --scope user

# Detect installed agents and preview all four skills.
python3 scripts/install.py install --all --auto-detect --scope user --dry-run
```

### Explicit destination

Use a custom root when the agent's documented path is different or when testing in a temporary directory:

```bash
python3 scripts/install.py install \
  --skill google-rust-style \
  --destination /tmp/codex-skills \
  --dry-run
```

The installer places the skill under `<destination>/google-rust-style`. An explicit destination is a single destination root; combine it with one selected skill set and do not combine it with multiple agent path resolutions. The destination must be provided explicitly when the installer cannot determine a safe path.

### Replacement and conflicts

Existing skill directories are never overwritten by default. Inspect the current directory and use `--replace` only when replacement is intentional:

```bash
python3 scripts/install.py install --skill google-cpp-style --agent claude-code --scope user --replace
```

Each individual copy is staged in a temporary sibling and attempts to restore the previous destination if replacement fails. A multi-skill or multi-agent batch is **per-operation atomic, not batch-transactional**: earlier successful operations remain if a later operation fails. Rerun `python3 scripts/validate.py` against the source pack and inspect only the explicitly reported destination before retrying.

### Uninstall

Uninstall is intentionally bounded to the resolved destination root and only removes directories marked by this installer's provenance marker. It preflights every selected target before deleting any of them:

```bash
python3 scripts/install.py uninstall --skill google-rust-style --agent codex --scope project
python3 scripts/install.py uninstall --skill google-typescript-style --destination /tmp/codex-skills
```

Uninstall refuses a missing, unowned, symlinked, or unsafe destination and cannot traverse outside the configured root. It does not remove an agent, alter configuration, or remove similarly named directories. Skills installed by the standard `npx skills` CLI should be removed with that CLI's `skills remove` command instead.

## Project-local versus user-global

- **Project-local** keeps the skill with a repository and is appropriate for team-shared conventions. Claude Code uses `.claude/skills/`; Codex and the shared standard path use `.agents/skills/`.
- **User-global** makes a skill available across projects for the selected agent. It writes only to the selected agent's documented skills directory.

Do not install both a project-local and global copy with the same name unless you understand precedence. The closer/project copy may shadow the global copy, which can make updates appear ineffective.

## Manual fallback

When an agent is compatible with the standard format but is not in the local installer's verified map, copy one complete skill directory—including `SKILL.md` and `references/`—to the agent's documented skills root:

```bash
cp -R google-python-style /path/documented/by/that-agent/skills/
```

Do not copy only `SKILL.md`; relative reference links depend on the complete directory. Validate the source first and verify the destination using that agent's own skill-list/discovery command. Record the agent and path in project documentation if the install becomes part of team setup.

## What has actually been tested

Automated tests exercise the installer with temporary directories for the documented path mappings, project/user scope resolution, custom destinations, dry runs, conflicts, replacement, uninstall containment, invalid names, duplicate shared project roots, and invalid-parent I/O failures. Permission branches are handled in code but are not forced by routine tests because filesystem permission behavior differs by platform and user privileges. A live Claude Code/Codex session is not started by the test suite, and no real global directory is modified during routine validation. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for discovery verification.
