---
name: google-rust-style
description: Applies the current Google Rust Style Guide to Rust code generation, review, refactoring, and bug fixes. Use for any Rust task, and especially when choosing between `&[T]` and `&Vec<T>`, unique ownership and `Rc`/`Arc`, a newtype and a type alias, a trait and an inherent impl, an enum and a `bool` parameter, `Option`/`Result`/`panic!`, or `unwrap` and `expect`; when naming a constructor, getter, or extension trait; when deciding on `#[non_exhaustive]`, `#[must_use]`, module and import layout, or doc comments; or when justifying `unsafe`. Also use when asked to follow Google style and when reviewing a Rust PR. Do not apply it to other languages or override explicit project conventions.
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

## Quick reference

Decide the common cases from this table without opening a reference file. Open the mapped reference when you need the rationale, the exceptions, or the codebase marker — every row below is the default, not the whole rule.

| Decision | Default |
| --- | --- |
| Parameter borrowing immutable data | `&[T]`, `&str`, `&T`, `Option<&T>` — not `&Vec<T>`, `&String`, `&Box<T>`, `&Option<T>` |
| Shared ownership | Unique ownership; `Rc`/`Arc` only when the alternative is unreasonably complex |
| `.clone()` to settle a borrow error | Borrow instead; clone only when a real independent value is needed |
| `bool` parameter | A named enum, unless the meaning is obvious at the call site |
| Reporting failure | `Option` simple absence · `Result` caller must distinguish causes · `panic!` bug or violated invariant |
| A panic is genuinely correct | `expect` with a message saying why, not `unwrap` |
| `is_some()` then `unwrap()` | Pattern match: `if let Some(v) = ...` |
| Same primitive, different meaning | Newtype, not a type alias |
| Tuple vs. named fields | Named fields, except a single-field newtype or a very local context |
| Trait with one implementor | An inherent `impl` |
| Extension trait | `Ext` suffix, owned by the team that owns the extended type |
| Constructor | `new()`, `new_with_foo()` when several, `try_new()` when fallible |
| Value conversion | `from_foo()` plus the matching `From` impl |
| Accessors | `foo()`, `foo_mut()`, `set_foo()`, `replace_foo()`, `take_foo()`, `with_foo(\|f\| ...)` |
| You wrote `len()` | Also write `is_empty()` |
| Public enum or public-field struct other teams use | `#[non_exhaustive]` |
| Ignoring the return value is a bug | `#[must_use]` on the function, or on the returned type |
| Reaching for `unsafe` | Last resort, wrapped in a safe abstraction, with a `SAFETY:` comment giving the argument |
| Concatenating more than two strings | `format!` / `write!` |
| Needing code generation | Function or type → `macro_rules!` → other codegen → `proc_macro` |
| Naming | No abbreviations outsiders would not know; descriptive lifetimes; short, bound-derived generic parameters |
| Imports | One module per `use`, no globs, traits imported locally, `module::function()`, type names unqualified |
| Public item | `///` on the item, `//!` at the top of the file for the module or crate; document panics and `unsafe` invariants |

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
