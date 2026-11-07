# Study guide: Interlude: Propositions, Proofs, and Indexing 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **Interlude: Propositions, Proofs, and Indexing 🔗** — Like many languages, Lean uses square brackets for indexing into arrays and lists.
- **Propositions and Proofs 🔗** — A proposition is a statement that can be true or false.
- **Tactics 🔗** — Proofs are normally written using tactics , rather than by providing evidence directly.
- **Connectives 🔗** — The basic building blocks of logic, such as “and”, “or”, “true”, “false”, and “not”, are called logical connectives .
- **Evidence as Arguments 🔗** — In some cases, safely indexing into a list requires that the list have some minimum size, but the list itself is a variable rather than a concrete value.
- **Indexing Without Evidence 🔗** — In cases where it's not practical to prove that an indexing operation is in bounds, there are other alternatives.
- **Messages You May Meet 🔗** — In addition to proving that a statement is true, the decide tactic can also prove that it is false.
- **Exercises 🔗** — Prove the following theorems using rfl : 2 + 3 = 5 , 15 - 8 = 7 , "Hello, " .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←2.6. Summary](Hello___-World___/Summary/#hello-world-summary "2.6. Summary")[3. Overloading and Type Classes→](Overloading-and-Type-Classes/#type-classes "3. Overloading and Type Classes")

# Interlude: Propositions, Proofs, and Indexing[🔗](find/?domain=Verso.Genre.Manual.section&name=props-proofs-indexing "Permalink")

Like many languages, Lean uses square brackets for indexing into arrays and lists.
For instance, if `woodlandCritters` is defined as follows:

`def woodlandCritters : List String :=
["hedgehog", "deer", "snail"]`

then the individual components can be extracted:

`def hedgehog := woodlandCritters[0]
def deer := woodlandCritters[1]
def snail := woodlandCritters[2]`

However, attempting to extract the fourth element results in a compile-time error, rather than a run-time error:

`` def oops := failed to prove index is valid, possible solutions:
 - Use `have`-expressions to prove the index is valid
 - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
 - Use `a[i]?` notation instead, result is an `Option` type
 - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
⊢ 3 < woodlandCritters.lengthwoodlandCritters[3] ``


```lean
failed to prove index is valid, possible solutions:
  - Use `have`-expressions to prove the index is valid
  - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
  - Use `a[i]?` notation instead, result is an `Option` type
  - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
⊢ 3 < woodlandCritters.length
```


This error message is saying Lean tried to automatically mathematically prove that `3 < woodlandCritters.length` (i.e. `3 < List.length woodlandCritters`), which would mean that the lookup was safe, but that it could not do so.
Out-of-bounds errors are a common class of bugs, and Lean uses its dual nature as a programming language and a theorem prover to rule out as many as possible.

Understanding how this works requires an understanding of three key ideas: propositions, proofs, and tactics.

## Propositions and Proofs[🔗](find/?domain=Verso.Genre.Manual.section&name=propositions-and-proofs "Permalink")

A *proposition* is a statement that can be true or false.
All of the following English sentences are propositions:

- `1 + 1 = 2`
- Addition is commutative.
- There are infinitely many prime numbers.
- `1 + 1 = 15`
- Paris is the capital of France.
- Buenos Aires is the capital of South Korea.
- All birds can fly.

On the other hand, nonsense statements are not propositions.
Despite being grammatical, none of the following are propositions:

- 1 + green = ice cream
- All capital cities are prime numbers.
- At least one gorg is a fleep.

Propositions come in two varieties: those that are purely mathematical, relying only on our definitions of concepts, and those that are facts about the world.
Theorem provers like Lean are concerned with the former category, and have nothing to say about the flight capabilities of penguins or the legal status of cities.

A *proof* is a convincing argument that a proposition is true.
For mathematical propositions, these arguments make use of the definitions of the concepts that are involved as well as the rules of logical argumentation.
Most proofs are written for people to understand, and leave out many tedious details.
Computer-aided theorem provers like Lean are designed to allow mathematicians to write proofs while omitting many details, and it is the software's responsibility to fill in the missing explicit steps.
These steps can be mechanically checked.
This decreases the likelihood of oversights or mistakes.

In Lean, a program's type describes the ways it can be interacted with.
For instance, a program of type `Nat → List String` is a function that takes a `Nat` argument and produces a list of strings.
In other words, each type specifies what counts as a program with that type.

In Lean, propositions are in fact types.
They specify what counts as evidence that the statement is true.
The proposition is proved by providing this evidence, which is checked by Lean.
On the other hand, if the proposition is false, then it will be impossible to construct this evidence.

For example, the proposition `1 + 1 = 2` can be written directly in Lean.
The evidence for this proposition is the constructor `rfl`, which is short for *reflexivity*.
In mathematics, a relation is *reflexive* if every element is related to itself; this is a basic requirement in order to have a sensible notion of equality.
Because `1 + 1` computes to `2`, they are really the same thing:

`` Definition `onePlusOneIsTwo` is a proposition; use `theorem` instead of `def`

Note: This linter can be disabled with `set_option linter.defProp false`def onePlusOneIsTwo : 1 + 1 = 2 := rfl ``

On the other hand, `rfl` does not prove the false proposition `1 + 1 = 15`:

`def Not a definitional equality: the left-hand side
1 + 1
is not definitionally equal to the right-hand side
15onePlusOneIsFifteen : 1 + 1 = 15 := Type mismatch
rfl
has type
?m.16 = ?m.16
but is expected to have type
1 + 1 = 15rfl`


```lean
Type mismatch
  rfl
has type
  ?m.16 = ?m.16
but is expected to have type
  1 + 1 = 15
```


This error message indicates that `rfl` can prove that two expressions are equal when both sides of the equality statement are already the same number.
Because `1 + 1` evaluates directly to `2`, they are considered to be the same, which allows `onePlusOneIsTwo` to be accepted.
Just as `Type` describes types such as `Nat`, `String`, and `List (Nat × String × (Int → Float))` that represent data structures and functions, `Prop` describes propositions.

When a proposition has been proven, it is called a *theorem*.
In Lean, it is conventional to declare theorems with the `theorem` keyword instead of `def`.
This helps readers see which declarations are intended to be read as mathematical proofs, and which are definitions.
Generally speaking, with a proof, what matters is that there is evidence that a proposition is true, but it's not particularly important *which* evidence was provided.
With definitions, on the other hand, it matters very much which particular value is selected—after all, a definition of addition that always returns `0` is clearly wrong.
Because the details of a proof don't matter for later proofs, using the `theorem` keyword enables greater parallelism in the Lean compiler.

The prior example could be rewritten as follows:

`def OnePlusOneIsTwo : Prop := 1 + 1 = 2
theorem onePlusOneIsTwo : OnePlusOneIsTwo := rfl`

## Tactics[🔗](find/?domain=Verso.Genre.Manual.section&name=tactics "Permalink")

Proofs are normally written using *tactics*, rather than by providing evidence directly.
Tactics are small programs that construct evidence for a proposition.
These programs run in a *proof state* that tracks the statement that is to be proved (called the *goal*) along with the assumptions that are available to prove it.
Running a tactic on a goal results in a new proof state that contains new goals.
The proof is complete when all goals have been proven.

To write a proof with tactics, begin the definition with `by`.
Writing `by` puts Lean into tactic mode until the end of the next indented block.
While in tactic mode, Lean provides ongoing feedback about the current proof state.
Written with tactics, `onePlusOneIsTwo` is still quite short:

`theorem onePlusOneIsTwo : 1 + 1 = 2 := by⊢ 1 + 1 = 2
decideAll goals completed! 🐙`

The `decide` tactic invokes a *decision procedure*, which is a program that can check whether a statement is true or false, returning a suitable proof in either case.
It is primarily used when working with concrete values like `1` and `2`.
The other important tactics in this book are `simp`, short for “simplify,” and `grind`, which can automatically prove many theorems.

Tactics are useful for a number of reasons:

1. Many proofs are complicated and tedious when written out down to the smallest detail, and tactics can automate these uninteresting parts.
2. Proofs written with tactics are easier to maintain over time, because flexible automation can paper over small changes to definitions.
3. Because a single tactic can prove many different theorems, Lean can use tactics behind the scenes to free users from writing proofs by hand. For instance, an array lookup requires a proof that the index is in bounds, and a tactic can typically construct that proof without the user needing to worry about it.

Behind the scenes, indexing notation uses a tactic to prove that the user's lookup operation is safe.
This tactic takes many facts about arithmetic into account, combining them with any locally-known facts to attempt to prove that the index is in bounds.

The `simp` tactic is a workhorse of Lean proofs.
It rewrites the goal to as simple a form as possible.
In many cases, this rewriting simplifies the statement so much that it can be automatically proved.
Behind the scenes, a detailed formal proof is constructed, but using `simp` hides this complexity.

Like `decide`, the `grind` tactic is used to finish proofs.
It uses a collection of techniques from SMT solvers that can prove a wide variety of theorems.
Unlike `simp`, `grind` can never make progress towards a proof without completing it entirely; it either succeeds fully or fails.
The `grind` tactic is very powerful, customizable, and extensible; due to this power and flexibility, its output when it fails to prove a theorem contains a lot of information that can help trained Lean users diagnose the reason for the failure.
This can be overwhelming in the beginning, so this chapter uses only `decide` and `simp`.

## Connectives[🔗](find/?domain=Verso.Genre.Manual.section&name=connectives "Permalink")

The basic building blocks of logic, such as “and”, “or”, “true”, “false”, and “not”, are called *logical connectives*.
Each connective defines what counts as evidence of its truth.
For example, to prove a statement “*A* and *B*”, one must prove both *A* and *B*.
This means that evidence for “*A* and *B*” is a pair that contains both evidence for *A* and evidence for *B*.
Similarly, evidence for “*A* or *B*” consists of either evidence for *A* or evidence for *B*.

In particular, most of these connectives are defined like datatypes, and they have constructors.
If `A` and `B` are propositions, then “`A` and `B`” (written `A ∧ B`) is a proposition.
Evidence for `A ∧ B` consists of the constructor `And.intro`, which has the type `A → B → A ∧ B`.
Replacing `A` and `B` with concrete propositions, it is possible to prove `1 + 1 = 2 ∧ "Str".append "ing" = "String"` with `And.intro rfl rfl`.
Of course, `decide` is also powerful enough to find this proof:

`theorem addAndAppend : 1 + 1 = 2 ∧ "Str".append "ing" = "String" := by⊢ 1 + 1 = 2 ∧ "Str".append "ing" = "String"
decideAll goals completed! 🐙`

Similarly, “`A` or `B`” (written `A ∨ B`) has two constructors, because a proof of “`A` or `B`” requires only that one of the two underlying propositions be true.
There are two constructors: `Or.inl`, with type `A → A ∨ B`, and `Or.inr`, with type `B → A ∨ B`.

Implication (if `A` then `B`) is represented using functions.
In particular, a function that transforms evidence for `A` into evidence for `B` is itself evidence that `A` implies `B`.
This is different from the usual description of implication, in which `A → B` is shorthand for `¬A ∨ B`, but the two formulations are equivalent.

Because evidence for an “and” is a constructor, it can be used with pattern matching.
For instance, a proof that `A` and `B` implies `A` or `B` is a function that pulls the evidence of `A` (or of `B`) out of the evidence for `A` and `B`, and then uses this evidence to produce evidence of `A` or `B`:

`theorem andImpliesOr : A ∧ B → A ∨ B :=
fun andEvidence =>
match andEvidence with
| And.intro a b => Or.inl a`

| Connective | Lean Syntax | Evidence |
| --- | --- | --- |
| True | `True` | `True.intro : True` |
| False | `False` | No evidence |
| `A` and `B` | `A ∧ B` | `And.intro : A → B → A ∧ B` |
| `A` or `B` | `A ∨ B` | Either `Or.inl : A → A ∨ B` or `Or.inr : B → A ∨ B` |
| `A` implies `B` | `A → B` | A function that transforms evidence of `A` into evidence of `B` |
| not `A` | `¬A` | A function that would transform evidence of `A` into evidence of `False` |

The `decide` tactic can prove theorems that use these connectives.
For example:

`theorem onePlusOneOrLessThan : 1 + 1 = 2 ∨ 3 < 5 := by⊢ 1 + 1 = 2 ∨ 3 < 5 decideAll goals completed! 🐙
theorem notTwoEqualFive : ¬(1 + 1 = 5) := by⊢ ¬1 + 1 = 5 decideAll goals completed! 🐙
theorem trueIsTrue : True := by⊢ True decideAll goals completed! 🐙
theorem trueOrFalse : True ∨ False := by⊢ True ∨ False decideAll goals completed! 🐙
theorem falseImpliesTrue : False → True := by⊢ False → True decideAll goals completed! 🐙`

## Evidence as Arguments[🔗](find/?domain=Verso.Genre.Manual.section&name=evidence-passing "Permalink")

In some cases, safely indexing into a list requires that the list have some minimum size, but the list itself is a variable rather than a concrete value.
For this lookup to be safe, there must be some evidence that the list is long enough.
One of the easiest ways to make indexing safe is to have the function that performs a lookup into a data structure take the required evidence of safety as an argument.
For instance, a function that returns the third entry in a list is not generally safe because lists might contain zero, one, or two entries:

`` def third (xs : List α) : α := failed to prove index is valid, possible solutions:
 - Use `have`-expressions to prove the index is valid
 - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
 - Use `a[i]?` notation instead, result is an `Option` type
 - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
α:Type ?u.3xs:List α⊢ 2 < xs.lengthxs[2] ``


```lean
failed to prove index is valid, possible solutions:
  - Use `have`-expressions to prove the index is valid
  - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
  - Use `a[i]?` notation instead, result is an `Option` type
  - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
α:Type ?u.3xs:List α⊢ 2 < xs.length
```


However, the obligation to show that the list has at least three entries can be imposed on the caller by adding an argument that consists of evidence that the indexing operation is safe:

`def third (xs : List α) (ok : xs.length > 2) : α := xs[2]`

In this example, `xs.length > 2` is not a program that checks *whether* `xs` has more than 2 entries.
It is a proposition that could be true or false, and the argument `ok` must be evidence that it is true.

When the function is called on a concrete list, its length is known.
In these cases, `by decide` can construct the evidence automatically:

`"snail"#eval third woodlandCritters (by⊢ woodlandCritters.length > 2 decideAll goals completed! 🐙)`


```lean
"snail"
```


## Indexing Without Evidence[🔗](find/?domain=Verso.Genre.Manual.section&name=indexing-without-evidence "Permalink")

In cases where it's not practical to prove that an indexing operation is in bounds, there are other alternatives.
Adding a question mark results in an `Option`, where the result is `some` if the index is in bounds, and `none` otherwise.
For example:

`def thirdOption (xs : List α) : Option α := xs[2]?``some "snail"#eval thirdOption woodlandCritters`


```lean
some "snail"
```


`none#eval thirdOption ["only", "two"]`


```lean
none
```


There is also a version that crashes the program when the index is out of bounds, rather than returning an `Option`:

`"deer"#eval woodlandCritters[1]!`


```lean
"deer"
```


## Messages You May Meet[🔗](find/?domain=Verso.Genre.Manual.section&name=props-proofs-indexing-messages "Permalink")

In addition to proving that a statement is true, the `decide` tactic can also prove that it is false.
When asked to prove that a one-element list has more than two elements, it returns an error that indicates that the statement is indeed false:

`` #eval third ["rabbit"] (by⊢ ["rabbit"].length > 2 Tactic `decide` proved that the proposition
["rabbit"].length > 2
is falsedecide⊢ ["rabbit"].length > 2) ``


```lean
Tactic `decide` proved that the proposition
  ["rabbit"].length > 2
is false
```


The `simp` and `decide` tactics do not automatically unfold definitions with `def`.
Attempting to prove `OnePlusOneIsTwo` using `simp` fails:

`` theorem onePlusOneIsStillTwo : OnePlusOneIsTwo := by⊢ OnePlusOneIsTwo `simp` made no progresssimp⊢ OnePlusOneIsTwo ``

The error messages simply states that it could do nothing, because without unfolding `OnePlusOneIsTwo`, no progress can be made:


```lean
`simp` made no progress
```


Using `decide` also fails:

`` theorem onePlusOneIsStillTwo : OnePlusOneIsTwo := by⊢ OnePlusOneIsTwo failed to synthesize
Decidable OnePlusOneIsTwo

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.decide⊢ OnePlusOneIsTwo ``

This is also due to it not unfolding `OnePlusOneIsTwo`:


```lean
failed to synthesize
  Decidable OnePlusOneIsTwo

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
```


Defining `OnePlusOneIsTwo` with [`abbrev` fixes the problem](Getting-to-Know-Lean/Functions-and-Definitions/#abbrev-vs-def) by marking the definition for unfolding.

In addition to the error that occurs when Lean is unable to find compile-time evidence that an indexing operation is safe, polymorphic functions that use unsafe indexing may produce the following message:

`` def unsafeThird (xs : List α) : α := failed to synthesize instance of type class
Inhabited α

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.xs[2]! ``


```lean
failed to synthesize instance of type class
  Inhabited α

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


This is due to a technical restriction that is part of keeping Lean usable as both a logic for proving theorems and a programming language.
In particular, only programs whose types contain at least one value are allowed to crash.
This is because a proposition in Lean is a kind of type that classifies evidence of its truth.
False propositions have no such evidence.
If a program with an empty type could crash, then that crashing program could be used as a kind of fake evidence for a false proposition.

Internally, Lean contains a table of types that are known to have at least one value.
This error is saying that some arbitrary type `α` is not necessarily in that table.
The next chapter describes how to add to this table, and how to successfully write functions like `unsafeThird`.

Adding whitespace between a list and the brackets used for lookup can cause another message:

`#eval Function expected at
woodlandCritters
but this term has type
List String

Note: Expected a function because this term is being applied to the argument
[1]woodlandCritters [1]`


```lean
Function expected at
  woodlandCritters
but this term has type
  List String

Note: Expected a function because this term is being applied to the argument
  [1]
```


Adding a space causes Lean to treat the expression as a function application, and the index as a list that contains a single number.
This error message results from having Lean attempt to treat `woodlandCritters` as a function.

### Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=props-proofs-indexing-exercises "Permalink")

- Prove the following theorems using `rfl`: `2 + 3 = 5`, `15 - 8 = 7`, `"Hello, ".append "world" = "Hello, world"`. What happens if `rfl` is used to prove `5 < 18`? Why?
- Prove the following theorems using `by decide`: `2 + 3 = 5`, `15 - 8 = 7`, `"Hello, ".append "world" = "Hello, world"`, `5 < 18`.
- Write a function that looks up the fifth entry in a list. Pass the evidence that this lookup is safe as an argument to the function.

[←2.6. Summary](Hello___-World___/Summary/#hello-world-summary "2.6. Summary")[3. Overloading and Type Classes→](Overloading-and-Type-Classes/#type-classes "3. Overloading and Type Classes")
