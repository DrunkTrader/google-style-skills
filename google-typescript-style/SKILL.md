---
name: google-typescript-style
description: Applies the current Google TypeScript Style Guide to TypeScript code generation, review, refactoring, and bug fixes. Use when a TypeScript task needs guidance on modules, exports, language features, classes, functions, naming, types, toolchain, comments, or policy; do not apply it to other languages or override explicit project conventions.
license: Mixed licensing; adapted guidance is CC BY 3.0 and code examples are Apache-2.0. See references/source-and-license.md.
metadata:
  source: google/styleguide
  source-revision: c775c0c2f73c110613243520c001577cdbc0034d
  retrieved: "2026-10-24"
---

# Google TypeScript Style

Use this skill only for TypeScript or TypeScript-facing JavaScript modules. The upstream guide uses RFC 2119 terminology: `must` and `must not` are prescriptive, while `should`, `prefer`, `avoid`, and `may` carry different strengths.

## Operating rules

1. Inspect `AGENTS.md`, `CLAUDE.md`, package/build configuration, TypeScript version, compiler options, formatter/linter rules, generated-code boundaries, and nearby code first.
2. Apply instructions in this order: explicit user request; project instructions; established local conventions; then the applicable Google rules. Explain material conflicts.
3. Load the relevant reference file for the specific decision. Treat examples as illustrative, not as extra normative rules.
4. Preserve the guide's distinctions between must/should/may, disallowed features, exceptions, and policy guidance.
5. Make focused changes. Do not reformat unrelated files or change module/export architecture solely for style.
6. Separate style findings from type-system correctness, runtime behavior, security, performance, browser compatibility, and generated-code concerns.
7. Run the repository's formatter, ESLint/other lint, `tsc` or build, and tests when available. State exactly what ran; never imply checks ran when they did not.
8. Summarize changes, applicable upstream headings, checks, project overrides, and unresolved issues.

## Reference map

- [Source files, imports, exports, and modules](references/source-files.md)
- [Language features, classes, functions, and control flow](references/language-features.md)
- [Naming and type system](references/naming-and-types.md)
- [Toolchain requirements](references/toolchain.md)
- [Comments, documentation, and policies](references/documentation-and-policies.md)
- [Source and license record](references/source-and-license.md)

## Review format

For each meaningful finding, include file/line, the upstream heading and official link, normative strength, concrete behavior or maintenance impact, and the smallest compatible fix. Do not report a subjective formatting choice as a violation when the guide leaves it optional.
