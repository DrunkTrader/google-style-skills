# Types, traits, concurrency, and macros

Official sections: [Types](https://google.github.io/styleguide/rustguide.html#Types), [Traits](https://google.github.io/styleguide/rustguide.html#Traits), [Concurrency](https://google.github.io/styleguide/rustguide.html#Concurrency), and [Macros](https://google.github.io/styleguide/rustguide.html#Macros).

## Types

### Newtypes versus type aliases

Use a newtype when a concept has meaningful semantics, its own API, future representation flexibility, or needs type-safety against mixing values such as `Day`, `Month`, and `Year`. Use an alias when the underlying type is intentionally interchangeable and a named spelling improves readability without adding a new invariant.

### Prefer named fields over tuples and non-newtype tuple structs

Prefer named fields when positions have meaning or a value crosses an API boundary. Tuple indexes become hard to read. Single-field tuple structs remain appropriate as newtypes; local tuples are fine when confusion is unlikely.

## Traits

### Add trait implementations when they become necessary

Low-level libraries may anticipate common user needs, but application code should add trait implementations as required. Avoid implementing a large “everything” trait surface speculatively.

### Implement known standard library traits instead of custom methods

If a method has the purpose and semantics of a standard trait, implement the trait (for example `FromStr`) instead of inventing a parallel method. A discoverability helper may coexist with the trait implementation.

### Use `#[derive()]` if possible

Prefer derives over hand-written implementations when the semantics match. A manual implementation needs a concrete reason, such as an invariant or behavior not expressible by a derive.

### Generics versus `dyn Trait`

Library functions should generally accept generics or `impl Trait` instead of `dyn Trait` for efficiency, inlining, and trait compatibility. Use dynamic dispatch when code size or runtime polymorphism is the real requirement. Make the dispatch and allocation consequences visible.

### When to define a trait versus an inherent implementation

Define a trait to enable generic constraints, accept/return `impl Trait`/`dyn Trait`, or provide an extension trait. Do not use a trait merely to organize methods that belong on an inherent implementation.

### Extension traits

An extension trait adds methods to a type owned by another crate and is not primarily a generic/dynamic-dispatch abstraction. Name it with an `Ext` suffix (for example `ForeignTypeExt`), preferably in the team that owns the original type. Exceptions are high-value foundational extensions expected to become widely known.

### Specific guidance for important traits

- Public-field types should consider traits implemented by all subfields.
- Error types should implement `Copy` when practical; non-`Copy` fields such as `String` can make that impossible.
- Implement `Copy` when future `Copy` stability is reasonably clear.
- Most types should implement `Clone` unless they represent an external resource.
- Implement `Default` when a type has `new()` or a meaningful default state.
- Prefer `PartialEq`/`PartialOrd` unless the stronger `Eq`/`Ord` contract is true.
- Types likely to be map keys should implement `Hash` and `Eq`; add `Ord` when total ordering is meaningful.

### Pair important `From` impls with explicit constructor methods

For an important `From` conversion that is a primary construction path, provide a discoverable inherent `new()`, `new_from_foo()`, or `from_foo()` method as appropriate.

### Options structs should implement `Default`

All-public options structs should implement `Default` so callers can use struct update syntax and add future fields without repeating every default.

## Concurrency

### Handling poison

Never reach into a poisoned mutex to retrieve its contents merely because it is convenient. Treat the poison signal as part of the synchronization/error contract and follow the codebase's recovery policy.

### Don't use `async` / `.await` `[chrome]`

Chromium's current guidance says not to use Rust `async`/`.await`. This is conditional codebase guidance, not a general Rust rule; verify the repository before filing it.

### Don't start new threads through the Rust standard library `[chrome]`

In Chromium, prefer sequences over starting threads through the Rust standard library. Use the repository's scheduler/runtime and its lifecycle model.

### Use `fuchsia_sync::Mutex` `[Fuchsia]`

Fuchsia code should use its prescribed mutex type rather than `std::sync` or `parking_lot`. Confirm the target is Fuchsia.

## Macros

Prefer, in order:

1. Ordinary functions, types, traits, objects, and modules.
2. `macro_rules!` for simple AST-level generation.
3. Other code generation such as a `genrule`.
4. Procedural macros only when the benefit justifies their tooling and maintenance cost.

Macros can reduce IDE/code-search quality, create a dialect, complicate large-scale changes, and be harder to reason about. Keep macro APIs small, document generated behavior, and prefer generated source or normal Rust when it is clearer.
