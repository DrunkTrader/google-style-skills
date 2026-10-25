# Troubleshooting

## The skill does not appear

1. Confirm the complete skill directory exists, not only `SKILL.md`.
2. Run `python3 scripts/validate.py` from the repository root.
3. Check the host's documented path and scope. Claude Code project skills are under `.claude/skills/`; Codex repository/user skills are under `.agents/skills/`.
4. Restart or reload skills if the host requires it. Codex detects changes automatically in current documentation but may need a restart; Claude Code supports `/reload-skills` for some newly created roots.
5. Look for a same-named project/global skill shadowing this one.

## Invalid metadata or name

`SKILL.md` frontmatter must start on the first line and contain lowercase hyphenated `name` matching the parent directory. The Agent Skills spec limits names to 1–64 characters, forbids leading/trailing/consecutive hyphens, and requires a non-empty description of at most 1024 characters. Run:

```bash
python3 scripts/validate.py
```

Do not add Claude-only fields such as invocation controls unless the host-specific extension is genuinely needed; the four skills intentionally use the open required fields plus portable metadata.

## Incorrect installation path

Run the installer in dry-run mode to print the resolved destination:

```bash
python3 scripts/install.py install --skill google-cpp-style --agent codex --scope project --dry-run
python3 scripts/install.py install --skill google-cpp-style --destination /tmp/skills-check --dry-run
```

If the path is not one of the verified mappings, use `--destination` with the agent's documented skills root. Do not guess a path from a similarly named product.

## Existing destination or conflict

The installer refuses to overwrite an existing skill. Inspect it first, then either:

- choose a different scope/destination;
- remove the old copy using the agent's documented mechanism; or
- pass `--replace` only after confirming that replacement is intended.

An existing same-named skill may shadow the new copy even when installation succeeds. Use the host's skill-list command and inspect both paths.

## Permission errors

Use a project-local or temporary destination, or choose the correct user account. Do not run the installer with broad privileges just to bypass a path mistake. The installer reports the source/destination pair and returns a non-zero status; it does not alter shell configuration.

## Partial install or interrupted replacement

The installer stages copies in a temporary sibling. If a replacement fails, it attempts to restore the prior directory. Inspect the printed destination and any temporary sibling before retrying. Run the validator against the complete source pack; it is not an installed-destination validator, so a destination containing one selected skill will fail the source-pack checks. Use the installer's printed paths plus the agent's own discovery command to verify an installed copy.

## Uninstall safety error

Uninstall accepts only a resolved agent root or explicit destination and one of the four exact skill names. It refuses paths that would escape the configured destination. Re-run with the same `--agent`, `--scope`, or `--destination` used for installation; do not pass the skill subdirectory itself as the destination.

## Standard CLI versus local installer

The `npx skills` CLI can discover more agents and may use symlinks, while this repository installer uses conservative copies and a verified five-agent map. Do not mix a CLI symlink installation with a local replacement without checking where the canonical source lives. For a published repository, use the standard CLI's `--list` and `--skill` options; for a local checkout, use a local path or `scripts/install.py`.

## The agent cites a rule incorrectly

Ask it to open the relevant `references/*.md` file and the official URL, then classify the statement as required, recommended, exception, or preference. Check the project language/version and any `[chrome]`/`[Fuchsia]`/generated-code boundary. A style skill cannot prove a compiler, formatter, linter, security scan, or test was run.
