# TypeScript toolchain requirements

Official section: [Toolchain requirements](https://google.github.io/styleguide/tsguide.html#toolchain-requirements).

## TypeScript compiler

Use the TypeScript compiler and compiler options selected by the repository. Do not change `target`, module resolution, strictness, or emit settings solely to silence a style finding. Check `tsconfig.json`, package scripts, lockfiles, and CI before choosing a command.

### `@ts-ignore`

Avoid `@ts-ignore`. Prefer fixing the type or using a narrower, justified suppression such as `@ts-expect-error` when the repository allows it and the error is intentionally tested. A suppression should explain the boundary or issue and should not hide an unrelated error. Never claim type correctness when broad suppressions remain unexplained.

## Conformance

The upstream guide refers to Google's internal conformance tooling. External repositories may use ESLint, TypeScript ESLint, a compiler plugin, or no equivalent. Treat conformance as a project-specific check:

1. Find the configured lint/conformance command.
2. Run it on the changed scope.
3. If unavailable, perform a focused review against the relevant reference and say that automated conformance was not run.

Do not invent a tool, download a Google-internal checker, or present this skill as a replacement for type checking/build/test validation.

## Toolchain review checklist

- What TypeScript version and runtime target are supported?
- Are files generated, framework-managed, or hand-authored?
- Which formatter/linter controls whitespace and prohibited features?
- Does the build use file-by-file transpilation (`isolatedModules`) or type-only import/export checks?
- Which command actually runs compiler and conformance checks in CI?
