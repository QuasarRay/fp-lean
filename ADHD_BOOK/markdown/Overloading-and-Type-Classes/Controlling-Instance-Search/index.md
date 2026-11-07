# Study guide: 3.3. Controlling Instance Search 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **3.3. Controlling Instance Search 🔗** — An instance of the Add class is sufficient to allow two expressions with type Pos to be conveniently added, producing another Pos .
- **3.3.1. Heterogeneous Overloadings 🔗** — As mentioned in the section on overloaded addition , Lean provides a type class called HAdd for overloading addition heterogeneously.
- **3.3.2. Output Parameters 🔗** — This problem can also be solved by declaring γ to be an output parameter .
- **3.3.3. Default Instances 🔗** — Deciding whether a parameter is an input or an output controls the circumstances under which Lean will initiate type class search.
- **3.3.4. Exercises 🔗** — Define an instance of HMul ( PPoint α ) α ( PPoint α ) that multiplies both projections by the scalar.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←3.2. Type Classes and Polymorphism](Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/#tc-polymorphism "3.2. Type Classes and Polymorphism")[3.4. Arrays and Indexing→](Overloading-and-Type-Classes/Arrays-and-Indexing/#Functional-Programming-in-Lean--Overloading-and-Type-Classes--Arrays-and-Indexing "3.4. Arrays and Indexing")

# 3.3. Controlling Instance Search[🔗](find/?domain=Verso.Genre.Manual.section&name=out-params "Permalink")

An instance of the `Add` class is sufficient to allow two expressions with type `Pos` to be conveniently added, producing another `Pos`.
However, in many cases, it can be useful to be more flexible and allow *heterogeneous* operator overloading, where the arguments may have different types.
For example, adding a `Nat` to a `Pos` or a `Pos` to a `Nat` will always yield a `Pos`:

`def addNatPos : Nat → Pos → Pos
| 0, p => p
| n + 1, p => Pos.succ (addNatPos n p)
def addPosNat : Pos → Nat → Pos
| p, 0 => p
| p, n + 1 => Pos.succ (addPosNat p n)`

These functions allow natural numbers to be added to positive numbers, but they cannot be used with the `Add` type class, which expects both arguments to `add` to have the same type.

## 3.3.1. Heterogeneous Overloadings[🔗](find/?domain=Verso.Genre.Manual.section&name=heterogeneous-operators "Permalink")

As mentioned in the section on [overloaded addition](Overloading-and-Type-Classes/Positive-Numbers/#overloaded-addition), Lean provides a type class called `HAdd` for overloading addition heterogeneously.
The `HAdd` class takes three type parameters: the two argument types and the return type.
Instances of `HAdd Nat Pos Pos` and `HAdd Pos Nat Pos` allow ordinary addition notation to be used to mix the types:

`instance : HAdd Nat Pos Pos where
hAdd := addNatPos
instance : HAdd Pos Nat Pos where
hAdd := addPosNat`

Given the above two instances, the following examples work:

`8#eval (3 : Pos) + (5 : Nat)`


```lean
8
```


`8#eval (3 : Nat) + (5 : Pos)`


```lean
8
```


The definition of the `HAdd` type class is very much like the following definition of `HPlus` with the corresponding instances:

`class HPlus (α : Type) (β : Type) (γ : Type) where
hPlus : α → β → γ``instance : HPlus Nat Pos Pos where
hPlus := addNatPos
instance : HPlus Pos Nat Pos where
hPlus := addPosNat`

However, instances of `HPlus` are significantly less useful than instances of `HAdd`.
When attempting to use these instances with `#eval`, an error occurs:

`` #eval toString (typeclass instance problem is stuck
HPlus Pos Nat ?m.6

Note: Lean will not try to resolve this typeclass instance problem because the third type argument to `HPlus` is a metavariable. This argument must be fully determined before Lean will try to resolve the typeclass.

Hint: Adding type annotations and supplying implicit arguments to functions can give Lean more information for typeclass resolution. For example, if you have a variable `x` that you intend to be a `Nat`, but Lean reports it as having an unresolved type like `?m`, replacing `x` with `(x : Nat)` can get typeclass resolution un-stuck.HPlus.hPlus (3 : Pos) (5 : Nat)) ``


```lean
typeclass instance problem is stuck
  HPlus Pos Nat ?m.6

Note: Lean will not try to resolve this typeclass instance problem because the third type argument to `HPlus` is a metavariable. This argument must be fully determined before Lean will try to resolve the typeclass.

Hint: Adding type annotations and supplying implicit arguments to functions can give Lean more information for typeclass resolution. For example, if you have a variable `x` that you intend to be a `Nat`, but Lean reports it as having an unresolved type like `?m`, replacing `x` with `(x : Nat)` can get typeclass resolution un-stuck.
```


The message indicates that this happens because there is a metavariable in the type, and Lean has no way to solve it.

As discussed in [the initial description of polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism), metavariables represent unknown parts of a program that could not be inferred.
When an expression is written following `#eval`, Lean attempts to determine its type automatically.
In this case, it could not.
Because the third type parameter for `HPlus` was unknown, Lean couldn't carry out type class instance search, but instance search is the only way that Lean could determine the expression's type.
That is, the `HPlus Pos Nat Pos` instance can only apply if the expression should have type `Pos`, but there's nothing in the program other than the instance itself to indicate that it should have this type.

One solution to the problem is to ensure that all three types are available by adding a type annotation to the whole expression:

`8#eval (HPlus.hPlus (3 : Pos) (5 : Nat) : Pos)`


```lean
8
```


However, this solution is not very convenient for users of the positive number library.

## 3.3.2. Output Parameters[🔗](find/?domain=Verso.Genre.Manual.section&name=output-parameters "Permalink")

This problem can also be solved by declaring `γ` to be an *output parameter*.
Most type class parameters are inputs to the search algorithm: they are used to select an instance.
For example, in an `OfNat` instance, both the type and the natural number are used to select a particular interpretation of a natural number literal.
However, in some cases, it can be convenient to start the search process even when some of the type parameters are not yet known, and use the instances that are discovered in the search to determine values for metavariables.
The parameters that aren't needed to start instance search are outputs of the process, which is declared with the `outParam` modifier:

`class HPlus (α : Type) (β : Type) (γ : outParam Type) where
hPlus : α → β → γ`

With this output parameter, type class instance search is able to select an instance without knowing `γ` in advance.
For instance:

`8#eval HPlus.hPlus (3 : Pos) (5 : Nat)`


```lean
8
```


It might be helpful to think of output parameters as defining a kind of function.
Any given instance of a type class that has one or more output parameters provides Lean with instructions for determining the outputs from the inputs.
The process of searching for an instance, possibly recursively, ends up being more powerful than mere overloading.
Output parameters can determine other types in the program, and instance search can assemble a collection of underlying instances into a program that has this type.

## 3.3.3. Default Instances[🔗](find/?domain=Verso.Genre.Manual.section&name=default-instances "Permalink")

Deciding whether a parameter is an input or an output controls the circumstances under which Lean will initiate type class search.
In particular, type class search does not occur until all inputs are known.
However, in some cases, output parameters are not enough, and instance search should also occur when some inputs are unknown.
This is a bit like default values for optional function arguments in Python or Kotlin, except default *types* are being selected.

*Default instances* are instances that are available for instance search *even when not all their inputs are known*.
When one of these instances can be used, it will be used.
This can cause programs to successfully type check, rather than failing with errors related to unknown types and metavariables.
On the other hand, default instances can make instance selection less predictable.
In particular, if an undesired default instance is selected, then an expression may have a different type than expected, which can cause confusing type errors to occur elsewhere in the program.
Be selective about where default instances are used!

One example of where default instances can be useful is an instance of `HPlus` that can be derived from an `Add` instance.
In other words, ordinary addition is a special case of heterogeneous addition in which all three types happen to be the same.
This can be implemented using the following instance:

`instance [Add α] : HPlus α α α where
hPlus := Add.add`

With this instance, `hPlus` can be used for any addable type, like `Nat`:

`8#eval HPlus.hPlus (3 : Nat) (5 : Nat)`


```lean
8
```


However, this instance will only be used in situations where the types of both arguments are known.
For example,

`HPlus.hPlus 5 3 : Nat#check HPlus.hPlus (5 : Nat) (3 : Nat)`

yields the type


```lean
HPlus.hPlus 5 3 : Nat
```


as expected, but

`HPlus.hPlus 5 : ?m.2 → ?m.3#check HPlus.hPlus (5 : Nat)`

yields a type that contains two metavariables, one for the remaining argument and one for the return type:


```lean
HPlus.hPlus 5 : ?m.2 → ?m.3
```


In the vast majority of cases, when someone supplies one argument to addition, the other argument will have the same type.
To make this instance into a default instance, apply the `default_instance` attribute:

`@[default_instance]
instance [Add α] : HPlus α α α where
hPlus := Add.add`

With this default instance, the example has a more useful type:

`HPlus.hPlus 5 : Nat → Nat#check HPlus.hPlus (5 : Nat)`

yields


```lean
HPlus.hPlus 5 : Nat → Nat
```


Each operator that exists in overloadable heterogeneous and homogeneous versions follows the pattern of a default instance that allows the homogeneous version to be used in contexts where the heterogeneous is expected.
The infix operator is replaced with a call to the heterogeneous version, and the homogeneous default instance is selected when possible.

Similarly, simply writing `5` gives a `Nat` rather than a type with a metavariable that is waiting for more information in order to select an `OfNat` instance.
This is because the `OfNat` instance for `Nat` is a default instance.

Default instances can also be assigned *priorities* that affect which will be chosen in situations where more than one might apply.
For more information on default instance priorities, please consult the Lean manual.

## 3.3.4. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=out-params-exercises "Permalink")

Define an instance of `HMul (PPoint α) α (PPoint α)` that multiplies both projections by the scalar.
It should work for any type `α` for which there is a `Mul α` instance.
For example,

`{ x := 5.000000, y := 7.400000 }#eval {x := 2.5, y := 3.7 : PPoint Float} * 2.0`

should yield


```lean
{ x := 5.000000, y := 7.400000 }
```


[←3.2. Type Classes and Polymorphism](Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/#tc-polymorphism "3.2. Type Classes and Polymorphism")[3.4. Arrays and Indexing→](Overloading-and-Type-Classes/Arrays-and-Indexing/#Functional-Programming-in-Lean--Overloading-and-Type-Classes--Arrays-and-Indexing "3.4. Arrays and Indexing")
