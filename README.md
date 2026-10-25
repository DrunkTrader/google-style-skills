# Google Style Guides as Portable Agent Skills

Four independently installable [Agent Skills](https://agentskills.io/specification) that help coding agents apply Google's current C++, Rust, Python, and TypeScript style guidance without forcing it over project-specific conventions.

## Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Source coverage matrix](docs/SOURCE_MAPPING.md)
- [Maintaining the skills](docs/MAINTAINING_SKILLS.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Agent-driven installation prompt](docs/AGENT_INSTALLATION_PROMPT.md)

## Skills

| Skill | Language | Official source |
| --- | --- | --- |
| `google-cpp-style` | C++ | [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) |
| `google-rust-style` | Rust | [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html) |
| `google-python-style` | Python | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) |
| `google-typescript-style` | TypeScript | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) |

Each skill contains a concise `SKILL.md` plus locally available references. Install one language without installing the others.

## Quick installation

The standard ecosystem CLI is the first choice when this repository is published. Replace `DrunkTrader/google-style-skills` with the future repository coordinates; this project intentionally does not invent a public URL.

```bash
# List skills from a published repository
npx skills add DrunkTrader/google-style-skills --list

# Install one skill for Claude Code
npx skills add DrunkTrader/google-style-skills --skill google-python-style --agent claude-code -g -y

# Install all four skills for Codex
npx skills add DrunkTrader/google-style-skills --skill '*' --agent codex -g -y
```

For a local checkout, use the repository-provided installer:

```bash
python3 scripts/install.py list
python3 scripts/install.py install --skill google-rust-style --agent codex --scope project --dry-run
python3 scripts/install.py install --skill google-rust-style --agent codex --scope project
python3 scripts/install.py install --all --agent claude-code --scope user
```

The local installer never overwrites an existing skill unless `--replace` is explicit. See [docs/INSTALLATION.md](docs/INSTALLATION.md) for Windows, custom destinations, uninstall, detection, and tested versus untested integrations.

## Usage

After installation, invoke the skill explicitly or describe a matching task:

```text
$google-cpp-style Review this header for ownership, include-order, and API issues.
$google-python-style Refactor this function while preserving the project's Python version and local conventions.
$google-rust-style Review this public library API and cite the applicable Google section for every finding.
$google-typescript-style Add this module without changing generated files or unrelated formatting.
```

The skills inspect repository instructions first, distinguish rules from recommendations and exceptions, consult detailed references on demand, and report exactly which checks ran. They do not replace the project's formatter, linter, compiler, type checker, security review, or tests.

## Attribution and Licensing

This project, **Google Style Guides as Portable Agent Skills**, is an independently maintained project by Neeraj Kumar (DrunkTrader). It adapts Google's C++, Rust, Python, and TypeScript style guides into reusable skills for AI coding agents.

This project is not affiliated with, endorsed by, or maintained by Google.

### License Scope

This repository uses a mixed-license model:

- **MIT License:** Applies to original project code and independently authored material created for this repository, to the extent that such material is owned by the applicable copyright holder.
- **Creative Commons Attribution 3.0 (CC BY 3.0):** Google's style guide documentation is identified by Google as licensed under this license. Adapted material remains subject to applicable attribution and licensing requirements.
- **Apache License 2.0:** Google's code samples are identified by Google as licensed under Apache 2.0. Applicable license terms and notices must be preserved when redistributing those samples or derivative material.

The root `LICENSE` file does not replace or override the licensing terms applicable to Google's material or other third-party content. See [`NOTICE.md`](NOTICE.md) and the source and licensing references bundled with each skill for further details.

### Official Google Sources

- [Google Style Guides Index](https://google.github.io/styleguide/)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [Google Style Guides Repository and Licensing](https://github.com/google/styleguide#licensing)

### Attribution and Independence

The skills reorganize and summarize guidance from the official sources into instructions and locally available reference documents for coding agents. They are intended to make the guidance easier to apply during code generation, code review, and refactoring. The official Google documentation remains the authoritative source for the original guidelines.

Google and its associated names and marks belong to their respective owners. References to Google identify the source of the guidelines and do not imply endorsement or affiliation.

### Copyright

Copyright for original project contributions belongs to their respective authors. The root MIT license identifies Neeraj Kumar (aka DrunkTrader) as the copyright holder for the original material covered by that license. This claim does not extend to Google's original material or third-party contributions owned by others.

For the applicable license terms, attribution requirements, source snapshot, and maintenance information, consult [`NOTICE.md`](NOTICE.md) and [`docs/MAINTAINING_SKILLS.md`](docs/MAINTAINING_SKILLS.md).

