---
name: google-cpp-style
description: Applies the current Google C++ Style Guide to C++ code generation, review, refactoring, and bug fixes. Use when a C++ task needs Google-style naming, headers, ownership, API design, formatting, comments, or feature guidance; do not apply it to other languages or override explicit project conventions.
license: Mixed licensing; adapted guidance is CC BY 3.0 and code examples are Apache-2.0. See references/source-and-license.md.
metadata:
  source: google/styleguide
  source-revision: c775c0c2f73c110613243520c001577cdbc0034d
  retrieved: "2026-10-24"
---

# Google C++ Style

Use this skill only when the task concerns C++ source, headers, build-facing C++ interfaces, or C++ review. It is an independently maintained adaptation of Google's guide, not a Google product.

## Operating rules

1. Read the repository's `AGENTS.md`, `CLAUDE.md`, contribution guide, build files, language version, formatter/linter configuration, and nearby code before changing anything.
2. Apply instructions in this order: explicit user request; project instructions; established local conventions; then the applicable Google rules. If they conflict, preserve the higher-priority convention and explain the choice.
3. Classify each observation as **required**, **recommended**, **exception/waiver**, or **local preference**. Do not turn a recommendation into a prohibition.
4. Load only the relevant detailed references. Use the section links in each reference to give review findings an upstream heading and official URL.
5. Change only the requested scope. Do not reformat unrelated files or perform architectural cleanup merely because a style rule exists.
6. Distinguish style findings from correctness, security, performance, ABI, and build failures. Escalate those concerns separately when present.
7. Use the repository's formatter, lint, static analysis, build, and tests when available. State exactly which commands ran; never imply a check ran when it did not.
8. Finish with a concise summary of changes, checks, unresolved conflicts, and any rule exceptions.

## Reference map

- [Background, version, and source boundaries](references/background-and-version.md)
- [Headers, includes, and scoping](references/headers-scoping.md)
- [Classes and functions](references/classes-functions.md)
- [C++ features, ownership, and libraries](references/features-and-libraries.md)
- [Naming and comments](references/naming-comments.md)
- [Formatting and exceptions](references/formatting-exceptions.md)
- [Source and license record](references/source-and-license.md)

## Review format

For each meaningful finding, include: file/line, the observed behavior, the Google section heading, whether it is a rule or recommendation, why it matters, and the smallest compatible fix. If local instructions intentionally differ, say so instead of filing a false violation.
