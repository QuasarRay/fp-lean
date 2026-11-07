# Study guide: 7.6. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **7.6.1. Dependent Types 🔗** — Dependent types, where types contain non-type code such as function calls and ordinary data constructors, lead to a massive increase in the expressive power of a type system.
- **7.6.2. The Universe Pattern 🔗** — A common pattern when working with dependent types is to section off some subset of the type system.
- **7.6.3. Indexed Families 🔗** — Datatypes can take two separate kinds of arguments: parameters are identical in each constructor of the datatype, while indices may vary between constructors.
- **7.6.4. Definitional and Propositional Equality 🔗** — Lean's type checker must, from time to time, check whether two types should be considered interchangeable.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←7.5. Pitfalls of Programming with Dependent Types](Programming-with-Dependent-Types/Pitfalls-of-Programming-with-Dependent-Types/#dependent-type-pitfalls "7.5. Pitfalls of Programming with Dependent Types")[Interlude: Tactics, Induction, and Proofs→](Interlude___-Tactics___-Induction___-and-Proofs/#tactics-induction-proofs "Interlude: Tactics, Induction, and Proofs")

# 7.6. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=dependent-types-summary "Permalink")

## 7.6.1. Dependent Types[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming-with-Dependent-Types--Summary--Dependent-Types "Permalink")

Dependent types, where types contain non-type code such as function calls and ordinary data constructors, lead to a massive increase in the expressive power of a type system.
The ability to *compute* a type from the *value* of an argument means that the return type of a function can vary based on which argument is provided.
This can be used, for example, to have the result type of a database query depend on the database's schema and the specific query issued, without needing any potentially-failing cast operations on the result of the query.
When the query changes, so does the type that results from running it, enabling immediate compile-time feedback.

When a function's return type depends on a value, analyzing the value with pattern matching can result in the type being *refined*, as a variable that stands for a value is replaced by the constructors in the pattern.
The type signature of a function documents the way that the return type depends on the argument value, and pattern matching then explains how the return type can be fulfilled for each potential argument.

Ordinary code that occurs in types is run during type checking, though `partial` functions that might loop infinitely are not called.
Mostly, this computation follows the rules of ordinary evaluation that were introduced in [the very beginning of this book](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating), with expressions being progressively replaced by their values until a final value is found.
Computation during type checking has an important difference from run-time computation: some values in types may be *variables* whose values are not yet known.
In these cases, pattern-matching gets “stuck” and does not proceed until or unless a particular constructor is selected, e.g. by pattern matching.
Type-level computation can be seen as a kind of partial evaluation, where only the parts of the program that are sufficiently known need to be evaluated and other parts are left alone.

## 7.6.2. The Universe Pattern[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming-with-Dependent-Types--Summary--The-Universe-Pattern "Permalink")

A common pattern when working with dependent types is to section off some subset of the type system.
For example, a database query library might be able to return varying-length strings, fixed-length strings, or numbers in certain ranges, but it will never return a function, a user-defined datatype, or an `IO` action.
A domain-specific subset of the type system can be defined by first defining a datatype with constructors that match the structure of the desired types, and then defining a function that interprets values from this datatype into honest-to-goodness types.
The constructors are referred to as *codes* for the types in question, and the entire pattern is sometimes referred to as a *universe à la Tarski*, or just as a *universe* when context makes it clear that universes such as `Type 3` or `Prop` are not what's meant.

Custom universes are an alternative to defining a type class with instances for each type of interest.
Type classes are extensible, but extensibility is not always desired.
Defining a custom universe has a number of advantages over using the types directly:

- Generic operations that work for *any* type in the universe, such as equality testing and serialization, can be implemented by recursion on codes.
- The types accepted by external systems can be represented precisely, and the definition of the code datatype serves to document what can be expected.
- Lean's pattern matching completeness checker ensures that no codes are forgotten, while solutions based on type classes defer missing instance errors to client code.

## 7.6.3. Indexed Families[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming-with-Dependent-Types--Summary--Indexed-Families "Permalink")

Datatypes can take two separate kinds of arguments: *parameters* are identical in each constructor of the datatype, while *indices* may vary between constructors.
For a given choice of index, only some constructors of the datatype are available.
As an example, `Vect.nil` is available only when the length index is `0`, and `Vect.cons` is available only when the length index is `n+1` for some `n`.
While parameters are typically written as named arguments before the colon in a datatype declaration, and indices as arguments in a function type after the colon, Lean can infer when an argument after the colon is used as a parameter.

Indexed families allow the expression of complicated relationships between data, all checked by the compiler.
The datatype's invariants can be encoded directly, and there is no way to violate them, not even temporarily.
Informing the compiler about the datatype's invariants brings a major benefit: the compiler can now inform the programmer about what must be done to satisfy them.
The strategic use of compile-time errors, especially those resulting from underscores, can make it possible to offload some of the programming thought process to Lean, freeing up the programmer's mind to worry about other things.

Encoding invariants using indexed families can lead to difficulties.
First off, each invariant requires its own datatype, which then requires its own support libraries.
`List.zip` and `Vect.zip` are not interchangeable, after all.
This can lead to code duplication.
Secondly, convenient use of indexed families requires that the recursive structure of functions used in types match the recursive structure of the programs being type checked.
Programming with indexed families is the art of arranging for the right coincidences to occur.
While it's possible to work around missing coincidences with appeals to equality proofs, it is difficult, and it leads to programs littered with cryptic justifications.
Thirdly, running complicated code on large values during type checking can lead to compile-time slowdowns.
Avoiding these slowdowns for complicated programs can require specialized techniques.

## 7.6.4. Definitional and Propositional Equality[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming-with-Dependent-Types--Summary--Definitional-and-Propositional-Equality "Permalink")

Lean's type checker must, from time to time, check whether two types should be considered interchangeable.
Because types can contain arbitrary programs, it must therefore be able to check arbitrary programs for equality.
However, there is no efficient algorithm to check arbitrary programs for fully-general mathematical equality.
To work around this, Lean contains two notions of equality:

- *Definitional equality* is an underapproximation of equality that essentially checks for equality of syntactic representation modulo computation and renaming of bound variables. Lean automatically checks for definitional equality in situations where it is required.
- *Propositional equality* must be explicitly proved and explicitly invoked by the programmer. In return, Lean automatically checks that the proofs are valid and that the invocations accomplish the right goal.

The two notions of equality represent a division of labor between programmers and Lean itself.
Definitional equality is simple, but automatic, while propositional equality is manual, but expressive.
Propositional equality can be used to unstick otherwise-stuck programs in types.

However, the frequent use of propositional equality to unstick type-level computation is typically a code smell.
It typically means that coincidences were not well-engineered, and it's usually a better idea to either redesign the types and indices or to use a different technique to enforce the needed invariants.
When propositional equality is instead used to prove that a program meets a specification, or as part of a subtype, there is less reason to be suspicious.

[←7.5. Pitfalls of Programming with Dependent Types](Programming-with-Dependent-Types/Pitfalls-of-Programming-with-Dependent-Types/#dependent-type-pitfalls "7.5. Pitfalls of Programming with Dependent Types")[Interlude: Tactics, Induction, and Proofs→](Interlude___-Tactics___-Induction___-and-Proofs/#tactics-induction-proofs "Interlude: Tactics, Induction, and Proofs")


> **Review needed:** The following headings have no short source sentence: 7.6. Summary 🔗