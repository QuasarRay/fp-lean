# Study guide: 1.9. Summary 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.9.1. Evaluating Expressions 🔗** — In Lean, computation occurs when expressions are evaluated.
- **1.9.2. Functions 🔗** — Functions in Lean are first-class values, meaning that they can be passed as arguments to other functions, saved in variables, and used like any other value.
- **1.9.3. Types 🔗** — Lean checks that every expression has a type.
- **1.9.4. Structures and Inductive Types 🔗** — Brand new datatypes can be introduced to Lean using the structure or inductive features.
- **1.9.5. Strings and Slices 🔗** — Strings are sequences of characters, which are themselves Unicode code points.
- **1.9.6. Recursion 🔗** — A definition is recursive when the name being defined is used in the definition itself.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.8. Additional Conveniences](Getting-to-Know-Lean/Additional-Conveniences/#getting-to-know-conveniences "1.8. Additional Conveniences")[2. Hello, World!→](Hello___-World___/#hello-world "2. Hello, World!")

# 1.9. Summary[🔗](find/?domain=Verso.Genre.Manual.section&name=getting-to-know-summary "Permalink")

## 1.9.1. Evaluating Expressions[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Evaluating-Expressions "Permalink")

In Lean, computation occurs when expressions are evaluated.
This follows the usual rules of mathematical expressions: sub-expressions are replaced by their values following the usual order of operations, until the entire expression has become a value.
When evaluating an `if` or a `match`, the expressions in the branches are not evaluated until the value of the condition or the match subject has been found.

Once they have been given a value, variables never change.
Similarly to mathematics but unlike most programming languages, Lean variables are simply placeholders for values, rather than addresses to which new values can be written.
Variables' values may come from global definitions with `def`, local definitions with `let`, as named arguments to functions, or from pattern matching.

## 1.9.2. Functions[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Functions "Permalink")

Functions in Lean are first-class values, meaning that they can be passed as arguments to other functions, saved in variables, and used like any other value.
Every Lean function takes exactly one argument.
To encode a function that takes more than one argument, Lean uses a technique called currying, where providing the first argument returns a function that expects the remaining arguments.
To encode a function that takes no arguments, Lean uses the `Unit` type, which is the least informative possible argument.

There are three primary ways of creating functions:

1. Anonymous functions are written using `fun`.
   For instance, a function that swaps the fields of a `Point` can be written `fun (point : Point) => { x := point.y, y := point.x : Point }`
2. Very simple anonymous functions are written by placing one or more centered dots `·` inside of parentheses.
   Each centered dot becomes an argument to the function, and the parentheses delimit its body.
   For instance, a function that subtracts one from its argument can be written as `(· - 1)` instead of as `fun x => x - 1`.
3. Functions can be defined using `def` or `let` by adding an argument list or by using pattern-matching notation.

## 1.9.3. Types[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Types "Permalink")

Lean checks that every expression has a type.
Types, such as `Int`, `Point`, `{α : Type} → Nat → α → List α`, and `Option (String ⊕ (Nat × String))`, describe the values that may eventually be found for an expression.
Like other languages, types in Lean can express lightweight specifications for programs that are checked by the Lean compiler, obviating the need for certain classes of unit test.
Unlike most languages, Lean's types can also express arbitrary mathematics, unifying the worlds of programming and theorem proving.
While using Lean for proving theorems is mostly out of scope for this book, *[Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)* contains more information on this topic.

Some expressions can be given multiple types.
For instance, `3` can be an `Int` or a `Nat`.
In Lean, this should be understood as two separate expressions, one with type `Nat` and one with type `Int`, that happen to be written in the same way, rather than as two different types for the same thing.

Lean is sometimes able to determine types automatically, but types must often be provided by the user.
This is because Lean's type system is so expressive.
Even when Lean can find a type, it may not find the desired type—`3` could be intended to be used as an `Int`, but Lean will give it the type `Nat` if there are no further constraints.
In general, it is a good idea to write most types explicitly, only letting Lean fill out the very obvious types.
This improves Lean's error messages and helps make programmer intent more clear.

Some functions or datatypes take types as arguments.
They are called *polymorphic*.
Polymorphism allows programs such as one that calculates the length of a list without caring what type the entries in the list have.
Because types are first class in Lean, polymorphism does not require any special syntax, so types are passed just like other arguments.
Naming an argument in a function type allows later types to mention that name, and when the function is applied to an argument, the type of the resulting term is found by replacing the argument's name with the actual value it was applied to.

## 1.9.4. Structures and Inductive Types[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Structures-and-Inductive-Types "Permalink")

Brand new datatypes can be introduced to Lean using the `structure` or `inductive` features.
These new types are not considered to be equivalent to any other type, even if their definitions are otherwise identical.
Datatypes have *constructors* that explain the ways in which their values can be constructed, and each constructor takes some number of arguments.
Constructors in Lean are not the same as constructors in object-oriented languages: Lean's constructors are inert holders of data, rather than active code that initializes an allocated object.

Typically, `structure` is used to introduce a product type (that is, a type with just one constructor that takes any number of arguments), while `inductive` is used to introduce a sum type (that is, a type with many distinct constructors).
Datatypes defined with `structure` are provided with one accessor function for each field.
Both structures and inductive datatypes may be consumed with pattern matching, which exposes the values stored inside of constructors using a subset of the syntax used to call said constructors.
Pattern matching means that knowing how to create a value implies knowing how to consume it.

## 1.9.5. Strings and Slices[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Strings-and-Slices "Permalink")

Strings are sequences of characters, which are themselves Unicode code points.
Their run-time representation consists of an array of bytes in the UTF-8 encoding and a cached character count field.
Because Lean is a pure functional language, operations such as trimming whitespace from strings would normally need to copy them.
This is avoided by having many functions on strings return [string slices](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#--tech-term-string-slices), which pair a reference to a string with starting and ending positions.
Slices can be manipulated by updating these starting and ending positions, avoiding copying.

## 1.9.6. Recursion[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Getting-to-Know-Lean--Summary--Recursion "Permalink")

A definition is recursive when the name being defined is used in the definition itself.
Because Lean is an interactive theorem prover in addition to being a programming language, there are certain restrictions placed on recursive definitions.
In Lean's logical side, circular definitions could lead to logical inconsistency.

In order to ensure that recursive definitions do not undermine the logical side of Lean, Lean must be able to prove that all recursive functions terminate, no matter what arguments they are called with.
In practice, this means either that recursive calls are all performed on a structurally-smaller piece of the input, which ensures that there is always progress towards a base case, or that users must provide some other evidence that the function always terminates.
Similarly, recursive inductive types are not allowed to have a constructor that takes a function *from* the type as an argument, because this would make it possible to encode non-terminating functions.

[←1.8. Additional Conveniences](Getting-to-Know-Lean/Additional-Conveniences/#getting-to-know-conveniences "1.8. Additional Conveniences")[2. Hello, World!→](Hello___-World___/#hello-world "2. Hello, World!")


> **Review needed:** The following headings have no short source sentence: 1.9. Summary 🔗