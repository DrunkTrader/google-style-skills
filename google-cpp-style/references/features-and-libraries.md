# Google-specific and other C++ features

Official sections: [Google-Specific Magic](https://google.github.io/styleguide/cppguide.html#Google-Specific_Magic) and [Other C++ Features](https://google.github.io/styleguide/cppguide.html#Other_C++_Features).

## Google-Specific Magic

### `cpplint`

The upstream guide points users to the community-maintained <https://github.com/cpplint/cpplint> project. Treat it as a linting aid, not as proof that a file is fully compliant. Run the version and configuration selected by the repository; do not install or invoke a tool just because this reference mentions it.

## Ownership and resource-related features

### Ownership and Smart Pointers

Make ownership explicit. Prefer `std::unique_ptr` for exclusive ownership and `std::shared_ptr` only when shared ownership is real and required. Use raw pointers/references for non-owning access when the lifetime contract is clear; do not use a raw pointer to hide ownership. At call sites, make transfers visible and avoid unnecessary heap allocation.

### Rvalue References

Use rvalue references and move operations to express efficient transfer or forwarding, not as a reflexive optimization. A moved-from object must remain valid for its documented operations. Do not add forwarding-reference templates when a value or concrete reference type would be clearer.

### Friends

Use `friend` narrowly when it improves a type's interface or allows a tightly coupled helper/operator to access invariants. Do not use friendship as a general substitute for encapsulation; keep the friend relationship close to the type and document non-obvious reasons.

## Error handling, RTTI, and casts

### Exceptions

Google code generally does not use C++ exceptions. Do not introduce throwing APIs or exception-based control flow unless the repository explicitly permits them and the task is within that boundary. A project that changes this policy needs a project-level decision, not a local style waiver.

### `noexcept`

Use `noexcept` when an operation is actually non-throwing and the contract benefits from that fact, especially for move operations and low-level cleanup. Do not add it speculatively: an incorrect `noexcept` can turn a recoverable failure into termination. Keep the exception specification consistent with the project's build and standard-library assumptions.

### Run-Time Type Information (RTTI)

Avoid RTTI such as `dynamic_cast` and `typeid` unless the project explicitly supports it and the design cannot be expressed more clearly with a virtual interface, tagged state, or another checked abstraction. A style finding should explain the maintenance or binary/runtime cost rather than merely naming the feature.

### Casting

Prefer implicit conversions only when they are safe and obvious. Otherwise use the appropriate named cast (`static_cast`, `const_cast`, `reinterpret_cast`, or `dynamic_cast`) with a clear justification. Avoid C-style casts because they hide which conversion is taking place. `reinterpret_cast` and `const_cast` deserve special scrutiny for correctness and lifetime implications; report those separately when they create a real bug risk.

### Streams

Use the repository's established string, formatting, and I/O abstractions. The guide discourages C++ iostreams where they impose unwanted performance, binary-size, or readability costs; do not replace a project-approved stream interface mechanically. Check whether the code is formatting data, logging, or doing interactive I/O before proposing a change.

### Preincrement and Predecrement

Prefer preincrement/predecrement (`++i`, `--i`) when either form is equivalent, especially for iterators and user-defined types, because it avoids an unnecessary temporary. Postfix is appropriate when the old value is intentionally needed.

## Constants, types, and templates

### Use of `const`

Use `const` to communicate non-mutation and to enable compiler checking. Place `const` consistently with the surrounding code and make pointer/reference constness unambiguous. In particular, distinguish a pointer-to-const from a const pointer. See [Formatting](formatting-exceptions.md) for pointer/reference spacing.

### `constexpr`, `constinit`, and `consteval`

Use compile-time facilities when they make initialization, lookup, or an invariant clearer. Use `constexpr` for values/functions that are valid and useful at compile time, `constinit` to enforce constant initialization of static/thread-local objects, and `consteval` only when a compile-time call is required by the interface. Do not add keywords as decoration or to force a complex design into a constant-expression form.

### Integer Types

Choose an integer type that communicates range, signedness, and interoperability. Use fixed-width types when the bit width is part of the contract; use `int` for ordinary small integers when the project convention supports it; use `size_t`/container size types for sizes and indexes with the required conversion care. Avoid mixing signed and unsigned values silently. Unsigned arithmetic is not a general replacement for “non-negative” and can produce surprising wraparound or comparison behavior.

### Floating-Point Types

Choose floating-point types based on required precision, performance, ABI, and library interfaces. Do not compare computed floating-point values for exact equality unless the values are known to be exact; define an error/tolerance policy appropriate to the domain. Keep numeric-type conversions visible.

### Architecture Portability

Do not assume pointer size, endianness, alignment, integer width, or compiler extensions unless the target is explicitly constrained. Use the project's portability abstractions and test matrix. A style fix that changes a type can be an ABI or serialization change; review it as such.

### Preprocessor Macros

Prefer language constructs, constants, templates, and inline functions to macros. Macros that remain should have distinctive names, avoid evaluating arguments more than once, and be limited to conditional compilation or facilities that cannot be expressed otherwise. Parenthesize macro arguments and results when appropriate, and `#undef` private helper macros when the local convention requires it.

### `0` and `nullptr`/`NULL`

Use `nullptr` for null pointers in C++11 and later. Do not use `0` or `NULL` where a pointer value is intended; this avoids overload ambiguity and communicates the type.

### `sizeof`

Prefer `sizeof(variable)` or `sizeof(type)` in the form consistent with the repository. Use `sizeof` on the expression/type actually being allocated or processed rather than duplicating a type name that can drift.

### Type Deduction (including `auto`)

Use `auto` when it makes the type clear from the initializer, removes repetition, or preserves a type in generic code. Do not use it when the type is important for understanding the API, ownership, signedness, precision, or lifetime. Apply the guide's distinctions to:

- Function-template argument deduction.
- Local variable deduction.
- Return-type deduction.
- Function-parameter deduction.
- Lambda init captures.
- Structured bindings.

In reviews, ask whether the reader can determine the type locally and whether deduction could hide a narrowing conversion or proxy/reference type.

For lambda parameters whose type is needed inside the body, prefer a named template
parameter over `auto` plus `decltype`. Structured bindings are a special case: they
can improve readability by giving meaningful names to pair/tuple elements or map
entries. If a binding name differs from an underlying struct field, a field-name
comment can make the positional relationship explicit.

### Class Template Argument Deduction

Use CTAD only for templates that have explicitly opted into it by providing at least
one explicit deduction guide; standard-library templates are presumed to have opted
in. The general type-deduction rules still apply. Provide explicit template
arguments when they clarify ownership, element type, narrowing, or overload
selection. Do not rely on a deduction guide that is difficult to discover at the
call site.

### Designated Initializers

Use designated initializers only in the C++20-compliant form supported by the
project's compiler set. Designators must follow the declaration order of the
aggregate's fields; do not rely on C extensions that permit reordering. Do not use
designators to bypass constructors or invariants.

### Lambda Expressions

Use lambdas for short local behavior and callbacks. Prefer explicit captures when a
lambda may escape the current scope. Use default reference capture (`[&]`) only when
the lambda's lifetime is obviously shorter than every possible capture. Use default
value capture (`[=]`) only for a short lambda binding a few obvious variables and
never when it implicitly captures `this`; capture `this` explicitly when needed.
Use captures only to capture enclosing variables—do not use init captures merely to
introduce new names or substantially rename values. Avoid reference captures when a
callback may outlive the referenced object. A complex or reusable lambda may be
clearer as a named function object or function.

### Template Metaprogramming

Avoid complex template metaprogramming when a normal function, type, or runtime operation is adequate. Keep compile-time machinery localized, documented, and diagnosable. Consider compile cost and error messages as maintenance costs.

### Concepts and Constraints

Use concepts sparingly, generally only where a pre-C++20 template would have been
used. Prefer standard-library concepts and `requires(Condition)` syntax; avoid the
`template<Concept T>` form and legacy `enable_if` when a constraint is clearer. Do
not introduce new concepts in public headers unless they are internal, do not define
concepts the compiler cannot enforce, and do not duplicate an obvious function-body
requirement. New concepts should provide a demonstrated improvement such as better
diagnostics or a genuinely non-obvious compile-time contract.

### C++20 modules

Do not use C++20 modules under the current Google guide. The upstream rationale is
that modules are not yet sufficiently supported by Google's build systems, compilers,
and tooling. If a non-Google project has a deliberate module policy, that project
instruction takes precedence and should be documented as an explicit divergence.

### Coroutines

Use C++20 coroutines only through libraries approved by project leads. Do not roll
your own promise or awaitable type. The language does not provide one standard
promise implementation, and lifetime, scheduling, dangling-reference, and race
hazards are easy to hide behind coroutine syntax.

## Libraries and extensions

### Disallowed standard library features

The current guide disallows these standard-library facilities in Google code:

- `<ratio>` compile-time rational numbers.
- `<cfenv>` and `<fenv.h>` floating-point environment headers.
- `<filesystem>`, citing insufficient testing support and inherent security vulnerabilities.

Do not assume that “standard” means “approved”; check for a project-approved
alternative and record any explicit project divergence.

### Third-party Libraries

When choosing a library, be consistent with nearby code. First look for a library
the codebase already uses for the problem. The guide's rough preference order is:
Abseil, the C++ standard library except the disallowed facilities above, existing
first-party libraries, then other third-party libraries. Account for license
compliance, vulnerability patching, monitoring, build cost, support burden, and
upstream breaking changes. Follow the repository's third-party policy.

### Nonstandard Extensions

Do not use nonstandard extensions. A designated project-wide portability header may
wrap extensions when the project explicitly provides that boundary. Keep direct
uses out of ordinary application/library code. Examples include compiler
attributes/intrinsics, pragmas, inline assembly, `__COUNTER__`,
`__PRETTY_FUNCTION__`, statement expressions, VLAs, `alloca`, and the Elvis
operator.

### Aliases

Use `using` rather than `typedef` in new C++ code. A public alias exists for API
users and must be documented: explain whether it is guaranteed to remain identical
to the aliased type or only promises a narrower compatibility contract. Do not put a
namespace alias in a public API, and do not publish an alias merely to save typing in
an implementation. Local aliases in function definitions, private class sections,
internal namespaces, and `.cc` files are implementation details.

### Switch Statements

Use `switch` for a finite choice. If the condition is not an enum, include a
`default`; if an impossible default is reached, treat it as an error. Annotate
fallthrough with `[[fallthrough]];` at the execution point, except for consecutive
case labels with no intervening code. Do not use a switch to disguise unrelated
conditionals.
