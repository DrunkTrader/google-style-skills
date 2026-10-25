# Python naming, program structure, and function size

Official sections: [3.16 Naming](https://google.github.io/styleguide/pyguide.html#3.16_Naming), [3.17 Main](https://google.github.io/styleguide/pyguide.html#3.17_Main), and [3.18 Function length](https://google.github.io/styleguide/pyguide.html#3.18_Function_length).

## 3.16 Naming

Names should be descriptive, searchable, and consistent with Python conventions. Avoid names that are misleading, too generic in a public API, or likely to collide with built-ins/framework vocabulary.

### 3.16.1 Names to Avoid

Avoid single-character names outside narrow loops/math, names that shadow built-ins or modules, generic names such as `foo`/`bar` in production APIs, and abbreviations that hide meaning. Do not use names that differ only by case or punctuation in a way that confuses readers.

### 3.16.2 Naming Conventions

Use:

- `lower_snake_case` for functions, methods, variables, parameters, and modules.
- `UpperCamelCase` for classes and exceptions.
- `CONSTANT_CASE` for constants.
- A leading underscore for internal module/class members, following the exact visibility semantics of Python.
- A trailing underscore when a meaningful name collides with a keyword (`class_`, `from_`) rather than adding arbitrary letters.

Use `self` and `cls` for the conventional instance/class receiver names. Keep acronyms readable rather than forcing inconsistent capitalization.

#### 3.16.2.1 Exemptions

External APIs, protocol-required names, framework callbacks, serialization fields, test fixtures, and mathematical notation can require exceptions. Keep them narrow, use a Pylint suppression when needed, and explain non-obvious exceptions.

### 3.16.3 File Naming

Use lowercase module/package filenames with underscores where needed, always with a
`.py` extension. Never use dashes in Python filenames. Test files should follow the
repository's discovery pattern. A filename change can affect imports, packaging,
and tooling; treat it as a compatibility change, not a cosmetic rename.

### 3.16.4 Guidelines derived from Guido's Recommendations

Prefer readable, conventional Python over clever compression. Use meaningful names, standard library idioms, and a consistent public/private boundary. Let the code's structure communicate intent before adding comments.

### 3.16.5 Mathematical Notation

Short conventional symbols are acceptable in tightly scoped mathematical code when the surrounding documentation defines them. Use descriptive names in general application code and public interfaces.

## 3.17 Main

Put executable program logic in a `main()` function and call it under `if __name__ == '__main__':`. Keep module import behavior side-effect-light so tools, tests, and other modules can import it safely. Define constants and declarations at module scope, but defer argument parsing, I/O, and process actions until the entry point.

## 3.18 Function length

Prefer focused functions that fit on one screen and have one coherent responsibility. The guide does not prescribe a magic line count; split when nesting, state, branching, or multiple phases make reasoning difficult. Do not extract artificial wrappers merely to reduce a line count, and preserve a clear local abstraction when a longer function is the most readable choice.

## Structural review questions

- Does the name communicate the domain concept and visibility?
- Could import-time execution surprise tests or tooling?
- Is a long function long because it contains one coherent algorithm, or because it mixes responsibilities?
- Is a naming exemption required by an external interface, and is it documented?
