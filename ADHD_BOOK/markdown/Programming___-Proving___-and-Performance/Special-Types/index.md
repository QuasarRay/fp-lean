# Study guide: 8.7. Special Types 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **8.7. Special Types 🔗** — Understanding the representation of data in memory is very important.
- **8.7.1. Exercise 🔗** — The definition of Pos does not take advantage of Lean's compilation of Nat to an efficient type.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←8.6. Insertion Sort and Array Mutation](Programming___-Proving___-and-Performance/Insertion-Sort-and-Array-Mutation/#insertion-sort-mutation "8.6. Insertion Sort and Array Mutation")[8.8. Summary→](Programming___-Proving___-and-Performance/Summary/#programs-proofs-summary "8.8. Summary")

# 8.7. Special Types[🔗](find/?domain=Verso.Genre.Manual.section&name=runtime-special-types "Permalink")

Understanding the representation of data in memory is very important.
Usually, the representation can be understood from the definition of a datatype.
Each constructor corresponds to an object in memory that has a header that includes a tag and a reference count.
The constructor's arguments are each represented by a pointer to some other object.
In other words, `List` really is a linked list and extracting a field from a `structure` really does just chase a pointer.

There are, however, some important exceptions to this rule.
A number of types are treated specially by the compiler.
For example, the type `UInt32` is defined as `Fin (2 ^ 32)`, but it is replaced at run-time with an actual native implementation based on machine words.
Similarly, even though the definition of `Nat` suggests an implementation similar to `List Unit`, the actual run-time representation uses immediate machine words for sufficiently-small numbers and an efficient arbitrary-precision arithmetic library for larger numbers.
The Lean compiler translates from definitions that use pattern matching into the appropriate operations for this representation, and calls to operations like addition and subtraction are mapped to fast operations from the underlying arithmetic library.
After all, addition should not take time linear in the size of the addends.

The fact that some types have special representations also means that care is needed when working with them.
Most of these types consist of a `structure` that is treated specially by the compiler.
With these structures, using the constructor or the field accessors directly can trigger expensive conversions between efficient representations and representations designed for use in proofs.

For example, arrays are defined as structures that wrap linked lists.
In compiled code, they are represented as efficient dynamic arrays, and applying the constructor `Array.mk` to a list converts the list to such an efficient array, which takes linear time.
The field accessor `toList` converts the array back to a linked list, which also takes linear time.
This definition of `Array` exists entirely to make it easier to prove things about arrays, and these conversions should be avoided in code that is intended to be run.
Similarly, `String` is defined as a structure that contains an array of bytes together with a proof that the bytes are valid UTF-8, but the run-time representation additionally includes a field that caches the number of characters in the string.
Applying the constructor to a byte array can only be done when the byte array is valid, so there's no need to check that the bytes are in fact a UTF-8 sequence, but the character count is computed in linear time.
The accessor `toByteArray` allocates a new byte array object and copies the underlying bytes, taking linear time and space.
Many of the basic operations on strings are replaced by the compiler with efficient versions that mutate the run-time version of the string when possible instead of allocating a new one.

Both types themselves and proofs of propositions are completely erased from compiled code.
In other words, they take up no space, and any computations that might have been performed as part of a proof are similarly erased.
This means that proofs can take advantage of the convenient interface to arrays as inductively-defined lists, including using induction to prove things about them, without imposing slow conversion steps while the program is running.
For these built-in types, a convenient logical representation of the data does not imply that the program must be slow.

If a structure type has only a single non-type non-proof field, then the constructor itself disappears at run time, being replaced with its single argument.
In other words, a subtype is represented identically to its underlying type, rather than with an extra layer of indirection.
Similarly, `Fin` is just `Nat` in memory, and single-field structures can be created to keep track of different uses of `Nat`s or `String`s without paying a performance penalty.
If a constructor has no non-type non-proof arguments, then the constructor also disappears and is replaced with a constant value where the pointer would otherwise be used.
This means that `true`, `false`, and `none` are constant values, rather than pointers to heap-allocated objects.

The following types have special representations:

| Type | Logical representation | Run-time Representation |
| --- | --- | --- |
| `Nat` | Unary, with one pointer from each `Nat.succ` | Efficient arbitrary-precision integers |
| `Int` | A sum type with constructors for positive or negative values, each containing a `Nat` | Efficient arbitrary-precision integers |
| `BitVec w` | A `Fin` with an appropriate bound `2^w` | Efficient arbitrary-precision integers |
| `UInt8`, `UInt16`, `UInt32`, `UInt64`, `USize` | A bitvector of the correct width | Fixed-precision machine integers |
| `Int8`, `Int16`, `Int32`, `Int64`, `ISize` | A wrapped unsigned integer of the same width | Fixed-precision machine integers |
| `Char` | A `UInt32` paired with a proof that it's a valid code point | Ordinary characters |
| `String` | A structure that contains a `ByteArray` in a field called `toByteArray`, along with a proof that the array is valid UTF-8 | UTF-8-encoded string and character count |
| `Array α` | A structure that contains a `List α` in a field called `toList` | Packed arrays of pointers to `α` values |
| `Sort u` | A type | Erased completely |
| Proofs of propositions | Whatever data is suggested by the proposition when considered as a type of evidence | Erased completely |

## 8.7.1. Exercise[🔗](find/?domain=Verso.Genre.Manual.section&name=runtime-special-types-exercise "Permalink")

The [definition of `Pos`](Overloading-and-Type-Classes/Positive-Numbers/#positive-numbers) does not take advantage of Lean's compilation of `Nat` to an efficient type.
At run time, it is essentially a linked list.
Alternatively, a subtype can be defined that allows Lean's fast `Nat` type to be used internally, as described [in the initial section on subtypes](Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/#subtypes).
At run time, the proof will be erased.
Because the resulting structure has only a single data field, it is represented as that field, which means that this new representation of `Pos` is identical to that of `Nat`.

After proving the theorem `∀ {n k : Nat}, n ≠ 0 → k ≠ 0 → n + k ≠ 0`, define instances of `ToString`, and `Add` for this new representation of `Pos`. Then, define an instance of `Mul`, proving any necessary theorems along the way.

[←8.6. Insertion Sort and Array Mutation](Programming___-Proving___-and-Performance/Insertion-Sort-and-Array-Mutation/#insertion-sort-mutation "8.6. Insertion Sort and Array Mutation")[8.8. Summary→](Programming___-Proving___-and-Performance/Summary/#programs-proofs-summary "8.8. Summary")
