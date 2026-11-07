# Study guide: 6.6. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **6.6.1. Combining Monads 🔗** — When writing a monad from scratch, there are design patterns that tend to describe the ways that each effect is added to the monad.
- **6.6.2. Type Classes for Effects 🔗** — A common design pattern is to implement a particular effect by defining a monad that has the effect, a monad transformer that adds it to another monad, and a type class that provides a generic interface to the effect.
- **6.6.3. Monad Transformers Don't Commute 🔗** — It is important to note that changing the order of transformers in a monad can change the meaning of programs that use the monad.
- **6.6.4. do -Notation for Monad Transformers 🔗** — Lean's do -blocks support early return, in which the block is terminated with some value, locally mutable variables, for -loops with break and continue , and single-branched if -statements.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←6.5. Additional Conveniences](Monad-Transformers/Additional-Conveniences/#monad-transformer-conveniences "6.5. Additional Conveniences")[7. Programming with Dependent Types→](Programming-with-Dependent-Types/#dependent-types "7. Programming with Dependent Types")

# 6.6. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-transformer-summary "Permalink")

## 6.6.1. Combining Monads[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monad-Transformers--Summary--Combining-Monads "Permalink")

When writing a monad from scratch, there are design patterns that tend to describe the ways that each effect is added to the monad.
Reader effects are added by having the monad's type be a function from the reader's environment, state effects are added by including a function from the initial state to the value paired with the final state, failure or exceptions are added by including a sum type in the return type, and logging or other output is added by including a product type in the return type.
Existing monads can be made part of the return type as well, allowing their effects to be included in the new monad.

These design patterns are made into a library of reusable software components by defining *monad transformers*, which add an effect to some base monad.
Monad transformers take the simpler monad types as arguments, returning the enhanced monad types.
At a minimum, a monad transformer should provide the following instances:

1. A `Monad` instance that assumes the inner type is already a monad
2. A `MonadLift` instance to translate an action from the inner monad to the transformed monad

Monad transformers may be implemented as polymorphic structures or inductive datatypes, but they are most often implemented as functions from the underlying monad type to the enhanced monad type.

## 6.6.2. Type Classes for Effects[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monad-Transformers--Summary--Type-Classes-for-Effects "Permalink")

A common design pattern is to implement a particular effect by defining a monad that has the effect, a monad transformer that adds it to another monad, and a type class that provides a generic interface to the effect.
This allows programs to be written that merely specify which effects they need, so the caller can provide any monad that has the right effects.

Sometimes, auxiliary type information (e.g. the state's type in a monad that provides state, or the exception's type in a monad that provides exceptions) is an output parameter, and sometimes it is not.
The output parameter is most useful for simple programs that use each kind of effect only once, but it risks having the type checker commit to a the wrong type too early when multiple instances of the same effect are used in a given program.
Thus, both versions are typically provided, with the ordinary-parameter version of the type class having a name that ends in `-Of`.

## 6.6.3. Monad Transformers Don't Commute[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monad-Transformers--Summary--Monad-Transformers-Don___t-Commute "Permalink")

It is important to note that changing the order of transformers in a monad can change the meaning of programs that use the monad.
For instance, re-ordering `StateT` and `ExceptT` can result either in programs that lose state modifications when exceptions are thrown or programs that keep changes.
While most imperative languages provide only the latter, the increased flexibility provided by monad transformers demands thought and attention to choose the correct variety for the task at hand.

## 6.6.4. `do`-Notation for Monad Transformers[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monad-Transformers--Summary--do--Notation-for-Monad-Transformers "Permalink")

Lean's `do`-blocks support early return, in which the block is terminated with some value, locally mutable variables, `for`-loops with `break` and `continue`, and single-branched `if`-statements.
While this may seem to be introducing imperative features that would get in the way of using Lean to write proofs, it is in fact nothing more than a more convenient syntax for certain common uses of monad transformers.
Behind the scenes, whatever monad the `do`-block is written in is transformed by appropriate uses of `ExceptT` and `StateT` to support these additional effects.

[←6.5. Additional Conveniences](Monad-Transformers/Additional-Conveniences/#monad-transformer-conveniences "6.5. Additional Conveniences")[7. Programming with Dependent Types→](Programming-with-Dependent-Types/#dependent-types "7. Programming with Dependent Types")


> **Review needed:** The following headings have no short source sentence: 6.6. Summary 🔗