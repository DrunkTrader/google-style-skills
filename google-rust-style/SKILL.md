---
name: google-rust-style
description: Applies the current Google Rust Style Guide to Rust code generation, review, refactoring, and bug fixes. Use when a Rust task needs Google guidance on modules, imports, ownership, APIs, traits, concurrency, naming, documentation, or implementation choices; do not apply it to other languages or override explicit project conventions.
license: Mixed licensing; adapted guidance is CC BY 3.0 and code examples are Apache-2.0. See references/source-and-license.md.
metadata:
  source: google/styleguide
  source-revision: c775c0c2f73c110613243520c001577cdbc0034d
  retrieved: "2026-10-24"
---

# Google Rust Style

Use this skill only for Rust code and Rust-facing APIs. The upstream guide includes codebase-scoped rules marked for Chromium or Fuchsia; never apply those markers to an unrelated repository without confirming that the project uses the same environment.

## Operating rules

1. Inspect `AGENTS.md`, `CLAUDE.md`, Cargo manifests, toolchain files, `rustfmt`/Clippy configuration, build scripts, and nearby code first.
2. Apply instructions in this order: explicit user request; project instructions; established local conventions; then the applicable Google rules. Explain material conflicts.
3. Determine whether the code is library or application code. Google API-design guidance is binding for library code and a strong recommendation for application code.
4. Load the relevant reference file for the decision. Preserve the upstream distinction between rules, rationale, exceptions, and codebase-specific markers.
5. Make focused changes. Do not mechanically reformat unrelated code or introduce abstractions solely to satisfy a style preference.
6. Separate style findings from ownership/correctness, unsafe-code, concurrency, security, and performance findings.
7. Run the repository's configured formatter, Clippy/static analysis, build, and tests when available. Report commands and outcomes exactly; do not claim unrun checks.
8. Summarize changed files, applicable sections, checks, exceptions, and unresolved issues.

## Reference map

- [Scope, goals, and external Rust rules](references/background-and-scope.md)
- [Organization and imports](references/organization-and-imports.md)
- [Formatting, ownership, and function APIs](references/formatting-ownership-apis.md)
- [Types, traits, concurrency, and macros](references/types-traits-concurrency.md)
- [Naming and documentation](references/naming-documentation.md)
- [Other features and implementation concerns](references/other-features.md)
- [Testing, source, and license record](references/testing-source-and-license.md)

## Review format

For each finding, identify the file/line, the upstream section heading and link, the rule strength and scope marker, the concrete impact, and the smallest compatible fix. Treat `chrome` and `Fuchsia` guidance as conditional, not universal.
