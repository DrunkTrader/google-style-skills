# Header files and scoping

Official sections: [Header Files](https://google.github.io/styleguide/cppguide.html#Header_Files) and [Scoping](https://google.github.io/styleguide/cppguide.html#Scoping).

## Header Files

In general, pair a `.cc` file with a `.h` file. Unit tests and small `main()` translation units are common exceptions.

### Self-contained Headers

- Headers should compile when included on their own and should end in `.h`.
- Include every header needed for declarations and definitions exposed by the header; do not rely on transitive includes.
- Use `.inc` only for deliberately non-self-contained include fragments, usually included at unusual locations, and use them sparingly.
- Definitions of inline functions and templates that clients instantiate belong in the header or in a file it includes. Do not create new `-inl.h` files for this purpose. A template whose instantiations are confined to one `.cc` can remain there.

### The `#define` Guard

Every header uses a path-derived guard of the form `PROJECT_PATH_FILE_H_`, based on the full path in the source tree:

```cpp
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_

// declarations

#endif  // FOO_BAR_BAZ_H_
```

Match the project's established project-prefix convention when the source tree uses one.

### Include What You Use

If a file refers to a symbol, directly include the header that intentionally provides it. Do not include a header merely because another header currently includes it. This applies to a related header too: a `.cc` should include the related `.h` even when another local header happens to include it.

### Forward Declarations

Avoid forward declarations where a direct include is reasonable. They can reduce compile work, but they hide dependencies, weaken tooling, break when owned APIs evolve, and can silently change overload resolution. Never forward-declare entities in `std`.

For symbols the project owns, first make the real header cheap enough to include or improve its compile cost. Use a forward declaration only when engineering judgment shows it is the better fix for a measured or material dependency problem. Do not forward-declare symbols the project does not own.

### Defining Functions in Header Files

Define a function at its public declaration only when it is short (the guide uses roughly ten lines as a rule of thumb) or when a technical reason such as templates, `constexpr`, or performance requires header visibility. Put longer bodies in `.cc` or an internal section of the header. Any header definition must be ODR-safe, either through `inline` or an implicitly-inline form such as a template or in-class definition.

## Names and Order of Includes

Use this group order, with one blank line between non-empty groups:

1. Related header.
2. C system headers and other angle-bracket `.h` headers.
3. C++ standard-library headers.
4. Other libraries' headers.
5. Project headers.

Within a group, order alphabetically. Project headers normally use a path below the source root without `.` or `..` aliases and use quotes. Use angle brackets for C/C++ standard, POSIX/Linux/Windows system, and rare third-party headers that require them. Conditional system-specific includes may follow the normal groups when kept small and localized.

Including the related header first makes missing self-containment fail close to the implementation that owns the dependency.

## Scoping

### Namespaces

- Put code in a project-unique namespace except where a narrow exception applies.
- Follow the namespace naming rules in [Naming](naming-comments.md#namespace-names).
- Wrap the source after includes, flags, and permitted forward declarations; do not indent the contents merely because they are in a namespace.
- Close multi-line namespaces with a comment. Single-line nested namespace syntax is preferred in new code but not mandatory.
- Never add declarations, including forward declarations, to `std`.
- Never use a using-directive such as `using namespace foo;`.
- Avoid namespace-scope aliases in public headers unless they are explicitly internal-only; local aliases and `.cc` aliases may be appropriate.
- Do not use inline namespaces. Use an `internal`-named namespace to signal implementation-only API, with a sufficiently unique internal name.

### Internal Linkage

Definitions used only by one `.cc` should have internal linkage with an unnamed namespace or `static`. Do not use these constructs in headers. Format an unnamed namespace like a named namespace and close it with `}  // namespace`.

### Nonmember, Static Member, and Global Functions

Prefer free functions in a namespace for operations that are not tied to an object. Avoid a class made only of static members unless it provides real type semantics, policy, traits, or a deliberately closed interface. Truly global functions should be rare. A nonmember function should not depend on external mutable variables and should use internal linkage when it is `.cc`-local.

### Local Variables

- Declare variables in the narrowest practical scope and close to first use.
- Initialize at declaration instead of declaring then assigning.
- Prefer brace initialization for containers when it makes the initial state clear.
- Variables used only by an `if`, `while`, or `for` normally belong in that statement's scope.
- Consider constructor/destructor cost before moving an object into or out of a loop; a narrower scope is not automatically faster.

### Static and Global Variables

Objects with static storage duration should be trivially destructible. Static function-local variables may use dynamic initialization; dynamic initialization of namespace-scope or static data members is discouraged and permitted only when initialization order cannot affect observable behavior. Prefer `constexpr` or `constinit` for constant initialization.

Avoid global strings, dynamic containers, and smart pointers with non-trivial cleanup as static objects. Prefer string views/character data, trivial fixed tables, a custom type with a trivial destructor and `constexpr` constructor, or—only as a last resort—a function-local dynamically allocated object whose lifetime is intentionally leaked.

### `thread_local` Variables

Prefer `thread_local` to non-standard thread-local mechanisms. Namespace- or class-scope `thread_local` must use true compile-time initialization enforced with `constinit` (or rarely `constexpr`). Function-scope `thread_local` avoids initialization-order concerns but still has thread-exit destruction hazards; prefer trivial types or demonstrably safe destructors.
