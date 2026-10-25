# Naming and comments

Official sections: [Naming](https://google.github.io/styleguide/cppguide.html#Naming) and [Comments](https://google.github.io/styleguide/cppguide.html#Comments).

## Inclusive Language

Choose clear, respectful terminology in identifiers, comments, diagnostics, and documentation. Prefer neutral terms such as `primary/replica`, `allowlist/denylist`, and `leader/follower` when they accurately describe the concept. Do not rename an established public API casually; use a compatibility plan when changing a public name.

## Naming

### Choosing Names

Names should be descriptive, unambiguous, and appropriate to scope. A short local name can be fine when the scope and type make it obvious; public APIs and long-lived state need more context. Avoid clever abbreviations and names that encode stale implementation details. Use the established project prefix for globally visible identifiers.

### File Names

Use lowercase filenames with underscores where that is the repository convention. Match related `.h`, `.cc`, test, and generated files. Header guards derive from the full path; do not treat a filename rename as style-only when it affects include paths, build rules, or public users.

### Type Names

Use `PascalCase` for classes, structs, type aliases, enums, and concepts. A type name should read as a noun and avoid unnecessary suffixes such as `Object` or `Manager` unless they convey a real role.

### Concept Names

Use a descriptive `PascalCase` name for a concept. Name it for the semantic requirement, not for the implementation trick used to check it.

### Variable Names

Use `snake_case` for variables, parameters, and data members. Avoid one-letter names except for conventional short-lived loop/index variables or mathematical notation with an immediately clear scope.

#### Common Variable Names

Use names such as `i`, `j`, `k` only for simple local iteration; use a domain name for nested loops or nontrivial lifetimes. Boolean names should read as a predicate (`is_ready`, `has_value`, `can_retry`).

#### Class Data Members

Use the project's member suffix/prefix convention consistently. The current Google guide uses a trailing underscore for private data members in ordinary examples (`value_`); verify nearby code before changing an existing convention.

#### Struct Data Members

Use plain descriptive names without a private-member marker for public struct fields. A struct's fields should be simple enough that direct access is part of its intended contract.

### Constant Names

Use `kPascalCase` for named constants, including `constexpr` values, when that is the project convention. Do not call a mutable variable a constant. A constant's name should describe the domain meaning rather than its current literal representation.

### Function Names

Use `PascalCase` for functions and methods in the Google C++ convention. Name accessors consistently with the surrounding API and make mutating or ownership-changing behavior visible.

### Namespace Names

Use lowercase names with underscores as needed, based on the project and component path. Keep namespace names stable and unique. Avoid names that collide with standard or third-party namespaces.

### Enumerator Names

Use the same convention as constants (`kPascalCase`) for unscoped/scoped enum values where the codebase follows the guide. Prefer scoped enums when they improve collision resistance and type safety.

### Template Parameter Names

Use a short but meaningful name. `T` is acceptable for a generic type when the role is obvious; use a descriptive name for a constrained or multi-parameter template.

### Macro Names

Macros should be uppercase with underscores and a project-specific prefix. Avoid macros whenever a language construct works. Macro names must not collide with common platform or library names.

### Aliases

Use a readable alias name that follows the kind of thing it names. A type alias should not look like a concrete class if it is merely a substitution; use the local convention for aliases and keep public aliases stable.

### Exceptions to Naming Rules

Generated code, protocol/compiler-required names, external APIs, platform/OS names, and established compatibility symbols can require exceptions. Keep the exception narrow and document it where a reviewer might otherwise “fix” it. Do not use an exception to justify inconsistent new names.

## Comments

Comments should explain intent, invariants, constraints, ownership, or non-obvious consequences. They should not restate syntax or compensate for an unclear name when a small code improvement would be better.

### Comment Style

Use complete sentences where practical. Keep comments near the code they explain and update them when behavior changes. Use `//` for ordinary comments and the project's established documentation format for API comments.

### File Comments

Put a concise file-level description where the repository expects one. Include a legal notice and author line only when required by the project's licensing policy; do not invent personal author boilerplate.

### Struct and Class Comments

Document the purpose, invariants, ownership, thread-safety, lifecycle, and important usage constraints of public types. A class comment should help a caller decide whether to use the type, not merely repeat its name.

### Function Comments

#### Function Declarations

Document public declarations with preconditions, postconditions, ownership/lifetime, thread-safety, error behavior, and meaningful parameter/return semantics. The declaration comment is the contract visible to callers.

#### Function Definitions

Use a definition comment for implementation details that are not part of the public contract. Do not copy a declaration comment into the definition without adding value.

### Variable Comments

#### Class Data Members

Document non-obvious member state, ownership, units, synchronization, and invariants. A comment is not a substitute for a clear member name.

#### Global Variables

Explain why global/static state exists, its initialization/lifetime, and how it is synchronized or intentionally immutable. Prefer eliminating the global where that produces a clearer API.

### Implementation Comments

#### Explanatory Comments

Explain the “why,” especially for workarounds, performance choices, ordering constraints, and code that looks wrong but is intentional. Link to a bug/design document when the external reason matters.

#### Function Argument Comments

Use argument comments sparingly to clarify an otherwise ambiguous literal, unit, or ownership transfer. Prefer a named local or a stronger type when the meaning is important.

#### Don'ts

Do not write comments that contradict the code, narrate every line, leave stale TODOs without an owner, or use comments to justify undefined behavior without a real safety argument.

### Punctuation, Spelling, and Grammar

Use clear spelling, punctuation, and grammar in comments and diagnostics. Preserve technical names and code identifiers exactly. Review comments as user-facing text when they appear in public documentation or error messages.

### TODO Comments

Use the repository's TODO format, preferably including an issue/owner when one exists. State the action, not merely that the code is “bad.” Do not add a TODO as a substitute for fixing a small, known defect or for documenting an unresolved safety issue.
