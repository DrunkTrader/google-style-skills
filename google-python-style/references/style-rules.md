# Python formatting, resources, strings, and comments

Official sections: [3 Python Style Rules](https://google.github.io/styleguide/pyguide.html#3_Python_Style_Rules), especially sections 3.1–3.15.

## 3.1 Semicolons

Do not terminate lines with semicolons or place two statements on one line with a semicolon.

## 3.2 Line length

The normal maximum is 80 characters. Exceptions include long imports, URLs/pathnames/flags in comments, long no-whitespace module constants, and Pylint disable comments. Do not use explicit backslash continuation; use implicit joining inside parentheses, brackets, or braces. Break at the highest useful syntactic level and keep repeated breaks at the same level. A formatter such as Black/Pyink may justify an exception when it cannot reduce a line below the limit; docstring summary lines still stay within 80 characters.

## 3.3 Parentheses

Use parentheses sparingly. They are fine for tuples and implicit line joining, but do not write `if (x):`, `if not(x):`, or `return (foo)` when the parentheses add no meaning. A one-item tuple needs the comma, and a tuple return may use either a clear tuple form or the natural comma form.

## 3.4 Indentation

Indent with four spaces and never tabs. For implicit continuation, align with the opening delimiter or use a four-space hanging indent. Closing delimiters may be at the end of the final expression or on their own line aligned with the opening delimiter.

### 3.4.1 Trailing commas in sequences of items?

Use a trailing comma when the closing delimiter is on a different line from the final element, and for one-element tuples. This also gives Black/Pyink a signal to keep one item per line. Do not put the closing bracket on the same line as a trailing comma in a multi-line sequence.

## 3.5 Blank Lines

Use two blank lines between top-level class/function definitions and one blank line between methods. Leave no blank line immediately after a `def` line. Within functions, use single blank lines only to separate logical groups. A related leading comment can occupy the space before a definition.

## 3.6 Whitespace

- No whitespace inside parentheses, brackets, or braces.
- No space before comma/semicolon/colon; use a following space except at end of line.
- No space before an argument/indexing/slicing delimiter (`spam(1)`, `items[0]`).
- No trailing whitespace.
- Use one space around assignment, comparison, boolean, and appropriate arithmetic operators.
- Do not put spaces around `=` in keyword arguments or unannotated defaults; with an annotated default, use spaces around the `=`.
- Do not vertically align tokens across lines; that creates maintenance burden.

## 3.7 Shebang Line

Most `.py` files do not need a shebang. A directly executable program may use `#!/usr/bin/env python3` for virtualenv support or `#!/usr/bin/python3` per PEP 394. Imported modules normally omit it.

## 3.8 Comments and Docstrings

Use the appropriate docstring/comment form for modules, functions, methods, classes, and inline explanations. Comments should add information not apparent from the code.

### 3.8.1 Docstrings

Use triple double quotes. Start with a one-line summary under 80 characters ending in punctuation; add a blank line before a longer description. Document public behavior, arguments, returns/yields, exceptions, side effects, and examples where they help.

### 3.8.2 Modules

Files should carry the project's license boilerplate and a module docstring describing contents and usage. Test modules are exempt from a module docstring; test classes/methods under `unittest.TestCase` are also exempt when the name is self-explanatory, but retain docs for unusual setup or execution details.

### 3.8.3 Functions and Methods

Document behavior and contracts rather than repeating the function name. Include `Args:`, `Returns:`, `Yields:`, and `Raises:` sections as applicable. Do not promise a particular response to obvious API misuse unless that response is part of the stable contract.

#### 3.8.3.1 Overridden Methods

A child method with an `@override` decorator may rely on the base documentation when the docstring would be trivial. Without `@override`, provide a docstring unless the inherited contract is unambiguously sufficient under the project's tooling.

### 3.8.4 Classes

Document a class's purpose, public behavior, invariants, lifecycle, and important attributes. A class docstring need not restate obvious method names. Keep constructor/attribute documentation consistent with how users create and use the object.

### 3.8.5 Block and Inline Comments

Explain why, algorithmic invariants, non-obvious constraints, and deliberate workarounds. Do not narrate the code line by line or leave a comment that becomes false after refactoring. Prefer a clearer name or code structure when it removes the need for a comment.

### 3.8.6 Punctuation, Spelling, and Grammar

Use readable, correctly punctuated comments and diagnostics. Preserve code identifiers and technical names. Treat user-visible error text as product text, not just internal commentary.

## 3.10 Strings

Use an f-string, `%`, or `str.format()` for interpolation; a single `+` join is
fine, but do not build formatted strings by concatenating literals and converted
values with `+`. Do not accumulate a string with `+`/`+=` in a loop; append pieces
to a list and `''.join()` them or use `io.StringIO` for predictable linear
behavior. Choose one quote character consistently within a file, using the other
quote when it avoids escaping. Prefer `"""` for multi-line strings; docstrings
must use `"""` regardless. Use concatenated literals or `textwrap.dedent()` when
multi-line indentation would otherwise become part of the value.

### 3.10.1 Logging

For logging APIs whose first argument is a %-pattern, pass a string literal as the
pattern and values as subsequent arguments. This preserves lazy formatting and lets
logging systems index the unexpanded pattern. Include useful safe context and avoid
secrets/PII.

### 3.10.2 Error Messages

Error messages should precisely match the actual condition, make interpolated
values clearly identifiable, and be easy to process/search automatically. Include
safe context and recovery guidance when known; do not expose credentials or
sensitive data.

## 3.11 Files, Sockets, and similar Stateful Resources

Explicitly close files, sockets, database connections, mappings, figures, and other
stateful resources. Prefer `with` or `contextlib.closing()`; do not rely on
destructors, garbage collection, or process exit. If context management is
infeasible, document the resource lifetime clearly.

## 3.12 TODO Comments

Use `TODO` in all caps followed by a parenthesized context link/bug reference, a
colon, and an explanation, for example `TODO(issue): Investigate ...`. Avoid
assigning a TODO to an individual/team as the only context. If the TODO depends on
a future date or event, state a specific date/event that future maintainers can
understand.

## 3.13 Imports formatting

Put imports on separate lines, except the documented typing/`collections.abc`
exceptions. Place them after module comments/docstrings and before globals. Group
them from most generic to least generic: future imports, standard library,
third-party, then repository subpackages. Treat application-specific subpackage
imports like other subpackage imports in new code. Sort each group
lexicographically by full module path, ignoring case; optional blank lines may
separate groups.

## 3.14 Statements

Generally use one statement per line. A short `if` may put its body on the same line
when the complete statement fits and there is no `else`; do not use same-line
`try`/`except` or multi-clause one-liners. Keep statement-level behavior easy to
debug.

## 3.15 Getters and Setters

Use getter/setter functions when they provide meaningful behavior or when access
may be complex or costly. If a pair only reads/writes a field, make the field
public; use a property only for simple logic. Name accessors with the normal
`get_foo()`/`set_foo()` convention. If old code accessed a value as a property,
do not silently bind the new methods to that property—make the complexity change
visible to callers.
