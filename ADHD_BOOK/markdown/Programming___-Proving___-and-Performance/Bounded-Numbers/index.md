# Study guide: 8.5. Bounded Numbers 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **8.5. Bounded Numbers 🔗** — The GetElem instance for Array and Nat requires a proof that the provided Nat is smaller than the array.
- **8.5.1. Exercise 🔗** — Write a function Fin.next?

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←8.4. More Inequalities](Programming___-Proving___-and-Performance/More-Inequalities/#more-inequalities "8.4. More Inequalities")[8.6. Insertion Sort and Array Mutation→](Programming___-Proving___-and-Performance/Insertion-Sort-and-Array-Mutation/#insertion-sort-mutation "8.6. Insertion Sort and Array Mutation")

# 8.5. Bounded Numbers[🔗](find/?domain=Verso.Genre.Manual.section&name=Fin "Permalink")

The `GetElem` instance for `Array` and `Nat` requires a proof that the provided `Nat` is smaller than the array.
In practice, these proofs often end up being passed to functions along with the indices.
Rather than passing an index and a proof separately, a type called `Fin` can be used to bundle up the index and the proof into a single value.
This can make code easier to read.

The type `Fin n` represents numbers that are strictly less than `n`.
In other words, `Fin 3` describes `0`, `1`, and `2`, while `Fin 0` has no values at all.
The definition of `Fin` resembles `Subtype`, as a `Fin n` is a structure that contains a `Nat` and a proof that it is less than `n`:

`structure Fin (n : Nat) where
val : Nat
isLt : LT.lt val n`

Lean includes instances of `ToString` and `OfNat` that allow `Fin` values to be conveniently used as numbers.
In other words, the output of `#eval (5 : Fin 8)` is `5`, rather than something like `{val := 5, isLt := _}`.

Instead of failing when the provided number is larger than the bound, the `OfNat` instance for `Fin` returns a value modulo the bound.
This means that `#eval (45 : Fin 10)` results in `5` rather than a compile-time error.

In a return type, a `Fin` returned as a found index makes its connection to the data structure in which it was found more clear.
The `Array.find` in the [previous section](Programming___-Proving___-and-Performance/Arrays-and-Termination/#proving-termination) returns an index that the caller cannot immediately use to perform lookups into the array, because the information about its validity has been lost.
A more specific type results in a value that can be used without making the program significantly more complicated:

`def findHelper (arr : Array α) (p : α → Bool) (i : Nat) :
Option (Fin arr.size × α) :=
if h : i < arr.size then
let x := arr[i]
if p x then
some (⟨i, h⟩, x)
else findHelper arr p (i + 1)
else none``def Array.find (arr : Array α) (p : α → Bool) : Option (Fin arr.size × α) :=
findHelper arr p 0`

## 8.5.1. Exercise[🔗](find/?domain=Verso.Genre.Manual.section&name=Fin-exercises "Permalink")

Write a function `Fin.next? : Fin n → Option (Fin n)` that returns the next largest `Fin` when it would be in bounds, or `none` if not.
Check that

`some 4#eval (3 : Fin 8).next?`

outputs


```lean
some 4
```


and that

`none#eval (7 : Fin 8).next?`

outputs


```lean
none
```


[←8.4. More Inequalities](Programming___-Proving___-and-Performance/More-Inequalities/#more-inequalities "8.4. More Inequalities")[8.6. Insertion Sort and Array Mutation→](Programming___-Proving___-and-Performance/Insertion-Sort-and-Array-Mutation/#insertion-sort-mutation "8.6. Insertion Sort and Array Mutation")
