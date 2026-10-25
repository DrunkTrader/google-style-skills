# Formatting, ownership, and function APIs

Official sections: [Code formatting and aesthetics](https://google.github.io/styleguide/rustguide.html#Code_formatting_and_aesthetics), [Ownership and borrowing](https://google.github.io/styleguide/rustguide.html#Ownership_and_borrowing), and [Function inputs and outputs](https://google.github.io/styleguide/rustguide.html#Function_inputs_and_outputs).

## Code formatting and aesthetics

### Use the appropriate formatting tool

Use the formatter selected by the codebase, such as `rustfmt` or a Chromium command such as `git cl format`. Check `rust-toolchain.toml`, `rustfmt.toml`, CI scripts, and build docs. The upstream guide calls out a 100-column `max_width`, lowercase hex literals, macro matcher formatting, and invisible-character escaping as options that a codebase may omit when its stable toolchain cannot support them. Do not claim formatter compliance without running the configured formatter.

### Opting out of automatic formatting

`#[rustfmt::skip]` is for situation-specific manual alignment or generated code. It is not for personal formatting preference. Prefer a generation rule or formatter configuration at the correct boundary for generated files.

## Ownership and borrowing

### Avoid `Rc` and `Arc`

Prefer unique ownership and borrowing rather than reference-counted ownership. `Rc`/`Arc` are acceptable when the alternative ownership design would be unreasonably complex to write, read, or maintain. Explain the exception, because shared ownership adds runtime cost and often hides a design that could use ordinary Rust ownership.

### Prefer borrows over deep copies

Do not call `.clone()` merely to escape the borrow checker. Design APIs and lifetimes so borrowing is natural, while considering readability and performance. A clone is appropriate when a real independent value is needed or when borrow relationships are excessively complex. Cloning an `Rc`/`Arc` pointer is not a deep copy and is treated differently.

## Function inputs and outputs

### Accept flexible references for immutable data

Use the most general borrowed type that satisfies the operation:

| Prefer | Over | Reason |
| --- | --- | --- |
| `&T` | `&Box<T>` | Borrow the value inside the box |
| `&[T]` | `&Vec<T>` | Accept any slice |
| `&str` | `&String` | Accept string slices |
| `Option<&T>` | `&Option<T>` | Borrow the optional value |

The guide notes non-linear character data such as Rope/Cord as an exception. Use a specific wrapper when its semantics are part of the API rather than accepting it accidentally.

### Iterators vs. owned collections in return types

Library code should prefer an iterator or `impl Iterator` over `Vec<T>` when callers may consume the result in different ways and allocation can be avoided. Returning a `Vec<T>` is fine when most callers need ownership, random access, a naturally materialized vector, or a simpler application API. Do not force an iterator abstraction when it only hides a straightforward owned result.

### Iterators vs. slices in function parameters

Highly reusable library functions should accept an iterator/`impl IntoIterator` when they only need to traverse the input. Application code may use `&[T]` when callers are predictable and the simpler signature is better. Consider flexibility, allocation, composability, and readability together.

### Accepting `Into`

Use `impl Into<T>` for library APIs when call-site ergonomics are paramount and several compatible input types are expected. Do not proliferate `Into` in application code or ignore code-size and inference costs. It is a trade-off, not a universal generic-API rule.

### Prefer `enum` over `bool` in APIs

Use a named enum when a boolean parameter's meaning is not obvious at the call site. If a bool is appropriate, an inline argument comment can clarify its purpose.

### Reporting errors

Choose by contract:

- `Option` for a simple, expected absence or failure whose cause needs no detail.
- `Result` for recoverable external/operational failures where callers need context to distinguish causes.
- `panic!` for a bug or violated invariant that correct callers should never trigger; some codebases avoid even this and require `Result`.

Developer-facing binaries may use panics for non-fatal errors and tests may use panics for assertions. Document the behavior and keep the failure mechanism aligned with the caller's recovery options.
