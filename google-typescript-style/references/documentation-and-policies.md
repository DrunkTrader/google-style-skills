# TypeScript comments, documentation, and policies

Official sections: [Comments and documentation](https://google.github.io/styleguide/tsguide.html#comments-and-documentation) and [Policies](https://google.github.io/styleguide/tsguide.html#policies).

## Comments and documentation

### JSDoc versus comments

Use JSDoc for API/documentation consumed by tooling and ordinary comments for implementation rationale. Do not use JSDoc merely to repeat a self-evident name. A comment should explain intent, constraints, side effects, invariants, or a non-obvious workaround.

### Multi-line comments

Format multi-line comments consistently, keep them near the code they explain, and avoid stale narrative. Use the repository's formatter/linter for wrapping where configured.

### JSDoc general form

Use the project's JSDoc syntax and Markdown conventions. Keep the summary clear, then document parameters, returns, throws, type relationships, examples, deprecation, and side effects as needed.

### Markdown

Use valid, readable Markdown inside JSDoc. Keep code spans/fenced examples accurate and links useful. Do not include untrusted user input as if it were documentation or expose secrets in examples.

### JSDoc tags

Use tags supported by the repository's compiler/linter and place them in the conventional order. Avoid invented tags that tools will ignore. See the upstream guide for the complete tag list and examples.

### Line wrapping

Wrap documentation at the repository's configured width without changing code meaning. Keep `@fileoverview` and summary text easy to scan.

### Document all top-level exports of modules

Document exported classes, functions, constants, types, and interfaces when the project treats them as public API. A generated or framework-owned export may be exempt; preserve the boundary and record why.

### Class comments

Explain a public class's role, lifecycle, invariants, ownership, and thread/event behavior. Do not restate the word “class” or every method name.

### Method and function comments

Document behavior, parameter meaning, return values, thrown errors, side effects, and important preconditions. Prefer a clear type/name and code contract over a long comment that compensates for an opaque function.

### Parameter property comments

Use an `@param` tag for a constructor parameter property that needs documentation. Keep it consistent with the property visibility and public API.

### JSDoc type annotations

Prefer TypeScript syntax and compiler-checked types in `.ts` source. Use JSDoc type annotations only where the toolchain requires them (for example JS-with-checkJs) and keep them consistent with the compiler's interpretation.

### Make comments that actually add information

Explain why, not what the syntax obviously does. Include a link to the issue/design when a workaround or compatibility constraint is likely to be “cleaned up” later. Update or delete stale comments.

#### Comments when calling a function

Add a call-site comment when an argument is surprising, a side effect is intentional, a unit/ordering constraint is non-obvious, or a workaround is required. Prefer a named options object or stronger type when the explanation would otherwise be repeated.

### Place documentation prior to decorators

Put JSDoc immediately before the declaration and before decorators, so tools
associate the documentation with the intended class/member/function. Decorators
themselves must immediately precede the decorated symbol with no blank line.

## Policies

### Consistency

Consistency is a tie-breaker after correctness and project direction, not an excuse to preserve an obsolete convention forever. When reformatting existing code, limit changes to the requested scope unless the user explicitly asks for a broader migration. Avoid drive-by format-only edits in unrelated files.

### Deprecation

Use the repository's deprecation annotation/documentation convention. Explain the replacement, migration window, and compatibility constraints. Do not remove or rename a deprecated public export without the project's versioning/release process.

### Generated code: mostly exempt

Generated code is generally exempt from hand-authored style rules. Do not edit generated output to satisfy this skill; update the generator/template or add a narrowly scoped tool exception. Generated code should still be reviewed for correctness, security, licensing, and build behavior.

### Style guide goals

The guide's policies are intended to improve readability, consistency, and maintainability within Google's context. Apply them with project precedence, avoid large unrelated refactors, and identify when the repository's framework/build constraints require an exception.
