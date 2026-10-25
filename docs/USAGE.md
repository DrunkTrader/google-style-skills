# Usage

The skills are instruction packs, not language compilers or linters. An agent should load one when the task is about the matching language and then inspect project-local instructions and tooling before applying a rule.

## General request pattern

Good prompts state the language, task, scope, and verification expectation:

```text
Use google-python-style. Review src/parser.py for Google Python style issues only.
Respect CONTRIBUTING.md and the project's pyproject.toml. Separate style findings
from correctness/security issues, cite the upstream section for each finding, and
run only the configured checks that are available.
```

The skill will not use a Google rule to override an explicit user instruction or a project convention. If the project intentionally differs, ask the agent to explain the conflict and preserve the local rule unless the requested change is a migration.

## C++ examples

### Generate

```text
Use google-cpp-style to add a small C++20 value type. Inspect the existing
namespace, header guard, include order, copy/move policy, and clang-format setup.
Implement only the requested files and run the narrowest configured build/test.
```

### Review

```text
Use google-cpp-style to review this PR. Check self-contained headers, direct
includes, ownership transfer, implicit conversions, static initialization,
names, comments, and formatting. Cite the official heading and classify each
finding as required, recommended, exception, or non-style.
```

### Refactor or bug fix

```text
Use google-cpp-style while fixing the lifetime bug in foo.cc. Preserve the
public API and local conventions. Do not reformat unrelated code. Explain any
ownership or noexcept changes separately from style changes and report the
commands that actually ran.
```

## Rust examples

### Generate

```text
Use google-rust-style to add a public library API. First determine whether this
is library or application code, inspect Cargo/rustfmt/Clippy settings, then apply
the guidance on flexible references, error types, traits, docs, and naming.
```

### Review

```text
Use google-rust-style to review the changed crate. Check module structure,
glob imports, borrowing versus clone, bool parameters, Result/Option/panic,
trait choices, unsafe blocks, and future-proof public APIs. Do not apply Chrome
or Fuchsia-only rules unless this repository uses that codebase.
```

### Refactor or bug fix

```text
Use google-rust-style while replacing this check-then-unwrap bug. Preserve the
crate's test framework and toolchain. Distinguish the correctness fix from any
style cleanup and run the configured formatter, Clippy, build, and focused tests
when available.
```

## Python examples

### Generate

```text
Use google-python-style to add a typed module. Respect the supported Python
version and existing formatter/type-checker configuration. Use full imports,
safe defaults, focused exceptions, 4-space indentation, docstrings, and a
main guard only if this is an executable module.
```

### Review

```text
Use google-python-style to review this module. Check imports, mutable defaults,
assertions, broad exceptions, truthiness/None checks, comprehensions, resource
cleanup, naming, docstrings, and type annotations. Cite the section and do not
call an allowed feature a violation.
```

### Refactor or bug fix

```text
Use google-python-style to fix the shared-default bug in this function. Keep the
change focused, preserve the project's Python version, run the configured tests
and type/lint checks if available, and say which commands were not run.
```

## TypeScript examples

### Generate

```text
Use google-typescript-style to add a module with named exports. Inspect tsconfig,
ESLint/formatter rules, generated-code boundaries, and the supported target.
Apply the guide's import/export, const/let, type-only import, visibility, and
error-handling rules without changing unrelated files.
```

### Review

```text
Use google-typescript-style to review this change. Check default exports,
mutable exports, var, unsafe coercion/parseInt, enum truthiness, #private
fields, prototype manipulation, callback signatures, any, JSDoc placement,
and generated-code exceptions. Cite the upstream heading for each finding.
```

### Refactor or bug fix

```text
Use google-typescript-style to fix this event-handler leak. Preserve the public
API and framework lifecycle, use a stable handler reference where removal is
required, run the configured typecheck/lint/tests, and separate the runtime bug
from style observations.
```

## Explicit invocation names

Hosts vary in syntax. Common forms are:

- Claude Code: `/google-python-style` or a prompt that matches the description.
- Codex: `$google-python-style` or select the skill from `/skills`.
- Other compatible hosts: use their skill selector or mention the exact skill name.

If the host displays only a short description, open the installed `SKILL.md` and use the relative references directory when a rule depends on an exception or specific section.
