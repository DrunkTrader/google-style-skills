# TypeScript naming and type system

Official sections: [Naming](https://google.github.io/styleguide/tsguide.html#naming) and [Type system](https://google.github.io/styleguide/tsguide.html#type-system).

## Naming

### Identifiers

Identifiers must use ASCII letters, digits, and underscores only for constants and
structured test method names, plus the `$` sign only rarely. Use names that are
descriptive, searchable, and consistent with TypeScript/JavaScript conventions.
The guide's rules are normative where it says “must”; examples are illustrative.

#### Naming style

Use `lowerCamelCase` for variables, parameters, functions, and properties;
`UpperCamelCase` for classes, interfaces, enums, and type names; and
`CONSTANT_CASE` for module-level constants when they are true constants. Do not
decorate names with type information. Do not use leading/trailing underscores to
simulate private visibility or an `opt_` prefix for optional parameters. Do not
mark interfaces with an `I` prefix or an `Interface` suffix unless the surrounding
environment has an established idiom. Use the repository's naming rules for
framework-required exceptions.

#### Descriptive names

Prefer a name that communicates the domain and avoids accidental ambiguity. A short local name is fine when scope and type make it obvious; public symbols need more context. Do not encode stale implementation details or use a name whose meaning depends on a hidden framework convention.

#### Camel case

Use camel case rather than underscores for ordinary identifiers. Preserve recognized acronyms according to local convention, but do not create inconsistent initialism capitalization within one API.

#### Dollar sign

Avoid `$` in ordinary identifiers unless a framework/generated API requires it.
An `Observable` suffix with `$` may be useful for distinguishing observable values
from concrete values, but the choice is team-local and must be consistent.

### Rules by identifier type

#### Type parameters

Use short, meaningful names such as `T` for broadly generic values and a descriptive name when the parameter has a specific role or constraint.

#### Test names

Use names that state the behavior/scenario under test and follow the test runner's discovery convention. Avoid names that merely repeat an implementation method.

#### `_` prefix/suffix

Use underscore prefixes/suffixes only for a documented convention, generated code, or framework boundary. Do not use them to simulate visibility when TypeScript modifiers or module scope can express the boundary.

#### Imports

Prefer names that preserve the source symbol's meaning; alias only for collision, generated names, or improved clarity. See [source files](source-files.md) for import form rules.

#### Constants

Use `CONSTANT_CASE` for module-level values that are immutable and conceptually constant. A `readonly` property is not necessarily a global constant; name it according to its class/API role.

#### Aliases

An alias should make a real concept or collision clearer. Do not create aliases that conceal a type's meaning or make a public API harder to search.

## Type inference

Prefer inference when the initializer makes the type obvious. Add an explicit type when it communicates a public contract, prevents a surprising widening/narrowing, documents an important boundary, or helps a checker. Return types should be explicit for exported/public functions when the repository's lint/build policy expects stable API signatures; small local functions may rely on inference when clear.

## Undefined and null

Model optionality explicitly. Use `undefined`/`null` according to the repository's strict-null and API convention, and avoid an alias that obscures which absence value callers must handle.

### Nullable/undefined type aliases

Use a named alias only when it represents a meaningful repeated concept. Do not hide nullable behavior behind an alias that makes a public API harder to read.

### Prefer optional over `|undefined`

For optional object properties/parameters, prefer `foo?: T` over `foo: T | undefined` when omission and explicit `undefined` have the same semantics. Use the union when the distinction matters or the project configuration requires it.

## Use structural types

TypeScript is structurally typed; use structural object types when the shape is the contract. Avoid nominal wrappers that add no invariant, but use a class/newtype-like boundary when runtime behavior or brand safety is important.

## Prefer interfaces over type literal aliases

Prefer an `interface` for an extendable object contract or public shape. Use a type alias for unions, mapped/conditional types, primitives, tuples, or a local non-extendable composition. Do not mechanically convert every alias to an interface.

## `Array<T>` type

Prefer `T[]` for simple array types and `Array<T>` when the generic form is necessary for nested/complex types or local readability. Follow the project's lint rule consistently.

## Indexable types / index signatures

Use an index signature only when arbitrary keys are part of the contract. Prefer `Map` or an explicit interface when keys/fields are known. Avoid `{[key: string]: T}` if it erases useful property information.

## Mapped and conditional types

Use them when they preserve a meaningful relationship and avoid duplicated types. Keep complex type transformations local/documented; do not use advanced types merely to demonstrate cleverness or make diagnostics unreadable.

## `any` type

Avoid `any`; it disables type checking and leaks uncertainty through the API. Prefer a more specific type, a generic, `unknown` with narrowing, or an explicit boundary adapter.

### Providing a more specific type

When a checker reports `any`, inspect the source boundary first: generated code, untyped dependency, JSON, or an unsafe cast. Add a real schema/type guard rather than sprinkling assertions.

### Using `unknown` over `any`

Use `unknown` for values whose type is not yet known; narrow before use. It preserves the obligation to validate.

### Suppressing `any` lint warnings

Suppress narrowly and explain why the boundary cannot be typed. Do not disable the rule for a file or project just to make a migration quiet.

## `{}` type

Avoid `{}` as a catch-all “non-nullish” type; it is usually not the intended empty object contract. Use `object`, `unknown`, a specific interface, or a generic constraint that matches the actual values.

## Tuple types

Use tuples for fixed-length, positionally meaningful values. Prefer named object fields when positions are easy to confuse or values have different semantics. Use readonly tuples when callers should not mutate the shape.

## Wrapper types

Do not use boxed primitive object types (`String`, `Boolean`, `Number`, `Object`) as types or constructors. Use primitive types and literals. See the disallowed-features guidance.

## Return type only generics

Avoid generic type parameters that appear only in a return type and cannot be inferred or constrained by inputs; they give callers a false impression of a relationship. Use a concrete return type or redesign the generic contract.
