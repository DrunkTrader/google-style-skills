# Other Rust features and implementation concerns

Official sections: [Other Rust features](https://google.github.io/styleguide/rustguide.html#Other_Rust_features) and [Implementation concerns](https://google.github.io/styleguide/rustguide.html#Implementation_concerns).

## Other Rust features

### Unsafe code

Do not write `unsafe` when safe Rust can provide the same behavior. When it is required:

- Encapsulate it behind a safe abstraction and isolate it from business logic, ideally in a small crate with few dependencies.
- Put a `SAFETY:` comment beside the unsafe block/abstraction explaining the proof obligations.
- Record why a safe alternative is not sufficient and, for performance-driven unsafe code, provide benchmarks.

Do not treat the presence of a safety comment as proof; review aliasing, lifetime, initialization, thread-safety, and FFI invariants concretely.

### No unstable features

Do not use unstable Rust features. Android Embedded, approved Chrome features, and Fuchsia have explicitly described exceptions. Confirm the codebase-specific approval and toolchain before applying one.

### Getters and setters

Use predictable names:

- `foo()` returns `&T` or a `Copy` value.
- `foo_mut()` returns `&mut T`.
- `take_foo()` clears the field and returns the old value.
- `set_foo(T)` writes a value.
- `with_foo()` / `with_mut_foo()` scopes closure access.
- `replace_foo(T)` writes a value and returns the old one.

#### More on accessors that accept closures

Closure accessors are useful for `Mutex`/`RefCell` interior mutability because the closure bounds the access scope, avoiding an exposed guard type. They are also useful when validation/follow-up work must happen while a non-cloneable or expensive property is borrowed. A closure accessor may return the closure's result.

### Implement expected API sets together

If a type has `len()`, also provide `is_empty()` where the semantics fit. Look for analogous standard API pairs and Clippy guidance before exposing only half of an expected set.

### Do not access items marked `#[doc(hidden)]` that you don't own

Treat hidden documentation items as private. Do not depend on them from external code; they may change without a public compatibility promise.

### Use `const` functions responsibly

Mark a public function `const` only when the project expects it to remain const or can help clients migrate. Removing `const` later is a breaking change.

### Avoid overloading for non-mathematical purposes

Operator overloads should express the operator's original mathematical/logical meaning. Do not use operators merely as syntax sugar for an unrelated domain action.

### Apply `#[non_exhaustive]` to publicly-exposed enums

Mark a public enum used across team boundaries `#[non_exhaustive]` so callers must handle future variants. Exceptions include a fixed ontology, a two-state value that is effectively a boolean, or a codebase that commits to fixing every resulting breakage through a large-scale change.

### Apply `#[non_exhaustive]` to public structs with public fields

Apply the same forward-compatibility principle to public structs whose fields are public and consumed by other teams. Exceptions include stable types, tightly controlled use, or an explicit migration commitment.

### `#[must_use]` on functions

Use `#[must_use]` when a caller cannot use the function correctly while ignoring
the return value, including pure functions such as `HashMap::get()`, or when the
return value carries an error/critical information. Do not redundantly annotate a
function when its return type is already `#[must_use]` (as `Result` is). Avoid noisy
diagnostics for intentionally discardable values.

### `#[must_use]` on types

Use `#[must_use]` on types returned by functions that should be must-use: error
types and lazily evaluated computations are examples. Check whether the type's
normal use includes intentional discard before adding the attribute.

### Do not run code before `main()`

Avoid pre-`main()` execution and initialization mechanisms that run before the program's normal entry point. Make startup order explicit and testable. Follow an established framework mechanism only when the repository requires it.

## Implementation concerns

### Don't overuse type inference

Use inference when the type is clear from the initializer and keeps code readable.
Add explicit types—preferably on the variable declaration rather than a turbofish—
for generic-returning calls such as `.into()`/`.parse()` and for complex iterator
chains, as well as when they communicate an important boundary or ownership choice.

### Prefer pattern matching over check-then-unwrap

Use `match`, `if let`, `while let`, or the appropriate combinator to handle an `Option`/`Result` in one operation. Avoid a separate check followed by `unwrap()` that duplicates the condition or can drift.

### Prefer `expect` over `unwrap`

When a panic is justified, use `expect("...context...")` so the failure explains the invariant or assumption. Prefer error propagation or a check when the condition is recoverable.

### Don't omit patterns on `non_exhaustive` enums when matching

Use a wildcard/future-proof arm when matching an external `#[non_exhaustive]` enum. Keep the fallback behavior explicit and safe; do not assume the current variants are permanent.

### Use context strings to clarify assertions

Assertions and test failures should state the relevant values or invariant. A bare assertion that fails far from its cause is harder to diagnose.

### Don't use iterator combinator chains when direct iteration is clearer

Iterator chains are powerful, but a direct `for` loop is preferable when a chain becomes difficult to read, debug, or explain. Optimize for the reader, not maximum chaining density.

### Don't call `panic::catch_unwind`

Do not use `panic::catch_unwind` in first-party Rust code. A narrow defense-in-depth
exception is possible only when it is not relied upon for correctness, the codebase
is already designed to avoid panics, and the target can run with `panic=unwind`.
Chrome, Android, and Fuchsia `panic=abort` environments do not receive that
exception. Otherwise fix the invariant or propagate a typed error.

### Prefer `format!` / `write!` for concatenation and substitution

Use `format!`/`write!` when constructing formatted strings or writing into a buffer. Avoid repeated `+` concatenation that obscures formatting intent or creates unnecessary intermediate strings.
