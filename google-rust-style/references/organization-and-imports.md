# Code organization and imports

Official section: [Code organization](https://google.github.io/styleguide/rustguide.html#Code_organization).

## Crates and modules

### Prefer small crates `[chrome]`

In Chromium, prefer small crates, ideally one file focused on one abstraction. First decide whether APIs truly need to share a crate; only then decide whether modules help. Larger crates are justified by trait coherence or foundational-library needs. The marker is conditional, but the rationale—dependency-graph cost, parallel compilation, and cacheability—can still inform other large codebases.

### Use flat file layout for `rust_library` sources `[chrome]`

In Chromium, source files belonging to one `rust_library`/crate live in one directory rather than nested subdirectories. Cargo-based Rust under `third_party` is the stated exception. Do not import this layout into an ordinary Cargo repository without checking its build convention.

### Name source files and leaf modules after the primary user-defined item

If a leaf module is primarily about `Foo`, name it `foo`/`foo.rs`. A leaf without one primary abstraction may use a descriptive name. The purpose is to make a file's content discoverable at a glance.

### Don't implement APIs in non-leaf modules

Non-leaf modules should normally contain module declarations and re-exports, not the API definitions themselves. Small “tie things together” code, inline test modules, and cross-language binding modules are explicit exceptions. Keep structure and implementation easy to find.

## Imports

### Don't use glob imports

Avoid `use foo::*`. The upstream exceptions allow `use super::*` in inline modules, `use enum::*` inside enum-focused bodies, `pub use submodule::*` for non-leaf re-exports, and a private glob merge for C++ namespaces. A third-party prelude is a review judgment, not a blanket exception. Avoid defining new preludes.

### A `use` statement should import items from one module

Use the equivalent of rustfmt's `imports_granularity = Module`: do not put nested `::` paths inside the `{ ... }` group. Prefer:

```rust
use foo::Foo;
use foo::bar::{Bar, Baz};
```

over a group that mixes `Foo` and `bar::Bar` from different modules.

### Prefer locally-scoped trait imports

Import a trait inside the function that needs its methods unless the trait is used extensively throughout the file. This keeps method-providing imports close to their use and avoids a large, opaque module-level import block.

### Qualify calls to top-level functions with a module name

Import the module and call `module::function()` by default. Exceptions include sufficiently disambiguated C++ interop functions, small single-purpose first-party crates in Chromium, and module names prone to collisions. The primary benefit is consistent readability without cross-reference tooling.

### Type names should be imported and used unqualified

Import types and traits and write `Regex`, not `regex::Regex`, unless ambiguity, generated code/macros, a large type group, or a dependency-heavy file makes a qualified path clearer. Rename common collisions (`io::Error as IoError`) rather than forcing an unreadable import list.

### Use the appropriate import mechanism `[chrome]`

Chromium uses `chromium::import!()` as its prescribed import mechanism. Confirm whether the repository is Chromium and whether that macro is active before applying this rule.

## Organization review questions

- Is the code in the right crate/module, or is the change mixing module structure with implementation?
- Does an import hide origin, create a glob namespace, or make an LSC/tooling change harder?
- Is a codebase-specific marker being applied outside its scope?
- Is an import exception documented by the upstream rule or merely familiar to the reviewer?
