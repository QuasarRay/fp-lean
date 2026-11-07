# Study guide: 3.2. Type Classes and Polymorphism 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **3.2. Type Classes and Polymorphism 🔗** — It can be useful to write functions that work for any overloading of a given function.
- **3.2.1. Checking Polymorphic Functions' Types 🔗** — Checking the type of a function that takes implicit arguments or uses type classes requires the use of some additional syntax.
- **3.2.2. Defining Polymorphic Functions with Instance Implicits 🔗** — A function that sums all entries in a list needs two instances: Add allows the entries to be added, and an OfNat instance for 0 provides a sensible value to return for the empty list:
- **3.2.3. Methods and Implicit Arguments 🔗** — The type of OfNat.ofNat may be surprising.
- **3.2.4.1. Even Number Literals 🔗** — Write an instance of OfNat for the even number datatype from the previous section's exercises that uses recursive instance search.
- **3.2.4.2. Recursive Instance Search Depth 🔗** — There is a limit to how many times the Lean compiler will attempt a recursive instance search.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←3.1. Positive Numbers](Overloading-and-Type-Classes/Positive-Numbers/#positive-numbers "3.1. Positive Numbers")[3.3. Controlling Instance Search→](Overloading-and-Type-Classes/Controlling-Instance-Search/#out-params "3.3. Controlling Instance Search")

# 3.2. Type Classes and Polymorphism[🔗](find/?domain=Verso.Genre.Manual.section&name=tc-polymorphism "Permalink")

It can be useful to write functions that work for *any* overloading of a given function.
For example, `IO.println` works for any type that has an instance of `ToString`.
This is indicated using square brackets around the required instance: the type of `IO.println` is `{α : Type} → [ToString α] → α → IO Unit`.
This type says that `IO.println` accepts an argument of type `α`, which Lean should determine automatically, and that there must be a `ToString` instance available for `α`.
It returns an `IO` action.

## 3.2.1. Checking Polymorphic Functions' Types[🔗](find/?domain=Verso.Genre.Manual.section&name=checking-polymorphic-types "Permalink")

Checking the type of a function that takes implicit arguments or uses type classes requires the use of some additional syntax.
Simply writing

`IO.println : ?m.1 → IO Unit#check (IO.println)`

yields a type with metavariables:


```lean
IO.println : ?m.1 → IO Unit
```


This is because Lean does its best to discover implicit arguments, and the presence of metavariables indicates that it did not yet discover enough type information to do so.
To understand the signature of a function, this feature can be suppressed with an at-sign (`@`) before the function's name:

`@IO.println : {α : Type u_1} → [ToString α] → α → IO Unit#check @IO.println`


```lean
@IO.println : {α : Type u_1} → [ToString α] → α → IO Unit
```


There is a `u_1` after `Type`, which uses a feature of Lean that has not yet been introduced.
For now, ignore these parameters to `Type`.

## 3.2.2. Defining Polymorphic Functions with Instance Implicits[🔗](find/?domain=Verso.Genre.Manual.section&name=defining-polymorphic-functions-with-instance-implicits "Permalink")

A function that sums all entries in a list needs two instances: `Add` allows the entries to be added, and an `OfNat` instance for `0` provides a sensible value to return for the empty list:

`def List.sumOfContents [Add α] [OfNat α 0] : List α → α
| [] => 0
| x :: xs => x + xs.sumOfContents`

This function can be also defined with a `Zero α` requirement instead of `OfNat α 0`.
Both are equivalent, but `Zero α` can be easier to read:

`def List.sumOfContents [Add α] [Zero α] : List α → α
| [] => 0
| x :: xs => x + xs.sumOfContents`

This function can be used for a list of `Nat`s:

`def fourNats : List Nat := [1, 2, 3, 4]``10#eval fourNats.sumOfContents`


```lean
10
```


but not for a list of `Pos` numbers:

`def fourPos : List Pos := [1, 2, 3, 4]``` #eval failed to synthesize instance of type class
Zero Pos

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.fourPos.sumOfContents ``


```lean
failed to synthesize instance of type class
  Zero Pos

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


The Lean standard library includes this function, where it is called `List.sum`.

Specifications of required instances in square brackets are called *instance implicits*.
Behind the scenes, every type class defines a structure that has a field for each overloaded operation.
Instances are values of that structure type, with each field containing an implementation.
At a call site, Lean is responsible for finding an instance value to pass for each instance implicit argument.
The most important difference between ordinary implicit arguments and instance implicits is the strategy that Lean uses to find an argument value.
In the case of ordinary implicit arguments, Lean uses a technique called *unification* to find a single unique argument value that would allow the program to pass the type checker.
This process relies only on the specific types involved in the function's definition and the call site.
For instance implicits, Lean instead consults a built-in table of instance values.

Just as the `OfNat` instance for `Pos` took a natural number `n` as an automatic implicit argument, instances may also take instance implicit arguments themselves.
The [section on polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism) presented a polymorphic point type:

`structure PPoint (α : Type) where
x : α
y : α`

Addition of points should add the underlying `x` and `y` fields.
Thus, an `Add` instance for `PPoint` requires an `Add` instance for whatever type these fields have.
In other words, the `Add` instance for `PPoint` requires a further `Add` instance for `α`:

`instance [Add α] : Add (PPoint α) where
add p1 p2 := { x := p1.x + p2.x, y := p1.y + p2.y }`

When Lean encounters an addition of two points, it searches for and finds this instance.
It then performs a further search for the `Add α` instance.

The instance values that are constructed in this way are values of the type class's structure type.
A successful recursive instance search results in a structure value that has a reference to another structure value.
An instance of `Add (PPoint Nat)` contains a reference to the instance of `Add Nat` that was found.

This recursive search process means that type classes offer significantly more power than plain overloaded functions.
A library of polymorphic instances is a set of code building blocks that the compiler will assemble on its own, given nothing but the desired type.
Polymorphic functions that take instance arguments are latent requests to the type class mechanism to assemble helper functions behind the scenes.
The API's clients are freed from the burden of plumbing together all of the necessary parts by hand.

## 3.2.3. Methods and Implicit Arguments[🔗](find/?domain=Verso.Genre.Manual.section&name=method-implicit-params "Permalink")

The type of `OfNat.ofNat` may be surprising.
It is `: {α : Type} → (n : Nat) → [OfNat α n] → α`, in which the `Nat` argument `n` occurs as an explicit function parameter.
In the declaration of the method, however, `ofNat` simply has type `α`.
This seeming discrepancy is because declaring a type class really results in the following:

- A structure type to contain the implementation of each overloaded operation
- A namespace with the same name as the class
- For each method, a function in the class's namespace that retrieves its implementation from an instance

This is analogous to the way that declaring a new structure also declares accessor functions.
The primary difference is that a structure's accessors take the structure value as an explicit parameter, while the type class methods take the instance value as an instance implicit to be found automatically by Lean.

In order for Lean to find an instance, its parameters must be available.
This means that each parameter to the type class must be a parameter to the method that occurs before the instance.
It is most convenient when these parameters are implicit, because Lean does the work of discovering their values.
For example, `Add.add` has the type `{α : Type} → [Add α] → α → α → α`.
In this case, the type parameter `α` can be implicit because the arguments to `Add.add` provide information about which type the user intended.
This type can then be used to search for the `Add` instance.

In the case of `OfNat.ofNat`, however, the particular `Nat` literal to be decoded does not appear as part of any other parameter's type.
This means that Lean would have no information to use when attempting to figure out the implicit parameter `n`.
The result would be a very inconvenient API.
Thus, in these cases, Lean uses an explicit parameter for the class's method.

## 3.2.4. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=type-class-polymorphism-exercises "Permalink")

### 3.2.4.1. Even Number Literals[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Overloading-and-Type-Classes--Type-Classes-and-Polymorphism--Exercises--Even-Number-Literals "Permalink")

Write an instance of `OfNat` for the even number datatype from the [previous section's exercises](Overloading-and-Type-Classes/Positive-Numbers/#even-numbers-ex) that uses recursive instance search.

### 3.2.4.2. Recursive Instance Search Depth[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Overloading-and-Type-Classes--Type-Classes-and-Polymorphism--Exercises--Recursive-Instance-Search-Depth "Permalink")

There is a limit to how many times the Lean compiler will attempt a recursive instance search.
This places a limit on the size of even number literals defined in the previous exercise.
Experimentally determine what the limit is.

[←3.1. Positive Numbers](Overloading-and-Type-Classes/Positive-Numbers/#positive-numbers "3.1. Positive Numbers")[3.3. Controlling Instance Search→](Overloading-and-Type-Classes/Controlling-Instance-Search/#out-params "3.3. Controlling Instance Search")


> **Review needed:** The following headings have no short source sentence: 3.2.4. Exercises 🔗