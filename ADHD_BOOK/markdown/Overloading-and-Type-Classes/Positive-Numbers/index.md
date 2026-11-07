# Study guide: 3.1. Positive Numbers 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **3.1. Positive Numbers 🔗** — In some applications, only positive numbers make sense.
- **3.1.1. Classes and Instances 🔗** — A type class consists of a name, some parameters, and a collection of methods .
- **3.1.2. Overloaded Addition 🔗** — Lean's built-in addition operator is syntactic sugar for a type class called HAdd , which flexibly allows the arguments to addition to have different types.
- **3.1.3. Conversion to Strings 🔗** — Another useful built-in class is called ToString .
- **3.1.4. Overloaded Multiplication 🔗** — For multiplication, there is a type class called HMul that allows mixed argument types, just like HAdd .
- **3.1.5. Literal Numbers 🔗** — It is quite inconvenient to write out a sequence of constructors for positive numbers.
- **3.1.6.1. Another Representation 🔗** — An alternative way to represent a positive number is as the successor of some Nat .
- **3.1.6.2. Even Numbers 🔗** — Define a datatype that represents only even numbers.
- **3.1.6.3. HTTP Requests 🔗** — An HTTP request begins with an identification of a HTTP method, such as GET or POST , along with a URI and an HTTP version.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←3. Overloading and Type Classes](Overloading-and-Type-Classes/#type-classes "3. Overloading and Type Classes")[3.2. Type Classes and Polymorphism→](Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/#tc-polymorphism "3.2. Type Classes and Polymorphism")

# 3.1. Positive Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=positive-numbers "Permalink")

In some applications, only positive numbers make sense.
For example, compilers and interpreters typically use one-indexed line and column numbers for source positions, and a datatype that represents only non-empty lists will never report a length of zero.
Rather than relying on natural numbers, and littering the code with assertions that the number is not zero, it can be useful to design a datatype that represents only positive numbers.

One way to represent positive numbers is very similar to `Nat`, except with `one` as the base case instead of `zero`:

`inductive Pos : Type where
| one : Pos
| succ : Pos → Pos`

This datatype represents exactly the intended set of values, but it is not very convenient to use.
For example, numeric literals are rejected:

`` def seven : Pos := failed to synthesize instance of type class
OfNat Pos 7
numerals are polymorphic in Lean, but the numeral `7` cannot be used in a context where the expected type is
Pos
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.7 ``


```lean
failed to synthesize instance of type class
  OfNat Pos 7
numerals are polymorphic in Lean, but the numeral `7` cannot be used in a context where the expected type is
  Pos
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


Instead, the constructors must be used directly:

`def seven : Pos :=
Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ Pos.one)))))`

Similarly, addition and multiplication are not easy to use:

`` def fourteen : Pos := failed to synthesize instance of type class
HAdd Pos Pos ?m.3

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.seven + seven ``


```lean
failed to synthesize instance of type class
  HAdd Pos Pos ?m.3

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


`` def fortyNine : Pos := failed to synthesize instance of type class
HMul Pos Pos ?m.3

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.seven * seven ``


```lean
failed to synthesize instance of type class
  HMul Pos Pos ?m.3

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


Each of these error messages begins with `failed to synthesize`.
This indicates that the error is due to an overloaded operation that has not been implemented, and it describes the type class that must be implemented.

## 3.1.1. Classes and Instances[🔗](find/?domain=Verso.Genre.Manual.section&name=classes-and-instances "Permalink")

A type class consists of a name, some parameters, and a collection of *methods*.
The parameters describe the types for which overloadable operations are being defined, and the methods are the names and type signatures of the overloadable operations.
Once again, there is a terminology clash with object-oriented languages.
In object-oriented programming, a method is essentially a function that is connected to a particular object in memory, with special access to the object's private state.
Objects are interacted with via their methods.
In Lean, the term “method” refers to an operation that has been declared to be overloadable, with no special connection to objects or values or private fields.

One way to overload addition is to define a type class named `Plus`, with an addition method named `plus`.
Once an instance of `Plus` for `Nat` has been defined, it becomes possible to add two `Nat`s using `Plus.plus`:

`8#eval Plus.plus 5 3`


```lean
8
```


Adding more instances allows `Plus.plus` to take more types of arguments.

In the following type class declaration, `Plus` is the name of the class, `α : Type` is the only argument, and `plus : α → α → α` is the only method:

`class Plus (α : Type) where
plus : α → α → α`

This declaration says that there is a type class `Plus` that overloads operations with respect to a type `α`.
In particular, there is one overloaded operation called `plus` that takes two `α`s and returns an `α`.

Type classes are first class, just as types are first class.
In particular, a type class is another kind of type.
The type of `Plus` is `Type → Type`, because it takes a type as an argument (`α`) and results in a new type that describes the overloading of `Plus`'s operation for `α`.

To overload `plus` for a particular type, write an instance:

`instance : Plus Nat where
plus := Nat.add`

The colon after `instance` indicates that `Plus Nat` is indeed a type.
Each method of class `Plus` should be assigned a value using `:=`.
In this case, there is only one method: `plus`.

By default, type class methods are defined in a namespace with the same name as the type class.
It can be convenient to `open` the namespace so that users don't need to type the name of the class first.
Parentheses in an `open` command indicate that only the indicated names from the namespace are to be made accessible:

`open Plus (plus)``8#eval plus 5 3`


```lean
8
```


Defining an addition function for `Pos` and an instance of `Plus Pos` allows `plus` to be used to add both `Pos` and `Nat` values:

`def Pos.plus : Pos → Pos → Pos
| Pos.one, k => Pos.succ k
| Pos.succ n, k => Pos.succ (n.plus k)
instance : Plus Pos where
plus := Pos.plus
def fourteen : Pos := plus seven seven`

Because there is not yet an instance of `Plus Float`, attempting to add two floating-point numbers with `plus` fails with a familiar message:

`` #eval failed to synthesize instance of type class
Plus Float

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.plus 5.2 917.25861 ``


```lean
failed to synthesize instance of type class
  Plus Float

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


These errors mean that Lean was unable to find an instance for a given type class.

## 3.1.2. Overloaded Addition[🔗](find/?domain=Verso.Genre.Manual.section&name=overloaded-addition "Permalink")

Lean's built-in addition operator is syntactic sugar for a type class called `HAdd`, which flexibly allows the arguments to addition to have different types.
`HAdd` is short for *heterogeneous addition*.
For example, an `HAdd` instance can be written to allow a `Nat` to be added to a `Float`, resulting in a new `Float`.
When a programmer writes `x + y`, it is interpreted as meaning `HAdd.hAdd x y`.

While an understanding of the full generality of `HAdd` relies on features that are discussed in [another section in this chapter](Overloading-and-Type-Classes/Controlling-Instance-Search/#out-params), there is a simpler type class called `Add` that does not allow the types of the arguments to be mixed.
The Lean libraries are set up so that an instance of `Add` will be found when searching for an instance of `HAdd` in which both arguments have the same type.

Defining an instance of `Add Pos` allows `Pos` values to use ordinary addition syntax:

`instance : Add Pos where
add := Pos.plus``def fourteen : Pos := seven + seven`

## 3.1.3. Conversion to Strings[🔗](find/?domain=Verso.Genre.Manual.section&name=conversion-to-strings "Permalink")

Another useful built-in class is called `ToString`.
Instances of `ToString` provide a standard way of converting values from a given type into strings.
For example, a `ToString` instance is used when a value occurs in an interpolated string, and it determines how the `IO.println` function used at the [beginning of the description of `IO`](Hello___-World___/Running-a-Program/#running-a-program) will display a value.

For example, one way to convert a `Pos` into a `String` is to reveal its inner structure.
The function `posToString` takes a `Bool` that determines whether to parenthesize uses of `Pos.succ`, which should be `true` in the initial call to the function and `false` in all recursive calls.

`def posToString (atTop : Bool) (p : Pos) : String :=
let paren s := if atTop then s else "(" ++ s ++ ")"
match p with
| Pos.one => "Pos.one"
| Pos.succ n => paren s!"Pos.succ {posToString false n}"`

Using this function for a `ToString` instance:

`instance : ToString Pos where
toString := posToString true`

results in informative, yet overwhelming, output:

`"There are Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ Pos.one)))))"#eval s!"There are {seven}"`


```lean
"There are Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ (Pos.succ Pos.one)))))"
```


On the other hand, every positive number has a corresponding `Nat`.
Converting it to a `Nat` and then using the `ToString Nat` instance (that is, the overloading of `ToString` for `Nat`) is a quick way to generate much shorter output:

`def Pos.toNat : Pos → Nat
| Pos.one => 1
| Pos.succ n => n.toNat + 1``instance : ToString Pos where
toString x := toString (x.toNat)``"There are 7"#eval s!"There are {seven}"`


```lean
"There are 7"
```


When more than one instance is defined, the most recent takes precedence.
Additionally, if a type has a `ToString` instance, then it can be used to display the result of `#eval` so `#eval seven` outputs `7`.

## 3.1.4. Overloaded Multiplication[🔗](find/?domain=Verso.Genre.Manual.section&name=overloaded-multiplication "Permalink")

For multiplication, there is a type class called `HMul` that allows mixed argument types, just like `HAdd`.
Just as `x + y` is interpreted as `HAdd.hAdd x y`, `x * y` is interpreted as `HMul.hMul x y`.
For the common case of multiplication of two arguments with the same type, a `Mul` instance suffices.

An instance of `Mul` allows ordinary multiplication syntax to be used with `Pos`:

`def Pos.mul : Pos → Pos → Pos
| Pos.one, k => k
| Pos.succ n, k => n.mul k + k
instance : Mul Pos where
mul := Pos.mul`

With this instance, multiplication works as expected:

`[7, 49, 14]#eval [seven * Pos.one,
seven * seven,
Pos.succ Pos.one * seven]`


```lean
[7, 49, 14]
```


## 3.1.5. Literal Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=literal-numbers "Permalink")

It is quite inconvenient to write out a sequence of constructors for positive numbers.
One way to work around the problem would be to provide a function to convert a `Nat` into a `Pos`.
However, this approach has downsides.
First off, because `Pos` cannot represent `0`, the resulting function would either convert a `Nat` to a bigger number, or it would return `Option Pos`.
Neither is particularly convenient for users.
Secondly, the need to call the function explicitly would make programs that use positive numbers much less convenient to write than programs that use `Nat`.
Having a trade-off between precise types and convenient APIs means that the precise types become less useful.

There are three type classes that are used to overload numeric literals: `Zero`, `One`, and `OfNat`.
Because many types have values that are naturally written with `0`, the `Zero` class allow these specific values to be overridden.
It is defined as follows:

`class Zero (α : Type) where
zero : α`

Because `0` is not a positive number, there should be no instance of `Zero Pos`.

Similarly, many types have values that are naturally written with `1`.
The `One` class allows these to be overridden:

`class One (α : Type) where
one : α`

An instance of `One Pos` makes perfect sense:

`instance : One Pos where
one := Pos.one`

With this instance, `1` can be used for `Pos.one`:

`1#eval (1 : Pos)`


```lean
1
```


In Lean, natural number literals are interpreted using a type class called `OfNat`:

`class OfNat (α : Type) (_ : Nat) where
ofNat : α`

This type class takes two arguments: `α` is the type for which a natural number is overloaded, and the unnamed `Nat` argument is the actual literal number that was encountered in the program.
The method `ofNat` is then used as the value of the numeric literal.
Because the class contains the `Nat` argument, it becomes possible to define only instances for those values where the number makes sense.

`OfNat` demonstrates that the arguments to type classes do not need to be types.
Because types in Lean are first-class participants in the language that can be passed as arguments to functions and given definitions with `def` and `abbrev`, there is no barrier that prevents non-type arguments in positions where a less-flexible language could not permit them.
This flexibility allows overloaded operations to be provided for particular values as well as particular types.
Additionally, it allows the Lean standard library to arrange for there to be a `Zero α` instance whenever there's an `OfNat α 0` instance, and vice versa.
Similarly, an instance of `One α` implies an instance of `OfNat α 1`, just as an instance of `OfNat α 1` implies an instance of `One α`.

A sum type that represents natural numbers less than four can be defined as follows:

`inductive LT4 where
| zero
| one
| two
| three`

While it would not make sense to allow *any* literal number to be used for this type, numbers less than four clearly make sense:

`instance : OfNat LT4 0 where
ofNat := LT4.zero
instance : OfNat LT4 1 where
ofNat := LT4.one
instance : OfNat LT4 2 where
ofNat := LT4.two
instance : OfNat LT4 3 where
ofNat := LT4.three`

With these instances, the following examples work:

`LT4.three#eval (3 : LT4)`


```lean
LT4.three
```


`LT4.zero#eval (0 : LT4)`


```lean
LT4.zero
```


On the other hand, out-of-bounds literals are still not allowed:

`` #eval (failed to synthesize instance of type class
OfNat LT4 4
numerals are polymorphic in Lean, but the numeral `4` cannot be used in a context where the expected type is
LT4
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.4 : LT4) ``


```lean
failed to synthesize instance of type class
  OfNat LT4 4
numerals are polymorphic in Lean, but the numeral `4` cannot be used in a context where the expected type is
  LT4
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


For `Pos`, the `OfNat` instance should work for *any* `Nat` other than `Nat.zero`.
Another way to phrase this is to say that for all natural numbers `n`, the instance should work for `n + 1`.
Just as names like `α` automatically become implicit arguments to functions that Lean fills out on its own, instances can take automatic implicit arguments.
In this instance, the argument `n` stands for any `Nat`, and the instance is defined for a `Nat` that's one greater:

`instance : OfNat Pos (n + 1) where
ofNat :=
let rec natPlusOne : Nat → Pos
| 0 => Pos.one
| k + 1 => Pos.succ (natPlusOne k)
natPlusOne n`

Because `n` stands for a `Nat` that's one less than what the user wrote, the helper function `natPlusOne` returns a `Pos` that's one greater than its argument.
This makes it possible to use natural number literals for positive numbers, but not for zero:

`def eight : Pos := 8``` def zero : Pos := failed to synthesize instance of type class
OfNat Pos 0
numerals are polymorphic in Lean, but the numeral `0` cannot be used in a context where the expected type is
Pos
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.0 ``


```lean
failed to synthesize instance of type class
  OfNat Pos 0
numerals are polymorphic in Lean, but the numeral `0` cannot be used in a context where the expected type is
  Pos
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


## 3.1.6. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=positive-numbers-exercises "Permalink")

### 3.1.6.1. Another Representation[🔗](find/?domain=Verso.Genre.Manual.section&name=positive-numbers-another-representation "Permalink")

An alternative way to represent a positive number is as the successor of some `Nat`.
Replace the definition of `Pos` with a structure whose constructor is named `succ` that contains a `Nat`:

`structure Pos where
succ ::
pred : Nat`

Define instances of `Add`, `Mul`, `ToString`, and `OfNat` that allow this version of `Pos` to be used conveniently.

### 3.1.6.2. Even Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=even-numbers-ex "Permalink")

Define a datatype that represents only even numbers. Define instances of `Add`, `Mul`, and `ToString` that allow it to be used conveniently.
`OfNat` requires a feature that is introduced in [the next section](Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/#tc-polymorphism).

### 3.1.6.3. HTTP Requests[🔗](find/?domain=Verso.Genre.Manual.section&name=http-request-ex "Permalink")

An HTTP request begins with an identification of a HTTP method, such as `GET` or `POST`, along with a URI and an HTTP version.
Define an inductive type that represents an interesting subset of the HTTP methods, and a structure that represents HTTP responses.
Responses should have a `ToString` instance that makes it possible to debug them.
Use a type class to associate different `IO` actions with each HTTP method, and write a test harness as an `IO` action that calls each method and prints the result.

[←3. Overloading and Type Classes](Overloading-and-Type-Classes/#type-classes "3. Overloading and Type Classes")[3.2. Type Classes and Polymorphism→](Overloading-and-Type-Classes/Type-Classes-and-Polymorphism/#tc-polymorphism "3.2. Type Classes and Polymorphism")


> **Review needed:** The following headings have no short source sentence: 3.1.6. Exercises 🔗