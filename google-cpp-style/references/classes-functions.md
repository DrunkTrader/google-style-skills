# Classes and functions

Official sections: [Classes](https://google.github.io/styleguide/cppguide.html#Classes) and [Functions](https://google.github.io/styleguide/cppguide.html#Functions).

## Classes

### Doing Work in Constructors

Constructors should not call virtual functions. Avoid constructor work that can fail when there is no safe way to report the failure: use a factory or an explicit initialization operation only when the object genuinely has a meaningful partially initialized state. Termination can be appropriate for an unrecoverable invariant, but do not hide recoverable failure in a constructor.

### Implicit Conversions

Conversion operators and constructors callable with one argument must be `explicit`. Copy and move constructors are the exception. Constructors with more than one required argument need not be explicit; a single `std::initializer_list` constructor is normally left non-explicit to preserve copy-list initialization. Request a project waiver for a type intentionally designed to be interchangeable with another type.

The goal is to make conversions visible at the call site and avoid overload ambiguity or accidental type-mismatch behavior.

### Copyable and Movable Types

Make the public API clear about whether a type is copyable, move-only, or neither. Support copy and/or move when the operation is meaningful and unsurprising. If a type owns a resource or has identity, disable the operations explicitly rather than letting an accidental compiler-generated operation decide the contract. Prefer the standard copy/move operations over ad-hoc `Clone`, `CopyFrom`, or `Swap` APIs when their semantics fit.

If copy or move is supported, ensure all members and bases have coherent semantics. Avoid adding a custom destructor or custom copy/move implementation without checking the resulting special-member behavior.

### Structs vs. Classes

Use a `struct` for passive data with related fields and no invariant or behavior beyond direct access. Use a `class` when invariants, encapsulation, or behavior matter. These are conventions, not a substitute for documenting a type's contract.

### Structs vs. Pairs and Tuples

Prefer a named struct when elements have meaningful names or the value may grow. `std::pair`/tuple fields such as `.first` and `.second` are acceptable for narrow, local utility values where the positions are obvious.

### Inheritance

Use inheritance only when the derived type genuinely satisfies the base abstraction and the base contract supports substitution. Prefer composition when code reuse is the only reason. Multiple inheritance is permitted for a narrow interface/mixin-style use or a well-understood implementation design; avoid multiple concrete implementation bases. Make virtual destructors and overrides explicit where required by the ownership and polymorphism contract.

### Operator Overloading

Overload operators only when the meaning is unsurprising and close to the operator's conventional semantics. Do not overload an operator merely to make a non-mathematical operation shorter. Preserve expected algebraic, comparison, ownership, and ordering behavior, and ensure the overload is discoverable near the type.

### Access Control

Make data members private unless the type is a simple data carrier. Put public API first, then protected/private implementation details as appropriate. Do not use `friend` or inheritance to bypass a clearer interface; if a friendship is necessary, keep it narrow and document why.

### Declaration Order

Keep declarations in a predictable order: public types and constants, constructors/destructor, public methods, protected API, private methods, then data members, following local project convention. Within each group, use a logical order and keep related declarations together. Do not treat this as a reason to reorder an unrelated legacy class.

## Functions

### Inputs and Outputs

Prefer clear value semantics for small, cheap types. For input parameters, use the simplest type that states ownership, lifetime, mutability, and optionality. Avoid output parameters when a return value or a small result type is clearer. A function that takes ownership should make the transfer visible, typically with a smart pointer or value move; a borrowed parameter should not imply ownership.

Order parameters consistently within an API, especially when input and output or related values could otherwise be confused. Make nullable, optional, and non-null requirements explicit in the type or documentation.

### Write Short Functions

Keep functions focused and readable. If a function needs a long explanation, deep nesting, many flags, or several independent phases, consider extracting a cohesive helper, but do not split code into artificial one-line wrappers. A short function is not a correctness requirement; clarity and a stable interface matter more than an arbitrary line count.

### Function Overloading

Overload when the operations have the same semantic meaning and differ only in natural parameter types or a small, obvious variation. Avoid overload sets that make calls ambiguous or hide expensive behavior. Prefer a named function when the operations are conceptually different.

### Default Arguments

Avoid default arguments in virtual functions and public APIs where changing a default silently changes callers compiled against a different declaration. Prefer overloads or an options type when defaults need documentation, vary by call context, or are part of an evolving interface. Default arguments can be reasonable for stable, non-virtual, local APIs; keep the default at the declaration visible to callers.

### Trailing Return Type Syntax

Use trailing return syntax when it makes dependent types, lambdas, or complex declarations clearer. Do not use it as a blanket replacement for ordinary return syntax when the leading return type is easier to read.

## Class/function review questions

- Does the type's copy/move and ownership contract follow from its public API?
- Can a constructor fail, call virtual behavior, or leave an object in a state callers can misuse?
- Is a free function being wrapped in a static-only class without a real reason?
- Does an overload/default argument make a call ambiguous or obscure cost/ownership?
- Would a named type or parameter make a call site safer than a pair, tuple, bool, or output parameter?
