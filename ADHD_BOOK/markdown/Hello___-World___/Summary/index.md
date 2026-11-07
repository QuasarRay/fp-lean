# Study guide: 2.6. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **2.6.1. Evaluation vs Execution 🔗** — Side effects are aspects of program execution that go beyond the evaluation of mathematical expressions, such as reading files, throwing exceptions, or triggering industrial machinery.
- **2.6.2. do Notation 🔗** — The Lean standard library provides a number of basic IO actions that represent effects such as reading from and writing to files and interacting with standard input and standard output.
- **2.6.3. Compiling and Running Programs 🔗** — A Lean program that consists of a single file with a main definition can be run using lean --run FILE .
- **2.6.4. Partiality 🔗** — One consequence of following the mathematical model of expression evaluation is that every expression must have a value.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←2.5. Additional Conveniences](Hello___-World___/Additional-Conveniences/#hello-world-conveniences "2.5. Additional Conveniences")[Interlude: Propositions, Proofs, and Indexing→](Interlude___-Propositions___-Proofs___-and-Indexing/#props-proofs-indexing "Interlude: Propositions, Proofs, and Indexing")

# 2.6. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=hello-world-summary "Permalink")

## 2.6.1. Evaluation vs Execution[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Hello___-World___--Summary--Evaluation-vs-Execution "Permalink")

Side effects are aspects of program execution that go beyond the evaluation of mathematical expressions, such as reading files, throwing exceptions, or triggering industrial machinery.
While most languages allow side effects to occur during evaluation, Lean does not.
Instead, Lean has a type called `IO` that represents *descriptions* of programs that use side effects.
These descriptions are then executed by the language's run-time system, which invokes the Lean expression evaluator to carry out specific computations.
Values of type `IO α` are called *`IO` actions*.
The simplest is `pure`, which returns its argument and has no actual side effects.

`IO` actions can also be understood as functions that take the whole world as an argument and return a new world in which the side effect has occurred.
Behind the scenes, the `IO` library ensures that the world is never duplicated, created, or destroyed.
While this model of side effects cannot actually be implemented, as the whole universe is too big to fit in memory, the real world can be represented by a token that is passed around through the program.

An `IO` action `main` is executed when the program starts.
`main` can have one of three types:

- `main : IO Unit` is used for simple programs that cannot read their command-line arguments and always return exit code `0`,
- `main : IO UInt32` is used for programs without arguments that may signal success or failure, and
- `main : List String → IO UInt32` is used for programs that take command-line arguments and signal success or failure.

## 2.6.2. `do` Notation[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Hello___-World___--Summary--do--Notation "Permalink")

The Lean standard library provides a number of basic `IO` actions that represent effects such as reading from and writing to files and interacting with standard input and standard output.
These base `IO` actions are composed into larger `IO` actions using `do` notation, which is a built-in domain-specific language for writing descriptions of programs with side effects.
A `do` expression contains a sequence of *statements*, which may be:

- expressions that represent `IO` actions,
- ordinary local definitions with `let` and `:=`, where the defined name refers to the value of the provided expression, or
- local definitions with `let` and `←`, where the defined name refers to the result of executing the value of the provided expression.

`IO` actions that are written with `do` are executed one statement at a time.

Furthermore, `if` and `match` expressions that occur immediately under a `do` are implicitly considered to have their own `do` in each branch.
Inside of a `do` expression, *nested actions* are expressions with a left arrow immediately under parentheses.
The Lean compiler implicitly lifts them to the nearest enclosing `do`, which may be implicitly part of a branch of a `match` or `if` expression, and gives them a unique name.
This unique name then replaces the origin site of the nested action.

## 2.6.3. Compiling and Running Programs[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Hello___-World___--Summary--Compiling-and-Running-Programs "Permalink")

A Lean program that consists of a single file with a `main` definition can be run using `lean --run FILE`.
While this can be a nice way to get started with a simple program, most programs will eventually graduate to a multiple-file project that should be compiled before running.

Lean projects are organized into *packages*, which are collections of libraries and executables together with information about dependencies and a build configuration.
Packages are described using Lake, a Lean build tool.
Use `lake new` to create a Lake package in a new directory, or `lake init` to create one in the current directory.
Lake package configuration is another domain-specific language.
Use `lake build` to build a project.

## 2.6.4. Partiality[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Hello___-World___--Summary--Partiality "Permalink")

One consequence of following the mathematical model of expression evaluation is that every expression must have a value.
This rules out both incomplete pattern matches that fail to cover all constructors of a datatype and programs that can fall into an infinite loop.
Lean ensures that all `match` expressions cover all cases, and that all recursive functions are either structurally recursive or have an explicit proof of termination.

However, some real programs require the possibility of looping infinitely, because they handle potentially-infinite data, such as POSIX streams.
Lean provides an escape hatch: functions whose definition is marked `partial` are not required to terminate.
This comes at a cost.
Because types are a first-class part of the Lean language, functions can return types.
Partial functions, however, are not evaluated during type checking, because an infinite loop in a function could cause the type checker to enter an infinite loop.
Furthermore, mathematical proofs are unable to inspect the definitions of partial functions, which means that programs that use them are much less amenable to formal proof.

[←2.5. Additional Conveniences](Hello___-World___/Additional-Conveniences/#hello-world-conveniences "2.5. Additional Conveniences")[Interlude: Propositions, Proofs, and Indexing→](Interlude___-Propositions___-Proofs___-and-Indexing/#props-proofs-indexing "Interlude: Propositions, Proofs, and Indexing")


> **Review needed:** The following headings have no short source sentence: 2.6. Summary 🔗