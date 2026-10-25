# TypeScript source files, imports, exports, and modules

Official sections: [Source file basics](https://google.github.io/styleguide/tsguide.html#source-file-basics) and [Source file structure](https://google.github.io/styleguide/tsguide.html#source-file-structure).

## Introduction rules

The guide uses RFC 2119 terminology: `must`/`must not` are requirements; `should`/`should not` are recommendations; `may` is optional; `prefer`/`avoid` correspond to should/should not. Examples are non-normative illustrations and should not be treated as exhaustive formatting rules.

## File encoding: UTF-8

Use UTF-8 source files. Apart from line terminators, ASCII horizontal space (`0x20`) is the only literal whitespace character in source; escape other whitespace characters inside strings. Use named escape sequences such as `\n`, `\t`, and `\\` when available, not numeric equivalents. Use printable non-ASCII characters directly when they are readable; use an escape plus an explanatory comment for non-printable characters.

## Source file structure

Present sections, in order, as:

1. Copyright/license information.
2. Optional top-level `@fileoverview` JSDoc.
3. Imports.
4. Implementation.

Separate each present section with exactly one blank line.

### Copyright information

Put required copyright/license information in a top-of-file JSDoc. Follow the repository's actual license; do not copy a Google notice into unrelated code.

### `@fileoverview` JSDoc

Use a top-level `@fileoverview` block when a file's contents, uses, or dependencies need an overview. Wrap lines without extra indentation.

## Imports

Use the import form that matches the symbol and build semantics:

- Namespace import (`import * as foo`) for many symbols from a large API or to avoid common-name collisions.
- Named import (`import {Foo}`) for frequently used or clearly named symbols.
- Default import only when required by external code.
- Side-effect import only for an intentional load-time effect.

### Import paths

TypeScript imports must use paths to TypeScript code. Relative paths are preferred within the same logical project; limit excessive `../../../` depth. Rooted/base paths are allowed when the project defines that module mapping.

### Namespace versus named imports

Choose the form that makes call sites readable. Namespace imports avoid enormous aliased lists from large APIs; named imports make common functions such as `describe` and `expect` clear. Alias only to resolve collisions, generated names, or unclear context.

#### Special case: Apps JSPB protos

Apps JSPB protos must use named imports even when the line is long, supporting build performance and dead-code elimination.

### Renaming imports

Prefer a namespace import or a clearer exported name for collisions. An import alias is appropriate for a generated symbol, a collision, or a name whose context is unclear.

## Exports

Use named exports. Do not use default exports because they permit multiple local names for the same symbol and weaken maintenance/type errors. Export only symbols used outside the module and minimize module API surface.

### Export visibility

TypeScript exports are public to importers; the default is not a visibility mechanism. Keep implementation helpers unexported.

### Mutable exports

Do not use mutable `export let`. Re-exported mutation can be hard to reason about. If external code needs mutable state, expose an explicit getter or an object/service API with a clear contract. Ensure conditional exports are finalized after module initialization.

### Container classes

Do not create a class containing only static constants/functions for namespacing. Export file-level constants/functions instead; the module itself is the namespace.

## Import and export type

Use `import type` when a symbol is used only as a type, and `export type` for type-only re-exports. Use a regular import when runtime loading or side effects are required. The compiler can enforce the distinction in different transpilation modes, so follow the project's `isolatedModules`/build configuration.

## Use modules not namespaces

Use ES module imports/exports. Do not use `namespace`/old internal `module` constructs, `import x = require(...)`, or triple-slash reference paths in ordinary code. A namespace is allowed only when required to interface with external third-party code.
