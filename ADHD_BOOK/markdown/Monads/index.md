# Study guide: 4. Monads 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **4. Monads 🔗** — In C# and Kotlin, the ?. operator is a way to look up a property or call a method on a potentially-null value.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←3.8. Summary](Overloading-and-Type-Classes/Summary/#type-classes-summary "3.8. Summary")[4.1. One API, Many Applications→](Monads/One-API___-Many-Applications/#monad-api-examples "4.1. One API, Many Applications")

# 4. Monads[🔗](find/?domain=Verso.Genre.Manual.section&name=monads "Permalink")

In C# and Kotlin, the `?.` operator is a way to look up a property or call a method on a potentially-null value.
If the receiver is `null`, the whole expression is null.
Otherwise, the underlying non-`null` value receives the call.
Uses of `?.` can be chained, in which case the first `null` result terminates the chain of lookups.
Chaining null-checks like this is much more convenient than writing and maintaining deeply nested `if`s.

Similarly, exceptions are significantly more convenient than manually checking and propagating error codes.
At the same time, logging is easiest to accomplish by having a dedicated logging framework, rather than having each function return both its log results and its return value.
Chained null checks and exceptions typically require language designers to anticipate this use case, while logging frameworks typically make use of side effects to decouple code that logs from the accumulation of the logs.

1. [4.1. One API, Many Applications](Monads/One-API___-Many-Applications/#monad-api-examples)
2. [4.2. The Monad Type Class](Monads/The-Monad-Type-Class/#monad-type-class)
3. [4.3. Example: Arithmetic in Monads](Monads/Example___-Arithmetic-in-Monads/#monads-arithmetic-example)
4. [4.4. `do`-Notation for Monads](Monads/do--Notation-for-Monads/#monad-do-notation)
5. [4.5. The IO Monad](Monads/The-IO-Monad/#io-monad)
6. [4.6. Additional Conveniences](Monads/Additional-Conveniences/#monads-conveniences)
7. [4.7. Summary](Monads/Summary/#monads-summary)

[←3.8. Summary](Overloading-and-Type-Classes/Summary/#type-classes-summary "3.8. Summary")[4.1. One API, Many Applications→](Monads/One-API___-Many-Applications/#monad-api-examples "4.1. One API, Many Applications")
