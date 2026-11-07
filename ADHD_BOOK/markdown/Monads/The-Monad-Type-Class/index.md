# Study guide: 4.2. The Monad Type Class 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **4.2. The Monad Type Class 🔗** — Rather than having to import an operator like ok or andThen for each type that is a monad, the Lean standard library contains a type class that allow them to be overloaded, so that the same operators can be used for any monad.
- **4.2.1. General Monad Operations 🔗** — Because many different types are monads, functions that are polymorphic over any monad are very powerful.
- **4.2.2. The Identity Monad 🔗** — Monads encode programs with effects, such as failure, exceptions, or logging, into explicit representations as data and functions.
- **4.2.3. The Monad Contract 🔗** — Just as every pair of instances of BEq and Hashable should ensure that any two equal values have the same hash, there is a contract that each instance of Monad should obey.
- **4.2.4.1. Mapping on a Tree 🔗** — Define a function BinTree.mapM .
- **4.2.4.2. The Option Monad Contract 🔗** — First, write a convincing argument that the Monad instance for Option satisfies the monad contract.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←4.1. One API, Many Applications](Monads/One-API___-Many-Applications/#monad-api-examples "4.1. One API, Many Applications")[4.3. Example: Arithmetic in Monads→](Monads/Example___-Arithmetic-in-Monads/#monads-arithmetic-example "4.3. Example: Arithmetic in Monads")

# 4.2. The Monad Type Class[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-type-class "Permalink")

Rather than having to import an operator like `ok` or `andThen` for each type that is a monad, the Lean standard library contains a type class that allow them to be overloaded, so that the same operators can be used for *any* monad.
Monads have two operations, which are the equivalent of `ok` and `andThen`:

`class Monad (m : Type → Type) where
pure : α → m α
bind : m α → (α → m β) → m β`

This definition is slightly simplified.
The actual definition in the Lean library is somewhat more involved, and will be presented later.

The `Monad` instances for `Option` and `Except ε` can be created by adapting the definitions of their respective `andThen` operations:

`instance : Monad Option where
pure x := some x
bind opt next :=
match opt with
| none => none
| some x => next x
instance : Monad (Except ε) where
pure x := Except.ok x
bind attempt next :=
match attempt with
| Except.error e => Except.error e
| Except.ok x => next x`

As an example, `firstThirdFifthSeventh` was defined separately for `Option α` and `Except String α` return types.
Now, it can be defined polymorphically for *any* monad.
It does, however, require a lookup function as an argument, because different monads might fail to find a result in different ways.
The infix version of `bind` is `>>=`, which plays the same role as `~~>` in the examples.

`def firstThirdFifthSeventh [Monad m] (lookup : List α → Nat → m α)
(xs : List α) : m (α × α × α × α) :=
lookup xs 0 >>= fun first =>
lookup xs 2 >>= fun third =>
lookup xs 4 >>= fun fifth =>
lookup xs 6 >>= fun seventh =>
pure (first, third, fifth, seventh)`

Given example lists of slow mammals and fast birds, this implementation of `firstThirdFifthSeventh` can be used with `Option`:

`def slowMammals : List String :=
["Three-toed sloth", "Slow loris"]
def fastBirds : List String := [
"Peregrine falcon",
"Saker falcon",
"Golden eagle",
"Gray-headed albatross",
"Spur-winged goose",
"Swift",
"Anna's hummingbird"
]``none#eval firstThirdFifthSeventh (fun xs i => xs[i]?) slowMammals`


```lean
none
```


`some ("Peregrine falcon", "Golden eagle", "Spur-winged goose", "Anna's hummingbird")#eval firstThirdFifthSeventh (fun xs i => xs[i]?) fastBirds`


```lean
some ("Peregrine falcon", "Golden eagle", "Spur-winged goose", "Anna's hummingbird")
```


After renaming `Except`'s lookup function `get` to something more specific, the very same implementation of `firstThirdFifthSeventh` can be used with `Except` as well:

`def getOrExcept (xs : List α) (i : Nat) : Except String α :=
match xs[i]? with
| none =>
Except.error s!"Index {i} not found (maximum is {xs.length - 1})"
| some x =>
Except.ok x``Except.error "Index 2 not found (maximum is 1)"#eval firstThirdFifthSeventh getOrExcept slowMammals`


```lean
Except.error "Index 2 not found (maximum is 1)"
```


`Except.ok ("Peregrine falcon", "Golden eagle", "Spur-winged goose", "Anna's hummingbird")#eval firstThirdFifthSeventh getOrExcept fastBirds`


```lean
Except.ok ("Peregrine falcon", "Golden eagle", "Spur-winged goose", "Anna's hummingbird")
```


The fact that `m` must have a `Monad` instance means that the `>>=` and `pure` operations are available.

## 4.2.1. General Monad Operations[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-class-polymorphism "Permalink")

Because many different types are monads, functions that are polymorphic over *any* monad are very powerful.
For example, the function `mapM` is a version of `map` that uses a `Monad` to sequence and combine the results of applying a function:

`def mapM [Monad m] (f : α → m β) : List α → m (List β)
| [] => pure []
| x :: xs =>
f x >>= fun hd =>
mapM f xs >>= fun tl =>
pure (hd :: tl)`

The return type of the function argument `f` determines which `Monad` instance will be used.
In other words, `mapM` can be used for functions that produce logs, for functions that can fail, or for functions that use mutable state.
Because `f`'s type determines the available effects, they can be tightly controlled by API designers.

As described in [this chapter's introduction](Monads/One-API___-Many-Applications/#numbering-tree-nodes), `State σ α` represents programs that make use of a mutable variable of type `σ` and return a value of type `α`.
These programs are actually functions from a starting state to a pair of a value and a final state.
The `Monad` class requires that its parameter expect a single type argument—that is, it should be a `Type → Type`.
This means that the instance for `State` should mention the state type `σ`, which becomes a parameter to the instance:

`instance : Monad (State σ) where
pure x := fun s => (s, x)
bind first next :=
fun s =>
let (s', x) := first s
next x s'`

This means that the type of the state cannot change between calls to `get` and `set` that are sequenced using `bind`, which is a reasonable rule for stateful computations.
The operator `increment` increases a saved state by a given amount, returning the old value:

`def increment (howMuch : Int) : State Int Int :=
get >>= fun i =>
set (i + howMuch) >>= fun () =>
pure i`

Using `mapM` with `increment` results in a program that computes the sum of the entries in a list.
More specifically, the mutable variable contains the sum so far, while the resulting list contains a running sum.
In other words, `mapM increment` has type `List Int → State Int (List Int)`, and expanding the definition of `State` yields `List Int → Int → (Int × List Int)`.
It takes an initial sum as an argument, which should be `0`:

`(15, [0, 1, 3, 6, 10])#eval mapM increment [1, 2, 3, 4, 5] 0`


```lean
(15, [0, 1, 3, 6, 10])
```


A [logging effect](Monads/One-API___-Many-Applications/#logging) can be represented using `WithLog`.
Just like `State`, its `Monad` instance is polymorphic with respect to the type of the logged data:

`instance : Monad (WithLog logged) where
pure x := {log := [], val := x}
bind result next :=
let {log := thisOut, val := thisRes} := result
let {log := nextOut, val := nextRes} := next thisRes
{log := thisOut ++ nextOut, val := nextRes}`

`saveIfEven` is a function that logs even numbers but returns its argument unchanged:

`def saveIfEven (i : Int) : WithLog Int Int :=
(if isEven i then
save i
else pure ()) >>= fun () =>
pure i`

Using this function with `mapM` results in a log containing even numbers paired with an unchanged input list:

`{ log := [2, 4], val := [1, 2, 3, 4, 5] }#eval mapM saveIfEven [1, 2, 3, 4, 5]`


```lean
{ log := [2, 4], val := [1, 2, 3, 4, 5] }
```


## 4.2.2. The Identity Monad[🔗](find/?domain=Verso.Genre.Manual.section&name=Id-monad "Permalink")

Monads encode programs with effects, such as failure, exceptions, or logging, into explicit representations as data and functions.
Sometimes, however, an API will be written to use a monad for flexibility, but the API's client may not require any encoded effects.
The *identity monad* is a monad that has no effects.
It allows pure code to be used with monadic APIs:

`def Id (t : Type) : Type := t
instance : Monad Id where
pure x := x
bind x f := f x`

The type of `pure` should be `α → Id α`, but `Id α` reduces to just `α`.
Similarly, the type of `bind` should be `α → (α → Id β) → Id β`.
Because this reduces to `α → (α → β) → β`, the second argument can be applied to the first to find the result.

With the identity monad, `mapM` becomes equivalent to `map`
To call it this way, however, Lean requires a hint that the intended monad is `Id`:

`def numbers := mapM (m := Id) (do return · + 1) [1, 2, 3, 4, 5]`

Using `mapM` in a context in which the type doesn't provide any specific hints about which monad is to be used results in an “instance problem is stuck” message:

`` def numbers := mapM (do typeclass instance problem is stuck
Pure ?m.6

Note: Lean will not try to resolve this typeclass instance problem because the type argument to `Pure` is a metavariable. This argument must be fully determined before Lean will try to resolve the typeclass.

Hint: Adding type annotations and supplying implicit arguments to functions can give Lean more information for typeclass resolution. For example, if you have a variable `x` that you intend to be a `Nat`, but Lean reports it as having an unresolved type like `?m`, replacing `x` with `(x : Nat)` can get typeclass resolution un-stuck.return · + 1) [1, 2, 3, 4, 5] ``


```lean
typeclass instance problem is stuck
  Pure ?m.6

Note: Lean will not try to resolve this typeclass instance problem because the type argument to `Pure` is a metavariable. This argument must be fully determined before Lean will try to resolve the typeclass.

Hint: Adding type annotations and supplying implicit arguments to functions can give Lean more information for typeclass resolution. For example, if you have a variable `x` that you intend to be a `Nat`, but Lean reports it as having an unresolved type like `?m`, replacing `x` with `(x : Nat)` can get typeclass resolution un-stuck.
```


## 4.2.3. The Monad Contract[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-contract "Permalink")

Just as every pair of instances of `BEq` and `Hashable` should ensure that any two equal values have the same hash, there is a contract that each instance of `Monad` should obey.
First, `pure` should be a left identity of `bind`.
That is, `bind (pure v) f` should be the same as `f v`.
Secondly, `pure` should be a right identity of `bind`, so `bind v pure` is the same as `v`.
Finally, `bind` should be associative, so `bind (bind v f) g` is the same as `bind v (fun x => bind (f x) g)`.

This contract specifies the expected properties of programs with effects more generally.
Because `pure` has no effects, sequencing its effects with `bind` shouldn't change the result.
The associative property of `bind` basically says that the sequencing bookkeeping itself doesn't matter, so long as the order in which things are happening is preserved.

## 4.2.4. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-class-exercises "Permalink")

### 4.2.4.1. Mapping on a Tree[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--The-Monad-Type-Class--Exercises--Mapping-on-a-Tree "Permalink")

Define a function `BinTree.mapM`.
By analogy to `mapM` for lists, this function should apply a monadic function to each data entry in a tree, as a preorder traversal.
The type signature should be:

`def BinTree.mapM [Monad m] (f : α → m β) : BinTree α → m (BinTree β)`

### 4.2.4.2. The Option Monad Contract[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monads--The-Monad-Type-Class--Exercises--The-Option-Monad-Contract "Permalink")

First, write a convincing argument that the `Monad` instance for `Option` satisfies the monad contract.
Then, consider the following instance:

`instance : Monad Option where
pure x := some x
bind opt next := none`

Both methods have the correct type.
Why does this instance violate the monad contract?

[←4.1. One API, Many Applications](Monads/One-API___-Many-Applications/#monad-api-examples "4.1. One API, Many Applications")[4.3. Example: Arithmetic in Monads→](Monads/Example___-Arithmetic-in-Monads/#monads-arithmetic-example "4.3. Example: Arithmetic in Monads")


> **Review needed:** The following headings have no short source sentence: 4.2.4. Exercises 🔗