# Formatting and exceptions

Official sections: [Formatting](https://google.github.io/styleguide/cppguide.html#Formatting) and [Exceptions to the Rules](https://google.github.io/styleguide/cppguide.html#Exceptions_to_the_Rules).

## Formatting principles

Formatting should be consistent with the repository's formatter and neighboring code. Apply the following rules to new or touched code; do not use them as a reason to reformat unrelated files.

### Line Length

The guide favors a practical line limit rather than a strict universal number. Break long expressions at meaningful syntactic boundaries, keep indentation easy to follow, and prefer readable names over horizontal alignment. If the repository configures `clang-format`, use it rather than hand-inventing a competing layout.

### Non-ASCII Characters

Use non-ASCII characters only when the source encoding and readability make the intent clear. Escape non-printable characters and follow the project/toolchain policy for source encoding.

### Spaces vs. Tabs

Use spaces for indentation. Do not introduce tabs in C++ source unless a legacy file and formatter explicitly require them.

### Function Declarations and Definitions

Keep return type, function name, parameters, qualifiers, and braces in the repository's established layout. Put each parameter on its own line when wrapping improves readability. Keep declarations and definitions consistent about `const`, ref qualifiers, `noexcept`, and attributes.

### Lambda Expressions

Format lambdas so capture, parameters, return type, and body are easy to scan. A multi-line lambda should use ordinary block indentation. Do not line-break a short lambda merely to satisfy visual symmetry.

### Floating-point Literals

Make the type and precision clear (`1.0`, `1.0f` where relevant); do not use ambiguous leading/trailing-dot forms. Use separators only if the local formatter and compiler standard support them.

### Function Calls

Break calls at argument boundaries and align or indent according to the formatter. Do not align unrelated calls by inserting maintenance-heavy whitespace.

### Braced Initializer List Format

Use braces consistently with the type and local code. For multi-line initializers, put each element on its own line and make the closing brace easy to match. Do not obscure a narrowing conversion or a constructor choice merely for compactness.

### Looping and Branching Statements

Always use braces for multi-statement bodies. A single-line body may follow the local formatter policy, but adding braces is preferable when a future edit could otherwise change control flow. Keep `else`/`case` layout unambiguous and avoid surprising fallthrough.

### Pointer and Reference Expressions and Types

Use the repository's consistent `T*`/`T&` spacing and keep the declarator associated with the name. Do not let formatting hide whether a qualifier applies to the pointee or pointer.

### Boolean Expressions

Wrap long boolean expressions at logical operators in a way that preserves grouping. Use parentheses when they clarify precedence; do not add redundant parentheses everywhere.

### Return Values

Keep simple returns short. For multi-line return expressions, use a layout that makes the returned value obvious. Do not add temporary variables only to force a visual layout unless they improve naming or debugging.

### Variable and Array Initialization

Initialize variables at declaration. Use the form that makes construction, narrowing, and container contents clear. Prefer a fixed-size `std::array` or a project-approved abstraction when an array's size is part of the type.

### Preprocessor Directives

Place directives at the appropriate indentation/column for the project. Comment closing `#endif`s for nontrivial conditionals. Keep conditional compilation small and avoid hiding normal logic behind macros.

### Class Format

Keep access labels and declarations in predictable groups. Put a blank line between meaningful groups, not between every member. Do not use formatting as a substitute for a coherent public/private boundary.

### Constructor Initializer Lists

Initialize members in declaration order to avoid warnings and misleading readers. Format long initializer lists one member per line. Do not reorder members solely to match the initializer list; change declaration order only when the object layout/API impact is understood.

### Namespace Formatting

Do not indent the contents of a namespace solely because it is nested. Close the namespace with a comment identifying it; use the compact nested syntax only when it matches the codebase.

### Horizontal Whitespace

#### General

Use one space where the grammar and readability expect it. Avoid trailing whitespace and alignment columns that make later edits noisy.

#### Loops and Conditionals

Keep keywords, conditions, and braces visually distinct. Add parentheses when they make precedence or a non-obvious condition clearer.

#### Operators

Use spaces around binary operators and after commas; follow the local convention for unary operators and overloaded operators. Do not use whitespace to imply semantics the language does not have.

#### Templates and Casts

Format nested template arguments and named casts so their boundaries are visible. Prefer a named cast over a C-style cast; formatting cannot repair an unsafe conversion.

### Vertical Whitespace

Use blank lines to separate logical groups, not to create visual gaps between every statement. Keep related declarations and implementation steps together.

## Exceptions to the Rules

### Existing Non-conformant Code

Do not reformat legacy code merely because it is non-conformant. When touching a line, make the smallest style change needed for the task; a broader cleanup needs explicit scope, review, and tests.

### Windows Code

Windows/platform code may require different headers, macros, line endings, naming, or compiler constraints. Follow the platform and repository rules where they conflict with the general guide, isolate the exception, and avoid spreading platform-specific conventions into portable code.

## Review questions

- Did the change run the configured formatter, or is the formatting assessment manual?
- Is a reported difference required by the guide, recommended, generated-code/tooling policy, or merely a local preference?
- Does a formatting edit change macro expansion, overload selection, initialization order, ABI, or control flow?
- Is the code an existing exception boundary that should be preserved rather than “fixed” opportunistically?
