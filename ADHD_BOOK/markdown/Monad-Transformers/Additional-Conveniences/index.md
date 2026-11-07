# Study guide: 6.5. Additional Conveniences 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **6.5.1. Pipe Operators 🔗** — Functions are normally written before their arguments.
- **6.5.2. Infinite Loops 🔗** — Within a do -block, the repeat keyword introduces an infinite loop.
- **6.5.3. While Loops 🔗** — When programming with local mutability, while loops can be a convenient alternative to repeat with an if -guarded break :

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←6.4. More do Features](Monad-Transformers/More-do-Features/#more-do-features "6.4. More do Features")[6.6. Summary→](Monad-Transformers/Summary/#monad-transformer-summary "6.6. Summary")

# 6.5. Additional Conveniences[🔗](find/?domain=Verso.Genre.Manual.section&name=monad-transformer-conveniences "Permalink")

## 6.5.1. Pipe Operators[🔗](find/?domain=Verso.Genre.Manual.section&name=pipe-operators "Permalink")

Functions are normally written before their arguments.
When reading a program from left to right, this promotes a view in which the function's *output* is paramount—the function has a goal to achieve (that is, a value to compute), and it receives arguments to support it in this process.
But some programs are easier to understand in terms of an input that is successively refined to produce the output.
For these situations, Lean provides a *pipeline* operator which is similar to the that provided by F#.
Pipeline operators are useful in the same situations as Clojure's threading macros.

The pipeline `E₁ |> E₂` is short for `E₂ E₁`.
For example, evaluating:

`"(some 5)"#eval some 5 |> toString`

results in:


```lean
"(some 5)"
```


While this change of emphasis can make some programs more convenient to read, pipelines really come into their own when they contain many components.

With the definition:

`def times3 (n : Nat) : Nat := n * 3`

the following pipeline:

`"It is 15"#eval 5 |> times3 |> toString |> ("It is " ++ ·)`

yields:


```lean
"It is 15"
```


More generally, a series of pipelines `E₁ |> E₂ |> E₃ |> E₄` is short for nested function applications `E₄ (E₃ (E₂ E₁))`.

Pipelines may also be written in reverse.
In this case, they do not place the subject of data transformation first; however, in cases where many nested parentheses pose a challenge for readers, they can clarify the steps of application.
The prior example could be equivalently written as:

`"It is 15"#eval ("It is " ++ ·) <| toString <| times3 <| 5`

which is short for:

`"It is 15"#eval ("It is " ++ ·) (toString (times3 5))`

Lean's method dot notation that uses the name of the type before the dot to resolve the namespace of the operator after the dot serves a similar purpose to pipelines.
Even without the pipeline operator, it is possible to write `[1, 2, 3].reverse` instead of `List.reverse [1, 2, 3]`.
However, the pipeline operator is also useful for dotted functions when using many of them.
`([1, 2, 3].reverse.drop 1).reverse` can also be written as `[1, 2, 3] |> List.reverse |> List.drop 1 |> List.reverse`.
This version avoids having to parenthesize expressions simply because they accept arguments, and it recovers the convenience of a chain of method calls in languages like Kotlin or C#.
However, it still requires the namespace to be provided by hand.
As a final convenience, Lean provides the “pipeline dot” operator, which groups functions like the pipeline but uses the name of the type to resolve namespaces.
With “pipeline dot”, the example can be rewritten to `[1, 2, 3] |>.reverse |>.drop 1 |>.reverse`.

## 6.5.2. Infinite Loops[🔗](find/?domain=Verso.Genre.Manual.section&name=infinite-loops "Permalink")

Within a `do`-block, the `repeat` keyword introduces an infinite loop.
For example, a program that spams the string `"Spam!"` can use it:

`def spam : IO Unit := do
repeat IO.println "Spam!"`

A `repeat` loop supports `break` and `continue`, just like `for` loops.

The `dump` function from the [implementation of `feline`](Hello___-World___/Worked-Example___--cat/#streams) uses a recursive function to run forever:

`partial def dump (stream : IO.FS.Stream) : IO Unit := do
let buf ← stream.read bufsize
if buf.isEmpty then
pure ()
else
let stdout ← IO.getStdout
stdout.write buf
dump stream`

This function can be greatly shortened using `repeat`:

`def dump (stream : IO.FS.Stream) : IO Unit := do
let stdout ← IO.getStdout
repeat do
let buf ← stream.read bufsize
if buf.isEmpty then break
stdout.write buf`

Neither `spam` nor `dump` need to be declared as `partial` because they are not themselves infinitely recursive.
Instead, `repeat` makes use of a type whose `ForM` instance is `partial`.
Partiality does not “infect” calling functions.

## 6.5.3. While Loops[🔗](find/?domain=Verso.Genre.Manual.section&name=while-loops "Permalink")

When programming with local mutability, `while` loops can be a convenient alternative to `repeat` with an `if`-guarded `break`:

`def dump (stream : IO.FS.Stream) : IO Unit := do
let stdout ← IO.getStdout
let mut buf ← stream.read bufsize
while not buf.isEmpty do
stdout.write buf
buf ← stream.read bufsize`

Behind the scenes, `while` is just a simpler notation for `repeat`.

[←6.4. More do Features](Monad-Transformers/More-do-Features/#more-do-features "6.4. More do Features")[6.6. Summary→](Monad-Transformers/Summary/#monad-transformer-summary "6.6. Summary")


> **Review needed:** The following headings have no short source sentence: 6.5. Additional Conveniences 🔗