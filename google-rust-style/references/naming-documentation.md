# Naming and documentation

Official sections: [Naming](https://google.github.io/styleguide/rustguide.html#Naming) and [When and how to write documentation](https://google.github.io/styleguide/rustguide.html#When_and_how_to_write_documentation).

## Naming

### Naming methods

Follow standard-library conventions. Use `as_...`, `to_...`, and `into_...` with the appropriate borrowing/ownership semantics. Names should make cost and conversion behavior unsurprising.

### Naming lifetimes

Use descriptive lifetime names for type-level relationships. Anonymous `'_` is fine when it works; a single-character lifetime is fine for a simple input/output relationship or a local higher-ranked bound. More than two local lifetimes is a signal to choose descriptive names.

### Naming generic parameters

Use short names related to the type/trait role. `T`/`U` are acceptable for broadly generic parameters; use an indicative letter or short word when bounds convey a more specific concept.

### Naming extension traits

Use an `Ext` suffix, such as `ForeignTypeExt`, for extension traits.

### Naming initialization functions

- Use `new()` for the primary constructor, or `new_with_foo()` when multiple constructor variants are needed.
- If a constructor returns `Result`, use `try_new()`.
- Use `from_foo()` for value-to-value conversions paired with a `From` implementation.

### Avoid abbreviations

Avoid acronyms/initialisms and deleted-letter abbreviations that people outside the project may not know. Common Wikipedia-level abbreviations or clearly non-confusing terms such as `IpAddr` may be acceptable after reviewer judgment. Prefer clarity over saving characters.

## Documentation

Document public APIs, potentially with `missing_docs` linting. Include examples somewhere that show how important functionality is used, not necessarily on every function. Document panic cases caused by malformed input and state invariants for unsafe functions and traits. Use capitalization and punctuation.

Do not write comments that merely repeat a name or explain basic language syntax. An individual enum variant may omit docs when its name is self-explanatory.

### Comment forms

- Use `///` for the item that follows.
- Use `//!` at the top of a file/module for module or crate documentation.
- Use Markdown in documentation comments and follow the public Rust doc-comment style guide.
- Use ordinary `//` for implementation notes, TODOs not intended for users, and commented-out code.
- It is fine to combine a public `///` contract with a nearby implementation `//` note when each adds different information.

Prefer direct, readable doc comments over generating documentation through macros. Documentation comments are part of the AST and are consumed by rustdoc, IDEs, and other tooling, so applying the correct form matters.

## Documentation review questions

- Is the comment a caller-facing contract or an implementation note?
- Does it state panic, safety, ownership, lifetime, thread-safety, or invariant behavior that a caller needs?
- Is it still true after this change?
- Would a shorter name or type make the comment unnecessary?
