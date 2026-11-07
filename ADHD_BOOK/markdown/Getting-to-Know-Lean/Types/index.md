# Study guide: 1.2. Types 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.2. Types 🔗** — Types classify programs based on the values that they can
compute. Types serve a number of roles in a program:

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.1. Evaluating Expressions](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating "1.1. Evaluating Expressions")[1.3. Functions and Definitions→](Getting-to-Know-Lean/Functions-and-Definitions/#functions-and-definitions "1.3. Functions and Definitions")

# 1.2. Types[🔗](find/?domain=Verso.Genre.Manual.section&name=getting-to-know-types "Permalink")

Types classify programs based on the values that they can
compute. Types serve a number of roles in a program:

1. They allow the compiler to make decisions about the in-memory representation of a value.
2. They help programmers to communicate their intent to others, serving as a lightweight specification for the inputs and outputs of a function.
   The compiler ensures that the program adheres to this specification.
3. They prevent various potential mistakes, such as adding a number to a string, and thus reduce the number of tests that are necessary for a program.
4. They help the Lean compiler automate the production of auxiliary code that can save boilerplate.

Lean's type system is unusually expressive.
Types can encode strong specifications like “this sorting function returns a permutation of its input” and flexible specifications like “this function has different return types, depending on the value of its argument”.
The type system can even be used as a full-blown logic for proving mathematical theorems.
This cutting-edge expressive power doesn't make simpler types unnecessary, however, and understanding these simpler types is a prerequisite for using the more advanced features.

Every program in Lean must have a type. In particular, every
expression must have a type before it can be evaluated. In the
examples so far, Lean has been able to discover a type on its own, but
it is sometimes necessary to provide one. This is done using the colon
operator inside parentheses:

`3#eval (1 + 2 : Nat)`

Here, `Nat` is the type of *natural numbers*, which are arbitrary-precision unsigned integers.
In Lean, `Nat` is the default type for non-negative integer literals.
This default type is not always the best choice.
In C, unsigned integers underflow to the largest representable numbers when subtraction would otherwise yield a result less than zero.
`Nat`, however, can represent arbitrarily-large unsigned numbers, so there is no largest number to underflow to.
Thus, subtraction on `Nat` returns `zero` when the answer would have otherwise been negative.
For instance,

`0#eval (1 - 2 : Nat)`

evaluates to `0` rather than `-1`.
To use a type that can represent the negative integers, provide it directly:

`-1#eval (1 - 2 : Int)`

With this type, the result is `-1`, as expected.

To check the type of an expression without evaluating it, use `#check` instead of `#eval`. For instance:

`1 - 2 : Int#check (1 - 2 : Int)`

reports `1 - 2 : Int` without actually performing the subtraction.

When a program can't be given a type, an error is returned from both `#check` and `#eval`. For instance:

`sorry.append "world" : String#check String.append Application type mismatch: The argument
["hello", " "]
has type
List String
but is expected to have type
String
in the application
String.append ["hello", " "]["hello", " "] "world"`

outputs


```lean
Application type mismatch: The argument
  ["hello", " "]
has type
  List String
but is expected to have type
  String
in the application
  String.append ["hello", " "]
```


because the first argument to `String.append` is expected to be a string, but a list of strings was provided instead.

[←1.1. Evaluating Expressions](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating "1.1. Evaluating Expressions")[1.3. Functions and Definitions→](Getting-to-Know-Lean/Functions-and-Definitions/#functions-and-definitions "1.3. Functions and Definitions")
