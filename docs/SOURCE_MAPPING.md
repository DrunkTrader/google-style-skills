# Source coverage matrix

This matrix records the source outline inspected from Google `styleguide` commit `c775c0c2f73c110613243520c001577cdbc0034d` on October 24, 2026. **Covered** means the topic is represented in one or more local references; the local reference is a concise adaptation, not a verbatim copy. The official guide remains authoritative for exact wording and examples.

No substantive source section is intentionally excluded. Python's source numbering skips 2.15 and 3.9; those are recorded explicitly rather than treated as missing coverage. Codebase markers such as Rust `[chrome]` and `[Fuchsia]` are covered as conditional rules.

## C++

| Source section and meaningful subsections | Local reference(s) | Status |
| --- | --- | --- |
| Background; Goals of the Style Guide | [background-and-version.md](../google-cpp-style/references/background-and-version.md) | Covered |
| C++ Version | [background-and-version.md](../google-cpp-style/references/background-and-version.md) | Covered |
| Header Files; Self-contained Headers; The `#define` Guard; Include What You Use; Forward Declarations; Defining Functions in Header Files; Names and Order of Includes | [headers-scoping.md](../google-cpp-style/references/headers-scoping.md) | Covered |
| Scoping; Namespaces; Internal Linkage; Nonmember, Static Member, and Global Functions; Local Variables; Static and Global Variables (destruction, initialization, common patterns); `thread_local` Variables | [headers-scoping.md](../google-cpp-style/references/headers-scoping.md) | Covered |
| Classes; Doing Work in Constructors; Implicit Conversions; Copyable and Movable Types; Structs vs. Classes; Structs vs. Pairs and Tuples; Inheritance; Operator Overloading; Access Control; Declaration Order | [classes-functions.md](../google-cpp-style/references/classes-functions.md) | Covered |
| Functions; Inputs and Outputs; Write Short Functions; Function Overloading; Default Arguments; Trailing Return Type Syntax | [classes-functions.md](../google-cpp-style/references/classes-functions.md) | Covered |
| Google-Specific Magic; `cpplint` | [features-and-libraries.md](../google-cpp-style/references/features-and-libraries.md) | Covered |
| Other C++ Features; Ownership and Smart Pointers; Rvalue References; Friends; Exceptions; `noexcept`; RTTI; Casting; Streams; Preincrement and Predecrement; `const`; `constexpr`/`constinit`/`consteval`; Integer Types; Floating-Point Types; Architecture Portability; Preprocessor Macros; `0` and `nullptr`/`NULL`; `sizeof` | [features-and-libraries.md](../google-cpp-style/references/features-and-libraries.md) | Covered |
| Other C++ Features continued: Type Deduction (`auto`, function-template arguments, locals, returns, parameters, lambda captures, structured bindings); Class Template Argument Deduction; Designated Initializers; Lambda Expressions; Template Metaprogramming; Concepts and Constraints; C++20 modules; Coroutines | [features-and-libraries.md](../google-cpp-style/references/features-and-libraries.md) | Covered |
| Other C++ Features continued: Disallowed standard library features; Third-party Libraries; Nonstandard Extensions; Aliases; Switch Statements | [features-and-libraries.md](../google-cpp-style/references/features-and-libraries.md) | Covered |
| Inclusive Language | [naming-comments.md](../google-cpp-style/references/naming-comments.md) | Covered |
| Naming; Choosing Names; File Names; Type Names; Concept Names; Variable Names (common, class data members, struct data members); Constant Names; Function Names; Namespace Names; Enumerator Names; Template Parameter Names; Macro Names; Aliases; Exceptions to Naming Rules | [naming-comments.md](../google-cpp-style/references/naming-comments.md) | Covered |
| Comments; Comment Style; File Comments (legal notice/author); Struct and Class Comments (class comments); Function Comments (declarations/definitions); Variable Comments (class members/globals); Implementation Comments (explanatory, argument comments, don'ts); Punctuation, Spelling, and Grammar; TODO Comments | [naming-comments.md](../google-cpp-style/references/naming-comments.md) | Covered |
| Formatting; Line Length; Non-ASCII Characters; Spaces vs. Tabs; Function Declarations and Definitions; Lambda Expressions; Floating-point Literals; Function Calls; Braced Initializer List Format; Looping and Branching Statements; Pointer and Reference Expressions and Types; Boolean Expressions; Return Values; Variable and Array Initialization; Preprocessor Directives; Class Format; Constructor Initializer Lists; Namespace Formatting; Horizontal Whitespace (general, loops/conditionals, operators, templates/casts); Vertical Whitespace | [formatting-exceptions.md](../google-cpp-style/references/formatting-exceptions.md) | Covered |
| Exceptions to the Rules; Existing Non-conformant Code; Windows Code | [formatting-exceptions.md](../google-cpp-style/references/formatting-exceptions.md) | Covered |

## Rust

| Source section and meaningful subsections | Local reference(s) | Status |
| --- | --- | --- |
| Background; Scope; Goals of the style guide | [background-and-scope.md](../google-rust-style/references/background-and-scope.md) | Covered |
| Follow public Rust style rules; Rust Style Guide; Rust API Guidelines | [background-and-scope.md](../google-rust-style/references/background-and-scope.md) | Covered |
| Apply API design rules in context; library code; application code | [background-and-scope.md](../google-rust-style/references/background-and-scope.md) | Covered |
| Code organization; Prefer small crates `[chrome]`; flat `rust_library` layout `[chrome]`; source/leaf module names; non-leaf modules; glob imports; one-module `use`; local trait imports; qualified top-level functions; unqualified type names; appropriate import mechanism `[chrome]` | [organization-and-imports.md](../google-rust-style/references/organization-and-imports.md) | Covered |
| Code formatting and aesthetics; appropriate formatting tool; opting out of automatic formatting | [formatting-ownership-apis.md](../google-rust-style/references/formatting-ownership-apis.md) | Covered |
| Ownership and borrowing; avoid `Rc`/`Arc`; prefer borrows over deep copies | [formatting-ownership-apis.md](../google-rust-style/references/formatting-ownership-apis.md) | Covered |
| Function inputs and outputs; flexible references; iterator vs. owned returns; iterator vs. slice parameters; accepting `Into`; enum over bool; reporting errors (`Option`, `Result`, `panic!`) | [formatting-ownership-apis.md](../google-rust-style/references/formatting-ownership-apis.md) | Covered |
| Types; newtypes vs. aliases; named fields over tuples/non-newtype tuple structs | [types-traits-concurrency.md](../google-rust-style/references/types-traits-concurrency.md) | Covered |
| Traits; necessary implementations; standard traits; derives; generics vs. `dyn Trait`; traits vs. inherent impls; extension traits; important traits; `From` plus constructors; options structs `Default` | [types-traits-concurrency.md](../google-rust-style/references/types-traits-concurrency.md) | Covered |
| Concurrency; handling poison; no `async`/`.await` `[chrome]`; no std threads `[chrome]`; `fuchsia_sync::Mutex` `[Fuchsia]` | [types-traits-concurrency.md](../google-rust-style/references/types-traits-concurrency.md) | Covered |
| Macros; preference order and macro/code-generation trade-offs | [types-traits-concurrency.md](../google-rust-style/references/types-traits-concurrency.md) | Covered |
| Naming; methods; lifetimes; generic parameters; extension traits; initialization functions; abbreviations | [naming-documentation.md](../google-rust-style/references/naming-documentation.md) | Covered |
| When and how to write documentation; examples; panic/safety/invariant docs; `///`; `//!`; Markdown; ordinary comments; generated-doc trade-offs | [naming-documentation.md](../google-rust-style/references/naming-documentation.md) | Covered |
| Other Rust features; unsafe code; no unstable features; getters/setters; closure accessors; expected API sets; `#[doc(hidden)]`; `const` functions; non-mathematical overloading; `#[non_exhaustive]` enums/structs; `#[must_use]` functions/types; code before `main()` | [other-features.md](../google-rust-style/references/other-features.md) | Covered |
| Implementation concerns; type inference; pattern matching vs. check-then-unwrap; `expect` vs. `unwrap`; non-exhaustive matches; assertion context; iterator chains; `panic::catch_unwind`; `format!`/`write!` | [other-features.md](../google-rust-style/references/other-features.md) | Covered |
| Use the right per-codebase test framework | [testing-source-and-license.md](../google-rust-style/references/testing-source-and-license.md) | Covered |

## Python

| Source section and meaningful subsections | Local reference(s) | Status |
| --- | --- | --- |
| 1 Background | [language-rules.md](../google-python-style/references/language-rules.md), [source-and-license.md](../google-python-style/references/source-and-license.md) | Covered |
| 2.1 Lint; Definition; Pros; Cons; Decision; suppressions and tooling | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.2 Imports; Definition; Pros; Cons; Decision; exemptions for `typing`, `collections.abc`, `typing_extensions` | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.3 Packages; pros, cons, decision; full package paths | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.4 Exceptions; definition, pros, cons, decision; assertions; custom exceptions; catch-all restrictions; `try`/`finally` | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.5 Mutable Global State; definition, pros, cons, decision; constants | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.6 Nested/Local/Inner Classes and Functions; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.7 Comprehensions & Generator Expressions; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.8 Default Iterators and Operators; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.9 Generators; definition, pros, cons, decision; `Yields:` and cleanup | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.10 Lambda Functions; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.11 Conditional Expressions; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.12 Default Argument Values; definition, pros, cons, decision; mutable/default-load caveats | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.13 Properties; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.14 True/False Evaluations; definition, pros, cons, decision; `None`, booleans, integers, NumPy | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.15 | No source section exists in the current upstream outline; recorded here to explain the numbering gap. | Covered |
| 2.16 Lexical Scoping; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.17 Function and Method Decorators; definition, pros, cons, decision; `staticmethod`/`classmethod` | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.18 Threading | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.19 Power Features; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.20 Modern Python / `__future__`; definition, pros, cons, decision; future imports | [language-rules.md](../google-python-style/references/language-rules.md) | Covered |
| 2.21 Type Annotated Code; definition, pros, cons, decision | [language-rules.md](../google-python-style/references/language-rules.md), [type-annotations.md](../google-python-style/references/type-annotations.md) | Covered |
| 3.1 Semicolons; 3.2 Line length; 3.3 Parentheses; 3.4 Indentation; 3.4.1 trailing commas | [style-rules.md](../google-python-style/references/style-rules.md) | Covered |
| 3.5 Blank Lines; 3.6 Whitespace; 3.7 Shebang Line | [style-rules.md](../google-python-style/references/style-rules.md) | Covered |
| 3.8 Comments and Docstrings; docstrings; modules/test modules; functions/methods/overrides; classes; block/inline comments; punctuation/spelling/grammar | [style-rules.md](../google-python-style/references/style-rules.md) | Covered |
| 3.9 | No source section exists in the current upstream outline; recorded here to explain the numbering gap. | Covered |
| 3.10 Strings; logging; error messages | [style-rules.md](../google-python-style/references/style-rules.md) | Covered |
| 3.11 Files, Sockets, and similar Stateful Resources; 3.12 TODO Comments; 3.13 Imports formatting; 3.14 Statements; 3.15 Getters and Setters | [style-rules.md](../google-python-style/references/style-rules.md) | Covered |
| 3.16 Naming; names to avoid; conventions/exemptions; file naming; Guido recommendations; mathematical notation | [naming-and-structure.md](../google-python-style/references/naming-and-structure.md) | Covered |
| 3.17 Main; 3.18 Function length | [naming-and-structure.md](../google-python-style/references/naming-and-structure.md) | Covered |
| 3.19 Type Annotations; general rules; line breaking; forward declarations; defaults; NoneType; aliases; ignoring types; variables; tuples/lists; type variables; strings; typing imports; conditional imports; circular dependencies; generics | [type-annotations.md](../google-python-style/references/type-annotations.md) | Covered |
| 4 Parting Words | [source-and-license.md](../google-python-style/references/source-and-license.md) and [SKILL.md](../google-python-style/SKILL.md) | Covered |

## TypeScript

| Source section and meaningful subsections | Local reference(s) | Status |
| --- | --- | --- |
| Introduction; Terminology notes; Guide notes | [source-files.md](../google-typescript-style/references/source-files.md) | Covered |
| Source file basics; UTF-8; whitespace characters; special escape sequences; non-ASCII characters | [source-files.md](../google-typescript-style/references/source-files.md) | Covered |
| Source file structure; copyright; `@fileoverview`; imports; import paths; namespace vs. named imports; Apps JSPB protos; renaming imports; exports; export visibility; mutable exports; container classes; import/export type; `import type`; `export type`; modules not namespaces | [source-files.md](../google-typescript-style/references/source-files.md) | Covered |
| Language features; local variables; `const`/`let`; one variable per declaration; array literals; Array constructor; array properties; spread; array destructuring | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Object literals; Object constructor; iterating objects; spread; computed property names; object destructuring | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Classes; declarations; methods; `toString`; static methods; private static methods; static dispatch; static `this`; constructors; class members; `#private`; `readonly`; parameter properties; field initializers; outside-lexical-scope properties; getters/setters; computed properties; visibility; prototype patterns | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Functions; terminology; declarations; nested functions; function expressions; arrow bodies; rebinding `this`; callbacks; arrow properties; event handlers; parameter initializers; rest/spread; formatting functions | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| `this`; Interfaces | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Primitive literals; string literals; single quotes; no line continuations; template literals; number literals; type coercion; implicit coercion | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Control structures; blocks; assignment in conditions; iterating containers; grouping parentheses; exception handling; errors; throwing/catching; empty catch blocks; switch; equality; type/non-null assertions; assertion syntax; double assertions; object literals; focused try blocks | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Decorators | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Disallowed features; wrapper objects; Automatic Semicolon Insertion; const enums; debugger; `with`; dynamic evaluation; non-standard features; modifying builtins | [language-features.md](../google-typescript-style/references/language-features.md) | Covered |
| Naming; identifiers; naming style; descriptive names; camel case; dollar sign; type parameters; test names; underscore prefix/suffix; imports; constants; aliases | [naming-and-types.md](../google-typescript-style/references/naming-and-types.md) | Covered |
| Type system; inference; return types; undefined/null; nullable aliases; optional vs. `|undefined`; structural types; interfaces vs. type aliases; `Array<T>`; index signatures; mapped/conditional types; `any`; specific types; `unknown`; suppressions; `{}`; tuples; wrapper types; return-type-only generics | [naming-and-types.md](../google-typescript-style/references/naming-and-types.md) | Covered |
| Toolchain requirements; TypeScript compiler; `@ts-ignore`; Conformance | [toolchain.md](../google-typescript-style/references/toolchain.md) | Covered |
| Comments and documentation; JSDoc vs. comments; multi-line comments; JSDoc general form; Markdown; tags; wrapping; top-level exports; class/method/function comments; parameter property comments; JSDoc type annotations; informative comments; call-site comments; docs before decorators | [documentation-and-policies.md](../google-typescript-style/references/documentation-and-policies.md) | Covered |
| Policies; consistency; reformatting existing code; deprecation; generated code; style guide goals | [documentation-and-policies.md](../google-typescript-style/references/documentation-and-policies.md) | Covered |

## Coverage interpretation

The matrix maps every current substantive source heading to a local reference. “Covered” does not mean that the reference repeats every upstream example or rationale; it means the topic, rule strength, major exceptions, and source link are represented. A future update must change a row to **Not yet covered** rather than silently dropping a new upstream topic.
