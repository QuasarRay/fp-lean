# Study guide: 2.5. Additional Conveniences 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **2.5.1. Nested Actions 🔗** — Many of the functions in feline exhibit a repetitive pattern in which an IO action's result is given a name, and then used immediately and only once.
- **2.5.2. Flexible Layouts for do 🔗** — In Lean, do expressions are whitespace-sensitive.
- **2.5.3. Running IO Actions With #eval 🔗** — Lean's #eval command can be used to execute IO actions, rather than just evaluating them.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←2.4. Worked Example: cat](Hello___-World___/Worked-Example___--cat/#example-cat "2.4. Worked Example: cat")[2.6. Summary→](Hello___-World___/Summary/#hello-world-summary "2.6. Summary")

# 2.5. Additional Conveniences[🔗](find/?domain=Verso.Genre.Manual.section&name=hello-world-conveniences "Permalink")

## 2.5.1. Nested Actions[🔗](find/?domain=Verso.Genre.Manual.section&name=nested-actions "Permalink")

Many of the functions in `feline` exhibit a repetitive pattern in which an `IO` action's result is given a name, and then used immediately and only once.
For instance, in `dump`:

`partial def dump (stream : IO.FS.Stream) : IO Unit := do
let buf ← stream.read bufsize
if buf.isEmpty then
pure ()
else
let stdout ← IO.getStdout
stdout.write buf
dump stream`

the pattern occurs for `stdout`:

`let stdout ← IO.getStdout
stdout.write buf`

Similarly, `fileStream` contains the following snippet:

`let fileExists ← filename.pathExists
if not fileExists then`

When Lean is compiling a `do` block, expressions that consist of a left arrow immediately under parentheses are lifted to the nearest enclosing `do`, and their results are bound to a unique name.
This unique name replaces the origin of the expression.
This means that `dump` can also be written as follows:

`partial def dump (stream : IO.FS.Stream) : IO Unit := do
let buf ← stream.read bufsize
if buf.isEmpty then
pure ()
else
(← IO.getStdout).write buf
dump stream`

This version of `dump` avoids introducing names that are used only once, which can greatly simplify a program.
`IO` actions that Lean lifts from a nested expression context are called *nested actions*.

`fileStream` can be simplified using the same technique:

`def fileStream (filename : System.FilePath) : IO (Option IO.FS.Stream) := do
if not (← filename.pathExists) then
(← IO.getStderr).putStrLn s!"File not found: {filename}"
pure none
else
let handle ← IO.FS.Handle.mk filename IO.FS.Mode.read
pure (some (IO.FS.Stream.ofHandle handle))`

In this case, the local name of `handle` could also have been eliminated using nested actions, but the resulting expression would have been long and complicated.
Even though it's often good style to use nested actions, it can still sometimes be helpful to name intermediate results.

It is important to remember, however, that nested actions are only a shorter notation for `IO` actions that occur in a surrounding `do` block.
The side effects that are involved in executing them still occur in the same order, and execution of side effects is not interspersed with the evaluation of expressions.
Therefore, nested actions cannot be lifted from the branches of an `if`.

For an example of where this might be confusing, consider the following helper definitions that return data after announcing to the world that they have been executed:

`def getNumA : IO Nat := do
(← IO.getStdout).putStrLn "A"
pure 5``def getNumB : IO Nat := do
(← IO.getStdout).putStrLn "B"
pure 7`

These definitions are intended to stand in for more complicated `IO` code that might validate user input, read a database, or open a file.

A program that prints `0` when number A is five, or number B otherwise, might be written as follows:

`` def test : IO Unit := do
let a : Nat := if (← getNumA) == 5 then 0 else (Nested action `← getNumB` must be nested inside a `do` expression.← getNumB)
(← IO.getStdout).putStrLn s!"The answer is {a}" ``

This program would be equivalent to:

`def test : IO Unit := do
let x ← getNumA
let y ← getNumB
let a : Nat := if x == 5 then 0 else y
(← IO.getStdout).putStrLn s!"The answer is {a}"`

which runs `getNumB` regardless of whether the result of `getNumA` is equal to `5`.
To prevent this confusion, nested actions are not allowed in an `if` that is not itself a line in the `do`, and the following error message results:


```lean
Nested action `← getNumB` must be nested inside a `do` expression.
```


## 2.5.2. Flexible Layouts for `do`[🔗](find/?domain=Verso.Genre.Manual.section&name=do-layout-syntax "Permalink")

In Lean, `do` expressions are whitespace-sensitive.
Each `IO` action or local binding in the `do` is expected to start on its own line, and they should all have the same indentation.
Almost all uses of `do` should be written this way.
In some rare contexts, however, manual control over whitespace and indentation may be necessary, or it may be convenient to have multiple small actions on a single line.
In these cases, newlines can be replaced with a semicolon and indentation can be replaced with curly braces.

For instance, all of the following programs are equivalent:

`-- This version uses only whitespace-sensitive layout
def main : IO Unit := do
let stdin ← IO.getStdin
let stdout ← IO.getStdout
stdout.putStrLn "How would you like to be addressed?"
let name := (← stdin.getLine).trimAscii
stdout.putStrLn s!"Hello, {name}!"``-- This version is as explicit as possible
def main : IO Unit := do {
let stdin ← IO.getStdin;
let stdout ← IO.getStdout;
stdout.putStrLn "How would you like to be addressed?";
let name := (← stdin.getLine).trimAscii;
stdout.putStrLn s!"Hello, {name}!"
}``-- This version uses a semicolon to put two actions on the same line
def main : IO Unit := do
let stdin ← IO.getStdin; let stdout ← IO.getStdout
stdout.putStrLn "How would you like to be addressed?"
let name := (← stdin.getLine).trimAscii
stdout.putStrLn s!"Hello, {name}!"`

Idiomatic Lean code uses curly braces with `do` very rarely.

## 2.5.3. Running `IO` Actions With `#eval`[🔗](find/?domain=Verso.Genre.Manual.section&name=eval-io "Permalink")

Lean's `#eval` command can be used to execute `IO` actions, rather than just evaluating them.
Normally, adding a `#eval` command to a Lean file causes Lean to evaluate the provided expression, convert the resulting value to a string, and provide that string as a tooltip and in the info window.
Rather than failing because `IO` actions can't be converted to strings, `#eval` executes them, carrying out their side effects.
If the result of execution is the `Unit` value `()`, then no result string is shown, but if it is a type that can be converted to a string, then Lean displays the resulting value.

This means that, given the prior definitions of `countdown` and `runActions`,

`3
2
1
Blast off!
#eval runActions (countdown 3)`

displays


```lean
3
2
1
Blast off!
```


This is the output produced by running the `IO` action, rather than some opaque representation of the action itself.
In other words, for `IO` actions, `#eval` both *evaluates* the provided expression and *executes* the resulting action value.

Quickly testing `IO` actions with `#eval` can be much more convenient that compiling and running whole programs.
However, there are some limitations.
For instance, reading from standard input simply returns empty input.
Additionally, the `IO` action is re-executed whenever Lean needs to update the diagnostic information that it provides to users, and this can happen at unpredictable times.
An action that reads and writes files, for instance, may do so unexpectedly.

[←2.4. Worked Example: cat](Hello___-World___/Worked-Example___--cat/#example-cat "2.4. Worked Example: cat")[2.6. Summary→](Hello___-World___/Summary/#hello-world-summary "2.6. Summary")


> **Review needed:** The following headings have no short source sentence: 2.5. Additional Conveniences 🔗