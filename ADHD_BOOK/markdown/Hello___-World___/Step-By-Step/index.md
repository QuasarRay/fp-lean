# Study guide: 2.2. Step By Step 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **2.2. Step By Step 🔗** — A do block can be executed one line at a time.
- **2.2.1. Standard IO 🔗** — The first line is let stdin ← IO.getStdin , while the remainder is:
- **2.2.2. Asking a Question 🔗** — Now that stdin and stdout have been found, the remainder of the block consists of a question and an answer:
- **2.2.3. Greeting the User 🔗** — All that remains to be executed in the do block is a single statement:
- **2.2.4. IO Actions as Values 🔗** — In the above description, it can be difficult to see why the distinction between evaluating expressions and executing IO actions is necessary.
- **2.2.5. Exercise 🔗** — Step through the execution of the following program on a piece of paper:

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←2.1. Running a Program](Hello___-World___/Running-a-Program/#running-a-program "2.1. Running a Program")[2.3. Starting a Project→](Hello___-World___/Starting-a-Project/#starting-a-project "2.3. Starting a Project")

# 2.2. Step By Step[🔗](find/?domain=Verso.Genre.Manual.section&name=step-by-step "Permalink")

A `do` block can be executed one line at a time.
Start with the program from the prior section:

`let stdin ← IO.getStdin
let stdout ← IO.getStdout
stdout.putStrLn "How would you like to be addressed?"
let input ← stdin.getLine
let name := input.dropEndWhile Char.isWhitespace
stdout.putStrLn s!"Hello, {name}!"`

## 2.2.1. Standard IO[🔗](find/?domain=Verso.Genre.Manual.section&name=stdio "Permalink")

The first line is `let stdin ← IO.getStdin`, while the remainder is:

`let stdout ← IO.getStdout
stdout.putStrLn "How would you like to be addressed?"
let input ← stdin.getLine
let name := input.dropEndWhile Char.isWhitespace
stdout.putStrLn s!"Hello, {name}!"`

To execute a `let` statement that uses a `←`, start by evaluating the expression to the right of the arrow (in this case, `IO.getStdin`).
Because this expression is just a variable, its value is looked up.
The resulting value is a built-in primitive `IO` action.
The next step is to execute this `IO` action, resulting in a value that represents the standard input stream, which has type `IO.FS.Stream`.
Standard input is then associated with the name to the left of the arrow (here `stdin`) for the remainder of the `do` block.

Executing the second line, `let stdout ← IO.getStdout`, proceeds similarly.
First, the expression `IO.getStdout` is evaluated, yielding an `IO` action that will return the standard output.
Next, this action is executed, actually returning the standard output.
Finally, this value is associated with the name `stdout` for the remainder of the `do` block.

## 2.2.2. Asking a Question[🔗](find/?domain=Verso.Genre.Manual.section&name=asking-a-question "Permalink")

Now that `stdin` and `stdout` have been found, the remainder of the block consists of a question and an answer:

`stdout.putStrLn "How would you like to be addressed?"
let input ← stdin.getLine
let name := input.dropEndWhile Char.isWhitespace
stdout.putStrLn s!"Hello, {name}!"`

The first statement in the block, `stdout.putStrLn "How would you like to be addressed?"`, consists of an expression.
To execute an expression, it is first evaluated.
In this case, `IO.FS.Stream.putStrLn` has type `IO.FS.Stream → String → IO Unit`.
This means that it is a function that accepts a stream and a string, returning an `IO` action.
The expression uses [accessor notation](Getting-to-Know-Lean/Structures/#behind-the-scenes) for a function call.
This function is applied to two arguments: the standard output stream and a string.
The value of the expression is an `IO` action that will write the string and a newline character to the output stream.
Having found this value, the next step is to execute it, which causes the string and newline to actually be written to `stdout`.
Statements that consist only of expressions do not introduce any new variables.

The next statement in the block is `let input ← stdin.getLine`.
`IO.FS.Stream.getLine` has type `IO.FS.Stream → IO String`, which means that it is a function from a stream to an `IO` action that will return a string.
Once again, this is an example of accessor notation.
This `IO` action is executed, and the program waits until the user has typed a complete line of input.
Assume the user writes “`David`”.
The resulting line (`"David\n"`) is associated with `input`, where the escape sequence `\n` denotes the newline character.

`let name := input.dropEndWhile Char.isWhitespace
stdout.putStrLn s!"Hello, {name}!"`

The next line, `let name := input.dropEndWhile Char.isWhitespace`, is a `let` statement.
Unlike the other `let` statements in this program, it uses `:=` instead of `←`.
This means that the expression will be evaluated, but the resulting value need not be an `IO` action and will not be executed.
In this case, `String.dropEndWhile` takes a string and a [pattern](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#string-matching) and returns a [string slice](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#--tech-term-string-slices) from which all substrings at the end of the string that match the pattern have been removed.
For example,

`#eval "Hello!!!".dropEndWhile (· == '!')`

yields


```lean
Hello
```


and

`#eval "Hello... ".dropEndWhile (fun c => not (c.isAlphanum))`

yields


```lean
Hello
```


in which all non-alphanumeric characters have been removed from the right side of the string.
In the current line of the program, whitespace characters (including the newline) are removed from the right side of the input string, resulting in `David`, which is associated with `name` for the remainder of the block.

## 2.2.3. Greeting the User[🔗](find/?domain=Verso.Genre.Manual.section&name=greeting "Permalink")

All that remains to be executed in the `do` block is a single statement:

`stdout.putStrLn s!"Hello, {name}!"`

The string argument to `putStrLn` is constructed via string interpolation, yielding the string `"Hello, David!"`.
Because this statement is an expression, it is evaluated to yield an `IO` action that will print this string with a newline to standard output.
Once the expression has been evaluated, the resulting `IO` action is executed, resulting in the greeting.

## 2.2.4. `IO` Actions as Values[🔗](find/?domain=Verso.Genre.Manual.section&name=actions-as-values "Permalink")

In the above description, it can be difficult to see why the distinction between evaluating expressions and executing `IO` actions is necessary.
After all, each action is executed immediately after it is produced.
Why not simply carry out the effects during evaluation, as is done in other languages?

The answer is twofold.
First off, separating evaluation from execution means that programs must be explicit about which functions can have side effects.
Because the parts of the program that do not have effects are much more amenable to mathematical reasoning, whether in the heads of programmers or using Lean's facilities for formal proof, this separation can make it easier to avoid bugs.
Secondly, not all `IO` actions need be executed at the time that they come into existence.
The ability to mention an action without carrying it out allows ordinary functions to be used as control structures.

For example, the function `twice` takes an `IO` action as its argument, returning a new action that will execute the argument action twice.

`def twice (action : IO Unit) : IO Unit := do
action
action`

Executing

`twice (IO.println "shy")`

results in


```lean
shy
shy
```


being printed.
This can be generalized to a version that runs the underlying action any number of times:

`def nTimes (action : IO Unit) : Nat → IO Unit
| 0 => pure ()
| n + 1 => do
action
nTimes action n`

In the base case for `Nat.zero`, the result is `pure ()`.
The function `pure` creates an `IO` action that has no side effects, but returns `pure`'s argument, which in this case is the constructor for `Unit`.
As an action that does nothing and returns nothing interesting, `pure ()` is at the same time utterly boring and very useful.
In the recursive step, a `do` block is used to create an action that first executes `action` and then executes the result of the recursive call.
Executing `Hello
Hello
Hello
#eval nTimes (IO.println "Hello") 3` causes the following output:


```lean
Hello
Hello
Hello
```


In addition to using functions as control structures, the fact that `IO` actions are first-class values means that they can be saved in data structures for later execution.
For instance, the function `countdown` takes a `Nat` and returns a list of unexecuted `IO` actions, one for each `Nat`:

`def countdown : Nat → List (IO Unit)
| 0 => [IO.println "Blast off!"]
| n + 1 => IO.println s!"{n + 1}" :: countdown n`

This function has no side effects, and does not print anything.
For example, it can be applied to an argument, and the length of the resulting list of actions can be checked:

`def from5 : List (IO Unit) := countdown 5`

This list contains six elements (one for each number, plus a `"Blast off!"` action for zero):

`#eval from5.length`


```lean
6
```


The function `runActions` takes a list of actions and constructs a single action that runs them all in order:

`def runActions : List (IO Unit) → IO Unit
| [] => pure ()
| act :: actions => do
act
runActions actions`

Its structure is essentially the same as that of `nTimes`, except instead of having one action that is executed for each `Nat.succ`, the action under each `List.cons` is to be executed.
Similarly, `runActions` does not itself run the actions.
It creates a new action that will run them, and that action must be placed in a position where it will be executed as a part of `main`:

`def main : IO Unit := runActions from5`

Running this program results in the following output:

`countdown``5
4
3
2
1
Blast off!`

What happens when this program is run?
The first step is to evaluate `main`. That occurs as follows:

`main``runActions from5``runActions (countdown 5)``runActions
[IO.println "5",
IO.println "4",
IO.println "3",
IO.println "2",
IO.println "1",
IO.println "Blast off!"]``do IO.println "5"
IO.println "4"
IO.println "3"
IO.println "2"
IO.println "1"
IO.println "Blast off!"
pure ()`

The resulting `IO` action is a `do` block.
Each step of the `do` block is then executed, one at a time, yielding the expected output.
The final step, `pure ()`, does not have any effects, and it is only present because the definition of `runActions` needs a base case.

## 2.2.5. Exercise[🔗](find/?domain=Verso.Genre.Manual.section&name=step-by-step-exercise "Permalink")

Step through the execution of the following program on a piece of paper:

`def main : IO Unit := do
let englishGreeting := IO.println "Hello!"
IO.println "Bonjour!"
englishGreeting`

While stepping through the program's execution, identify when an expression is being evaluated and when an `IO` action is being executed.
When executing an `IO` action results in a side effect, write it down.
After doing this, run the program with Lean and double-check that your predictions about the side effects were correct.

[←2.1. Running a Program](Hello___-World___/Running-a-Program/#running-a-program "2.1. Running a Program")[2.3. Starting a Project→](Hello___-World___/Starting-a-Project/#starting-a-project "2.3. Starting a Project")
