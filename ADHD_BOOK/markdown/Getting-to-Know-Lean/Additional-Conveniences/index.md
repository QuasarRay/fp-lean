# Study guide: 1.8. Additional Conveniences 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.8. Additional Conveniences 🔗** — Lean contains a number of convenience features that make programs much more concise.
- **1.8.1. Automatic Implicit Parameters 🔗** — When writing polymorphic functions in Lean, it is typically not necessary to list all the implicit parameters.
- **1.8.2. Pattern-Matching Definitions 🔗** — When defining functions with def , it is quite common to name an argument and then immediately use it with pattern matching.
- **1.8.3. Local Definitions 🔗** — It is often useful to name intermediate steps in a computation.
- **1.8.4. Type Inference 🔗** — In many situations, Lean can automatically determine an expression's type.
- **1.8.5. Simultaneous Matching 🔗** — Pattern-matching expressions, just like pattern-matching definitions, can match on multiple values at once.
- **1.8.6. Natural Number Patterns 🔗** — In the section on datatypes and patterns , even was defined like this:
- **1.8.7. Anonymous Functions 🔗** — Functions in Lean need not be defined at the top level.
- **1.8.8. Namespaces 🔗** — Each name in Lean occurs in a namespace , which is a collection of names.
- **1.8.9. if let 🔗** — When consuming values that have a sum type, it is often the case that only a single constructor is of interest.
- **1.8.10. Positional Structure Arguments 🔗** — The section on structures presents two ways of constructing structures:
- **1.8.11. String Interpolation 🔗** — In Lean, prefixing a string with s!

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.7. Characters, Strings, and Slices](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#chars-strings-slices "1.7. Characters, Strings, and Slices")[1.9. Summary→](Getting-to-Know-Lean/Summary/#getting-to-know-summary "1.9. Summary")

# 1.8. Additional Conveniences[🔗](find/?domain=Verso.Genre.Manual.section&name=getting-to-know-conveniences "Permalink")

Lean contains a number of convenience features that make programs much more concise.

## 1.8.1. Automatic Implicit Parameters[🔗](find/?domain=Verso.Genre.Manual.section&name=automatic-implicit-parameters "Permalink")

When writing polymorphic functions in Lean, it is typically not necessary to list all the implicit parameters.
Instead, they can simply be mentioned.
If Lean can determine their type, then they are automatically inserted as implicit parameters.
In other words, the previous definition of `length`:

`def length {α : Type} (xs : List α) : Nat :=
match xs with
| [] => 0
| y :: ys => Nat.succ (length ys)`

can be written without `{α : Type}`:

`def length (xs : List α) : Nat :=
match xs with
| [] => 0
| y :: ys => Nat.succ (length ys)`

This can greatly simplify highly polymorphic definitions that take many implicit parameters.

## 1.8.2. Pattern-Matching Definitions[🔗](find/?domain=Verso.Genre.Manual.section&name=pattern-matching-definitions "Permalink")

When defining functions with `def`, it is quite common to name an argument and then immediately use it with pattern matching.
For instance, in `length`, the argument `xs` is used only in `match`.
In these situations, the cases of the `match` expression can be written directly, without naming the argument at all.

The first step is to move the arguments' types to the right of the colon, so the return type is a function type.
For instance, the type of `length` is `List α → Nat`.
Then, replace the `:=` with each case of the pattern match:

`def length : List α → Nat
| [] => 0
| y :: ys => Nat.succ (length ys)`

This syntax can also be used to define functions that take more than one argument.
In this case, their patterns are separated by commas.
For instance, `drop` takes a number `n` and a list, and returns the list after removing the first `n` entries.

`def drop : Nat → List α → List α
| Nat.zero, xs => xs
| _, [] => []
| Nat.succ n, x :: xs => drop n xs`

Named arguments and patterns can also be used in the same definition.
For instance, a function that takes a default value and an optional value, and returns the default when the optional value is `none`, can be written:

`def fromOption (default : α) : Option α → α
| none => default
| some x => x`

This function is called `Option.getD` in the standard library, and can be called with dot notation:

`"salmonberry"#eval (some "salmonberry").getD ""`


```lean
"salmonberry"
```


`""#eval none.getD ""`


```lean
""
```


## 1.8.3. Local Definitions[🔗](find/?domain=Verso.Genre.Manual.section&name=local-definitions "Permalink")

It is often useful to name intermediate steps in a computation.
In many cases, intermediate values represent useful concepts all on their own, and naming them explicitly can make the program easier to read.
In other cases, the intermediate value is used more than once.
As in most other languages, writing down the same code twice in Lean causes it to be computed twice, while saving the result in a variable leads to the result of the computation being saved and re-used.

For instance, `unzip` is a function that transforms a list of pairs into a pair of lists.
When the list of pairs is empty, then the result of `unzip` is a pair of empty lists.
When the list of pairs has a pair at its head, then the two fields of the pair are added to the result of unzipping the rest of the list.
This definition of `unzip` follows that description exactly:

`def unzip : List (α × β) → List α × List β
| [] => ([], [])
| (x, y) :: xys =>
(x :: (unzip xys).fst, y :: (unzip xys).snd)`

Unfortunately, there is a problem: this code is slower than it needs to be.
Each entry in the list of pairs leads to two recursive calls, which makes this function take exponential time.
However, both recursive calls will have the same result, so there is no reason to make the recursive call twice.

In Lean, the result of the recursive call can be named, and thus saved, using `let`.
Local definitions with `let` resemble top-level definitions with `def`: it takes a name to be locally defined, arguments if desired, a type signature, and then a body following `:=`.
After the local definition, the expression in which the local definition is available (called the *body* of the `let`-expression) must be on a new line, starting at a column in the file that is less than or equal to that of the `let` keyword.
A local definition with `let` in `unzip` looks like this:

`def unzip : List (α × β) → List α × List β
| [] => ([], [])
| (x, y) :: xys =>
let unzipped : List α × List β := unzip xys
(x :: unzipped.fst, y :: unzipped.snd)`

To use `let` on a single line, separate the local definition from the body with a semicolon.

Local definitions with `let` may also use pattern matching when one pattern is enough to match all cases of a datatype.
In the case of `unzip`, the result of the recursive call is a pair.
Because pairs have only a single constructor, the name `unzipped` can be replaced with a pair pattern:

`def unzip : List (α × β) → List α × List β
| [] => ([], [])
| (x, y) :: xys =>
let (xs, ys) : List α × List β := unzip xys
(x :: xs, y :: ys)`

Judicious use of patterns with `let` can make code easier to read, compared to writing the accessor calls by hand.

The biggest difference between `let` and `def` is that recursive `let` definitions must be explicitly indicated by writing `let rec`.
For instance, one way to reverse a list involves a recursive helper function, as in this definition:

`def reverse (xs : List α) : List α :=
let rec helper : List α → List α → List α
| [], soFar => soFar
| y :: ys, soFar => helper ys (y :: soFar)
helper xs []`

The helper function walks down the input list, moving one entry at a time over to `soFar`.
When it reaches the end of the input list, `soFar` contains a reversed version of the input.

## 1.8.4. Type Inference[🔗](find/?domain=Verso.Genre.Manual.section&name=type-inference "Permalink")

In many situations, Lean can automatically determine an expression's type.
In these cases, explicit types may be omitted from both top-level definitions (with `def`) and local definitions (with `let`).
For example, the recursive call to `unzip` does not need an annotation:

`def unzip : List (α × β) → List α × List β
| [] => ([], [])
| (x, y) :: xys =>
let unzipped := unzip xys
(x :: unzipped.fst, y :: unzipped.snd)`

As a rule of thumb, omitting the types of literal values (like strings and numbers) usually works, although Lean may pick a type for literal numbers that is more specific than the intended type.
Lean can usually determine a type for a function application, because it already knows the argument types and the return type.
Omitting return types for function definitions will often work, but function parameters typically require annotations.
Definitions that are not functions, like `unzipped` in the example, do not need type annotations if their bodies do not need type annotations, and the body of this definition is a function application.

Omitting the return type for `unzip` is possible when using an explicit `match` expression:

`def unzip (pairs : List (α × β)) :=
match pairs with
| [] => ([], [])
| (x, y) :: xys =>
let unzipped := unzip xys
(x :: unzipped.fst, y :: unzipped.snd)`

Generally speaking, it is a good idea to err on the side of too many, rather than too few, type annotations.
First off, explicit types communicate assumptions about the code to readers.
Even if Lean can determine the type on its own, it can still be easier to read code without having to repeatedly query Lean for type information.
Secondly, explicit types help localize errors.
The more explicit a program is about its types, the more informative the error messages can be.
This is especially important in a language like Lean that has a very expressive type system.
Thirdly, explicit types make it easier to write the program in the first place.
The type is a specification, and the compiler's feedback can be a helpful tool in writing a program that meets the specification.
Finally, Lean's type inference is a best-effort system.
Because Lean's type system is so expressive, there is no “best” or most general type to find for all expressions.
This means that even if you get a type, there's no guarantee that it's the *right* type for a given application.
For instance, `14` can be a `Nat` or an `Int`:

`14 : Nat#check 14`


```lean
14 : Nat
```


`14 : Int#check (14 : Int)`


```lean
14 : Int
```


Missing type annotations can give confusing error messages.
Omitting all types from the definition of `unzip`:

`def unzip pairs :=
match pairs with
| Invalid match expression: This pattern contains metavariables:
[][] => ([], [])
| (x, y) :: xys =>
let unzipped := unzip xys
(x :: unzipped.fst, y :: unzipped.snd)`

leads to a message about the `match` expression:


```lean
Invalid match expression: This pattern contains metavariables:
  []
```


This is because `match` needs to know the type of the value being inspected, but that type was not available.
A “metavariable” is an unknown part of a program, written `?m.XYZ` in error messages—they are described in the [section on Polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism).
In this program, the type annotation on the argument is required.

Even some very simple programs require type annotations.
For instance, the identity function just returns whatever argument it is passed.
With argument and type annotations, it looks like this:

`def id (x : α) : α := x`

Lean is capable of determining the return type on its own:

`def id (x : α) := x`

Omitting the argument type, however, causes an error:

`` def Failed to infer type of definition `id`id Failed to infer type of binder `x`x := x ``


```lean
Failed to infer type of binder `x`
```


In general, messages that say something like “failed to infer” or that mention metavariables are often a sign that more type annotations are necessary.
Especially while still learning Lean, it is useful to provide most types explicitly.

## 1.8.5. Simultaneous Matching[🔗](find/?domain=Verso.Genre.Manual.section&name=simultaneous-matching "Permalink")

Pattern-matching expressions, just like pattern-matching definitions, can match on multiple values at once.
Both the expressions to be inspected and the patterns that they match against are written with commas between them, similarly to the syntax used for definitions.
Here is a version of `drop` that uses simultaneous matching:

`def drop (n : Nat) (xs : List α) : List α :=
match n, xs with
| Nat.zero, ys => ys
| _, [] => []
| Nat.succ n , y :: ys => drop n ys`

Simultaneous matching resembles matching on a pair, but there is an important difference.
Lean tracks the connection between the expression being matched and the patterns, and this information is used for purposes that include checking for termination and propagating static type information.
As a result, the version of `sameLength` that matches a pair is rejected by the termination checker, because the connection between `xs` and `x :: xs'` is obscured by the intervening pair:

`` def fail to show termination for
sameLength
with errors
failed to infer structural recursion:
Not considering parameter α of sameLength:
it is unchanged in the recursive calls
Not considering parameter β of sameLength:
it is unchanged in the recursive calls
Cannot use parameter xs:
failed to eliminate recursive application
sameLength xs' ys'
Cannot use parameter ys:
failed to eliminate recursive application
sameLength xs' ys'


Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
xs ys
1) 1816:28-46 ? ?
Please use `termination_by` to specify a decreasing measure.sameLength (xs : List α) (ys : List β) : Bool :=
match (xs, ys) with
| ([], []) => true
| (x :: xs', y :: ys') => sameLength xs' ys'
| _ => false ``


```lean
fail to show termination for
  sameLength
with errors
failed to infer structural recursion:
Not considering parameter α of sameLength:
  it is unchanged in the recursive calls
Not considering parameter β of sameLength:
  it is unchanged in the recursive calls
Cannot use parameter xs:
  failed to eliminate recursive application
    sameLength xs' ys'
Cannot use parameter ys:
  failed to eliminate recursive application
    sameLength xs' ys'


Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
              xs ys
1) 1816:28-46  ?  ?
Please use `termination_by` to specify a decreasing measure.
```


Simultaneously matching both lists is accepted:

`def sameLength (xs : List α) (ys : List β) : Bool :=
match xs, ys with
| [], [] => true
| x :: xs', y :: ys' => sameLength xs' ys'
| _, _ => false`

## 1.8.6. Natural Number Patterns[🔗](find/?domain=Verso.Genre.Manual.section&name=natural-number-patterns "Permalink")

In the section on [datatypes and patterns](Getting-to-Know-Lean/Datatypes-and-Patterns/#datatypes-and-patterns), `even` was defined like this:

`def even (n : Nat) : Bool :=
match n with
| Nat.zero => true
| Nat.succ k => not (even k)`

Just as there is special syntax to make list patterns more readable than using `List.cons` and `List.nil` directly, natural numbers can be matched using literal numbers and `+`.
For example, `even` can also be defined like this:

`def even : Nat → Bool
| 0 => true
| n + 1 => not (even n)`

In this notation, the arguments to the `+` pattern serve different roles.
Behind the scenes, the left argument (`n` above) becomes an argument to some number of `Nat.succ` patterns, and the right argument (`1` above) determines how many `Nat.succ`s to wrap around the pattern.
The explicit patterns in `halve`, which divides a `Nat` by two and drops the remainder:

`def halve : Nat → Nat
| Nat.zero => 0
| Nat.succ Nat.zero => 0
| Nat.succ (Nat.succ n) => halve n + 1`

can be replaced by numeric literals and `+`:

`def halve : Nat → Nat
| 0 => 0
| 1 => 0
| n + 2 => halve n + 1`

Behind the scenes, both definitions are completely equivalent.
Remember: `halve n + 1` is equivalent to `(halve n) + 1`, not `halve (n + 1)`.

When using this syntax, the second argument to `+` should always be a literal `Nat`.
Even though addition is commutative, flipping the arguments in a pattern can result in errors like the following:

`` def halve : Nat → Nat
| 0 => 0
| 1 => 0
Invalid pattern(s): `n` is an explicit pattern variable, but it only occurs in positions that are inaccessible to pattern matching:
.(Nat.add 2 n)| 2 + n => halve n + 1 ``


```lean
Invalid pattern(s): `n` is an explicit pattern variable, but it only occurs in positions that are inaccessible to pattern matching:
  .(Nat.add 2 n)
```


This restriction enables Lean to transform all uses of the `+` notation in a pattern into uses of the underlying `Nat.succ`, keeping the language simpler behind the scenes.

## 1.8.7. Anonymous Functions[🔗](find/?domain=Verso.Genre.Manual.section&name=anonymous-functions "Permalink")

Functions in Lean need not be defined at the top level.
As expressions, functions are produced with the `fun` syntax.
Function expressions begin with the keyword `fun`, followed by one or more parameters, which are separated from the return expression using `=>`.
For instance, a function that adds one to a number can be written:

`fun x => x + 1 : Nat → Nat#check fun x => x + 1`


```lean
fun x => x + 1 : Nat → Nat
```


Type annotations are written the same way as on `def`, using parentheses and colons:

`fun x => x + 1 : Int → Int#check fun (x : Int) => x + 1`


```lean
fun x => x + 1 : Int → Int
```


Similarly, implicit parameters may be written with curly braces:

`fun {α} x => x : {α : Type} → α → α#check fun {α : Type} (x : α) => x`


```lean
fun {α} x => x : {α : Type} → α → α
```


This style of anonymous function expression is often referred to as a *lambda expression*, because the typical notation used in mathematical descriptions of programming languages uses the Greek letter λ (lambda) where Lean has the keyword `fun`.
Even though Lean does permit `λ` to be used instead of `fun`, it is most common to write `fun`.

Anonymous functions also support the multiple-pattern style used in `def`.
For instance, a function that returns the predecessor of a natural number if it exists can be written:

`fun x =>
match x with
| 0 => none
| n.succ => some n : Nat → Option Nat#check fun
| 0 => none
| n + 1 => some n`


```lean
fun x =>
  match x with
  | 0 => none
  | n.succ => some n : Nat → Option Nat
```


Note that Lean's own description of the function has a named argument and a `match` expression.
Many of Lean's convenient syntactic shorthands are expanded to simpler syntax behind the scenes, and the abstraction sometimes leaks.

Definitions using `def` that take arguments may be rewritten as function expressions.
For instance, a function that doubles its argument can be written as follows:

`def double : Nat → Nat := fun
| 0 => 0
| k + 1 => double k + 2`

When an anonymous function is very simple, like `fun x => x + 1`, the syntax for creating the function can be fairly verbose.
In that particular example, six non-whitespace characters are used to introduce the function, and its body consists of only three non-whitespace characters.
For these simple cases, Lean provides a shorthand.
In an expression surrounded by parentheses, a centered dot character `·` can stand for a parameter, and the expression inside the parentheses becomes the function's body.
That particular function can also be written `(· + 1)`.

The centered dot always creates a function out of the *closest* surrounding set of parentheses.
For instance, `(· + 5, 3)` is a function that returns a pair of numbers, while `((· + 5), 3)` is a pair of a function and a number.
If multiple dots are used, then they become parameters from left to right:

`(· , ·) 1 2``(1, ·) 2``(1, 2)`

Anonymous functions can be applied in precisely the same way as functions defined using `def` or `let`.
The command `10#eval (fun x => x + x) 5` results in:


```lean
10
```


while `10#eval (· * 2) 5` results in:


```lean
10
```


## 1.8.8. Namespaces[🔗](find/?domain=Verso.Genre.Manual.section&name=namespaces "Permalink")

Each name in Lean occurs in a *namespace*, which is a collection of names.
Names are placed in namespaces using `.`, so `List.map` is the name `map` in the `List` namespace.
Names in different namespaces do not conflict with each other, even if they are otherwise identical.
This means that `List.map` and `Array.map` are different names.
Namespaces may be nested, so `Project.Frontend.User.loginTime` is the name `loginTime` in the nested namespace `Project.Frontend.User`.

Names can be directly defined within a namespace.
For instance, the name `double` can be defined in the `Nat` namespace:

`def Nat.double (x : Nat) : Nat := x + x`

Because `Nat` is also the name of a type, dot notation is available to call `Nat.double` on expressions with type `Nat`:

`8#eval (4 : Nat).double`


```lean
8
```


In addition to defining names directly in a namespace, a sequence of declarations can be placed in a namespace using the `namespace` and `end` commands.
For instance, this defines `triple` and `quadruple` in the namespace `NewNamespace`:

`namespace NewNamespace
def triple (x : Nat) : Nat := 3 * x
def quadruple (x : Nat) : Nat := 2 * x + 2 * x
end NewNamespace`

To refer to them, prefix their names with `NewNamespace.`:

`NewNamespace.triple (x : Nat) : Nat#check NewNamespace.triple`


```lean
NewNamespace.triple (x : Nat) : Nat
```


`NewNamespace.quadruple (x : Nat) : Nat#check NewNamespace.quadruple`


```lean
NewNamespace.quadruple (x : Nat) : Nat
```


Namespaces may be *opened*, which allows the names in them to be used without explicit qualification.
Writing `open` `MyNamespace``in` before an expression causes the contents of `MyNamespace` to be available in the expression.
For example, `timesTwelve` uses both `quadruple` and `triple` after opening `NewNamespace`:

`def timesTwelve (x : Nat) :=
open NewNamespace in
quadruple (triple x)`

Namespaces can also be opened prior to a command.
This allows all parts of the command to refer to the contents of the namespace, rather than just a single expression.
To do this, place the `open`﻿`...``in` prior to the command.

`open NewNamespace in
NewNamespace.quadruple (x : Nat) : Nat#check quadruple`


```lean
NewNamespace.quadruple (x : Nat) : Nat
```


Function signatures show the name's full namespace.
Namespaces may additionally be opened for *all* following commands for the rest of the file.
To do this, simply omit the `in` from a top-level usage of `open`.

## 1.8.9. `if let`[🔗](find/?domain=Verso.Genre.Manual.section&name=if-let "Permalink")

When consuming values that have a sum type, it is often the case that only a single constructor is of interest.
For example, given this type that represents a subset of Markdown inline elements:

`inductive Inline : Type where
| lineBreak
| string : String → Inline
| emph : Inline → Inline
| strong : Inline → Inline`

a function that recognizes string elements and extracts their contents can be written:

`def Inline.string? (inline : Inline) : Option String :=
match inline with
| Inline.string s => some s
| _ => none`

An alternative way of writing this function's body uses `if` together with `let`:

`def Inline.string? (inline : Inline) : Option String :=
if let Inline.string s := inline then
some s
else none`

This is very much like the pattern-matching `let` syntax.
The difference is that it can be used with sum types, because a fallback is provided in the `else` case.
In some contexts, using `if let` instead of `match` can make code easier to read.

## 1.8.10. Positional Structure Arguments[🔗](find/?domain=Verso.Genre.Manual.section&name=positional-structure-arguments "Permalink")

The [section on structures](Getting-to-Know-Lean/Structures/#structures) presents two ways of constructing structures:

1. The constructor can be called directly, as in `Point.mk 1 2`.
2. Brace notation can be used, as in `{ x := 1, y := 2 }`.

In some contexts, it can be convenient to pass arguments positionally, rather than by name, but without naming the constructor directly.
For instance, defining a variety of similar structure types can help keep domain concepts separate, but the natural way to read the code may treat each of them as being essentially a tuple.
In these contexts, the arguments can be enclosed in angle brackets `⟨` and `⟩`.
A `Point` can be written `⟨1, 2⟩`.
Be careful!
Even though they look like the less-than sign `<` and greater-than sign `>`, these brackets are different.
They can be input using `\<` and `\>`, respectively.

Just as with the brace notation for named constructor arguments, this positional syntax can only be used in a context where Lean can determine the structure's type, either from a type annotation or from other type information in the program.
For instance, `#eval ⟨1, 2⟩` yields the following error:


```lean
Invalid `⟨...⟩` notation: The expected type of this term could not be determined
```


This error occurs because there is no type information available.
Adding an annotation, such as in `#eval (⟨1, 2⟩ : Point)`, solves the problem:


```lean
{ x := 1.000000, y := 2.000000 }
```


## 1.8.11. String Interpolation[🔗](find/?domain=Verso.Genre.Manual.section&name=string-interpolation "Permalink")

In Lean, prefixing a string with `s!` triggers *interpolation*, where expressions contained in curly braces inside the string are replaced with their values.
This is similar to `f`-strings in Python and `$`-prefixed strings in C#.
For instance,

`"three fives is 15"#eval s!"three fives is {NewNamespace.triple 5}"`

yields the output


```lean
"three fives is 15"
```


Not all expressions can be interpolated into a string.
For instance, attempting to interpolate a function results in an error.

`` toString "three fives is " ++ sorry : String#check s!"three fives is {failed to synthesize instance of type class
ToString (Nat → Nat)

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.NewNamespace.triple}" ``

yields the error


```lean
failed to synthesize instance of type class
  ToString (Nat → Nat)

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


This is because there is no standard way to convert functions into strings.
Just as the compiler maintains a table that describes how to display the result of evaluating expressions of various types, it maintains a table that describes how to convert values of various types into strings.
The message `failed to synthesize instance` means that the Lean compiler didn't find an entry in this table for the given type.
The chapter on [type classes](Overloading-and-Type-Classes/#type-classes) describes this mechanism in more detail, including the means of adding new entries to the table.

[←1.7. Characters, Strings, and Slices](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#chars-strings-slices "1.7. Characters, Strings, and Slices")[1.9. Summary→](Getting-to-Know-Lean/Summary/#getting-to-know-summary "1.9. Summary")
