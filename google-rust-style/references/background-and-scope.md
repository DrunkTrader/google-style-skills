# Background, scope, and external rules

Official sections: [Background](https://google.github.io/styleguide/rustguide.html#Background), [Follow public Rust style rules](https://google.github.io/styleguide/rustguide.html#Follow_public_Rust_style_rules), and [Apply API design rules in context](https://google.github.io/styleguide/rustguide.html#Apply_API_design_rules_in_context).

## Scope

The upstream guide is written for Google's Rust use across google3, Android, ChromeOS, Fuchsia, and Chrome. It says Android, Chromium, and other codebases may have their own adoption and strictness rules. Do not apply a codebase marker such as `[chrome]` or `[Fuchsia]` to an unrelated Cargo project.

## Goals

The guide emphasizes:

- Readability and maintainability over ease of writing.
- Patterns that make large-scale automated changes easier.
- Consistency with the wider Rust ecosystem where possible.
- Rules that provide enough benefit to justify review and memory cost.
- Fewer recurring style disagreements.

These goals guide judgment but do not override explicit project instructions or a documented compatibility requirement.

## Follow public Rust style rules

Follow the official public Rust Style Guide and Rust API Guidelines unless this Google guide intentionally conflicts with their primary recommendations. `rustfmt` normally enforces much of the public formatting style. Consult the project's toolchain and configuration before relying on a nightly-only option.

Useful upstream references named by Google:

- [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

## Apply API design rules in context

Classify the crate/API as:

- **Library code:** intended for other projects or general reuse. API-design rules are binding.
- **Application code:** intended for one application or a specific product. API-design rules are strong recommendations; favor directness over premature generalization.

When reviewing a local application, do not file a violation merely because a library-level abstraction would be more flexible. Explain the trade-off and use the simpler design when the guide allows it.
