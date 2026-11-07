# Study guide: 8.3. Arrays and Termination 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **8.3. Arrays and Termination 🔗** — To write efficient code, it is important to select appropriate data structures.
- **8.3.1. Inequality 🔗** — Because different types have different notions of ordering, inequality is governed by two type classes, called LE and LT .
- **8.3.1.1. Inductively-Defined Propositions, Predicates, and Relations 🔗** — Nat.le is an inductively-defined relation .
- **8.3.1.2. Inequality of Natural Numbers 🔗** — The definition of Nat.le has a parameter and an index:
- **8.3.2. Proving Termination 🔗** — The function Array.map transforms an array with a function, returning a new array that contains the result of applying the function to each element of the input array.
- **8.3.3. Exercises 🔗** — Implement a ForM m ( Array α ) instance on arrays using a tail-recursive accumulator-passing function and a termination_by clause.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←8.2. Proving Equivalence](Programming___-Proving___-and-Performance/Proving-Equivalence/#proving-tail-rec-equiv "8.2. Proving Equivalence")[8.4. More Inequalities→](Programming___-Proving___-and-Performance/More-Inequalities/#more-inequalities "8.4. More Inequalities")

# 8.3. Arrays and Termination[🔗](find/?domain=Verso.Genre.Manual.section&name=array-termination "Permalink")

To write efficient code, it is important to select appropriate data structures.
Linked lists have their place: in some applications, the ability to share the tails of lists is very important.
However, most use cases for a variable-length sequential collection of data are better served by arrays, which have both less memory overhead and better locality.

Arrays, however, have two drawbacks relative to lists:

1. Arrays are accessed through indexing, rather than by pattern matching, which imposes [proof obligations](Interlude___-Propositions___-Proofs___-and-Indexing/#props-proofs-indexing) in order to maintain safety.
2. A loop that processes an entire array from left to right is a tail-recursive function, but it does not have an argument that decreases on each call.

Making effective use of arrays requires knowing how to prove to Lean that an array index is in bounds, and how to prove that an array index that approaches the size of the array also causes the program to terminate.
Both of these are expressed using an inequality proposition, rather than propositional equality.

## 8.3.1. Inequality[🔗](find/?domain=Verso.Genre.Manual.section&name=inequality "Permalink")

Because different types have different notions of ordering, inequality is governed by two type classes, called `LE` and `LT`.
The table in the section on [standard type classes](Overloading-and-Type-Classes/Standard-Classes/#equality-and-ordering) describes how these classes relate to the syntax:

| Expression | Desugaring | Class Name |
| --- | --- | --- |
| `x < y` | `LT.lt x y` | `LT` |
| `x ≤ y` | `LE.le x y` | `LE` |
| `x > y` | `LT.lt y x` | `LT` |
| `x ≥ y` | `LE.le y x` | `LE` |

In other words, a type may customize the meaning of the `<` and `≤` operators, while `>` and `≥` derive their meanings from `<` and `≤`.
The classes `LT` and `LE` have methods that return propositions rather than `Bool`s:

`class LE (α : Type u) where
le : α → α → Prop
class LT (α : Type u) where
lt : α → α → Prop`

The instance of `LE` for `Nat` delegates to `Nat.le`:

`instance : LE Nat where
le := Nat.le`

Defining `Nat.le` requires a feature of Lean that has not yet been presented: it is an inductively-defined relation.

### 8.3.1.1. Inductively-Defined Propositions, Predicates, and Relations[🔗](find/?domain=Verso.Genre.Manual.section&name=inductive-props "Permalink")

`Nat.le` is an *inductively-defined relation*.
Just as `inductive` can be used to create new datatypes, it can be used to create new propositions.
When a proposition takes an argument, it is referred to as a *predicate* that may be true for some, but not all, potential arguments.
Propositions that take multiple arguments are called *relations*.

Each constructor of an inductively defined proposition is a way to prove it.
In other words, the declaration of the proposition describes the different forms of evidence that it is true.
A proposition with no arguments that has a single constructor can be quite easy to prove:

`inductive EasyToProve : Prop where
| heresTheProof : EasyToProve`

The proof consists of using its constructor:

`theorem fairlyEasy : EasyToProve := by⊢ EasyToProve
constructorAll goals completed! 🐙`

In fact, the proposition `True`, which should always be easy to prove, is defined just like `EasyToProve`:

`inductive True : Prop where
| intro : True`

Inductively-defined propositions that don't take arguments are not nearly as interesting as inductively-defined datatypes.
This is because data is interesting in its own right—the natural number `3` is different from the number `35`, and someone who has ordered 3 pizzas will be upset if 35 arrive at their door 30 minutes later.
The constructors of a proposition describe ways in which the proposition can be true, but once a proposition has been proved, there is no need to know *which* underlying constructors were used.
This is why most interesting inductively-defined types in the `Prop` universe take arguments.

The inductively-defined predicate `IsThree` states that its argument is three:

`inductive IsThree : Nat → Prop where
| isThree : IsThree 3`

The mechanism used here is just like [indexed families such as `HasCol`](Programming-with-Dependent-Types/Worked-Example___-Typed-Queries/#column-pointers), except the resulting type is a proposition that can be proved rather than data that can be used.

Using this predicate, it is possible to prove that three is indeed three:

`theorem three_is_three : IsThree 3 := by⊢ IsThree 3
constructorAll goals completed! 🐙`

Similarly, `IsFive` is a predicate that states that its argument is `5`:

`inductive IsFive : Nat → Prop where
| isFive : IsFive 5`

If a number is three, then the result of adding two to it should be five.
This can be expressed as a theorem statement:

`theorem three_plus_two_five : IsThree n → IsFive (n + 2) := unsolved goals
n:Nat⊢ IsThree n → IsFive (n + 2)byn:Nat⊢ IsThree n → IsFive (n + 2)
skipn:Nat⊢ IsThree n → IsFive (n + 2)`

The resulting goal has a function type:


```lean
unsolved goals
n:Nat⊢ IsThree n → IsFive (n + 2)
```


Thus, the `intro` tactic can be used to convert the argument into an assumption:

`theorem three_plus_two_five : IsThree n → IsFive (n + 2) := unsolved goals
n:Natthree:IsThree n⊢ IsFive (n + 2)byn:Nat⊢ IsThree n → IsFive (n + 2)
intro threen:Natthree:IsThree n⊢ IsFive (n + 2)`


```lean
unsolved goals
n:Natthree:IsThree n⊢ IsFive (n + 2)
```


Given the assumption that `n` is three, it should be possible to use the constructor of `IsFive` to complete the proof:

`` theorem three_plus_two_five : IsThree n → IsFive (n + 2) := byn:Nat⊢ IsThree n → IsFive (n + 2)
intro threen:Natthree:IsThree n⊢ IsFive (n + 2)
Tactic `constructor` failed: no applicable constructor found

n:Natthree:IsThree n⊢ IsFive (n + 2)constructorn:Natthree:IsThree n⊢ IsFive (n + 2) ``

However, this results in an error:


```lean
Tactic `constructor` failed: no applicable constructor found

n:Natthree:IsThree n⊢ IsFive (n + 2)
```


This error occurs because `n + 2` is not definitionally equal to `5`.
In an ordinary function definition, dependent pattern matching on the assumption `three` could be used to refine `n` to `3`.
The tactic equivalent of dependent pattern matching is `cases`, which has a syntax similar to that of `induction`:

`theorem three_plus_two_five : IsThree n → IsFive (n + 2) := byn:Nat⊢ IsThree n → IsFive (n + 2)
intro threen:Natthree:IsThree n⊢ IsFive (n + 2)
cases three with
| isThree unsolved goals
isThree⊢ IsFive (3 + 2)=> skipisThree⊢ IsFive (3 + 2)`

In the remaining case, `n` has been refined to `3`:


```lean
unsolved goals
isThree⊢ IsFive (3 + 2)
```


Because `3 + 2` is definitionally equal to `5`, the constructor is now applicable:

`theorem three_plus_two_five : IsThree n → IsFive (n + 2) := byn:Nat⊢ IsThree n → IsFive (n + 2)
intro threen:Natthree:IsThree n⊢ IsFive (n + 2)
cases three with
| isThree =>isThree⊢ IsFive (3 + 2) constructorAll goals completed! 🐙`

The standard false proposition `False` has no constructors, making it impossible to provide direct evidence for.
The only way to provide evidence for `False` is if an assumption is itself impossible, similarly to how `nomatch` can be used to mark code that the type system can see is unreachable.
As described in [the initial Interlude on proofs](Interlude___-Propositions___-Proofs___-and-Indexing/#connectives), the negation `Not A` is short for `A → False`.
`Not A` can also be written `¬A`.

It is not the case that four is three:

`theorem four_is_not_three : ¬ IsThree 4 := unsolved goals
⊢ ¬IsThree 4by⊢ ¬IsThree 4
skip⊢ ¬IsThree 4`

The initial proof goal contains `Not`:


```lean
unsolved goals
⊢ ¬IsThree 4
```


The fact that it's actually a function type can be exposed using `unfold`:

`theorem four_is_not_three : ¬ IsThree 4 := unsolved goals
⊢ IsThree 4 → Falseby⊢ ¬IsThree 4
unfold Not⊢ IsThree 4 → False`


```lean
unsolved goals
⊢ IsThree 4 → False
```


Because the goal is a function type, `intro` can be used to convert the argument into an assumption.
There is no need to keep `unfold`, as `intro` can unfold the definition of `Not` itself:

`theorem four_is_not_three : ¬ IsThree 4 := unsolved goals
h:IsThree 4⊢ Falseby⊢ ¬IsThree 4
intro hh:IsThree 4⊢ False`


```lean
unsolved goals
h:IsThree 4⊢ False
```


In this proof, the `cases` tactic solves the goal immediately:

`theorem four_is_not_three : ¬ IsThree 4 := by⊢ ¬IsThree 4
intro hh:IsThree 4⊢ False
cases hAll goals completed! 🐙`

Just as a pattern match on a `Vect String 2` doesn't need to include a case for `Vect.nil`, a proof by cases over `IsThree 4` doesn't need to include a case for `isThree`.

### 8.3.1.2. Inequality of Natural Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=inequality-of-natural-numbers "Permalink")

The definition of `Nat.le` has a parameter and an index:

`inductive Nat.le (n : Nat) : Nat → Prop
| refl : Nat.le n n
| step : Nat.le n m → Nat.le n (m + 1)`

The parameter `n` is the number that should be smaller, while the index is the number that should be greater than or equal to `n`.
The `refl` constructor is used when both numbers are equal, while the `step` constructor is used when the index is greater than `n`.

From the perspective of evidence, a proof that `n \leq k` consists of finding some number `d` such that `n + d = m`.
In Lean, the proof then consists of a `Nat.le.refl` constructor wrapped by `d` instances of `Nat.le.step`.
Each `step` constructor adds one to its index argument, so `d` `step` constructors adds `d` to the larger number.
For example, evidence that four is less than or equal to seven consists of three `step`s around a `refl`:

`theorem four_le_seven : 4 ≤ 7 :=
open Nat.le in
step (step (step refl))`

The strict less-than relation is defined by adding one to the number on the left:

`def Nat.lt (n m : Nat) : Prop :=
Nat.le (n + 1) m
instance : LT Nat where
lt := Nat.lt`

Evidence that four is strictly less than seven consists of two `step`'s around a `refl`:

`theorem four_lt_seven : 4 < 7 :=
open Nat.le in
step (step refl)`

This is because `4 < 7` is equivalent to `5 ≤ 7`.

## 8.3.2. Proving Termination[🔗](find/?domain=Verso.Genre.Manual.section&name=proving-termination "Permalink")

The function `Array.map` transforms an array with a function, returning a new array that contains the result of applying the function to each element of the input array.
Writing it as a tail-recursive function follows the usual pattern of delegating to a function that passes the output array in an accumulator.
The accumulator is initialized with an empty array.
The accumulator-passing helper function also takes an argument that tracks the current index into the array, which starts at `0`:

`def Array.map (f : α → β) (arr : Array α) : Array β :=
arrayMapHelper f arr Array.empty 0`

The helper should, at each iteration, check whether the index is still in bounds.
If so, it should loop again with the transformed element added to the end of the accumulator and the index incremented by `1`.
If not, then it should terminate and return the accumulator.
An initial implementation of this code fails because Lean is unable to prove that the array index is valid:

`` def arrayMapHelper (f : α → β) (arr : Array α)
(soFar : Array β) (i : Nat) : Array β :=
if i < arr.size then
arrayMapHelper f arr (soFar.push (f failed to prove index is valid, possible solutions:
 - Use `have`-expressions to prove the index is valid
 - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
 - Use `a[i]?` notation instead, result is an `Option` type
 - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
α:Type ?u.7β:Type ?u.9f:α → βarr:Array αsoFar:Array βi:Nat⊢ i < arr.sizearr[i])) (i + 1)
else soFar ``


```lean
failed to prove index is valid, possible solutions:
  - Use `have`-expressions to prove the index is valid
  - Use `a[i]!` notation instead, runtime check is performed, and 'Panic' error message is produced if index is not valid
  - Use `a[i]?` notation instead, result is an `Option` type
  - Use `a[i]'h` notation instead, where `h` is a proof that index is valid
α:Type ?u.7β:Type ?u.9f:α → βarr:Array αsoFar:Array βi:Nat⊢ i < arr.size
```


However, the conditional expression already checks the precise condition that the array index's validity demands (namely, `i < arr.size`).
Adding a name to the `if` resolves the issue, because it adds an assumption that the array indexing tactic can use:

`def arrayMapHelper (f : α → β) (arr : Array α)
(soFar : Array β) (i : Nat) : Array β :=
if inBounds : i < arr.size then
arrayMapHelper f arr (soFar.push (f arr[i])) (i + 1)
else soFar`

Lean accepts the modified program, even though the recursive call is not made on an argument to one of the input constructors.
In fact, both the accumulator and the index grow, rather than shrinking.

Behind the scenes, Lean's proof automation constructs a termination proof.
Reconstructing this proof can make it easier to understand the cases that Lean cannot automatically recognize.

Why does `arrayMapHelper` terminate?
Each iteration checks whether the index `i` is still in bounds for the array `arr`.
If so, `i` is incremented and the loop repeats.
If not, the program terminates.
Because `arr.size` is a finite number, `i` can be incremented only a finite number of times.
Even though no argument to the function decreases on each call, `arr.size - i` decreases toward zero.

The value that decreases at each recursive call is called a *measure*.
Lean can be instructed to use a specific expression as the measure of termination by providing a `termination_by` clause at the end of a definition.
For `arrayMapHelper`, the explicit measure looks like this:

`def arrayMapHelper (f : α → β) (arr : Array α)
(soFar : Array β) (i : Nat) : Array β :=
if inBounds : i < arr.size then
arrayMapHelper f arr (soFar.push (f arr[i])) (i + 1)
else soFar
termination_by arr.size - i`

A similar termination proof can be used to write `Array.find`, a function that finds the first element in an array that satisfies a Boolean function and returns both the element and its index:

`def Array.find (arr : Array α) (p : α → Bool) :
Option (Nat × α) :=
findHelper arr p 0`

Once again, the helper function terminates because `arr.size - i` decreases as `i` increases:

`def findHelper (arr : Array α) (p : α → Bool)
(i : Nat) : Option (Nat × α) :=
if h : i < arr.size then
let x := arr[i]
if p x then
some (i, x)
else findHelper arr p (i + 1)
else none`

Adding a question mark to `termination_by` (that is, using `termination_by?`) causes Lean to explicitly suggest the measure that it chose.
Clicking `[apply]` replaces `termination_by?` with the suggested measure:

`def findHelper (arr : Array α) (p : α → Bool)
(i : Nat) : Option (Nat × α) :=
if h : i < arr.size then
let x := arr[i]
if p x then
some (i, x)
else findHelper arr p (i + 1)
else none
Try this:
[apply] termination_by arr.size - itermination_by?`


```lean
Try this:
  [apply] termination_by arr.size - i
```


Not all termination arguments are as quite as simple as this one.
However, the basic structure of identifying some expression based on the function's arguments that will decrease in each call occurs in all termination proofs.
Sometimes, creativity can be required in order to figure out just why a function terminates, and sometimes Lean requires additional proofs in order to accept that the measure in fact decreases.

## 8.3.3. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=array-termination-exercises "Permalink")

- Implement a `ForM m (Array α)` instance on arrays using a tail-recursive accumulator-passing function and a `termination_by` clause.
- Reimplement `Array.map`, `Array.find`, and the `ForM` instance using `for``...` `in``...` loops in the identity monad and compare the resulting code.
- Reimplement array reversal using a `for``...` `in``...` loop in the identity monad. Compare it to the tail-recursive function.

[←8.2. Proving Equivalence](Programming___-Proving___-and-Performance/Proving-Equivalence/#proving-tail-rec-equiv "8.2. Proving Equivalence")[8.4. More Inequalities→](Programming___-Proving___-and-Performance/More-Inequalities/#more-inequalities "8.4. More Inequalities")
