# Study guide: 5. Functors, Applicative Functors, and Monads 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **5. Functors, Applicative Functors, and Monads 🔗** — Functor and Monad both describe operations for types that are still waiting for a type argument.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←4.7. Summary](Monads/Summary/#monads-summary "4.7. Summary")[5.1. Structures and Inheritance→](Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/#structure-inheritance "5.1. Structures and Inheritance")

# 5. Functors, Applicative Functors, and Monads[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Functors___-Applicative-Functors___-and-Monads "Permalink")

`Functor` and `Monad` both describe operations for types that are still waiting for a type argument.
One way to understand them is that `Functor` describes containers in which the contained data can be transformed, and `Monad` describes an encoding of programs with side effects.
This understanding is incomplete, however.
After all, `Option` has instances for both `Functor` and `Monad`, and simultaneously represents an optional value *and* a computation that might fail to return a value.

From the perspective of data structures, `Option` is a bit like a nullable type or like a list that can contain at most one entry.
From the perspective of control structures, `Option` represents a computation that might terminate early without a result.
Typically, programs that use the `Functor` instance are easiest to think of as using `Option` as a data structure, while programs that use the `Monad` instance are easiest to think of as using `Option` to allow early failure, but learning to use both of these perspectives fluently is an important part of becoming proficient at functional programming.

There is a deeper relationship between functors and monads.
It turns out that *every monad is a functor*.
Another way to say this is that the monad abstraction is more powerful than the functor abstraction, because not every functor is a monad.
Furthermore, there is an additional intermediate abstraction, called *applicative functors*, that has enough power to write many interesting programs and yet permits libraries that cannot use the `Monad` interface.
The type class `Applicative` provides the overloadable operations of applicative functors.
Every monad is an applicative functor, and every applicative functor is a functor, but the converses do not hold.

1. [5.1. Structures and Inheritance](Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/#structure-inheritance)
2. [5.2. Applicative Functors](Functors___-Applicative-Functors___-and-Monads/Applicative-Functors/#applicative)
3. [5.3. The Applicative Contract](Functors___-Applicative-Functors___-and-Monads/The-Applicative-Contract/#applicative-laws)
4. [5.4. Alternatives](Functors___-Applicative-Functors___-and-Monads/Alternatives/#alternative)
5. [5.5. Universes](Functors___-Applicative-Functors___-and-Monads/Universes/#universe-levels)
6. [5.6. The Complete Definitions](Functors___-Applicative-Functors___-and-Monads/The-Complete-Definitions/#complete-definitions)
7. [5.7. Summary](Functors___-Applicative-Functors___-and-Monads/Summary/#structure-applicative-monad-summary)

[←4.7. Summary](Monads/Summary/#monads-summary "4.7. Summary")[5.1. Structures and Inheritance→](Functors___-Applicative-Functors___-and-Monads/Structures-and-Inheritance/#structure-inheritance "5.1. Structures and Inheritance")
