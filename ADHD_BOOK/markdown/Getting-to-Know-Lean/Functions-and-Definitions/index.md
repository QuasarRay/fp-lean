# Study guide: 1.3. Functions and Definitions 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.3. Functions and Definitions 🔗** — In Lean, definitions are introduced using the def keyword.
- **1.3.1. Defining Functions 🔗** — There are a variety of ways to define functions in Lean.
- **1.3.1.1. Exercises 🔗** — Define the function joinStringsWith with type String → String → String → String that creates a new string by placing its first argument between its second and third arguments.
- **1.3.2. Defining Types 🔗** — Most typed programming languages have some means of defining aliases for types, such as C's typedef .
- **1.3.2.1. Messages You May Meet 🔗** — Experimenting with using definitions for types is made more complicated by the way that Lean supports overloaded integer literals.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.2. Types](Getting-to-Know-Lean/Types/#getting-to-know-types "1.2. Types")[1.4. Structures→](Getting-to-Know-Lean/Structures/#structures "1.4. Structures")

# 1.3. Functions and Definitions[🔗](find/?domain=Verso.Genre.Manual.section&name=functions-and-definitions "Permalink")

In Lean, definitions are introduced using the `def` keyword.
For instance, to define the name `hello` to refer to the string `"Hello"`, write:

`def hello := "Hello"`

In Lean, new names are defined using the colon-equal operator `:=` rather than `=`.
This is because `=` is used to describe equalities between existing expressions, and using two different operators helps prevent confusion.

In the definition of `hello`, the expression `"Hello"` is simple enough that Lean is able to determine the definition's type automatically.
However, most definitions are not so simple, so it will usually be necessary to add a type.
This is done using a colon after the name being defined:

`def lean : String := "Lean"`

Now that the names have been defined, they can be used, so

`"Hello Lean"#eval String.append hello (String.append " " lean)`

outputs


```lean
"Hello Lean"
```


In Lean, defined names may only be used after their definitions.

In many languages, definitions of functions use a different syntax than definitions of other values.
For instance, Python function definitions begin with the `def` keyword, while other definitions are defined with an equals sign.
In Lean, functions are defined using the same `def` keyword as other values.
Nonetheless, definitions such as `hello` introduce names that refer *directly* to their values, rather than to zero-argument functions that return equivalent results each time they are called.

## 1.3.1. Defining Functions[🔗](find/?domain=Verso.Genre.Manual.section&name=defining-functions "Permalink")

There are a variety of ways to define functions in Lean. The simplest is to place the function's arguments before the definition's type, separated by spaces. For instance, a function that adds one to its argument can be written:

`def add1 (n : Nat) : Nat := n + 1`

Testing this function with `#eval` gives `8`, as expected:

`8#eval add1 7`

Just as functions are applied to multiple arguments by writing spaces between each argument, functions that accept multiple arguments are defined with spaces between the arguments' names and types. The function `maximum`, whose result is equal to the greatest of its two arguments, takes two `Nat` arguments `n` and `k` and returns a `Nat`.

`def maximum (n : Nat) (k : Nat) : Nat :=
if n < k then
k
else n`

Similarly, the function `spaceBetween` joins two strings with a space between them.

`def spaceBetween (before : String) (after : String) : String :=
String.append before (String.append " " after)`

When a defined function like `maximum` has been provided with its arguments, the result is determined by first replacing the argument names with the provided values in the body, and then evaluating the resulting body. For example:

`maximum (5 + 8) (2 * 7)``maximum 13 14``if 13 < 14 then 14 else 13``14`

Expressions that evaluate to natural numbers, integers, and strings have types that say this (`Nat`, `Int`, and `String`, respectively).
This is also true of functions.
A function that accepts a `Nat` and returns a `Bool` has type `Nat → Bool`, and a function that accepts two `Nat`s and returns a `Nat` has type `Nat → Nat → Nat`.

As a special case, Lean returns a function's signature when its name is used directly with `#check`.
Entering `#check add1` yields `add1 (n : Nat) : Nat`.
However, Lean can be “tricked” into showing the function's type by writing the function's name in parentheses, which causes the function to be treated as an ordinary expression, so `#check (add1)` yields `add1 : Nat → Nat` and `#check (maximum)` yields `maximum : Nat → Nat → Nat`.
This arrow can also be written with an ASCII alternative arrow `->`, so the preceding function types can be written `example : Nat -> Nat := add1` and `example : Nat -> Nat -> Nat := maximum`, respectively.

Behind the scenes, all functions actually expect precisely one argument.
Functions like `maximum` that seem to take more than one argument are in fact functions that take one argument and then return a new function.
This new function takes the next argument, and the process continues until no more arguments are expected.
This can be seen by providing one argument to a multiple-argument function: `#check maximum 3` yields `maximum 3 : Nat → Nat` and `#check spaceBetween "Hello "` yields `spaceBetween "Hello " : String → String`.
Using a function that returns a function to implement multiple-argument functions is called *currying* after the mathematician Haskell Curry.
Function arrows associate to the right, which means that `Nat → Nat → Nat` should be parenthesized `Nat → (Nat → Nat)`.

### 1.3.1.1. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=function-definition-exercises "Permalink")

- Define the function `joinStringsWith` with type `String → String → String → String` that creates a new string by placing its first argument between its second and third arguments. `joinStringsWith ", " "one" "and another"` should evaluate to `"one, and another"`.
- What is the type of `joinStringsWith ": "`? Check your answer with Lean.
- Define a function `volume` with type `Nat → Nat → Nat → Nat` that computes the volume of a rectangular prism with the given height, width, and depth.

## 1.3.2. Defining Types[🔗](find/?domain=Verso.Genre.Manual.section&name=defining-types "Permalink")

Most typed programming languages have some means of defining aliases for types, such as C's `typedef`.
In Lean, however, types are a first-class part of the language—they are expressions like any other.
This means that definitions can refer to types just as well as they can refer to other values.

For example, if `String` is too much to type, a shorter abbreviation `Str` can be defined:

`def Str : Type := String`

It is then possible to use `Str` as a definition's type instead of `String`:

`def aStr : Str := "This is a string."`

The reason this works is that types follow the same rules as the rest of Lean.
Types are expressions, and in an expression, a defined name can be replaced with its definition.
Because `Str` has been defined to mean `String`, the definition of `aStr` makes sense.

### 1.3.2.1. Messages You May Meet[🔗](find/?domain=Verso.Genre.Manual.section&name=abbrev-vs-def "Permalink")

Experimenting with using definitions for types is made more complicated by the way that Lean supports overloaded integer literals.
If `Nat` is too short, a longer name `NaturalNumber` can be defined:

`def NaturalNumber : Type := Nat`

However, using `NaturalNumber` as a definition's type instead of `Nat` does not have the expected effect.
In particular, the definition:

`` def thirtyEight : NaturalNumber := failed to synthesize instance of type class
OfNat NaturalNumber 38
numerals are polymorphic in Lean, but the numeral `38` cannot be used in a context where the expected type is
NaturalNumber
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.38 ``

results in the following error:


```lean
failed to synthesize instance of type class
  OfNat NaturalNumber 38
numerals are polymorphic in Lean, but the numeral `38` cannot be used in a context where the expected type is
  NaturalNumber
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


This error occurs because Lean allows number literals to be *overloaded*.
When it makes sense to do so, natural number literals can be used for new types, just as if those types were built in to the system.
This is part of Lean's mission of making it convenient to represent mathematics, and different branches of mathematics use number notation for very different purposes.
The specific feature that allows this overloading does not replace all defined names with their definitions before looking for overloading, which is what leads to the error message above.

One way to work around this limitation is by providing the type `Nat` on the right-hand side of the definition, causing `Nat`'s overloading rules to be used for `38`:

`def thirtyEight : NaturalNumber := (38 : Nat)`

The definition is still type-correct because `NaturalNumber` is the same type as `Nat`—by definition!

Another solution is to define an overloading for `NaturalNumber` that works equivalently to the one for `Nat`.
This requires more advanced features of Lean, however.

Finally, defining the new name for `Nat` using `abbrev` instead of `def` allows overloading resolution to replace the defined name with its definition.
Definitions written using `abbrev` are always unfolded.
For instance,

`abbrev N : Type := Nat`

and

`def thirtyNine : N := 39`

are accepted without issue.

Behind the scenes, some definitions are internally marked as being unfoldable during overload resolution, while others are not.
Definitions that are to be unfolded are called *reducible*.
Control over reducibility is essential to allow Lean to scale: fully unfolding all definitions can result in very large types that are slow for a machine to process and difficult for users to understand.
Definitions produced with `abbrev` are marked as reducible.

[←1.2. Types](Getting-to-Know-Lean/Types/#getting-to-know-types "1.2. Types")[1.4. Structures→](Getting-to-Know-Lean/Structures/#structures "1.4. Structures")
