# Python type annotations

Official section: [3.19 Type Annotations](https://google.github.io/styleguide/pyguide.html#3.19_Type_Annotations), with the language-rule context in [2.21 Type Annotated Code](https://google.github.io/styleguide/pyguide.html#2.21_Type_Annotated_Code).

## General rules

Annotate public functions/methods and new or modified APIs when feasible. Use annotations for parameters, returns, and variables where they improve readability or allow the configured checker to catch errors. Keep annotations accurate; stale types are worse than a focused omission with a tracked issue.

## Line breaking

Break long annotations with implicit continuation and a layout that keeps parameter/return relationships clear. Follow the repository formatter and the Python 80-column rule where practical.

## Forward declarations

Use quoted annotations or `from __future__ import annotations` only when required by the supported Python versions and import graph. Do not use forward references to hide a circular dependency that should be redesigned; see the circular-dependency section below.

## Default values

Keep a default's type compatible with the annotation and avoid mutable defaults. When `None` means “not supplied,” annotate an optional value and initialize the mutable object inside the function. With annotated defaults, follow the guide's whitespace rule around `=`.

## NoneType

Use `None` explicitly for optional values and test with `is None`/`is not None`. Do not rely on truthiness to distinguish `None` from an empty/false value. The checker should see the narrowing path clearly.

## Type aliases

Use a type alias when it gives a meaningful, stable concept or improves a complex annotation. Do not expose a public alias merely for convenience if it obscures the actual API or creates an unnecessary compatibility surface. A local alias may be acceptable for readability when it is not part of a public signature.

## Ignoring types

Use the narrowest checker suppression at the line or expression that requires it, with the project's syntax (for example a pytype directive). Explain why the checker is wrong or why the boundary is unavoidable. Do not disable an entire file/module to silence a small issue.

## Typing variables

Annotate variables when the inferred type is unclear, the variable is part of an important boundary, or a checker needs help. Avoid redundant annotations that merely repeat an obvious constructor, unless they communicate an intended interface type rather than the concrete implementation.

## Tuples vs Lists

Use tuples for fixed-size heterogeneous records and lists/sequences for homogeneous mutable collections. Annotate the shape when it matters. Do not use a tuple simply because it is shorter if callers need named fields; a small dataclass/class may be clearer.

## Type variables

Use a `TypeVar`/type parameter when a relationship between inputs and outputs matters. Constrain/bound it only as needed, choose a descriptive name, and avoid generic abstractions that provide no reusable type information.

## String types

Use `str` for text, `bytes` for binary data, and explicit protocol/library types for path-like or formatted data. Do not silently mix text and bytes; make encoding boundaries visible.

## Imports for typing

Follow the language-rule import exemptions for `typing`, `collections.abc`, and `typing_extensions`. Keep type-only imports organized and use future annotations or `TYPE_CHECKING` only when they fit the supported versions and avoid a real runtime cycle.

## Conditional imports

Use conditional imports for optional/platform dependencies only when the runtime boundary is real and documented. Keep the type-checking branch narrow, and ensure runtime code has a clear failure or fallback when the dependency is absent.

## Circular dependencies

Do not use type-only imports to conceal a design-level cycle indefinitely. First consider moving a shared type, inverting a dependency, or reducing module coupling. If a cycle is intentional, document the boundary and keep the conditional import/type reference explicit.

## Generics

Use generic types to preserve useful relationships and prevent `Any` leakage. Prefer the modern syntax supported by the project's Python version, but do not modernize annotations beyond the configured runtime. Avoid `Any` unless it is a deliberate boundary; use a more specific type or `object`/`unknown`-like narrowing strategy when possible.

## Type-checking workflow

The upstream guide points to `pytype`. Use the tool actually selected by the repository (pytype, mypy, pyright, or another configured checker), and run it on the relevant target. Report type-checker results separately from formatting and runtime tests.
