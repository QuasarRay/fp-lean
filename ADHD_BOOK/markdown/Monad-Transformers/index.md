# Study guide: 6. Monad Transformers 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **6. Monad Transformers 🔗** — A monad is a way to encode some collection of side effects in a pure language.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←5.7. Summary](Functors___-Applicative-Functors___-and-Monads/Summary/#structure-applicative-monad-summary "5.7. Summary")[6.1. Combining IO and Reader→](Monad-Transformers/Combining-IO-and-Reader/#io-reader "6.1. Combining IO and Reader")

# 6. Monad Transformers[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Monad-Transformers "Permalink")

A monad is a way to encode some collection of side effects in a pure language.
Different monads provide different effects, such as state and error handling.
Many monads even provide useful effects that aren't available in most languages, such as nondeterministic searches, readers, and even continuations.

A typical application has a core set of easily testable functions written without monads paired with an outer wrapper that uses a monad to encode the necessary application logic.
These monads are constructed from well-known components.
For example:

- Mutable state is encoded with a function parameter and a return value that have the same type
- Error handling is encoded by having a return type that is similar to `Except`, with constructors for success and failure
- Logging is encoded by pairing the return value with the log

Writing each monad by hand is tedious, however, involving boilerplate definitions of the various type classes.
Each of these components can also be extracted to a definition that modifies some other monad to add an additional effect.
Such a definition is called a *monad transformer*.
A concrete monad can be build from a collection of monad transformers, which enables much more code re-use.

1. [6.1. Combining IO and Reader](Monad-Transformers/Combining-IO-and-Reader/#io-reader)
2. [6.2. A Monad Construction Kit](Monad-Transformers/A-Monad-Construction-Kit/#Functional-Programming-in-Lean--Monad-Transformers--A-Monad-Construction-Kit)
3. [6.3. Ordering Monad Transformers](Monad-Transformers/Ordering-Monad-Transformers/#monad-transformer-order)
4. [6.4. More do Features](Monad-Transformers/More-do-Features/#more-do-features)
5. [6.5. Additional Conveniences](Monad-Transformers/Additional-Conveniences/#monad-transformer-conveniences)
6. [6.6. Summary](Monad-Transformers/Summary/#monad-transformer-summary)

[←5.7. Summary](Functors___-Applicative-Functors___-and-Monads/Summary/#structure-applicative-monad-summary "5.7. Summary")[6.1. Combining IO and Reader→](Monad-Transformers/Combining-IO-and-Reader/#io-reader "6.1. Combining IO and Reader")
