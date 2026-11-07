# Study guide: 5.1. Structures and Inheritance 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **5.1. Structures and Inheritance 🔗** — In order to understand the full definitions of Functor , Applicative , and Monad , another Lean feature is necessary: structure inheritance.
- **5.1.1. Multiple Inheritance 🔗** — A helper is a mythical creature that can provide assistance when given the correct payment:
- **5.1.1.1. Default Declarations 🔗** — When one structure inherits from another, default field definitions can be used to instantiate the parent structure's fields based on the child structure's fields.
- **5.1.1.2. Type Class Inheritance 🔗** — Behind the scenes, type classes are structures.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←5. Functors, Applicative Functors, and Monads](Functors___-Applicative-Functors___-and-Monads/#Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads "5. Functors, Applicative Functors, and Monads")[5.2. Applicative Functors→](Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/#applicative "5.2. Applicative Functors")

# 5.1. Structures and Inheritance[🔗](find/?domain=Verso.Genre.Manual.section&name=structure-inheritance "Permalink")

In order to understand the full definitions of `Functor`, `Applicative`, and `Monad`, another Lean feature is necessary: structure inheritance.
Structure inheritance allows one structure type to provide the interface of another, along with additional fields.
This can be useful when modeling concepts that have a clear taxonomic relationship.
For example, take a model of mythical creatures.
Some of them are large, and some are small:

`structure MythicalCreature where
large : Bool
deriving Repr`

Behind the scenes, defining the `MythicalCreature` structure creates an inductive type with a single constructor called `mk`:

`MythicalCreature.mk (large : Bool) : MythicalCreature#check MythicalCreature.mk`


```lean
MythicalCreature.mk (large : Bool) : MythicalCreature
```


Similarly, a function `MythicalCreature.large` is created that actually extracts the field from the constructor:

`MythicalCreature.large (self : MythicalCreature) : Bool#check MythicalCreature.large`


```lean
MythicalCreature.large (self : MythicalCreature) : Bool
```


In most old stories, each monster can be defeated in some way.
A description of a monster should include this information, along with whether it is large:

`structure Monster extends MythicalCreature where
vulnerability : String
deriving Repr`

The `extends MythicalCreature` in the heading states that every monster is also mythical.
To define a `Monster`, both the fields from `MythicalCreature` and the fields from `Monster` should be provided.
A troll is a large monster that is vulnerable to sunlight:

`def troll : Monster where
large := true
vulnerability := "sunlight"`

Behind the scenes, inheritance is implemented using composition.
The constructor `Monster.mk` takes a `MythicalCreature` as its argument:

`Monster.mk (toMythicalCreature : MythicalCreature) (vulnerability : String) : Monster#check Monster.mk`


```lean
Monster.mk (toMythicalCreature : MythicalCreature) (vulnerability : String) : Monster
```


In addition to defining functions to extract the value of each new field, a function `Monster.toMythicalCreature` is defined with type `Monster → MythicalCreature`.
This can be used to extract the underlying creature.

Moving up the inheritance hierarchy in Lean is not the same thing as upcasting in object-oriented languages.
An upcast operator causes a value from a derived class to be treated as an instance of the parent class, but the value retains its identity and structure.
In Lean, however, moving up the inheritance hierarchy actually erases the underlying information.
To see this in action, consider the result of evaluating `troll.toMythicalCreature`:

`{ large := true }#eval troll.toMythicalCreature`


```lean
{ large := true }
```


Only the fields of `MythicalCreature` remain.

Just like the `where` syntax, curly-brace notation with field names also works with structure inheritance:

`def troll : Monster := {large := true, vulnerability := "sunlight"}`

However, the anonymous angle-bracket notation that delegates to the underlying constructor reveals the internal details:

`def troll : Monster := ⟨Application type mismatch: The argument
true
has type
Bool
but is expected to have type
MythicalCreature
in the application
Monster.mk truetrue, "sunlight"⟩`


```lean
Application type mismatch: The argument
  true
has type
  Bool
but is expected to have type
  MythicalCreature
in the application
  Monster.mk true
```


An extra set of angle brackets is required, which invokes `MythicalCreature.mk` on `true`:

`def troll : Monster := ⟨⟨true⟩, "sunlight"⟩`

Lean's dot notation is capable of taking inheritance into account.
In other words, the existing `MythicalCreature.large` can be used with a `Monster`, and Lean automatically inserts the call to `Monster.toMythicalCreature` before the call to `MythicalCreature.large`.
However, this only occurs when using dot notation, and applying the field lookup function using normal function call syntax results in a type error:

`#eval MythicalCreature.large Application type mismatch: The argument
troll
has type
Monster
but is expected to have type
MythicalCreature
in the application
MythicalCreature.large trolltroll`


```lean
Application type mismatch: The argument
  troll
has type
  Monster
but is expected to have type
  MythicalCreature
in the application
  MythicalCreature.large troll
```


Dot notation can also take inheritance into account for user-defined functions.
A small creature is one that is not large:

`def MythicalCreature.small (c : MythicalCreature) : Bool := !c.large`

Evaluating `troll.small` yields `false`, while attempting to evaluate `MythicalCreature.small troll` results in:


```lean
Application type mismatch: The argument
  troll
has type
  Monster
but is expected to have type
  MythicalCreature
in the application
  MythicalCreature.small troll
```


## 5.1.1. Multiple Inheritance[🔗](find/?domain=Verso.Genre.Manual.section&name=multiple-structure-inheritance "Permalink")

A helper is a mythical creature that can provide assistance when given the correct payment:

`structure Helper extends MythicalCreature where
assistance : String
payment : String
deriving Repr`

For example, a *nisse* is a kind of small elf that's known to help around the house when provided with tasty porridge:

`def nisse : Helper where
large := false
assistance := "household tasks"
payment := "porridge"`

If domesticated, trolls make excellent helpers.
They are strong enough to plow a whole field in a single night, though they require model goats to keep them satisfied with their lot in life.
A monstrous assistant is a monster that is also a helper:

`structure MonstrousAssistant extends Monster, Helper where
deriving Repr`

A value of this structure type must fill in all of the fields from both parent structures:

`def domesticatedTroll : MonstrousAssistant where
large := true
assistance := "heavy labor"
payment := "toy goats"
vulnerability := "sunlight"`

Both of the parent structure types extend `MythicalCreature`.
If multiple inheritance were implemented naïvely, then this could lead to a “diamond problem”, where it would be unclear which path to `large` should be taken from a given `MonstrousAssistant`.
Should it take `large` from the contained `Monster` or from the contained `Helper`?
In Lean, the answer is that the first specified path to the grandparent structure is taken, and the additional parent structures' fields are copied rather than having the new structure include both parents directly.

This can be seen by examining the signature of the constructor for `MonstrousAssistant`:

`MonstrousAssistant.mk (toMonster : Monster) (assistance payment : String) : MonstrousAssistant#check MonstrousAssistant.mk`


```lean
MonstrousAssistant.mk (toMonster : Monster) (assistance payment : String) : MonstrousAssistant
```


It takes a `Monster` as an argument, along with the two fields that `Helper` introduces on top of `MythicalCreature`.
Similarly, while `MonstrousAssistant.toMonster` merely extracts the `Monster` from the constructor, `MonstrousAssistant.toHelper` has no `Helper` to extract.
The `#print` command exposes its implementation:

`@[reducible] def MonstrousAssistant.toHelper : MonstrousAssistant → Helper :=
fun self => { toMythicalCreature := self.toMythicalCreature, assistance := self.assistance, payment := self.payment }#print MonstrousAssistant.toHelper`


```lean
@[reducible] def MonstrousAssistant.toHelper : MonstrousAssistant → Helper :=
fun self => { toMythicalCreature := self.toMythicalCreature, assistance := self.assistance, payment := self.payment }
```


This function constructs a `Helper` from the fields of `MonstrousAssistant`.
The `@[reducible]` attribute has the same effect as writing `abbrev`.

### 5.1.1.1. Default Declarations[🔗](find/?domain=Verso.Genre.Manual.section&name=inheritance-defaults "Permalink")

When one structure inherits from another, default field definitions can be used to instantiate the parent structure's fields based on the child structure's fields.
If more size specificity is required than whether a creature is large or not, a dedicated datatype describing sizes can be used together with inheritance, yielding a structure in which the `large` field is computed from the contents of the `size` field:

`inductive Size where
| small
| medium
| large
deriving BEq
structure SizedCreature extends MythicalCreature where
size : Size
large := size == Size.large`

This default definition is only a default definition, however.
Unlike property inheritance in a language like C# or Scala, the definitions in the child structure are only used when no specific value for `large` is provided, and nonsensical results can occur:

`def nonsenseCreature : SizedCreature where
large := false
size := .large`

If the child structure should not deviate from the parent structure, there are a few options:

1. Documenting the relationship, as is done for `BEq` and `Hashable`
2. Defining a proposition that the fields are related appropriately, and designing the API to require evidence that the proposition is true where it matters
3. Not using inheritance at all

The second option could look like this:

`abbrev SizesMatch (sc : SizedCreature) : Prop :=
sc.large = (sc.size == Size.large)`

Note that a single equality sign is used to indicate the equality *proposition*, while a double equality sign is used to indicate a function that checks equality and returns a `Bool`.
`SizesMatch` is defined as an `abbrev` because it should automatically be unfolded in proofs, so that `decide` can see the equality that should be proven.

A *huldre* is a medium-sized mythical creature—in fact, they are the same size as humans.
The two sized fields on `huldre` match one another:

`def huldre : SizedCreature where
size := .medium
example : SizesMatch huldre := by⊢ SizesMatch huldre
decideAll goals completed! 🐙`

### 5.1.1.2. Type Class Inheritance[🔗](find/?domain=Verso.Genre.Manual.section&name=type-class-inheritance "Permalink")

Behind the scenes, type classes are structures.
Defining a new type class defines a new structure, and defining an instance creates a value of that structure type.
They are then added to internal tables in Lean that allow it to find the instances upon request.
A consequence of this is that type classes may inherit from other type classes.

Because it uses precisely the same language features, type class inheritance supports all the features of structure inheritance, including multiple inheritance, default implementations of parent types' methods, and automatic collapsing of diamonds.
This is useful in many of the same situations that multiple interface inheritance is useful in languages like Java, C# and Kotlin.
By carefully designing type class inheritance hierarchies, programmers can get the best of both worlds: a fine-grained collection of independently-implementable abstractions, and automatic construction of these specific abstractions from larger, more general abstractions.

[←5. Functors, Applicative Functors, and Monads](Functors___-Applicative-Functors___-and-Monads/#Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads "5. Functors, Applicative Functors, and Monads")[5.2. Applicative Functors→](Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/#applicative "5.2. Applicative Functors")
