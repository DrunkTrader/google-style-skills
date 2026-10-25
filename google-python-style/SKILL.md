---
name: google-python-style
description: Applies the current Google Python Style Guide to Python code generation, review, refactoring, and bug fixes. Use when a Python task needs guidance on imports, exceptions, mutability, typing, naming, formatting, documentation, linting, or language features; do not apply it to other languages or override explicit project conventions.
license: Mixed licensing; adapted guidance is CC BY 3.0 and code examples are Apache-2.0. See references/source-and-license.md.
metadata:
  source: google/styleguide
  source-revision: c775c0c2f73c110613243520c001577cdbc0034d
  retrieved: "2026-10-24"
---

# Google Python Style

Use this skill only for Python source, Python packaging, or Python review. The guide is prescriptive in many places but contains deliberate “okay”, “avoid”, and exception language; preserve that nuance.

## Operating rules

1. Read `AGENTS.md`, `CLAUDE.md`, packaging/build files, supported Python versions, formatter/linter/type-checker configuration, and nearby code.
2. Apply instructions in this order: explicit user request; project instructions; established local conventions; then the applicable Google rules. Explain conflicts rather than silently rewriting the project.
3. Identify the relevant language-rule and style-rule sections. Use the detailed references instead of relying on a generic PEP 8 summary.
4. Distinguish required rules, strong encouragement, “okay” features with caveats, exceptions, and local preferences.
5. Change only the requested scope. Do not reformat the repository or add type annotations, lint configuration, or dependencies unless the task calls for it.
6. Separate style issues from runtime correctness, security, resource lifetime, concurrency, and performance issues.
7. Run configured formatters, Pylint, type checking, tests, and other checks when available. Report the exact commands and outcomes; never claim a check was run if it was not.
8. Summarize the change, rule sections applied, checks, exceptions, and unresolved questions.

## Reference map

- [Language rules: lint, imports, exceptions, state, and features](references/language-rules.md)
- [Formatting, resources, strings, and comments](references/style-rules.md)
- [Naming, program entry points, and function size](references/naming-and-structure.md)
- [Type annotations and static analysis](references/type-annotations.md)
- [Source and license record](references/source-and-license.md)

## Review format

For every meaningful finding, include file/line, the exact Google section (for example, “2.4 Exceptions” or “3.19.5 NoneType”), rule strength, why the code is affected, and a minimal compatible fix. A formatter preference alone is not a correctness bug.
