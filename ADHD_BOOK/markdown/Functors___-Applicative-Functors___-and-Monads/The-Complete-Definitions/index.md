# Study guide: 5.6. The Complete Definitions 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **5.6. The Complete Definitions 🔗** — Now that all the relevant language features have been presented, this section describes the complete, honest definitions of Functor , Applicative , and Monad as they occur in the Lean standard library.
- **5.6.1. Functor 🔗** — The complete definition of the Functor class makes use of universe polymorphism and a default method implementation:
- **5.6.2. Applicative 🔗** — The Applicative type class is actually built from a number of smaller classes that each contain some of the relevant methods.
- **5.6.3. Monad 🔗** — Just as the constituent operations of Applicative are split into their own type classes, Bind has its own class as well:
- **5.6.4. Exercises 🔗** — Understand the default implementations of map , seq , seqLeft , and seqRight in Monad by working through examples such as Option and Except .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←5.5. Universes](Functors___-Applicative-Functors___-and-Monads/Universes/#universe-levels "5.5. Universes")[5.7. Summary→](Functors___-Applicative-Functors___-and-Monads/Summary/#structure-applicative-monad-summary "5.7. Summary")

# 5.6. The Complete Definitions[🔗](find/?domain=Verso.Genre.Manual.section&name=complete-definitions "Permalink")

Now that all the relevant language features have been presented, this section describes the complete, honest definitions of `Functor`, `Applicative`, and `Monad` as they occur in the Lean standard library.
For the sake of understanding, no details are omitted.

## 5.6.1. Functor[🔗](find/?domain=Verso.Genre.Manual.section&name=complete-functor-definition "Permalink")

The complete definition of the `Functor` class makes use of universe polymorphism and a default method implementation:

`class Functor (f : Type u → Type v) : Type (max (u+1) v) where
map : {α β : Type u} → (α → β) → f α → f β
mapConst : {α β : Type u} → α → f β → f α :=
Function.comp map (Function.const _)`

In this definition, `Function.comp` is function composition, which is typically written with the `∘` operator.
`Function.const` is the *constant function*, which is a two-argument function that ignores its second argument.
Applying this function to only one argument produces a function that always returns the same value, which is useful when an API demands a function but a program doesn't need to compute different results for different arguments.
A simple version of `Function.const` can be written as follows:

`def simpleConst (x : α) (_ : β) : α := x`

Using it with one argument as the function argument to `List.map` demonstrates its utility:

`["same", "same", "same"]#eval [1, 2, 3].map (simpleConst "same")`


```lean
["same", "same", "same"]
```


The actual function has the following signature:


```lean
Function.const.{u, v} {α : Sort u} (β : Sort v) (a : α) : β → α
```


Here, the type argument `β` is an explicit argument, so the default definition of `mapConst` provides an `_` argument that instructs Lean to find a unique type to pass to `Function.const` that would cause the program to type check.
`Function.comp map (Function.const _)` is equivalent to `fun (x : α) (y : f β) => map (fun _ => x) y`.

The `Functor` type class inhabits a universe that is the greater of `u+1` and `v`.
Here, `u` is the level of universes accepted as arguments to `f`, while `v` is the universe returned by `f`.
To see why the structure that implements the `Functor` type class must be in a universe that's larger than `u`, begin with a simplified definition of the class:

`class Functor (f : Type u → Type v) : Type (max (u+1) v) where
map : {α β : Type u} → (α → β) → f α → f β`

This type class's structure type is equivalent to the following inductive type:

`inductive Functor (f : Type u → Type v) : Type (max (u+1) v) where
| mk : ({α β : Type u} → (α → β) → f α → f β) → Functor f`

The implementation of the `map` method that is passed as an argument to `mk` contains a function that takes two types in `Type u` as arguments.
This means that the type of the function itself is in `Type (u+1)`, so `Functor` must also be at a level that is at least `u+1`.
Similarly, other arguments to the function have a type built by applying `f`, so it must also have a level that is at least `v`.
All the type classes in this section share this property.

## 5.6.2. Applicative[🔗](find/?domain=Verso.Genre.Manual.section&name=complete-applicative-definition "Permalink")

The `Applicative` type class is actually built from a number of smaller classes that each contain some of the relevant methods.
The first are `Pure` and `Seq`, which contain `pure` and `seq` respectively:

`class Pure (f : Type u → Type v) : Type (max (u+1) v) where
pure {α : Type u} : α → f α``class Seq (f : Type u → Type v) : Type (max (u+1) v) where
seq : {α β : Type u} → f (α → β) → (Unit → f α) → f β`

In addition to these, `Applicative` also depends on `SeqRight` and an analogous `SeqLeft` class:

`class SeqRight (f : Type u → Type v) : Type (max (u+1) v) where
seqRight : {α β : Type u} → f α → (Unit → f β) → f β``class SeqLeft (f : Type u → Type v) : Type (max (u+1) v) where
seqLeft : {α β : Type u} → f α → (Unit → f β) → f α`

The `seqRight` function, which was introduced in the [section about alternatives and validation](Functors___-Applicative-Functors___-and-Monads/Alternatives/#alternative), is easiest to understand from the perspective of effects.
`E1 *> E2`, which desugars to `SeqRight.seqRight E1 (fun () => E2)`, can be understood as first executing `E1`, and then `E2`, resulting only in `E2`'s result.
Effects from `E1` may result in `E2` not being run, or being run multiple times.
Indeed, if `f` has a `Monad` instance, then `E1 *> E2` is equivalent to `do let _ ← E1; E2`, but `seqRight` can be used with types like `Validate` that are not monads.

Its cousin `seqLeft` is very similar, except the leftmost expression's value is returned.
`E1 <* E2` desugars to `SeqLeft.seqLeft E1 (fun () => E2)`.
`SeqLeft.seqLeft` has type `f α → (Unit → f β) → f α`, which is identical to that of `seqRight` except for the fact that it returns `f α`.
`E1 <* E2` can be understood as a program that first executes `E1`, and then `E2`, returning the original result for `E1`.
If `f` has a `Monad` instance, then `E1 <* E2` is equivalent to `do let x ← E1; _ ← E2; pure x`.
Generally speaking, `seqLeft` is useful for specifying extra conditions on a value in a validation or parser-like workflow without changing the value itself.

The definition of `Applicative` extends all these classes, along with `Functor`:

`class Applicative (f : Type u → Type v)
extends Functor f, Pure f, Seq f, SeqLeft f, SeqRight f where
map := fun x y => Seq.seq (pure x) fun _ => y
seqLeft := fun a b => Seq.seq (Functor.map (Function.const _) a) b
seqRight := fun a b => Seq.seq (Functor.map (Function.const _ id) a) b`

A complete definition of `Applicative` requires only definitions for `pure` and `seq`.
This is because there are default definitions for all of the methods from `Functor`, `SeqLeft`, and `SeqRight`.
The `mapConst` method of `Functor` has its own default implementation in terms of `Functor.map`.
These default implementations should only be overridden with new functions that are behaviorally equivalent, but more efficient.
The default implementations should be seen as specifications for correctness as well as automatically-created code.

The default implementation for `seqLeft` is very compact.
Replacing some of the names with their syntactic sugar or their definitions can provide another view on it, so:

`Seq.seq (Functor.map (Function.const _) a) b`

becomes

`fun a b => Seq.seq ((fun x _ => x) <$> a) b`

How should `(fun x _ => x) <$> a` be understood?
Here, `a` has type `f α`, and `f` is a functor.
If `f` is `List`, then `(fun x _ => x) <$> [1, 2, 3]` evaluates to `[fun _ => 1, fun _ => 2, fun _ => 3`.
If `f` is `Option`, then `(fun x _ => x) <$> some "hello"` evaluates to `some (fun _ => "hello")`.
In each case, the values in the functor are replaced by functions that return the original value, ignoring their argument.
When combined with `seq`, this function discards the values from `seq`'s second argument.

The default implementation for `seqRight` is very similar, except `Function.const` has an additional argument `id`.
This definition can be understood similarly, by first introducing some standard syntactic sugar and then replacing some names with their definitions:

`fun a b => Seq.seq (Functor.map (Function.const _ id) a) b``fun a b => Seq.seq ((fun _ => id) <$> a) b``fun a b => Seq.seq ((fun _ => fun x => x) <$> a) b``fun a b => Seq.seq ((fun _ x => x) <$> a) b`

How should `(fun _ x => x) <$> a` be understood?
Once again, examples are useful.
`fun _ x => x) <$> [1, 2, 3]` is equivalent to `[fun x => x, fun x => x, fun x => x]`, and `(fun _ x => x) <$> some "hello"` is equivalent to `some (fun x => x)`.
In other words, `(fun _ x => x) <$> a` preserves the overall shape of `a`, but each value is replaced by the identity function.
From the perspective of effects, the side effects of `a` occur, but the values are thrown out when it is used with `seq`.

## 5.6.3. Monad[🔗](find/?domain=Verso.Genre.Manual.section&name=complete-monad-definition "Permalink")

Just as the constituent operations of `Applicative` are split into their own type classes, `Bind` has its own class as well:

`class Bind (m : Type u → Type v) where
bind : {α β : Type u} → m α → (α → m β) → m β`

`Monad` extends `Applicative` with `Bind`:

`class Monad (m : Type u → Type v) : Type (max (u+1) v)
extends Applicative m, Bind m where
map f x := bind x (Function.comp pure f)
seq f x := bind f fun y => Functor.map y (x ())
seqLeft x y := bind x fun a => bind (y ()) (fun _ => pure a)
seqRight x y := bind x fun _ => y ()`

Tracing the collection of inherited methods and default methods from the entire hierarchy shows that a `Monad` instance requires only implementations of `bind` and `pure`.
In other words, `Monad` instances automatically yield implementations of `seq`, `seqLeft`, `seqRight`, `map`, and `mapConst`.
From the perspective of API boundaries, any type with a `Monad` instance gets instances for `Bind`, `Pure`, `Seq`, `Functor`, `SeqLeft`, and `SeqRight`.

## 5.6.4. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=complete-functor-applicative-monad-exercises "Permalink")

1. Understand the default implementations of `map`, `seq`, `seqLeft`, and `seqRight` in `Monad` by working through examples such as `Option` and `Except`. In other words, substitute their definitions for `bind` and `pure` into the default definitions, and simplify them to recover the versions `map`, `seq`, `seqLeft`, and `seqRight` that would be written by hand.
2. On paper or in a text file, prove to yourself that the default implementations of `map` and `seq` satisfy the contracts for `Functor` and `Applicative`. In this argument, you're allowed to use the rules from the `Monad` contract as well as ordinary expression evaluation.

[←5.5. Universes](Functors___-Applicative-Functors___-and-Monads/Universes/#universe-levels "5.5. Universes")[5.7. Summary→](Functors___-Applicative-Functors___-and-Monads/Summary/#structure-applicative-monad-summary "5.7. Summary")
