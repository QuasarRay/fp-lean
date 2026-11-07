# Study guide: 4.7. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **4.7.1. Encoding Side Effects 🔗** — Lean is a pure functional language.
- **4.7.2. The Monad Type Class 🔗** — It's possible to write purely functional programs in languages that allow effects anywhere.
- **4.7.3. do -Notation for Monads 🔗** — Rather than being limited to IO , do -notation works for any monad.
- **4.7.4. Custom Monads 🔗** — Different languages provide different sets of side effects.
- **4.7.5. The IO Monad 🔗** — Programs that can affect the real world are written as IO actions in Lean.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←4.6. Additional Conveniences](Monads/Additional-Conveniences/#monads-conveniences "4.6. Additional Conveniences")[5. Functors, Applicative Functors, and Monads→](Functors___-Applicative-Functors___-and-Monads/#Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads "5. Functors, Applicative Functors, and Monads")

# 4.7. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=monads-summary "Permalink")

## 4.7.1. Encoding Side Effects[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--Summary--Encoding-Side-Effects "Permalink")

Lean is a pure functional language.
This means that it does not include side effects such as mutable variables, logging, or exceptions.
However, most side effects can be *encoded* using a combination of functions and inductive types or structures.
For example, mutable state can be encoded as a function from an initial state to a pair of a final state and a result, and exceptions can be encoded as an inductive type with constructors for successful termination and errors.

Each set of encoded effects is a type.
As a result, if a program uses these encoded effects, then this is apparent in its type.
Functional programming does not mean that programs can't use effects, it simply requires that they be *honest* about which effects they use.
A Lean type signature describes not only the types of arguments that a function expects and the type of result that it returns, but also which effects it may use.

## 4.7.2. The Monad Type Class[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--Summary--The-Monad-Type-Class "Permalink")

It's possible to write purely functional programs in languages that allow effects anywhere.
For example, `2 + 3` is a valid Python program that has no effects at all.
Similarly, combining programs that have effects requires a way to state the order in which the effects must occur.
It matters whether an exception is thrown before or after modifying a variable, after all.

The type class `Monad` captures these two important properties.
It has two methods: `pure` represents programs that have no effects, and `bind` sequences effectful programs.
The contract for `Monad` instances ensures that `bind` and `pure` actually capture pure computation and sequencing.

## 4.7.3. `do`-Notation for Monads[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--Summary--do--Notation-for-Monads "Permalink")

Rather than being limited to `IO`, `do`-notation works for any monad.
It allows programs that use monads to be written in a style that is reminiscent of statement-oriented languages, with statements sequenced after one another.
Additionally, `do`-notation enables a number of additional convenient shorthands, such as nested actions.
A program written with `do` is translated to applications of `>>=` behind the scenes.

## 4.7.4. Custom Monads[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--Summary--Custom-Monads "Permalink")

Different languages provide different sets of side effects.
While most languages feature mutable variables and file I/O, not all have features like exceptions.
Other languages offer effects that are rare or unique, like Icon's search-based program execution, Scheme and Ruby's continuations, and Common Lisp's resumable exceptions.
An advantage to encoding effects with monads is that programs are not limited to the set of effects that are provided by the language.
Because Lean is designed to make programming with any monad convenient, programmers are free to choose exactly the set of side effects that make sense for any given application.

## 4.7.5. The `IO` Monad[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--Summary--The--IO--Monad "Permalink")

Programs that can affect the real world are written as `IO` actions in Lean.
`IO` is one monad among many.
The `IO` monad encodes state and exceptions, with the state being used to keep track of the state of the world and the exceptions modeling failure and recovery.

[←4.6. Additional Conveniences](Monads/Additional-Conveniences/#monads-conveniences "4.6. Additional Conveniences")[5. Functors, Applicative Functors, and Monads→](Functors___-Applicative-Functors___-and-Monads/#Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads "5. Functors, Applicative Functors, and Monads")


> **Review needed:** The following headings have no short source sentence: 4.7. Summary 🔗