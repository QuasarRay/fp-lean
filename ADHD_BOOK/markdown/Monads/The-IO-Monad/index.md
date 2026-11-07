# Study guide: 4.5. The IO Monad 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **4.5. The IO Monad 🔗** — IO as a monad can be understood from two perspectives, which were described in the section on running programs .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←4.4. do-Notation for Monads](Monads/do--Notation-for-Monads/#monad-do-notation "4.4. do-Notation for Monads")[4.6. Additional Conveniences→](Monads/Additional-Conveniences/#monads-conveniences "4.6. Additional Conveniences")

# 4.5. The IO Monad[🔗](find/?domain=Verso.Genre.Manual.section&name=io-monad "Permalink")

`IO` as a monad can be understood from two perspectives, which were described in the section on [running programs](Hello___-World___/Running-a-Program/#running-a-program).
Each can help to understand the meanings of `pure` and `bind` for `IO`.

From the first perspective, an `IO` action is an instruction to Lean's run-time system.
For example, the instruction might be “read a string from this file descriptor, then re-invoke the pure Lean code with the string”.
This perspective is an *exterior* one, viewing the program from the perspective of the operating system.
In this case, `pure` is an `IO` action that does not request any effects from the RTS, and `bind` instructs the RTS to first carry out one potentially-effectful operation and then invoke the rest of the program with the resulting value.

From the second perspective, an `IO` action transforms the whole world.
`IO` actions are actually pure, because they receive a unique world as an argument and then return the changed world.
This perspective is an *interior* one that matches how `IO` is represented inside of Lean.
The world is represented in Lean as a token, and the `IO` monad is structured to make sure that each token is used exactly once.

To see how this works, it can be helpful to peel back one definition at a time.
The `#print` command reveals the internals of Lean datatypes and definitions.
For example,

`inductive Nat : Type
number of parameters: 0
constructors:
Nat.zero : Nat
Nat.succ : Nat → Nat#print Nat`

results in


```lean
inductive Nat : Type
number of parameters: 0
constructors:
Nat.zero : Nat
Nat.succ : Nat → Nat
```


and

`def String.toLower : String → String :=
fun s => String.map Char.toLower s#print String.toLower`

results in


```lean
def String.toLower : String → String :=
fun s => String.map Char.toLower s
```


Sometimes, the output of `#print` includes Lean features that have not yet been presented in this book.
For example,

`def List.head?.{u} : {α : Type u} → List α → Option α :=
fun {α} x =>
match x with
| [] => none
| a :: tail => some a#print List.head?`

produces


```lean
def List.head?.{u} : {α : Type u} → List α → Option α :=
fun {α} x =>
  match x with
  | [] => none
  | a :: tail => some a
```


which includes a `.{u}` after the definition's name, and annotates types as `Type u` rather than just `Type`.
This can be safely ignored for now.

Printing the definition of `IO` shows that it's defined in terms of simpler structures:

`@[reducible] def IO : Type → Type :=
EIO IO.Error#print IO`


```lean
@[reducible] def IO : Type → Type :=
EIO IO.Error
```


`IO.Error` represents all the errors that could be thrown by an `IO` action:

`inductive IO.Error : Type
number of parameters: 0
constructors:
IO.Error.alreadyExists : Option String → UInt32 → String → IO.Error
IO.Error.otherError : UInt32 → String → IO.Error
IO.Error.resourceBusy : UInt32 → String → IO.Error
IO.Error.resourceVanished : UInt32 → String → IO.Error
IO.Error.unsupportedOperation : UInt32 → String → IO.Error
IO.Error.hardwareFault : UInt32 → String → IO.Error
IO.Error.unsatisfiedConstraints : UInt32 → String → IO.Error
IO.Error.illegalOperation : UInt32 → String → IO.Error
IO.Error.protocolError : UInt32 → String → IO.Error
IO.Error.timeExpired : UInt32 → String → IO.Error
IO.Error.interrupted : String → UInt32 → String → IO.Error
IO.Error.noFileOrDirectory : String → UInt32 → String → IO.Error
IO.Error.invalidArgument : Option String → UInt32 → String → IO.Error
IO.Error.permissionDenied : Option String → UInt32 → String → IO.Error
IO.Error.resourceExhausted : Option String → UInt32 → String → IO.Error
IO.Error.inappropriateType : Option String → UInt32 → String → IO.Error
IO.Error.noSuchThing : Option String → UInt32 → String → IO.Error
IO.Error.unexpectedEof : IO.Error
IO.Error.userError : String → IO.Error#print IO.Error`


```lean
inductive IO.Error : Type
number of parameters: 0
constructors:
IO.Error.alreadyExists : Option String → UInt32 → String → IO.Error
IO.Error.otherError : UInt32 → String → IO.Error
IO.Error.resourceBusy : UInt32 → String → IO.Error
IO.Error.resourceVanished : UInt32 → String → IO.Error
IO.Error.unsupportedOperation : UInt32 → String → IO.Error
IO.Error.hardwareFault : UInt32 → String → IO.Error
IO.Error.unsatisfiedConstraints : UInt32 → String → IO.Error
IO.Error.illegalOperation : UInt32 → String → IO.Error
IO.Error.protocolError : UInt32 → String → IO.Error
IO.Error.timeExpired : UInt32 → String → IO.Error
IO.Error.interrupted : String → UInt32 → String → IO.Error
IO.Error.noFileOrDirectory : String → UInt32 → String → IO.Error
IO.Error.invalidArgument : Option String → UInt32 → String → IO.Error
IO.Error.permissionDenied : Option String → UInt32 → String → IO.Error
IO.Error.resourceExhausted : Option String → UInt32 → String → IO.Error
IO.Error.inappropriateType : Option String → UInt32 → String → IO.Error
IO.Error.noSuchThing : Option String → UInt32 → String → IO.Error
IO.Error.unexpectedEof : IO.Error
IO.Error.userError : String → IO.Error
```


`EIO ε α` represents `IO` actions that will either terminate with an error of type `ε` or succeed with a value of type `α`.
This means that, like the `Except ε` monad, the `IO` monad includes the ability to define error handling and exceptions.

Peeling back another layer, `EIO` is itself defined in terms of a simpler structure:

`def EIO : Type → Type → Type :=
fun ε α => EST ε IO.RealWorld α#print EIO`


```lean
def EIO : Type → Type → Type :=
fun ε α => EST ε IO.RealWorld α
```


The `EST` monad includes both errors and state—it's similar to a combination of `Except` and `State`.
It is defined using another type, `EST.Out`:

`def EST : Type → Type → Type → Type :=
fun ε σ α => Void σ → EST.Out ε σ α#print EST`


```lean
def EST : Type → Type → Type → Type :=
fun ε σ α => Void σ → EST.Out ε σ α
```


In other words, a program with type `EST ε σ α` is a function that accepts an initial state of type `σ` and returns an `EST.Out ε σ α`.
The state is wrapped in the type `Void`, which is an internal primitive that causes a value to be erased from compiled code; `Void σ` has the same representation as `Unit`.

`EST.Out` is very much like the definition of `Except`, with one constructor that indicates a successful termination and one constructor that indicates an error:

`inductive EST.Out : Type → Type → Type → Type
number of parameters: 3
constructors:
EST.Out.ok : {ε σ α : Type} → α → Void σ → EST.Out ε σ α
EST.Out.error : {ε σ α : Type} → ε → Void σ → EST.Out ε σ α#print EST.Out`


```lean
inductive EST.Out : Type → Type → Type → Type
number of parameters: 3
constructors:
EST.Out.ok : {ε σ α : Type} → α → Void σ → EST.Out ε σ α
EST.Out.error : {ε σ α : Type} → ε → Void σ → EST.Out ε σ α
```


Just like `Except ε α`, the `ok` constructor includes a result of type `α`, and the `error` constructor includes an exception of type `ε`.
Unlike `Except`, both constructors have an additional state field that includes the final state of the computation.

The `Monad` instance for `EST ε σ` requires `pure` and `bind`.
Just as with `State`, the implementation of `pure` for `EST` accepts an initial state and returns it unchanged, and just as with `Except`, it returns its argument in the `ok` constructor:

`protected def EST.pure : {α ε σ : Type} → α → EST ε σ α :=
fun {α ε σ} a s => EST.Out.ok a s#print EST.pure`


```lean
protected def EST.pure : {α ε σ : Type} → α → EST ε σ α :=
fun {α ε σ} a s => EST.Out.ok a s
```


`protected` means that the full name `EST.pure` is needed even if the `EST` namespace has been opened.

Similarly, `bind` for `EST` takes an initial state as an argument.
It passes this initial state to its first action.
Like `bind` for `Except`, it then checks whether the result is an error.
If so, the error is returned unchanged and the second argument to `bind` remains unused.
If the result was a success, then the second argument is applied to both the returned value and to the resulting state.

`protected def EST.bind : {ε σ α β : Type} → EST ε σ α → (α → EST ε σ β) → EST ε σ β :=
fun {ε σ α β} x f s =>
match x s with
| EST.Out.ok a s => f a s
| EST.Out.error e s => EST.Out.error e s#print EST.bind`


```lean
protected def EST.bind : {ε σ α β : Type} → EST ε σ α → (α → EST ε σ β) → EST ε σ β :=
fun {ε σ α β} x f s =>
  match x s with
  | EST.Out.ok a s => f a s
  | EST.Out.error e s => EST.Out.error e s
```


Putting all of this together, `IO` is a monad that tracks state and errors at the same time.
The collection of available errors is that given by the datatype `IO.Error`, which has constructors that describe many things that can go wrong in a program.
The state is a type that represents the real world, called `IO.RealWorld`.
Each basic `IO` action receives this real world and returns another one, paired either with an error or a result.
In `IO`, `pure` returns the world unchanged, while `bind` passes the modified world from one action into the next action.

Because the entire universe doesn't fit in a computer's memory, the world being passed around is just a representation.
So long as world tokens are not re-used, the representation is safe.
The type `IO.RealWorld` is a trivial primitive type that does not need any representation at all, because it is only used inside of `Void`.

[←4.4. do-Notation for Monads](Monads/do--Notation-for-Monads/#monad-do-notation "4.4. do-Notation for Monads")[4.6. Additional Conveniences→](Monads/Additional-Conveniences/#monads-conveniences "4.6. Additional Conveniences")
