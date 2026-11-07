# Study guide: 1. Getting to Know Lean 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1. Getting to Know Lean 🔗** — According to tradition, a programming language should be introduced by compiling and running a program that displays "Hello, world!" on the console.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←Acknowledgments](Acknowledgments/#Functional-Programming-in-Lean--Acknowledgments "Acknowledgments")[1.1. Evaluating Expressions→](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating "1.1. Evaluating Expressions")

# 1. Getting to Know Lean[🔗](find/?domain=Verso.Genre.Manual.section&name=getting-to-know "Permalink")

According to tradition, a programming language should be introduced by compiling and running a program that displays `"Hello, world!"` on the console.
This simple program ensures that the language tooling is installed correctly and that the programmer is able to run the compiled code.

Since the 1970s, however, programming has changed.
Today, compilers are typically integrated into text editors, and the programming environment offers feedback as the program is written.
Lean is no exception: it implements an extended version of the Language Server Protocol that allows it to communicate with a text editor and provide feedback as the user types.

Languages as varied as Python, Haskell, and JavaScript offer a read-eval-print-loop (REPL), also known as an interactive toplevel or a browser console, in which expressions or statements can be entered.
The language then computes and displays the result of the user's input.
Lean, on the other hand, integrates these features into the interaction with the editor, providing commands that cause the text editor to display feedback integrated into the program text itself.
This chapter provides a short introduction to interacting with Lean in an editor, while [Hello, World!](Hello___-World___/#hello-world) describes how to use Lean traditionally from the command line in batch mode.

It is best if you read this book with Lean open in your editor, following along and typing in each example. Please play with the
examples, and see what happens!

1. [1.1. Evaluating Expressions](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating)
2. [1.2. Types](Getting-to-Know-Lean/Types/#getting-to-know-types)
3. [1.3. Functions and Definitions](Getting-to-Know-Lean/Functions-and-Definitions/#functions-and-definitions)
4. [1.4. Structures](Getting-to-Know-Lean/Structures/#structures)
5. [1.5. Datatypes and Patterns](Getting-to-Know-Lean/Datatypes-and-Patterns/#datatypes-and-patterns)
6. [1.6. Polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism)
7. [1.7. Characters, Strings, and Slices](Getting-to-Know-Lean/Characters___-Strings___-and-Slices/#chars-strings-slices)
8. [1.8. Additional Conveniences](Getting-to-Know-Lean/Additional-Conveniences/#getting-to-know-conveniences)
9. [1.9. Summary](Getting-to-Know-Lean/Summary/#getting-to-know-summary)

[←Acknowledgments](Acknowledgments/#Functional-Programming-in-Lean--Acknowledgments "Acknowledgments")[1.1. Evaluating Expressions→](Getting-to-Know-Lean/Evaluating-Expressions/#evaluating "1.1. Evaluating Expressions")
