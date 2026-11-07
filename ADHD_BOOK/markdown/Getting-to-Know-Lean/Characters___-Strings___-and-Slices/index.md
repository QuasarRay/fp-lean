# Study guide: 1.7. Characters, Strings, and Slices 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.7. Characters, Strings, and Slices 🔗** — In Lean, strings contain Unicode text.
- **1.7.1. Slices 🔗** — Strings are represented by their UTF-8 encoding as an array of bytes paired with a cached character count.
- **1.7.2. Matching 🔗** — Functions that match parts of strings, such as String.dropWhile and String.dropEndWhile , are overloaded.
- **1.7.3. Messages You May Meet 🔗** — The overloaded string-matching functions are implemented using features that are explained later in the book, namely type classes and dependent types .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.6. Polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism "1.6. Polymorphism")[1.8. Additional Conveniences→](Getting-to-Know-Lean/Additional-Conveniences/#getting-to-know-conveniences "1.8. Additional Conveniences")

# 1.7. Characters, Strings, and Slices[🔗](find/?domain=Verso.Genre.Manual.section&name=chars-strings-slices "Permalink")

In Lean, strings contain Unicode text.
Specifically, they are sequences of characters, and characters are Unicode code points.
Strings are written in double quotes, and individual characters are written in single quotes.
The type of strings is `String` and the type of characters is `Char`.

Strings can be appended with the `++` operator:

`"Hello, world"#eval "Hello, " ++ "world"`


```lean
"Hello, world"
```


A character can be added to the end of a string using `String.push`:

`"Hello!"#eval String.push "Hello" '!'`


```lean
"Hello!"
```


This function can also be called using the [dot notation](Getting-to-Know-Lean/Structures/#behind-the-scenes) that is used with structure accessors:

`"Hello!"#eval "Hello".push '!'`


```lean
"Hello!"
```


## 1.7.1. Slices[🔗](find/?domain=Verso.Genre.Manual.section&name=string-slices "Permalink")

Strings are represented by their UTF-8 encoding as an array of bytes paired with a cached character count.
This means that removing even a single character from a string can result in copying the remaining characters to a new string.

To allow string-processing code to be written from small, composable pieces, many string operations return *string slices*, which are regions of some other string.
String slices have the type `String.Slice`.
A slice contains a reference to a string along with the start and end positions of the slice, and multiple slices can share the same string.
Operations such as dropping prefixes of strings return slices rather than allocating new strings, and large parts of the string API are also implemented for slices.

Operations that return slices include `String.trimAscii`, which returns a slice that drops leading and trailing space, tab, newline, and carriage return characters from a string; `String.drop` and `String.dropEnd`, which drop the specified number of characters from the start or end of a string; and `String.dropWhile` and `String.dropEndWhile`, which respectively remove all the characters that match a pattern from the beginning or end of a string.
The patterns used to search in strings are distinct from those used for [pattern matching](Getting-to-Know-Lean/Datatypes-and-Patterns/#pattern-matching); in the string API, they are function arguments that specify characters or specific substrings to match.
The string slice API includes all the slice-producing string functions as well, which makes it possible to write string manipulations as a series of incremental steps without risking intermediate string copying.

This code removes characters from the beginning and end of a string without allocating an intermediate string:

`"tortoise"#eval (("small tortoiseshell".drop 6).dropEnd 5).copy`


```lean
"tortoise"
```


The function `String.Slice.copy` returns a copy of the region of the underlying string that the slice indicates.
The initial call to `String.drop` returns a slice, and the call to `String.Slice.dropEnd` returns an adjusted slice.
The final call to `copy` creates a string once more.

Unlike strings, slices do not cache a character count.
Because the UTF-8 encoding of characters may occupy multiple bytes, there's no efficient way to check the length of a string slice.
However, checking whether it is empty can be accomplished with `String.Slice.isEmpty`.

## 1.7.2. Matching[🔗](find/?domain=Verso.Genre.Manual.section&name=string-matching "Permalink")

Functions that match parts of strings, such as `String.dropWhile` and `String.dropEndWhile`, are overloaded.
They can be called with a variety of different *patterns*, each of which matches substrings in its own way.

The pattern can be a character, in which case runs of the character are removed:

`red admira#eval "red admiral".dropEndWhile 'l'`


```lean
red admira
```


The output is not in quotes because it is a string slice, and string slices are displayed without surrounding quotes.
The pattern may also be a string, in which case runs of the complete string are removed:

`butterfly#eval "the the butterfly".dropWhile "the "`


```lean
butterfly
```


Incomplete matches are not removed:

`grayling#eval ("a gray grayling".drop 2).dropWhile "gray "`


```lean
grayling
```


The pattern may also be a function that returns `true` or `false`.
Characters are removed until the function returns `false`.
The slice is converted to a string in order to illustrate that the trailing space remains:

`"red "#eval ("red admiral".dropEndWhile Char.isAlpha).copy`


```lean
"red "
```


## 1.7.3. Messages You May Meet[🔗](find/?domain=Verso.Genre.Manual.section&name=string-messages-you-may-meet "Permalink")

The overloaded string-matching functions are implemented using features that are explained later in the book, namely [type classes](Overloading-and-Type-Classes/#type-classes) and [dependent types](Programming-with-Dependent-Types/#dependent-types).
There are two error messages in particular that are useful to learn to read before learning about those features of Lean.

Calling the functions without a pattern results in an error:

`` #eval don't know how to synthesize implicit argument `ρ`
@String.dropEndWhile ?m.2 "red admiral"
context:
⊢ Type"red admiral".dropEndWhile ``


```lean
don't know how to synthesize implicit argument `ρ`
  @String.dropEndWhile ?m.2 "red admiral"
context:
⊢ Type
```


This error is stating that Lean can't determine which pattern type to use, because no pattern was provided.
It can be fixed by providing a pattern.

When the functions are called with an argument that isn't a valid pattern, there is a compile-time error:

`` #eval failed to synthesize instance of type class
String.Slice.Pattern.BackwardPattern [12]

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command."12345abcde".dropEndWhile [12] ``


```lean
failed to synthesize instance of type class
  String.Slice.Pattern.BackwardPattern [12]

Hint: Type class instance resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` command.
```


This error message means that `String.dropEndWhile` is not overloaded for the pattern `[12]`.
It can be fixed by providing a meaningful pattern, such as a function, character, or string.

[←1.6. Polymorphism](Getting-to-Know-Lean/Polymorphism/#polymorphism "1.6. Polymorphism")[1.8. Additional Conveniences→](Getting-to-Know-Lean/Additional-Conveniences/#getting-to-know-conveniences "1.8. Additional Conveniences")
