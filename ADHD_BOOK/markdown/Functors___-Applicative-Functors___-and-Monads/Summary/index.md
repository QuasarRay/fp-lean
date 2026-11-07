# Study guide: 5.7. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **5.7.1. Type Classes and Structures 🔗** — Behind the scenes, type classes are represented by structures.
- **5.7.2. Structures and Inheritance 🔗** — Structures may inherit from other structures.
- **5.7.3. Applicative Functors 🔗** — An applicative functor is a functor with two additional operations:
- **5.7.4. Universes 🔗** — To allow Lean to be used as both a programming language and a theorem prover, some restrictions on the language are necessary.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←5.6. The Complete Definitions](Functors___-Applicative-Functors___-and-Monads/The-Complete-Definitions/#complete-definitions "5.6. The Complete Definitions")[6. Monad Transformers→](Monad-Transformers/#Functional-Programming-in-Lean--Monad-Transformers "6. Monad Transformers")

# 5.7. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=structure-applicative-monad-summary "Permalink")

## 5.7.1. Type Classes and Structures[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads--Summary--Type-Classes-and-Structures "Permalink")

Behind the scenes, type classes are represented by structures.
Defining a class defines a structure, and additionally creates an empty table of instances.
Defining an instance creates a value that either has the structure as its type or is a function that can return the structure, and additionally adds an entry to the table.
Instance search consists of constructing an instance by consulting the instance tables.
Both structures and classes may provide default values for fields (which are default implementations of methods).

## 5.7.2. Structures and Inheritance[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads--Summary--Structures-and-Inheritance "Permalink")

Structures may inherit from other structures.
Behind the scenes, a structure that inherits from another structure contains an instance of the original structure as a field.
In other words, inheritance is implemented with composition.
When multiple inheritance is used, only the unique fields from the additional parent structures are used to avoid a diamond problem, and the functions that would normally extract the parent value are instead organized to construct one.
Record dot notation takes structure inheritance into account.

Because type classes are just structures with some additional automation applied, all of these features are available in type classes.
Together with default methods, this can be used to create a fine-grained hierarchy of interfaces that nonetheless does not impose a large burden on clients, because the small classes that the large classes inherit from can be automatically implemented.

## 5.7.3. Applicative Functors[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads--Summary--Applicative-Functors "Permalink")

An applicative functor is a functor with two additional operations:

- `pure`, which is the same operator as that for `Monad`
- `seq`, which allows a function to be applied in the context of the functor.

While monads can represent arbitrary programs with control flow, applicative functors can only run function arguments from left to right.
Because they are less powerful, they provide less control to programs written against the interface, while the implementor of the method has a greater degree of freedom.
Some useful types can implement `Applicative` but not `Monad`.

In fact, the type classes `Functor`, `Applicative`, and `Monad` form a hierarchy of power.
Moving up the hierarchy, from `Functor` towards `Monad`, allows more powerful programs to be written, but fewer types implement the more powerful classes.
Polymorphic programs should be written to use as weak of an abstraction as possible, while datatypes should be given instances that are as powerful as possible.
This maximizes code re-use.
The more powerful type classes extend the less powerful ones, which means that an implementation of `Monad` provides implementations of `Functor` and `Applicative` for free.

Each class has a set of methods to be implemented and a corresponding contract that specifies additional rules for the methods.
Programs that are written against these interfaces expect that the additional rules are followed, and may be buggy if they are not.
The default implementations of `Functor`'s methods in terms of `Applicative`'s, and of `Applicative`'s in terms of `Monad`'s, will obey these rules.

## 5.7.4. Universes[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads--Summary--Universes "Permalink")

To allow Lean to be used as both a programming language and a theorem prover, some restrictions on the language are necessary.
This includes restrictions on recursive functions that ensure that they all either terminate or are marked as `partial` and written to return types that are not uninhabited.
Additionally, it must be impossible to represent certain kinds of logical paradoxes as types.

One of the restrictions that rules out certain paradoxes is that every type is assigned to a *universe*.
Universes are types such as `Prop`, `Type`, `Type 1`, `Type 2`, and so forth.
These types describe other types—just as `0` and `17` are described by `Nat`, `Nat` is itself described by `Type`, and `Type` is described by `Type 1`.
The type of functions that take a type as an argument must be a larger universe than the argument's universe.

Because each declared datatype has a universe, writing code that uses types like data would quickly become annoying, requiring each polymorphic type to be copy-pasted to take arguments from `Type 1`.
A feature called *universe polymorphism* allows Lean programs and datatypes to take universe levels as arguments, just as ordinary polymorphism allows programs to take types as arguments.
Generally speaking, Lean libraries should use universe polymorphism when implementing libraries of polymorphic operations.

[←5.6. The Complete Definitions](Functors___-Applicative-Functors___-and-Monads/The-Complete-Definitions/#complete-definitions "5.6. The Complete Definitions")[6. Monad Transformers→](Monad-Transformers/#Functional-Programming-in-Lean--Monad-Transformers "6. Monad Transformers")


> **Review needed:** The following headings have no short source sentence: 5.7. Summary 🔗