# Study guide: 3.6. Coercions 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **3.6. Coercions 🔗** — In mathematics, it is common to use the same symbol to stand for different aspects of some object in different contexts.
- **3.6.1. Strings and Paths 🔗** — In the source code to feline , a String is converted to a FilePath using the anonymous constructor syntax.
- **3.6.2. Positive Numbers 🔗** — Every positive number corresponds to a natural number.
- **3.6.3. Chaining Coercions 🔗** — When searching for coercions, Lean will attempt to assemble a coercion out of a chain of smaller coercions.
- **3.6.4. Non-Empty Lists and Dependent Coercions 🔗** — An instance of Coe α β makes sense when the type β has a value that can represent each value from the type α .
- **3.6.5. Coercing to Types 🔗** — In mathematics, it is common to have a concept that consists of a set equipped with additional structure.
- **3.6.6. Coercing to Functions 🔗** — Many datatypes that occur regularly in programming consist of a function along with some extra information about it.
- **3.6.6.1. Aside: JSON as a String 🔗** — It can be a bit difficult to understand JSON when encoded as Lean objects.
- **3.6.7. Messages You May Meet 🔗** — Natural number literals are overloaded with the OfNat type class.
- **3.6.8. Design Considerations 🔗** — Coercions are a powerful tool that should be used responsibly.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←3.5. Standard Classes](Overloading-and-Type-Classes/Standard-Classes/#standard-classes "3.5. Standard Classes")[3.7. Additional Conveniences→](Overloading-and-Type-Classes/Additional-Conveniences/#type-class-conveniences "3.7. Additional Conveniences")

# 3.6. Coercions[🔗](find/?domain=Verso.Genre.Manual.section&name=coercions "Permalink")

In mathematics, it is common to use the same symbol to stand for different aspects of some object in different contexts.
For example, if a ring is referred to in a context where a set is expected, then it is understood that the ring's underlying set is what's intended.
In programming languages, it is common to have rules to automatically translate values of one type into values of another type.
Java allows a `byte` to be automatically promoted to an `int`, and Kotlin allows a non-nullable type to be used in a context that expects a nullable version of the type.

In Lean, both purposes are served by a mechanism called *coercions*.
When Lean encounters an expression of one type in a context that expects a different type, it will attempt to coerce the expression before reporting a type error.
Unlike Java, C, and Kotlin, the coercions are extensible by defining instances of type classes.

## 3.6.1. Strings and Paths[🔗](find/?domain=Verso.Genre.Manual.section&name=string-path-coercion "Permalink")

In the [source code to `feline`](Hello___-World___/Worked-Example___--cat/#handling-input), a `String` is converted to a `FilePath` using the anonymous constructor syntax.
In fact, this was not necessary: Lean defines a coercion from `String` to `FilePath`, so a string can be used in a position where a path is expected.
Even though the function `IO.FS.readFile` has type `System.FilePath → IO String`, the following code is accepted by Lean:

`def fileDumper : IO Unit := do
let stdin ← IO.getStdin
let stdout ← IO.getStdout
stdout.putStr "Which file? "
stdout.flush
let f := (← stdin.getLine).trimAscii.copy
stdout.putStrLn s!"'The file {f}' contains:"
stdout.putStrLn (← IO.FS.readFile f)`

`String.trimAscii` removes leading and trailing whitespace from a string, returning a [string slice](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#--tech-term-string-slices) that is converted back to a string using `String.Slice.copy`.
On the last line of `fileDumper`, the coercion from `String` to `FilePath` automatically converts `f`, so it is not necessary to write `IO.FS.readFile ⟨f⟩`.

## 3.6.2. Positive Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=positive-number-coercion "Permalink")

Every positive number corresponds to a natural number.
The function `Pos.toNat` that was defined earlier converts a `Pos` to the corresponding `Nat`:

`def Pos.toNat : Pos → Nat
| Pos.one => 1
| Pos.succ n => n.toNat + 1`

The function `List.drop`, with type `{α : Type} → Nat → List α → List α`, removes a prefix of a list.
Applying `List.drop` to a `Pos`, however, leads to a type error:

`[1, 2, 3, 4].drop (2 : Pos)`


```lean
Application type mismatch: The argument
  2
has type
  Pos
but is expected to have type
  Nat
in the application
  List.drop 2
```


Because the author of `List.drop` did not make it a method of a type class, it can't be overridden by defining a new instance.

The type class `Coe` describes overloaded ways of coercing from one type to another:

`class Coe (α : Type) (β : Type) where
coe : α → β`

An instance of `Coe Pos Nat` is enough to allow the prior code to work:

`instance : Coe Pos Nat where
coe x := x.toNat``[3, 4]#eval [1, 2, 3, 4].drop (2 : Pos)`


```lean
[3, 4]
```


Using `#check` shows the result of the instance search that was used behind the scenes:

`List.drop (Pos.toNat 2) [1, 2, 3, 4] : List Nat#check [1, 2, 3, 4].drop (2 : Pos)`


```lean
List.drop (Pos.toNat 2) [1, 2, 3, 4] : List Nat
```


## 3.6.3. Chaining Coercions[🔗](find/?domain=Verso.Genre.Manual.section&name=chaining-coercions "Permalink")

When searching for coercions, Lean will attempt to assemble a coercion out of a chain of smaller coercions.
For example, there is already a coercion from `Nat` to `Int`.
Because of that instance, combined with the `Coe Pos Nat` instance, the following code is accepted:

`def oneInt : Int := Pos.one`

This definition uses two coercions: from `Pos` to `Nat`, and then from `Nat` to `Int`.

The Lean compiler does not get stuck in the presence of circular coercions.
For example, even if two types `A` and `B` can be coerced to one another, their mutual coercions can be used to find a path:

`inductive A where
| a
inductive B where
| b
instance : Coe A B where
coe _ := B.b
instance : Coe B A where
coe _ := A.a
instance : Coe Unit A where
coe _ := A.a
def coercedToB : B := ()`

Remember: the double parentheses `()` is short for the constructor `Unit.unit`.
After deriving a `Repr B` instance with `deriving instance Repr for B`,

`B.b#eval coercedToB`

results in:


```lean
B.b
```


The `Option` type can be used similarly to nullable types in C# and Kotlin: the `none` constructor represents the absence of a value.
The Lean standard library defines a coercion from any type `α` to `Option α` that wraps the value in `some`.
This allows option types to be used in a manner even more similar to nullable types, because `some` can be omitted.
For instance, the function `List.last?` that finds the last entry in a list can be written without a `some` around the return value `x`:

`def List.last? : List α → Option α
| [] => none
| [x] => x
| _ :: x :: xs => last? (x :: xs)`

Instance search finds the coercion, and inserts a call to `coe`, which wraps the argument in `some`.
These coercions can be chained, so that nested uses of `Option` don't require nested `some` constructors:

`def perhapsPerhapsPerhaps : Option (Option (Option String)) :=
"Please don't tell me"`

Coercions are only activated automatically when Lean encounters a mismatch between an inferred type and a type that is imposed from the rest of the program.
In cases with other errors, coercions are not activated.
For example, if the error is that an instance is missing, coercions will not be used:

`` def perhapsPerhapsPerhapsNat : Option (Option (Option Nat)) :=
failed to synthesize instance of type class
OfNat (Option (Option (Option Nat))) 392
numerals are polymorphic in Lean, but the numeral `392` cannot be used in a context where the expected type is
Option (Option (Option Nat))
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.392 ``


```lean
failed to synthesize instance of type class
  OfNat (Option (Option (Option Nat))) 392
numerals are polymorphic in Lean, but the numeral `392` cannot be used in a context where the expected type is
  Option (Option (Option Nat))
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


This can be worked around by manually indicating the desired type to be used for `OfNat`:

`def perhapsPerhapsPerhapsNat : Option (Option (Option Nat)) :=
(392 : Nat)`

Additionally, coercions can be manually inserted using an up arrow:

`def perhapsPerhapsPerhapsNat : Option (Option (Option Nat)) :=
↑(392 : Nat)`

In some cases, this can be used to ensure that Lean finds the right instances.
It can also make the programmer's intentions more clear.

## 3.6.4. Non-Empty Lists and Dependent Coercions[🔗](find/?domain=Verso.Genre.Manual.section&name=CoeDep "Permalink")

An instance of `Coe α β` makes sense when the type `β` has a value that can represent each value from the type `α`.
Coercing from `Nat` to `Int` makes sense, because the type `Int` contains all the natural numbers, but a coercion from `Int` to `Nat` is a poor idea because `Nat` does not contain the negative numbers.
Similarly, a coercion from non-empty lists to ordinary lists makes sense because the `List` type can represent every non-empty list:

`instance : Coe (NonEmptyList α) (List α) where
coe
| { head := x, tail := xs } => x :: xs`

This allows non-empty lists to be used with the entire `List` API.

On the other hand, it is impossible to write an instance of `Coe (List α) (NonEmptyList α)`, because there's no non-empty list that can represent the empty list.
This limitation can be worked around by using another version of coercions, which are called *dependent coercions*.
Dependent coercions can be used when the ability to coerce from one type to another depends on which particular value is being coerced.
Just as the `OfNat` type class takes the particular `Nat` being overloaded as a parameter, dependent coercion takes the value being coerced as a parameter:

`class CoeDep (α : Type) (x : α) (β : Type) where
coe : β`

This is a chance to select only certain values, either by imposing further type class constraints on the value or by writing certain constructors directly.
For example, any `List` that is not actually empty can be coerced to a `NonEmptyList`:

`instance : CoeDep (List α) (x :: xs) (NonEmptyList α) where
coe := { head := x, tail := xs }`

## 3.6.5. Coercing to Types[🔗](find/?domain=Verso.Genre.Manual.section&name=CoeSort "Permalink")

In mathematics, it is common to have a concept that consists of a set equipped with additional structure.
For example, a monoid is some set `S`, an element `s` of `S`, and an associative binary operator on `S`, such that `s` is neutral on the left and right of the operator.
`S` is referred to as the “carrier set” of the monoid.
The natural numbers with zero and addition form a monoid, because addition is associative and adding zero to any number is the identity.
Similarly, the natural numbers with one and multiplication also form a monoid.
Monoids are also widely used in functional programming: lists, the empty list, and the append operator form a monoid, as do strings, the empty string, and string append:

`structure Monoid where
Carrier : Type
neutral : Carrier
op : Carrier → Carrier → Carrier
def natMulMonoid : Monoid :=
{ Carrier := Nat, neutral := 1, op := (· * ·) }
def natAddMonoid : Monoid :=
{ Carrier := Nat, neutral := 0, op := (· + ·) }
def stringMonoid : Monoid :=
{ Carrier := String, neutral := "", op := String.append }
def listMonoid (α : Type) : Monoid :=
{ Carrier := List α, neutral := [], op := List.append }`

Given a monoid, it is possible to write the `foldMap` function that, in a single pass, transforms the entries in a list into a monoid's carrier set and then combines them using the monoid's operator.
Because monoids have a neutral element, there is a natural result to return when the list is empty, and because the operator is associative, clients of the function don't have to care whether the recursive function combines elements from left to right or from right to left.

`def foldMap (M : Monoid) (f : α → M.Carrier) (xs : List α) : M.Carrier :=
let rec go (soFar : M.Carrier) : List α → M.Carrier
| [] => soFar
| y :: ys => go (M.op soFar (f y)) ys
go M.neutral xs`

Even though a monoid consists of three separate pieces of information, it is common to just refer to the monoid's name in order to refer to its set.
Instead of saying “Let A be a monoid and let *x* and *y* be elements of its carrier set”, it is common to say “Let *A* be a monoid and let *x* and *y* be elements of *A*”.
This practice can be encoded in Lean by defining a new kind of coercion, from the monoid to its carrier set.

The `CoeSort` class is just like the `Coe` class, with the exception that the target of the coercion must be a *sort*, namely `Type` or `Prop`.
The term *sort* in Lean refers to these types that classify other types—`Type` classifies types that themselves classify data, and `Prop` classifies propositions that themselves classify evidence of their truth.
Just as `Coe` is checked when a type mismatch occurs, `CoeSort` is used when something other than a sort is provided in a context where a sort would be expected.

The coercion from a monoid into its carrier set extracts the carrier:

`instance : CoeSort Monoid Type where
coe m := m.Carrier`

With this coercion, the type signatures become less bureaucratic:

`def foldMap (M : Monoid) (f : α → M) (xs : List α) : M :=
let rec go (soFar : M) : List α → M
| [] => soFar
| y :: ys => go (M.op soFar (f y)) ys
go M.neutral xs`

Another useful example of `CoeSort` is used to bridge the gap between `Bool` and `Prop`.
As discussed in [the section on ordering and equality](Overloading-and-Type-Classes/Standard-Classes/#equality-and-ordering), Lean's `if` expression expects the condition to be a decidable proposition rather than a `Bool`.
Programs typically need to be able to branch based on Boolean values, however.
Rather than have two kinds of `if` expression, the Lean standard library defines a coercion from `Bool` to the proposition that the `Bool` in question is equal to `true`:

`instance : CoeSort Bool Prop where
coe b := b = true`

In this case, the sort in question is `Prop` rather than `Type`.

## 3.6.6. Coercing to Functions[🔗](find/?domain=Verso.Genre.Manual.section&name=CoeFun "Permalink")

Many datatypes that occur regularly in programming consist of a function along with some extra information about it.
For example, a function might be accompanied by a name to show in logs or by some configuration data.
Additionally, putting a type in a field of a structure, similarly to the `Monoid` example, can make sense in contexts where there is more than one way to implement an operation and more manual control is needed than type classes would allow.
For example, the specific details of values emitted by a JSON serializer may be important because another application expects a particular format.
Sometimes, the function itself may be derivable from just the configuration data.

A type class called `CoeFun` can transform values from non-function types to function types.
`CoeFun` has two parameters: the first is the type whose values should be transformed into functions, and the second is an output parameter that determines exactly which function type is being targeted.

`class CoeFun (α : Type) (makeFunctionType : outParam (α → Type)) where
coe : (x : α) → makeFunctionType x`

The second parameter is itself a function that computes a type.
In Lean, types are first-class and can be passed to functions or returned from them, just like anything else.

For example, a function that adds a constant amount to its argument can be represented as a wrapper around the amount to add, rather than by defining an actual function:

`structure Adder where
howMuch : Nat`

A function that adds five to its argument has a `5` in the `howMuch` field:

`def add5 : Adder := ⟨5⟩`

This `Adder` type is not a function, and applying it to an argument results in an error:

`#eval Function expected at
add5
but this term has type
Adder

Note: Expected a function because this term is being applied to the argument
3add5 3`


```lean
Function expected at
  add5
but this term has type
  Adder

Note: Expected a function because this term is being applied to the argument
  3
```


Defining a `CoeFun` instance causes Lean to transform the adder into a function with type `Nat → Nat`:

`instance : CoeFun Adder (fun _ => Nat → Nat) where
coe a := (· + a.howMuch)``8#eval add5 3`


```lean
8
```


Because all `Adder`s should be transformed into `Nat → Nat` functions, the argument to `CoeFun`'s second parameter was ignored.

When the value itself is needed to determine the right function type, then `CoeFun`'s second parameter is no longer ignored.
For example, given the following representation of JSON values:

`inductive JSON where
| true : JSON
| false : JSON
| null : JSON
| string : String → JSON
| number : Float → JSON
| object : List (String × JSON) → JSON
| array : List JSON → JSON`

a JSON serializer is a structure that tracks the type it knows how to serialize along with the serialization code itself:

`structure Serializer where
Contents : Type
serialize : Contents → JSON`

A serializer for strings need only wrap the provided string in the `JSON.string` constructor:

`def Str : Serializer :=
{ Contents := String,
serialize := JSON.string
}`

Viewing JSON serializers as functions that serialize their argument requires extracting the inner type of serializable data:

`instance : CoeFun Serializer (fun s => s.Contents → JSON) where
coe s := s.serialize`

Given this instance, a serializer can be applied directly to an argument:

`def buildResponse (title : String) (R : Serializer)
(record : R.Contents) : JSON :=
JSON.object [
("title", JSON.string title),
("status", JSON.number 200),
("record", R record)
]`

The serializer can be passed directly to `buildResponse`:

`JSON.object
[("title", JSON.string "Functional Programming in Lean"),
("status", JSON.number 200.000000),
("record", JSON.string "Programming is fun!")]#eval buildResponse "Functional Programming in Lean" Str "Programming is fun!"`


```lean
JSON.object
  [("title", JSON.string "Functional Programming in Lean"),
   ("status", JSON.number 200.000000),
   ("record", JSON.string "Programming is fun!")]
```


### 3.6.6.1. Aside: JSON as a String[🔗](find/?domain=Verso.Genre.Manual.section&name=json-string "Permalink")

It can be a bit difficult to understand JSON when encoded as Lean objects.
To help make sure that the serialized response was what was expected, it can be convenient to write a simple converter from `JSON` to `String`.
The first step is to simplify the display of numbers.
`JSON` doesn't distinguish between integers and floating point numbers, and the type `Float` is used to represent both.
In Lean, `Float.toString` includes a number of trailing zeros:

`"5.000000"#eval (5 : Float).toString`


```lean
"5.000000"
```


The solution is to write a little function that cleans up the presentation by dropping all trailing zeros, followed by a trailing decimal point:

`def dropDecimals (numString : String) : String :=
if numString.contains '.' then
let noTrailingZeros := numString.dropEndWhile (· == '0')
(noTrailingZeros.dropEndWhile (· == '.')).copy
else numString`

With this definition, `dropDecimals (5 : Float).toString` yields `5`, and `dropDecimals (5.2 : Float).toString` yields `5.2`.

The next step is to define a helper function to append a list of strings with a separator in between them:

`def String.separate (sep : String) (strings : List String) : String :=
match strings with
| [] => ""
| x :: xs => String.join (x :: xs.map (sep ++ ·))`

This function is useful to account for comma-separated elements in JSON arrays and objects.
`", ".separate ["1", "2"]` yields `"1, 2"`, `", ".separate ["1"]` yields `"1"`, and `", ".separate []` yields `""`.
In the Lean standard library, this function is called `String.intercalate`.

Finally, a string escaping procedure is needed for JSON strings, so that the Lean string containing `"Hello!"` can be output as `"\"Hello!\""`.
Fortunately, the Lean compiler contains an internal function for escaping JSON strings already, called `Lean.Json.escape`.
To access this function, add `import Lean` to the beginning of your file.

The function that emits a string from a `JSON` value is declared `partial` because Lean cannot see that it terminates.
This is because recursive calls to `asString` occur in functions that are being applied by `List.map`, and this pattern of recursion is complicated enough that Lean cannot see that the recursive calls are actually being performed on smaller values.
In an application that just needs to produce JSON strings and doesn't need to mathematically reason about the process, having the function be `partial` is not likely to cause problems.

`partial def JSON.asString (val : JSON) : String :=
match val with
| true => "true"
| false => "false"
| null => "null"
| string s => "\"" ++ Lean.Json.escape s ++ "\""
| number n => dropDecimals n.toString
| object members =>
let memberToString mem :=
"\"" ++ Lean.Json.escape mem.fst ++ "\": " ++ asString mem.snd
"{" ++ ", ".separate (members.map memberToString) ++ "}"
| array elements =>
"[" ++ ", ".separate (elements.map asString) ++ "]"`

With this definition, the output of serialization is easier to read:

`"{\"title\": \"Functional Programming in Lean\", \"status\": 200, \"record\": \"Programming is fun!\"}"#eval (buildResponse "Functional Programming in Lean" Str "Programming is fun!").asString`


```lean
"{\"title\": \"Functional Programming in Lean\", \"status\": 200, \"record\": \"Programming is fun!\"}"
```


## 3.6.7. Messages You May Meet[🔗](find/?domain=Verso.Genre.Manual.section&name=coercion-messages "Permalink")

Natural number literals are overloaded with the `OfNat` type class.
Because coercions fire in cases where types don't match, rather than in cases of missing instances, a missing `OfNat` instance for a type does not cause a coercion from `Nat` to be applied:

`` def perhapsPerhapsPerhapsNat : Option (Option (Option Nat)) :=
failed to synthesize instance of type class
OfNat (Option (Option (Option Nat))) 392
numerals are polymorphic in Lean, but the numeral `392` cannot be used in a context where the expected type is
Option (Option (Option Nat))
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.392 ``


```lean
failed to synthesize instance of type class
  OfNat (Option (Option (Option Nat))) 392
numerals are polymorphic in Lean, but the numeral `392` cannot be used in a context where the expected type is
  Option (Option (Option Nat))
due to the absence of the instance above

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


## 3.6.8. Design Considerations[🔗](find/?domain=Verso.Genre.Manual.section&name=coercion-design-considerations "Permalink")

Coercions are a powerful tool that should be used responsibly.
On the one hand, they can allow an API to naturally follow the everyday rules of the domain being modeled.
This can be the difference between a bureaucratic mess of manual conversion functions and a clear program.
As Abelson and Sussman wrote in the preface to *Structure and Interpretation of Computer Programs* (MIT Press, 1996),

> Programs must be written for people to read, and only incidentally for machines to execute.

Coercions, used wisely, are a valuable means of achieving readable code that can serve as the basis for communication with domain experts.
APIs that rely heavily on coercions have a number of important limitations, however.
Think carefully about these limitations before using coercions in your own libraries.

First off, coercions are only applied in contexts where enough type information is available for Lean to know all of the types involved, because there are no output parameters in the coercion type classes. This means that a return type annotation on a function can be the difference between a type error and a successfully applied coercion.
For example, the coercion from non-empty lists to lists makes the following program work:

`def lastSpider : Option String :=
List.getLast? idahoSpiders`

On the other hand, if the type annotation is omitted, then the result type is unknown, so Lean is unable to find the coercion:

`def lastSpider :=
List.getLast? Application type mismatch: The argument
idahoSpiders
has type
NonEmptyList String
but is expected to have type
List ?m.3
in the application
List.getLast? idahoSpidersidahoSpiders`


```lean
Application type mismatch: The argument
  idahoSpiders
has type
  NonEmptyList String
but is expected to have type
  List ?m.3
in the application
  List.getLast? idahoSpiders
```


More generally, when a coercion is not applied for some reason, the user receives the original type error, which can make it difficult to debug chains of coercions.

Finally, coercions are not applied in the context of field accessor notation.
This means that there is still an important difference between expressions that need to be coerced and those that don't, and this difference is visible to users of your API.

[←3.5. Standard Classes](Overloading-and-Type-Classes/Standard-Classes/#standard-classes "3.5. Standard Classes")[3.7. Additional Conveniences→](Overloading-and-Type-Classes/Additional-Conveniences/#type-class-conveniences "3.7. Additional Conveniences")
