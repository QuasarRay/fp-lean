# Study guide: 7.4. Indices, Parameters, and Universe Levels 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **7.4. Indices, Parameters, and Universe Levels 🔗** — The distinction between indices and parameters of an inductive type is more than just a way to describe arguments to the type that either vary or do not between the constructors.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←7.3. Worked Example: Typed Queries](Programming-with-Dependent-Types/Worked-Example___-Typed-Queries/#typed-queries "7.3. Worked Example: Typed Queries")[7.5. Pitfalls of Programming with Dependent Types→](Programming-with-Dependent-Types/Pitfalls-of-Programming-with-Dependent-Types/#dependent-type-pitfalls "7.5. Pitfalls of Programming with Dependent Types")

# 7.4. Indices, Parameters, and Universe Levels[🔗](find/?domain=Verso.Genre.Manual.section&name=indices-parameters-universe-levels "Permalink")

The distinction between indices and parameters of an inductive type is more than just a way to describe arguments to the type that either vary or do not between the constructors.
Whether an argument to an inductive type is a parameter or an index also matters when it comes time to determine the relationships between their universe levels.
In particular, an inductive type may have the same universe level as a parameter, but it must be in a larger universe than its indices.
This restriction is necessary to ensure that Lean can be used as a theorem prover as well as a programming language—without it, Lean's logic would be inconsistent.
Experimenting with error messages is a good way to illustrate these rules, as well as the precise rules that determine whether an argument to a type is a parameter or an index.

Generally speaking, the definition of an inductive type takes its parameters before a colon and its indices after the colon.
Parameters are given names like function arguments, whereas indices only have their types described.
This can be seen in the definition of `Vect`:

`inductive Vect (α : Type u) : Nat → Type u where
| nil : Vect α 0
| cons : α → Vect α n → Vect α (n + 1)`

In this definition, `α` is a parameter and the `Nat` is an index.
Parameters may be referred to throughout the definition (for example, `Vect.cons` uses `α` for the type of its first argument), but they must always be used consistently.
Because indices are expected to change, they are assigned individual values at each constructor, rather than being provided as arguments at the top of the datatype definition.

A very simple datatype with a parameter is `WithParameter`:

`inductive WithParameter (α : Type u) : Type u where
| test : α → WithParameter α`

The universe level `u` can be used for both the parameter and for the inductive type itself, illustrating that parameters do not increase the universe level of a datatype.
Similarly, when there are multiple parameters, the inductive type receives whichever universe level is greater:

`inductive WithTwoParameters (α : Type u) (β : Type v) : Type (max u v) where
| test : α → β → WithTwoParameters α β`

Because parameters do not increase the universe level of a datatype, they can be more convenient to work with.
Lean attempts to identify arguments that are described like indices (after the colon), but used like parameters, and turn them into parameters:
Both of the following inductive datatypes have their parameter written after the colon:

`inductive WithParameterAfterColon : Type u → Type u where
| test : α → WithParameterAfterColon α``inductive WithParameterAfterColon2 : Type u → Type u where
| test1 : α → WithParameterAfterColon2 α
| test2 : WithParameterAfterColon2 α`

When a parameter is not named in the initial datatype declaration, different names may be used for it in each constructor, so long as they are used consistently.
The following declaration is accepted:

`inductive WithParameterAfterColonDifferentNames : Type u → Type u where
| test1 : α → WithParameterAfterColonDifferentNames α
| test2 : β → WithParameterAfterColonDifferentNames β`

However, this flexibility does not extend to datatypes that explicitly declare the names of their parameters:

`` inductive WithParameterBeforeColonDifferentNames (α : Type u) : Type u where
| test1 : α → WithParameterBeforeColonDifferentNames α
Mismatched inductive type parameter in
WithParameterBeforeColonDifferentNames β
The provided argument
β
is not definitionally equal to the expected parameter
α

Note: The value of parameter `α` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.| test2 : β → WithParameterBeforeColonDifferentNames β ``


```lean
Mismatched inductive type parameter in
  WithParameterBeforeColonDifferentNames β
The provided argument
  β
is not definitionally equal to the expected parameter
  α

Note: The value of parameter `α` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.
```


Similarly, attempting to name an index results in an error:

`` inductive WithNamedIndex (α : Type u) : Type (u + 1) where
| test1 : WithNamedIndex α
Mismatched inductive type parameter in
WithNamedIndex (α × α)
The provided argument
α × α
is not definitionally equal to the expected parameter
α

Note: The value of parameter `α` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.| test2 : WithNamedIndex α → WithNamedIndex α → WithNamedIndex (α × α) ``


```lean
Mismatched inductive type parameter in
  WithNamedIndex (α × α)
The provided argument
  α × α
is not definitionally equal to the expected parameter
  α

Note: The value of parameter `α` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.
```


Using an appropriate universe level and placing the index after the colon results in a declaration that is acceptable:

`inductive WithIndex : Type u → Type (u + 1) where
| test1 : WithIndex α
| test2 : WithIndex α → WithIndex α → WithIndex (α × α)`

Even though Lean can sometimes determine that an argument after the colon in an inductive type declaration is a parameter when it is used consistently in all constructors, all parameters are still required to come before all indices.
Attempting to place a parameter after an index results in the argument being considered an index itself, which would require the universe level of the datatype to increase:

`` inductive ParamAfterIndex : Nat → Type u → Type u where
Invalid universe level in constructor `ParamAfterIndex.test1`: Parameter `γ` has type
Type u
at universe level
u + 2
which is not less than or equal to the inductive type's resulting universe level
u + 1| test1 : ParamAfterIndex 0 γ
| test2 : ParamAfterIndex n γ → ParamAfterIndex k γ → ParamAfterIndex (n + k) γ ``


```lean
Invalid universe level in constructor `ParamAfterIndex.test1`: Parameter `γ` has type
  Type u
at universe level
  u + 2
which is not less than or equal to the inductive type's resulting universe level
  u + 1
```


Parameters need not be types.
This example shows that ordinary datatypes such as `Nat` may be used as parameters:

`` inductive NatParam (n : Nat) : Nat → Type u where
Mismatched inductive type parameter in
NatParam 4 5
The provided argument
4
is not definitionally equal to the expected parameter
n

Note: The value of parameter `n` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.| five : NatParam 4 5 ``


```lean
Mismatched inductive type parameter in
  NatParam 4 5
The provided argument
  4
is not definitionally equal to the expected parameter
  n

Note: The value of parameter `n` must be fixed throughout the inductive declaration. Consider making this parameter an index if it must vary.
```


Using the `n` as suggested causes the declaration to be accepted:

`inductive NatParam (n : Nat) : Nat → Type u where
| five : NatParam n 5`

What can be concluded from these experiments?
The rules of parameters and indices are as follows:

1. Parameters must be used identically in each constructor's type.
2. All parameters must come before all indices.
3. The universe level of the datatype being defined must be at least as large as the largest parameter, and strictly larger than the largest index.
4. Named arguments written before the colon are always parameters, while arguments after the colon are typically indices. Lean may determine that the usage of arguments after the colon makes them into parameters if they are used consistently in all constructors and don't come after any indices.

When in doubt, the Lean command `#print` can be used to check how many of a datatype's arguments are parameters.
For example, for `Vect`, it points out that the number of parameters is 1:

`inductive Vect.{u} : Type u → Nat → Type u
number of parameters: 1
constructors:
Vect.nil : {α : Type u} → Vect α 0
Vect.cons : {α : Type u} → {n : Nat} → α → Vect α n → Vect α (n + 1)#print Vect`


```lean
inductive Vect.{u} : Type u → Nat → Type u
number of parameters: 1
constructors:
Vect.nil : {α : Type u} → Vect α 0
Vect.cons : {α : Type u} → {n : Nat} → α → Vect α n → Vect α (n + 1)
```


It is worth thinking about which arguments should be parameters and which should be indices when choosing the order of arguments to a datatype.
Having as many arguments as possible be parameters helps keep universe levels under control, which can make a complicated program easier to type check.
One way to make this possible is to ensure that all parameters come before all indices in the argument list.

Additionally, even though Lean is capable of determining that arguments after the colon are nonetheless parameters by their usage, it's a good idea to write parameters with explicit names.
This makes the intention clear to readers, and it causes Lean to report an error if the argument is mistakenly used inconsistently across the constructors.

[←7.3. Worked Example: Typed Queries](Programming-with-Dependent-Types/Worked-Example___-Typed-Queries/#typed-queries "7.3. Worked Example: Typed Queries")[7.5. Pitfalls of Programming with Dependent Types→](Programming-with-Dependent-Types/Pitfalls-of-Programming-with-Dependent-Types/#dependent-type-pitfalls "7.5. Pitfalls of Programming with Dependent Types")
