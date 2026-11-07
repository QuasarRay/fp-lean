# Study guide: 1.1. Evaluating Expressions 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.1. Evaluating Expressions 🔗** — The most important thing to understand as a programmer learning Lean is how evaluation works.
- **1.1.1. Messages You May Meet 🔗** — Asking Lean to evaluate a function application that is missing an argument will lead to an error message.
- **1.1.2. Exercises 🔗** — What are the values of the following expressions?

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1. Getting to Know Lean](Getting-to-Know-Lean/#getting-to-know "1. Getting to Know Lean")[1.2. Types→](Getting-to-Know-Lean/Types/#getting-to-know-types "1.2. Types")

# 1.1. Evaluating Expressions[🔗](find/?domain=Verso.Genre.Manual.section&name=evaluating "Permalink")

The most important thing to understand as a programmer learning Lean is how evaluation works.
Evaluation is the process of finding the value of an expression, just as one does in arithmetic.
For instance, the value of `15 - 6` is `9` and the value of `2 × (3 + 1)` is `8`.
To find the value of the latter expression, `3 + 1` is first replaced by `4`, yielding `2 × 4`, which itself can be reduced to `8`.
Sometimes, mathematical expressions contain variables: the value of `x + 1` cannot be computed until we know what the value of `x` is.
In Lean, programs are first and foremost expressions, and the primary way to think about computation is as evaluating expressions to find their values.

Most programming languages are *imperative*, where a program consists of a series of statements that should be carried out in order to find the program's result.
Programs have access to mutable memory, so the value referred to by a variable can change over time.
In addition to mutable state, programs may have other side effects, such as deleting files, making outgoing network connections,
throwing or catching exceptions, and reading data from a database.
“Side effects” is essentially a catch-all term for describing things that may happen in a program that don't follow the model of evaluating mathematical expressions.

In Lean, however, programs work the same way as mathematical expressions.
Once given a value, variables cannot be reassigned. Evaluating an expression cannot have side effects.
If two expressions have the same value, then replacing one with the other will not cause the program to compute a different result.
This does not mean that Lean cannot be used to write `Hello, world!` to the console, but performing I/O is not a core part of the experience of using Lean in the same way.
Thus, this chapter focuses on how to evaluate expressions interactively with Lean, while the next chapter describes how to write, compile, and run the `Hello, world!` program.

To ask Lean to evaluate an expression, write `#eval` before it in your editor, which will then report the result back.
Typically, the result is found by putting the cursor or mouse pointer over `#eval`.
For instance,

`3#eval 1 + 2`

yields the value


```lean
3
```


Lean obeys the ordinary rules of precedence and associativity for
arithmetic operators. That is,

`11#eval 1 + 2 * 5`

yields the value `11` rather than `15`.

While both ordinary mathematical notation and the majority of programming languages use parentheses (e.g. `f(x)`) to apply a function to its arguments, Lean simply writes the function next to its arguments (e.g. `f x`).
Function application is one of the most common operations, so it pays to keep it concise.
Rather than writing


```lean
#eval String.append("Hello, ", "Lean!")
```


to compute `"Hello, Lean!"`, one would instead write

`"Hello, Lean!"#eval String.append "Hello, " "Lean!"`

where the function's two arguments are simply written next to it with spaces.

Just as the order-of-operations rules for arithmetic demand parentheses in the expression `(1 + 2) * 5`, parentheses are also necessary when a function's argument is to be computed via another function call.
For instance, parentheses are required in

`"great oak tree"#eval String.append "great " (String.append "oak " "tree")`

because otherwise the second `String.append` would be interpreted as an argument to the first, rather than as a function being passed `"oak "` and `"tree"` as arguments.
The value of the inner `String.append` call must be found first, after which it can be appended to `"great "`, yielding the final value `"great oak tree"`.

Imperative languages often have two kinds of conditional: a conditional *statement* that determines which instructions to carry out based on a Boolean value, and a conditional *expression* that determines which of two expressions to evaluate based on a Boolean value.
For instance, in C and C++, the conditional statement is written using `if` and `else`, while the conditional expression is written with a ternary operator in which `?` and `:` separate the condition from the branches.
In Python, the conditional statement begins with `if`, while the conditional expression puts `if` in the middle.
Because Lean is an expression-oriented functional language, there are no conditional statements, only conditional expressions.
They are written using `if`, `then`, and `else`.
For example,

`String.append "it is " (if 1 > 2 then "yes" else "no")`

evaluates to

`String.append "it is " (if false then "yes" else "no")`

which evaluates to

`String.append "it is " "no"`

which finally evaluates to `"it is no"`.

For the sake of brevity, a series of evaluation steps like this will sometimes be written with arrows between them:

`String.append "it is " (if 1 > 2 then "yes" else "no")``String.append "it is " (if false then "yes" else "no")``String.append "it is " "no"``"it is no"`

## 1.1.1. Messages You May Meet[🔗](find/?domain=Verso.Genre.Manual.section&name=evaluating-messages "Permalink")

Asking Lean to evaluate a function application that is missing an argument will lead to an error message.
In particular, the example

`` Could not synthesize a `ToExpr`, `Repr`, or `ToString` instance for type
String → String#eval String.append "it is " ``

yields a quite long error message:


```lean
Could not synthesize a `ToExpr`, `Repr`, or `ToString` instance for type
  String → String
```


This message occurs because Lean functions that are applied to only some of their arguments return new functions that are waiting for the rest of the arguments.
Lean cannot display functions to users, and thus returns an error when asked to do so.

## 1.1.2. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=evaluating-exercises "Permalink")

What are the values of the following expressions? Work them out by hand,
then enter them into Lean to check your work.

- `42 + 19`
- `String.append "A" (String.append "B" "C")`
- `String.append (String.append "A" "B") "C"`
- `if 3 == 3 then 5 else 7`
- `if 3 == 4 then "equal" else "not equal"`

[←1. Getting to Know Lean](Getting-to-Know-Lean/#getting-to-know "1. Getting to Know Lean")[1.2. Types→](Getting-to-Know-Lean/Types/#getting-to-know-types "1.2. Types")
