# Study guide: 5.2. Applicative Functors 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **5.2. Applicative Functors 🔗** — An applicative functor is a functor that has two additional operations available: pure and seq .
- **5.2.1. A Non-Monadic Applicative 🔗** — When validating user input to a form, it's generally considered to be best to provide many errors at once, rather than one error at a time.
- **5.2.1.1. User Input 🔗** — As an example of user input, take the following structure:
- **5.2.1.2. Subtypes 🔗** — Representing these conditions is easiest with one additional Lean type, called Subtype :
- **5.2.1.3. Validated Input 🔗** — The validated user input is a structure that expresses the business logic using multiple techniques:

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←5.1. Structures and Inheritance](Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/#structure-inheritance "5.1. Structures and Inheritance")[5.3. The Applicative Contract→](Functors___-Applicative-Functors___-and-Monads/The-Applicative-Contract/#applicative-laws "5.3. The Applicative Contract")

# 5.2. Applicative Functors[🔗](find/?domain=Verso.Genre.Manual.section&name=applicative "Permalink")

An *applicative functor* is a functor that has two additional operations available: `pure` and `seq`.
`pure` is the same operator used in `Monad`, because `Monad` in fact inherits from `Applicative`.
`seq` is much like `map`: it allows a function to be used in order to transform the contents of a datatype.
However, with `seq`, the function is itself contained in the datatype: `f (α → β) → (Unit → f α) → f β`.
Having the function under the type `f` allows the `Applicative` instance to control how the function is applied, while `Functor.map` unconditionally applies a function.
The second argument has a type that begins with `Unit →` to allow the definition of `seq` to short-circuit in cases where the function will never be applied.

The value of this short-circuiting behavior can be seen in the instance of `Applicative Option`:

`instance : Applicative Option where
pure x := .some x
seq f x :=
match f with
| none => none
| some g => g <$> x ()`

In this case, if there is no function for `seq` to apply, then there is no need to compute its argument, so `x` is never called.
The same consideration informs the instance of `Applicative` for `Except`:

`instance : Applicative (Except ε) where
pure x := .ok x
seq f x :=
match f with
| .error e => .error e
| .ok g => g <$> x ()`

This short-circuiting behavior depends only on the `Option` or `Except` structures that *surround* the function, rather than on the function itself.

Monads can be seen as a way of capturing the notion of sequentially executing statements into a pure functional language.
The result of one statement can affect which further statements run.
This can be seen in the type of `bind`: `m α → (α → m β) → m β`.
The first statement's resulting value is an input into a function that computes the next statement to execute.
Successive uses of `bind` are like a sequence of statements in an imperative programming language, and `bind` is powerful enough to implement control structures like conditionals and loops.

Following this analogy, `Applicative` captures function application in a language that has side effects.
The arguments to a function in languages like Kotlin or C# are evaluated from left to right.
Side effects performed by earlier arguments occur before those performed by later arguments.
A function is not powerful enough to implement custom short-circuiting operators that depend on the specific *value* of an argument, however.

Typically, `seq` is not invoked directly.
Instead, the operator `<*>` is used.
This operator wraps its second argument in `fun () => ...`, simplifying the call site.
In other words, `E1 <*> E2` is syntactic sugar for `Seq.seq E1 (fun () => E2)`.

The key feature that allows `seq` to be used with multiple arguments is that a multiple-argument Lean function is really a single-argument function that returns another function that's waiting for the rest of the arguments.
In other words, if the first argument to `seq` is awaiting multiple arguments, then the result of the `seq` will be awaiting the rest.
For example, `some Plus.plus` can have the type `Option (Nat → Nat → Nat)`.
Providing one argument, `some Plus.plus <*> some 4`, results in the type `Option (Nat → Nat)`.
This can itself be used with `seq`, so `some Plus.plus <*> some 4 <*> some 7` has the type `Option Nat`.

Not every functor is applicative.
`Pair` is like the built-in product type `Prod`:

`structure Pair (α β : Type) : Type where
first : α
second : β`

Like `Except`, `Pair` has type `Type → Type → Type`.
This means that `Pair α` has type `Type → Type`, and a `Functor` instance is possible:

`instance : Functor (Pair α) where
map f x := ⟨x.first, f x.second⟩`

This instance obeys the `Functor` contract.

The two properties to check are that `id <$> Pair.mk x y``=` `Pair.mk x y` and that `f <$> g <$> Pair.mk x y``=` `(f ∘ g) <$> Pair.mk x y`.
The first property can be checked by just stepping through the evaluation of the left side, and noticing that it evaluates to the right side:

`id <$> Pair.mk x y``Pair.mk x (id y)``Pair.mk x y`

The second can be checked by stepping through both sides, and noting that they yield the same result:

`f <$> g <$> Pair.mk x y``f <$> Pair.mk x (g y)``Pair.mk x (f (g y))`

`(f ∘ g) <$> Pair.mk x y``Pair.mk x ((f ∘ g) y)``Pair.mk x (f (g y))`

Attempting to define an `Applicative` instance, however, does not work so well.
It will require a definition of `pure`:

`def Pair.pure (x : β) : Pair α β := don't know how to synthesize placeholder
context:
β α:Typex:β⊢ Pair α β_`


```lean
don't know how to synthesize placeholder
context:
β α:Typex:β⊢ Pair α β
```


There is a value with type `β` in scope (namely `x`), and the error message from the underscore suggests that the next step is to use the constructor `Pair.mk`:

`` def Pair.pure (x : β) : Pair α β := Pair.mk don't know how to synthesize placeholder for argument `first`
context:
β α:Typex:β⊢ α_ x ``


```lean
don't know how to synthesize placeholder for argument `first`
context:
β α:Typex:β⊢ α
```


Unfortunately, there is no `α` available.
Because `pure` would need to work for *all possible types* `α` to define an instance of `Applicative (Pair α)`, this is impossible.
After all, a caller could choose `α` to be `Empty`, which has no values at all.

## 5.2.1. A Non-Monadic Applicative[🔗](find/?domain=Verso.Genre.Manual.section&name=validate "Permalink")

When validating user input to a form, it's generally considered to be best to provide many errors at once, rather than one error at a time.
This allows the user to have an overview of what is needed to please the computer, rather than feeling badgered as they correct the errors field by field.

Ideally, validating user input will be visible in the type of the function that's doing the validating.
It should return a datatype that is specific—checking that a text box contains a number should return an actual numeric type, for instance.
A validation routine could throw an exception when the input does not pass validation.
Exceptions have a major drawback, however: they terminate the program at the first error, making it impossible to accumulate a list of errors.

On the other hand, the common design pattern of accumulating a list of errors and then failing when it is non-empty is also problematic.
A long nested sequences of `if` statements that validate each sub-section of the input data is hard to maintain, and it's easy to lose track of an error message or two.
Ideally, validation can be performed using an API that enables a new value to be returned yet automatically tracks and accumulates error messages.

An applicative functor called `Validate` provides one way to implement this style of API.
Like the `Except` monad, `Validate` allows a new value to be constructed that characterizes the validated data accurately.
Unlike `Except`, it allows multiple errors to be accumulated, without a risk of forgetting to check whether the list is empty.

### 5.2.1.1. User Input[🔗](find/?domain=Verso.Genre.Manual.section&name=user-input "Permalink")

As an example of user input, take the following structure:

`structure RawInput where
name : String
birthYear : String`

The business logic to be implemented is the following:

1. The name may not be empty
2. The birth year must be numeric and non-negative
3. The birth year must be greater than 1900, and less than or equal to the year in which the form is validated

Representing these as a datatype will require a new feature, called *subtypes*.
With this tool in hand, a validation framework can be written that uses an applicative functor to track errors, and these rules can be implemented in the framework.

### 5.2.1.2. Subtypes[🔗](find/?domain=Verso.Genre.Manual.section&name=subtypes "Permalink")

Representing these conditions is easiest with one additional Lean type, called `Subtype`:

`structure Subtype {α : Type} (p : α → Prop) where
val : α
property : p val`

This structure has two type parameters: an implicit parameter that is the type of data `α`, and an explicit parameter `p` that is a predicate over `α`.
A *predicate* is a logical statement with a variable in it that can be replaced with a value to yield an actual statement, like the [parameter to `GetElem`](Overloading-and-Type-Classes/Arrays-and-Indexing/#overloading-indexing) that describes what it means for an index to be in bounds for a lookup.
In the case of `Subtype`, the predicate slices out some subset of the values of `α` for which the predicate holds.
The structure's two fields are, respectively, a value from `α` and evidence that the value satisfies the predicate `p`.
Lean has special syntax for `Subtype`.
If `p` has type `α → Prop`, then the type `Subtype p` can also be written `{x : α // p x}`, or even `{x // p x}` when the type `α` can be inferred automatically.

[Representing positive numbers as inductive types](Overloading-and-Type-Classes/Positive-Numbers/#positive-numbers) is clear and easy to program with.
However, it has a key disadvantage.
While `Nat` and `Int` have the structure of ordinary inductive types from the perspective of Lean programs, the compiler treats them specially and uses fast arbitrary-precision number libraries to implement them.
This is not the case for additional user-defined types.
However, a subtype of `Nat` that restricts it to non-zero numbers allows the new type to use the efficient representation while still ruling out zero at compile time:

`def FastPos : Type := {x : Nat // x > 0}`

The smallest fast positive number is still one.
Now, instead of being a constructor of an inductive type, it's an instance of a structure that's constructed with angle brackets.
The first argument is the underlying `Nat`, and the second argument is the evidence that said `Nat` is greater than zero:

`def one : FastPos := ⟨1, by⊢ 1 > 0 decideAll goals completed! 🐙⟩`

The proposition `1 > 0` is decidable, so the `decide` tactic produces the necessary evidence.
The `OfNat` instance is very much like that for `Pos`, except it uses a short tactic proof to provide evidence that `n + 1 > 0`:

`instance : OfNat FastPos (n + 1) where
ofNat := ⟨n + 1, byn:Nat⊢ n + 1 > 0 simpAll goals completed! 🐙⟩`

Here, `simp` is needed because `decide` requires concrete values, but the proposition in question is `n + 1 > 0`.

Subtypes are a two-edged sword.
They allow efficient representation of validation rules, but they transfer the burden of maintaining these rules to the users of the library, who have to *prove* that they are not violating important invariants.
Generally, it's a good idea to use them internally to a library, providing an API to users that automatically ensures that all invariants are satisfied, with any necessary proofs being internal to the library.

Checking whether a value of type `α` is in the subtype `{x : α // p x}` usually requires that the proposition `p x` be decidable.
The [section on equality and ordering classes](Overloading-and-Type-Classes/Standard-Classes/#equality-and-ordering) describes how decidable propositions can be used with `if`.
When `if` is used with a decidable proposition, a name can be provided.
In the `then` branch, the name is bound to evidence that the proposition is true, and in the `else` branch, it is bound to evidence that the proposition is false.
This comes in handy when checking whether a given `Nat` is positive:

`def Nat.asFastPos? (n : Nat) : Option FastPos :=
if h : n > 0 then
some ⟨n, h⟩
else none`

In the `then` branch, `h` is bound to evidence that `n > 0`, and this evidence can be used as the second argument to `Subtype`'s constructor.

### 5.2.1.3. Validated Input[🔗](find/?domain=Verso.Genre.Manual.section&name=validated-input "Permalink")

The validated user input is a structure that expresses the business logic using multiple techniques:

- The structure type itself encodes the year in which it was checked for validity, so that `CheckedInput 2019` is not the same type as `CheckedInput 2020`
- The birth year is represented as a `Nat` rather than a `String`
- Subtypes are used to constrain the allowed values in the name and birth year fields

`structure CheckedInput (thisYear : Nat) : Type where
name : {n : String // n ≠ ""}
birthYear : {y : Nat // y > 1900 ∧ y ≤ thisYear}`

An input validator should take the current year and a `RawInput` as arguments, returning either a checked input or at least one validation failure.
This is represented by the `Validate` type:

`inductive Validate (ε α : Type) : Type where
| ok : α → Validate ε α
| errors : NonEmptyList ε → Validate ε α`

It looks very much like `Except`.
The only difference is that the `errors` constructor may contain more than one failure.

`Validate` is a functor.
Mapping a function over it transforms any successful value that might be present, just as in the `Functor` instance for `Except`:

`instance : Functor (Validate ε) where
map f
| .ok x => .ok (f x)
| .errors errs => .errors errs`

The `Applicative` instance for `Validate` has an important difference from the instance for `Except`: while the instance for `Except` terminates at the first error encountered, the instance for `Validate` is careful to accumulate all errors from *both* the function and the argument branches:

`instance : Applicative (Validate ε) where
pure := .ok
seq f x :=
match f with
| .ok g => g <$> (x ())
| .errors errs =>
match x () with
| .ok _ => .errors errs
| .errors errs' => .errors (errs ++ errs')`

Using `.errors` together with the constructor for `NonEmptyList` is a bit verbose.
Helpers like `reportError` make code more readable.
In this application, error reports will consist of field names paired with messages:

`def Field := String``def reportError (f : Field) (msg : String) : Validate (Field × String) α :=
.errors { head := (f, msg), tail := [] }`

The `Applicative` instance for `Validate` allows the checking procedures for each field to be written independently and then composed.
Checking a name consists of ensuring that a string is non-empty, then returning evidence of this fact in the form of a `Subtype`.
This uses the evidence-binding version of `if`:

`def checkName (name : String) :
Validate (Field × String) {n : String // n ≠ ""} :=
if h : name = "" then
reportError "name" "Required"
else pure ⟨name, h⟩`

In the `then` branch, `h` is bound to evidence that `name = ""`, while it is bound to evidence that `¬name = ""` in the `else` branch.

It's certainly the case that some validation errors make other checks impossible.
For example, it makes no sense to check whether the birth year field is greater than 1900 if a confused user wrote the word `"syzygy"` instead of a number.
Checking the allowed range of the number is only meaningful after ensuring that the field in fact contains a number.
This can be expressed using the function `andThen`:

`def Validate.andThen (val : Validate ε α)
(next : α → Validate ε β) : Validate ε β :=
match val with
| .errors errs => .errors errs
| .ok x => next x`

While this function's type signature makes it suitable to be used as `bind` in a `Monad` instance, there are good reasons not to do so.
They are described [in the section that describes the `Applicative` contract](Functors___-Applicative-Functors___-and-Monads/The-Applicative-Contract/#additional-stipulations).

To check that the birth year is a number, a built-in function called `String.Slice.toNat? : String.Slice → Option Nat` is useful.
It's most user-friendly to eliminate leading and trailing whitespace first using `String.trimAscii`:

`def checkYearIsNat (year : String) : Validate (Field × String) Nat :=
match year.trimAscii.toNat? with
| none => reportError "birth year" "Must be digits"
| some n => pure n`

To check that the provided year is in the expected range, nested uses of the evidence-providing form of `if` are in order:

`def checkBirthYear (thisYear year : Nat) :
Validate (Field × String) {y : Nat // y > 1900 ∧ y ≤ thisYear} :=
if h : year > 1900 then
if h' : year ≤ thisYear then
pure ⟨year, bythisYear:Natyear:Nath:year > 1900h':year ≤ thisYear⊢ year > 1900 ∧ year ≤ thisYear simp [*]All goals completed! 🐙⟩
else reportError "birth year" s!"Must be no later than {thisYear}"
else reportError "birth year" "Must be after 1900"`

Finally, these three components can be combined using `<*>`:

`def checkInput (year : Nat) (input : RawInput) :
Validate (Field × String) (CheckedInput year) :=
pure CheckedInput.mk <*>
checkName input.name <*>
(checkYearIsNat input.birthYear).andThen fun birthYearAsNat =>
checkBirthYear year birthYearAsNat`

Testing `checkInput` shows that it can indeed return multiple pieces of feedback:

`Validate.ok { name := "David", birthYear := 1984 }#eval checkInput 2023 {name := "David", birthYear := "1984"}`


```lean
Validate.ok { name := "David", birthYear := 1984 }
```


`Validate.errors { head := ("name", "Required"), tail := [("birth year", "Must be no later than 2023")] }#eval checkInput 2023 {name := "", birthYear := "2045"}`


```lean
Validate.errors { head := ("name", "Required"), tail := [("birth year", "Must be no later than 2023")] }
```


`Validate.errors { head := ("birth year", "Must be digits"), tail := [] }#eval checkInput 2023 {name := "David", birthYear := "syzygy"}`


```lean
Validate.errors { head := ("birth year", "Must be digits"), tail := [] }
```


Form validation with `checkInput` illustrates a key advantage of `Applicative` over `Monad`.
Because `>>=` provides enough power to modify the rest of the program's execution based on the value from the first step, it *must* receive a value from the first step to pass on.
If no value is received (e.g. because an error has occurred), then `>>=` cannot execute the rest of the program.
`Validate` demonstrates why it can be useful to run the rest of the program anyway: in cases where the earlier data isn't needed, running the rest of the program can yield useful information (in this case, more validation errors).
`Applicative`'s `<*>` may run both of its arguments before recombining the results.
Similarly, `>>=` forces sequential execution.
Each step must complete before the next may run.
This is generally useful, but it makes it impossible to have parallel execution of different threads that naturally emerges from the program's actual data dependencies.
A more powerful abstraction like `Monad` increases the flexibility that's available to the API consumer, but it decreases the flexibility that is available to the API implementor.

[←5.1. Structures and Inheritance](Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/#structure-inheritance "5.1. Structures and Inheritance")[5.3. The Applicative Contract→](Functors___-Applicative-Functors___-and-Monads/The-Applicative-Contract/#applicative-laws "5.3. The Applicative Contract")
