# TypeScript language features, classes, functions, and control flow

Official sections: [Language features](https://google.github.io/styleguide/tsguide.html#language-features), including local variables through control structures.

## Local variable declarations

Use `const` by default and `let` only when reassignment is needed. Never use `var`. Do not read a variable before its declaration. Declare one local variable per statement.

## Array literals

- Do not use `Array()`/`new Array()`; use `[]`, `Array.from`, or an explicit initialization pattern.
- Do not add non-numeric properties to arrays; use an object or `Map`.
- Spread only iterables into arrays, and ensure a conditional spread is always an iterable.
- Array destructuring is allowed; omit unused elements and use a default of `[]` for an optional destructured array parameter. Put defaults on the destructured elements, not by replacing the entire expected shape with a different default.
- Prefer object destructuring when returned/parameter values need names or different types.

## Object literals

- Do not use the `Object` constructor; use object literals.
- Do not use an unfiltered `for...in`; filter own properties or use `Object.keys`/`Object.entries` with `for...of`.
- Spread only objects into object literals. Do not spread arrays/primitives/nullish values, and be cautious with class instances/functions whose prototypes are not copied.
- Computed property names are allowed and count as dict-style keys unless the key is a symbol; do not mix key styles casually.
- Keep destructured parameters simple: one level of unquoted shorthand properties, defaults on the left-hand side, and `{}` as the default for an optional object. Avoid nested/computed parameter patterns.

## Classes

### Class declarations and methods

Do not terminate class declarations or method declarations with semicolons. A class expression assigned in a statement is a statement and does need its terminating semicolon. Separate methods and the constructor from surrounding code with one blank line where the guide requires it.

### Overriding `toString`

An override may exist but must always succeed and have no visible side effects. Avoid calling fragile methods from `toString` because errors can create recursive diagnostic failures.

### Static methods

Prefer module-local functions over private static methods where readability permits. Do not rely on dynamic dispatch of static methods, call inherited static methods through subclasses that do not define them, or use `this` in static methods. Static `this` can resolve inherited fields unexpectedly and encourages hard-to-test shared state.

### Constructors

Always write parentheses for constructor calls (`new Foo()`). Omit an empty constructor when the default constructor is sufficient, except when parameter properties, visibility modifiers, decorators, or a meaningful private constructor require it. Keep constructor spacing and field initialization consistent with the class-member rules.

### Class members

- Do not use ECMAScript `#private` fields; use TypeScript visibility modifiers.
- Mark fields `readonly` when they are not reassigned outside construction (this is shallow).
- Use parameter properties for obvious constructor-to-field plumbing.
- Initialize non-parameter fields at declaration when practical; initialize optional fields explicitly to `undefined` if later shape changes would hurt VM optimization.
- Properties used from outside class lexical scope (for example templates) must not be `private`; use `protected`/`public` according to the framework contract. Do not bypass visibility with `obj['foo']`.
- Getters must be pure and side-effect-free. An accessor pair must contain real logic; use a public field for a pass-through wrapper. Do not define accessors with `Object.defineProperty`.
- Computed class properties are limited to symbols; use symbols sparingly and consider older-target polyfill support.

### Visibility

Limit symbol visibility. TypeScript symbols are public by default; do not write the `public` modifier except for non-readonly public parameter properties where it is required by the intended constructor API. Prefer file-local functions/objects over private methods when that reduces coupling.

### Disallowed class patterns

Do not manipulate prototypes directly in ordinary implementation code. Framework interoperability may require it, but use the framework-approved boundary and do not modify built-in prototypes.

## Functions

### Terminology and declaration choice

Prefer function declarations for named top-level functions. Do not use function expressions; use arrow functions instead, except when dynamic `this` rebinding is required (discouraged) or for generator functions, which have no arrow form. Nested functions may use declarations or arrows; arrows are often clearer inside methods because they retain the outer `this`.

### Arrow function bodies

Use a concise body only when the return value is consumed. Use a block body when the return value should be `void`, the body has side effects, or a block improves readability. An explicit `void` can make a deliberately ignored result clear.

### Rebinding `this`

Do not use `this` in ordinary function declarations/expressions unless the function specifically exists to rebind it. Prefer an arrow, an explicit receiver parameter, or an intentional stable handler. Avoid `bind(this)` when it creates an unremovable event-listener reference.

### Prefer passing arrow functions as callbacks

Prefer an arrow callback that explicitly forwards parameters instead of passing a named function whose optional parameters may receive unexpected callback arguments (`map(parseInt)` is the classic trap). A named callback is fine when its signature is designed for that higher-order API and the behavior is stable.

### Arrow functions as properties

Classes generally should not store methods as arrow-function properties because it hides the binding contract at call sites. Use an arrow at the call site to preserve `this`. An arrow property is appropriate when a stable bound reference is required for event-handler installation/removal or a framework template makes it clearer.

### Event handlers

Use an anonymous arrow for handlers that never need removal. Use a stable arrow property when the handler must be uninstalled. Do not install/remove with `.bind(...)` expressions because each call creates a different temporary reference.

### Parameter initializers

Default parameter expressions must be simple and side-effect-free. Do not increment global state, expose shared mutable defaults, or perform I/O in a default. Prefer destructuring for more than a small number of optional parameters.

### Rest and spread

Use a rest parameter instead of `arguments`, and never name a parameter/local `arguments`. Use function spread instead of `Function.prototype.apply` where it preserves the call contract. Do not put a space after `...`.

### Formatting functions

Do not put blank lines at the start/end of a function body. Use a single internal blank line sparingly for logical groups. Write `function* foo()` and `yield* iter`; parentheses around a one-argument arrow parameter are recommended but optional.

## `this`

Use `this` only in class constructors/methods, functions with an explicit `this` type, or arrows nested in a scope where `this` is valid. Do not use it as a global/eval/event target or call/apply target without a clear receiver contract.

## Interfaces

Use interfaces when they express a structural object contract and are the clearest extension/implementation point. Consult the type-system reference for the guide's preference for interfaces over type-literal aliases in appropriate cases.

## Primitive literals and coercion

### Strings

Use single-quoted ordinary strings. Avoid backslash line continuations; use concatenated literals or a template literal. Use template literals for complex interpolation and multi-line strings.

### Numbers

Use lowercase `0x`, `0o`, and `0b` prefixes and do not add a leading zero to decimal numbers.

### Type coercion

Use `String()`, `Boolean()`, templates, or `!!` only where appropriate; never coerce enum values to booleans because the first numeric enum member is often falsy. Use `Number()` for numeric parsing and check `NaN`/finite behavior explicitly. Do not use unary `+`, `parseFloat`, or base-10 `parseInt` for general numeric parsing; `parseInt` is reserved for non-base-10 parsing after validating allowed digits.

### Implicit coercion

In `if`, `for`, and `while` conditions, do not write redundant `!!value`. Ordinary values may use implicit truthiness, but enum values must be compared explicitly against the relevant member/undefined.

## Control structures

Use braces and clear block structure according to the repository formatter. Keep assignments out of conditions unless the project has a documented pattern and the assignment is unmistakable. Prefer `for...of` for iterable values and filtered/object-key iteration rules above for objects.

### Grouping parentheses

Use parentheses to clarify precedence or a wrapped expression, not as a universal visual marker. Do not add redundant parentheses that make control flow harder to scan.

### Exception handling

- Instantiate errors with `new Error(...)` or an appropriate subclass.
- Throw only `Error` objects or subclasses, not strings/primitive values.
- Catch only when handling, translating, or rethrowing with added context; preserve the original cause where the runtime supports it.
- Do not leave empty catch blocks; if intentional, document why and make the suppression visible.
- Keep try blocks focused so unrelated failures are not hidden.

### Switch statements

Make cases exhaustive or provide an intentional default. Use explicit fallthrough comments where allowed by the linter. Do not rely on enum truthiness or accidental fallthrough for business logic.

### Equality checks

Prefer strict equality (`===`, `!==`) and follow the repository's nullish comparison policy. Use a broader comparison only when the coercion is deliberately part of the contract and documented.

### Type and non-nullability assertions

Prefer type narrowing and correct types over assertions. Use the `as` syntax, not angle-bracket assertions in TSX. Avoid double assertions; when unavoidable at a trusted boundary, document the invariant. Do not assert an object literal to bypass excess-property/type checks when the object can be typed correctly.

### Keep try blocks focused

Put only the operations expected to throw in a `try`; keep pure computation and unrelated calls outside so failures are not misclassified.

## Decorators and disallowed features

Do not define new decorators. Use only decorators supplied by an approved framework
(the upstream guide names Angular and Polymer), and put a decorator immediately
before the symbol it decorates with no empty line between them. JSDoc belongs before
the decorator. The guide discourages new decorators because the historical
implementation diverged from the TC39 proposal and has known bugs.

The disallowed features are specific requirements:

- Do not instantiate `String`, `Boolean`, or `Number` wrapper objects. Calling them
  as functions for coercion is allowed/preferred where appropriate.
- Do not rely on Automatic Semicolon Insertion; explicitly terminate statements.
- Do not use `const enum`; use plain `enum`.
- Do not include `debugger` statements in production code.
- Do not use `with`.
- Do not use `eval` or `Function(...string)`, except for code loaders.
- Do not use non-standard ECMAScript/Web Platform features, deprecated/removed
  features, unfinished TC39/WHATWG proposals, or non-standard transpiler
  extensions. Runtime-specific APIs are allowed only when the project explicitly
  targets that runtime; prefer a common abstraction when portability matters.
- Never modify built-in constructors/prototypes or depend on libraries that do so;
  do not add to the global object unless an external API absolutely requires it.
