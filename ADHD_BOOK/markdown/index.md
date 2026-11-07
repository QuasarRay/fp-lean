# Study guide: Functional Programming in Lean 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **Functional Programming in Lean 🔗** — Copyright Microsoft Corporation 2023 and Lean FRO, LLC 2023–2026

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[Introduction→](Introduction/#Functional-Programming-in-Lean--Introduction "Introduction")

# Functional Programming in Lean[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean "Permalink")

David Thrane Christiansen

*Copyright Microsoft Corporation 2023 and Lean FRO, LLC 2023–2026*

This is a free book on using Lean as a programming language. All code samples are tested with Lean release `4.33.0`.

## Contents

1. [Introduction](Introduction/#Functional-Programming-in-Lean--Introduction)
2. [Acknowledgments](Acknowledgments/#Functional-Programming-in-Lean--Acknowledgments)
3. [1. Getting to Know Lean](Getting-to-Know-Lean/#getting-to-know)
4. [2. Hello, World!](Hello___-World___/#hello-world)
5. [Interlude: Propositions, Proofs, and Indexing](Interlude___-Propositions___-Proofs___-and-Indexing/#props-proofs-indexing)
6. [3. Overloading and Type Classes](Overloading-and-Type-Classes/#type-classes)
7. [4. Monads](Monads/#monads)
8. [5. Functors, Applicative Functors, and Monads](Functors___-Applicative-Functors___-and-Monads/#Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads)
9. [6. Monad Transformers](Monad-Transformers/#Functional-Programming-in-Lean--Monad-Transformers)
10. [7. Programming with Dependent Types](Programming-with-Dependent-Types/#dependent-types)
11. [Interlude: Tactics, Induction, and Proofs](Interlude___-Tactics___-Induction___-and-Proofs/#tactics-induction-proofs)
12. [8. Programming, Proving, and Performance](Programming___-Proving___-and-Performance/#Functional-Programming-in-Lean--Programming___-Proving___-and-Performance)
13. [9. Next Steps](Next-Steps/#next-steps)

[Introduction→](Introduction/#Functional-Programming-in-Lean--Introduction "Introduction")
