# Python language rules

Official section: [2 Python Language Rules](https://google.github.io/styleguide/pyguide.html#2_Python_Language_Rules).

The upstream guide uses a repeated Definition/Pros/Cons/Decision structure. The summaries below preserve the decision and its caveats without treating every rationale as a new prohibition.

## 2.1 Lint

Run `pylint` with the project's selected configuration; the upstream guide points to Google's `pylintrc`. Suppress a warning only when it is inappropriate, prefer the symbolic `pylint: disable` form, and explain a suppression when the symbolic name is not self-explanatory. Prefer deleting an unused argument with a reason comment when that is the local policy; `_`/`unused_` forms are allowed but can break callers using keyword arguments. Run the actual configured command—mentioning Pylint in this reference is not evidence that it ran.

## 2.2 Imports

Use imports for packages/modules rather than individual types, classes, or functions:

- `import x` for a package or module.
- `from x import y` when `x` is the package prefix and `y` is the module.
- `from x import y as z` for collisions, long/generic names, or a public parameter conflict.
- `import y as z` only for standard abbreviations such as `numpy as np`.

Use full package names, not relative imports, even inside the same package. The exemptions are symbols from `typing`, `collections.abc`, and `typing_extensions` when used for static analysis/type checking. Keep imports grouped and ordered according to the style rules below.

## 2.3 Packages

Import modules by their full package path so the source of a module is unambiguous and does not depend on `sys.path` accident. Do not assume the directory containing the main binary is on `sys.path`; `import jodie` should not be used to reach a sibling `jodie.py` when the full package path is available.

## 2.4 Exceptions

Exceptions are allowed but must be deliberate:

- Use built-in exception types when they fit, such as `ValueError` for a violated argument precondition.
- Do not use `assert` for application-critical validation; Python can remove assertions. Assertions are appropriate for pytest expectations and non-critical internal checks.
- Custom exceptions must inherit from an existing exception; names end in `Error` without redundant repetition.
- Never use bare `except:` or catch `Exception`/`StandardError` unless re-raising or intentionally creating an isolation boundary that records/suppresses failures (for example, protecting a thread's outermost block).
- Keep `try` blocks small so unrelated defects are not hidden.
- Use `finally` for cleanup that must happen whether or not an exception is raised.

## 2.5 Mutable Global State

Avoid mutable module-level or class-level state because it breaks encapsulation and can change module behavior at import time. If a rare design requires it, make the entity internal with a leading underscore, expose access through functions/methods when needed, and document why it is necessary. Module-level constants are allowed and should use all caps with underscores.

## 2.6 Nested/Local/Inner Classes and Functions

Nested functions/classes are fine when they close over a local value other than `self`/`cls` or implement a genuinely local abstraction. Do not nest merely to hide a helper from module users; use a module-level underscore name so tests can reach it. Remember nested definitions are harder to test directly and can make the outer function less readable.

## 2.7 Comprehensions & Generator Expressions

Use comprehensions and generator expressions for simple, readable transformations. Multiple `for` clauses or filter expressions are not permitted by the guide's decision; replace a complicated comprehension with explicit loops. Optimize for readability, not token count. Generator expressions can avoid an intermediate list.

## 2.8 Default Iterators and Operators

Use default iterators and membership operators: `for key in mapping`, `if item in values`, `for line in file`, and `mapping.items()`. Prefer iterator methods to methods that materialize lists, and never mutate a container while iterating over it. The direct operation is both generic and efficient.

## 2.9 Generators

Use generators when preserving iteration state or avoiding a full list improves the design. A generator retains local state until exhaustion/collection, so manage expensive resources explicitly; a context manager can force cleanup. Generator docstrings should use `Yields:` rather than `Returns:`.

## 2.10 Lambda Functions

Lambdas are allowed for one-liners. Prefer a generator expression to `map`/`filter` plus a lambda, and prefer `operator.mul`/similar named helpers for common operations. If the lambda is longer than roughly 60–80 characters or spans multiple lines, use a regular function.

## 2.11 Conditional Expressions

Use a conditional expression only when all three portions fit clearly on one line or a simple, readable wrapped form. Use a complete `if` statement when a portion is long or the condition is hard to locate.

## 2.12 Default Argument Values

Default values are evaluated once at definition/module-load time. They are fine when immutable and stable, but never use mutable objects such as lists/dicts or values whose load-time evaluation is surprising. Use `None` and initialize inside the function, or an immutable empty tuple where appropriate. Be careful with flags and timestamps that may not be initialized when the module loads.

## 2.13 Properties

Properties may wrap trivial computation or access control, but attribute access should remain cheap, unsurprising, and side-effect-free. Do not create a property merely to hide a plain field; use a public attribute or a real getter/setter design. Use `@property`, not a hand-built descriptor, and avoid properties for computations a subclass may need to extend.

## 2.14 True/False Evaluations

Prefer implicit truthiness for empty sequences/containers and ordinary predicates (`if users:`). Use `is None`/`is not None` for `None`, do not compare booleans with `== False`, and compare known integers explicitly when `None` could be confused with zero. Use explicit `.size` for NumPy arrays because their truthiness can raise. Remember that the string `'0'` is truthy.

## 2.15

The current upstream guide has no section numbered 2.15. Do not invent one or infer a rule from the numbering gap.

## 2.16 Lexical Scoping

Lexical scoping is allowed. Use it when it makes a closure clearer, but remember that assignments in an enclosing function affect whether a name is treated as local and can surprise readers. Do not introduce a closure solely to avoid a module-level testable helper.

## 2.17 Function and Method Decorators

Use decorators when they provide a clear advantage; test them and follow normal import/naming rules. Document that a decorator is a decorator. Avoid external file/socket/database dependencies in decorator execution because decorators run at definition/import time. Never use `staticmethod` unless an existing API forces it; use a module-level function instead. Use `classmethod` for named constructors or class-specific routines that modify necessary process-wide state.

## 2.18 Threading

Do not rely on apparent atomicity of built-in operations or assignment. Python implementations and user-defined `__hash__`/`__eq__` can invalidate that assumption. Use `queue.Queue` for thread communication; otherwise use `threading` primitives, favoring condition variables/`threading.Condition` over low-level locks where appropriate.

## 2.19 Power Features

Avoid custom metaclasses, bytecode access, on-the-fly compilation, dynamic inheritance/reparenting, import hacks, broad reflection, system-internal mutation, and custom `__del__` cleanup unless absolutely necessary. Standard-library facilities that use such mechanisms internally, such as `dataclasses`, `enum`, and `abc.ABCMeta`, remain allowed.

## 2.20 Modern Python: `from __future__` imports

Future imports are encouraged when they enable modern semantics per file and smooth interpreter upgrades. Keep them until the minimum supported runtime no longer needs them; in code supporting Python 3.5, the guide specifically calls out `from __future__ import generator_stop`. Check the project's actual runtime support before removing or adding one.

## 2.21 Type Annotated Code

Type annotations are strongly encouraged, especially on public APIs, with build-time checking such as `pytype`. Third-party/extension modules may use `.pyi` stubs. Keep annotations current; if a checker or inference issue blocks adoption, record a TODO/bug in code or build configuration rather than silently disabling analysis.
