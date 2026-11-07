# Study guide: 8.2. Proving Equivalence 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **8.2. Proving Equivalence 🔗** — Programs that have been rewritten to use tail recursion and an accumulator can look quite different from the original program.
- **8.2.1. Proving sum Equal 🔗** — To prove that both versions of sum are equal, begin by writing the theorem statement with a stub proof:
- **8.2.2. A Second Attempt 🔗** — Rather than attempting to muddle through the proof, it's time to take a step back and think.
- **8.2.3. Functional Induction 🔗** — The proof of non_tail_sum_eq_helper_accum follows the implementation of Tail.sumHelper closely.
- **8.2.4.1. Warming Up 🔗** — Write your own proofs for Nat.zero_add , Nat.add_assoc , and Nat.add_comm using the induction tactic.
- **8.2.4.2.1. Reversing Lists 🔗** — Adapt the proof for sum into a proof for NonTail.reverse and Tail.reverse .
- **8.2.4.2.2. Factorial 🔗** — Prove that NonTail.factorial from the exercises in the previous section is equal to your tail-recursive solution by finding the relationship between the accumulator and the result and proving a suitable helper theorem.

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←8.1. Tail Recursion](Programming___-Proving___-and-Performance/Tail-Recursion/#tail-recursion "8.1. Tail Recursion")[8.3. Arrays and Termination→](Programming___-Proving___-and-Performance/Arrays-and-Termination/#array-termination "8.3. Arrays and Termination")

# 8.2. Proving Equivalence[🔗](find/?domain=Verso.Genre.Manual.section&name=proving-tail-rec-equiv "Permalink")

Programs that have been rewritten to use tail recursion and an accumulator can look quite different from the original program.
The original recursive function is often much easier to understand, but it runs the risk of exhausting the stack at run time.
After testing both versions of the program on examples to rule out simple bugs, proofs can be used to show once and for all that the programs are equivalent.

## 8.2.1. Proving `sum` Equal[🔗](find/?domain=Verso.Genre.Manual.section&name=proving-sum-equal "Permalink")

To prove that both versions of `sum` are equal, begin by writing the theorem statement with a stub proof:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := unsolved goals
⊢ NonTail.sum = Tail.sumby⊢ NonTail.sum = Tail.sum
skip⊢ NonTail.sum = Tail.sum`

As expected, Lean describes an unsolved goal:


```lean
unsolved goals
⊢ NonTail.sum = Tail.sum
```


The `rfl` tactic cannot be applied here because `NonTail.sum` and `Tail.sum` are not definitionally equal.
Functions can be equal in more ways than just definitional equality, however.
It is also possible to prove that two functions are equal by proving that they produce equal outputs for the same input.
In other words, `f = g` can be proved by proving that `f(x) = g(x)` for all possible inputs `x`.
This principle is called *function extensionality*.
Function extensionality is exactly the reason why `NonTail.sum` equals `Tail.sum`: they both sum lists of numbers.

In Lean's tactic language, function extensionality is invoked using `funext`, followed by a name to be used for the arbitrary argument.
The arbitrary argument is added as an assumption to the context, and the goal changes to require a proof that the functions applied to this argument are equal:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sum xsby⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs`


```lean
unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sum xs
```


This goal can be proved by induction on the argument `xs`.
Both `sum` functions return `0` when applied to the empty list, which serves as a base case.
Adding a number to the beginning of the input list causes both functions to add that number to the result, which serves as an induction step.
Invoking the `induction` tactic results in two goals:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
induction xs with
| nil unsolved goals
nil⊢ NonTail.sum [] = Tail.sum []=> skipnil⊢ NonTail.sum [] = Tail.sum []
| cons y ys ih unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)=> skipconsy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)`


```lean
unsolved goals
nil⊢ NonTail.sum [] = Tail.sum []
```



```lean
unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)
```


The base case for `nil` can be solved using `rfl`, because both functions return `0` when passed the empty list:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
induction xs with
| nil =>nil⊢ NonTail.sum [] = Tail.sum [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)=> skipconsy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)`

The first step in solving the induction step is to simplify the goal, asking `simp` to unfold `NonTail.sum` and `Tail.sum`:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
induction xs with
| nil =>nil⊢ NonTail.sum [] = Tail.sum [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper 0 (y :: ys)=>
simp [NonTail.sum, Tail.sum]consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper 0 (y :: ys)consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper 0 (y :: ys)
```


Unfolding `Tail.sum` revealed that it immediately delegates to `Tail.sumHelper`, which should also be simplified:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
induction xs with
| nil =>nil⊢ NonTail.sum [] = Tail.sum [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper y ys=>
simp [NonTail.sum, Tail.sum, Tail.sumHelper]consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper y ysconsy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)`

In the resulting goal, `sumHelper` has taken a step of computation and added `y` to the accumulator:


```lean
unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper y ys
```


Rewriting with the induction hypothesis removes all mentions of `NonTail.sum` from the goal:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
induction xs with
| nil =>nil⊢ NonTail.sum [] = Tail.sum [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + Tail.sum ys = Tail.sumHelper y ys=>
simp [NonTail.sum, Tail.sum, Tail.sumHelper]consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + NonTail.sum ys = Tail.sumHelper y ys
rw [ihconsy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + Tail.sum ys = Tail.sumHelper y ys]consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + Tail.sum ys = Tail.sumHelper y ysconsy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ NonTail.sum (y :: ys) = Tail.sum (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:NonTail.sum ys = Tail.sum ys⊢ y + Tail.sum ys = Tail.sumHelper y ys
```


This new goal states that adding some number to the sum of a list is the same as using that number as the initial accumulator in `sumHelper`.
For the sake of clarity, this new goal can be proved as a separate theorem:

`theorem helper_add_sum_accum (xs : List Nat) (n : Nat) :
n + Tail.sum xs = Tail.sumHelper n xs := unsolved goals
xs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xsbyxs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xs
skipxs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xs`


```lean
unsolved goals
xs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xs
```


Once again, this is a proof by induction where the base case uses `rfl`:

`theorem helper_add_sum_accum (xs : List Nat) (n : Nat) :
n + Tail.sum xs = Tail.sumHelper n xs := byxs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>niln:Nat⊢ n + Tail.sum [] = Tail.sumHelper n [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consn y:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sum (y :: ys) = Tail.sumHelper n (y :: ys)=> skipconsn:Naty:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consn y:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
```


Because this is an inductive step, the goal should be simplified until it matches the induction hypothesis `ih`.
Simplifying, using the definitions of `Tail.sum` and `Tail.sumHelper`, results in the following:

`theorem helper_add_sum_accum (xs : List Nat) (n : Nat) :
n + Tail.sum xs = Tail.sumHelper n xs := byxs:List Natn:Nat⊢ n + Tail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>niln:Nat⊢ n + Tail.sum [] = Tail.sumHelper n [] rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consn y:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sumHelper y ys = Tail.sumHelper (y + n) ys=>
simp [Tail.sum, Tail.sumHelper]consn:Naty:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sumHelper y ys = Tail.sumHelper (y + n) ysconsn:Naty:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consn y:Natys:List Natih:n + Tail.sum ys = Tail.sumHelper n ys⊢ n + Tail.sumHelper y ys = Tail.sumHelper (y + n) ys
```


Ideally, the induction hypothesis could be used to replace `Tail.sumHelper (y + n) ys`, but they don't match.
The induction hypothesis can be used for `Tail.sumHelper n ys`, not `Tail.sumHelper (y + n) ys`.
In other words, this proof is stuck.

## 8.2.2. A Second Attempt[🔗](find/?domain=Verso.Genre.Manual.section&name=proving-sum-equal-again "Permalink")

Rather than attempting to muddle through the proof, it's time to take a step back and think.
Why is it that the tail-recursive version of the function is equal to the non-tail-recursive version?
Fundamentally speaking, at each entry in the list, the accumulator grows by the same amount as would be added to the result of the recursion.
This insight can be used to write an elegant proof.
Crucially, the proof by induction must be set up such that the induction hypothesis can be applied to *any* accumulator value.

Discarding the prior attempt, the insight can be encoded as the following statement:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := unsolved goals
xs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xsbyxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
skipxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs`

In this statement, it's very important that `n` is part of the type that's after the colon.
The resulting goal begins with `∀ (n : Nat)`, which is short for “For all `n`”:


```lean
unsolved goals
xs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
```


Using the induction tactic results in goals that include this “for all” statement:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil unsolved goals
nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []=> skipnil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)=> skipconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`

In the `nil` case, the goal is:


```lean
unsolved goals
nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
```


For the induction step for `cons`, both the induction hypothesis and the specific goal contain the “for all `n`”:


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
```


In other words, the goal has become more challenging to prove, but the induction hypothesis is correspondingly more useful.

A mathematical proof for a statement that beings with “for all `x`” should assume some arbitrary `x`, and prove the statement.
“Arbitrary” means that no additional properties of `x` are assumed, so the resulting statement will work for *any* `x`.
In Lean, a “for all” statement is a dependent function: no matter which specific value it is applied to, it will return evidence of the proposition.
Similarly, the process of picking an arbitrary `x` is the same as using `fun x => ...`.
In the tactic language, this process of selecting an arbitrary `x` is performed using the `intro` tactic, which produces the function behind the scenes when the tactic script has completed.
The `intro` tactic should be provided with the name to be used for this arbitrary value.

Using the `intro` tactic in the `nil` case removes the `∀ (n : Nat),` from the goal, and adds an assumption `n : Nat`:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil unsolved goals
niln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []=> intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)=> skipconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
niln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
```


Both sides of this propositional equality are definitionally equal to `n`, so `rfl` suffices:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)=> skipconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`

The `cons` goal also contains a “for all”:


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
```


This suggests the use of `intro`.

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)=>
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
```


The proof goal now contains both `NonTail.sum` and `Tail.sumHelper` applied to `y :: ys`.
The simplifier can make the next step more clear:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys=>
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
simp [NonTail.sum, Tail.sumHelper]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ysconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
```


This goal is very close to matching the induction hypothesis.
There are two ways in which it does not match:

- The left-hand side of the equation is `n + (y + NonTail.sum ys)`, but the induction hypothesis needs the left-hand side to be a number added to `NonTail.sum ys`.
  In other words, this goal should be rewritten to `(n + y) + NonTail.sum ys`, which is valid because addition of natural numbers is associative.
- When the left side has been rewritten to `(y + n) + NonTail.sum ys`, the accumulator argument on the right side should be `n + y` rather than `y + n` in order to match.
  This rewrite is valid because addition is also commutative.

The associativity and commutativity of addition have already been proved in Lean's standard library.
The proof of associativity is named `Nat.add_assoc`, and its type is `(n m k : Nat) → (n + m) + k = n + (m + k)`, while the proof of commutativity is called `Nat.add_comm` and has type `(n m : Nat) → n + m = m + n`.
Normally, the `rw` tactic is provided with an expression whose type is an equality.
However, if the argument is instead a dependent function whose return type is an equality, it attempts to find arguments to the function that would allow the equality to match something in the goal.
There is only one opportunity to apply associativity, though the direction of the rewrite must be reversed because the right side of the equality in `(n + m) + k = n + (m + k)` is the one that matches the proof goal:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys=>
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
simp [NonTail.sum, Tail.sumHelper]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
rw [←Nat.add_assocconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ysconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys
```


Rewriting directly with `rw [Nat.add_comm]`, however, leads to the wrong result.
The `rw` tactic guesses the wrong location for the rewrite, leading to an unintended goal:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ NonTail.sum ys + (n + y) = Tail.sumHelper (y + n) ys=>
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
simp [NonTail.sum, Tail.sumHelper]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
rw [←Nat.add_assocconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys
rw [Nat.add_commconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ NonTail.sum ys + (n + y) = Tail.sumHelper (y + n) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ NonTail.sum ys + (n + y) = Tail.sumHelper (y + n) ysconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ NonTail.sum ys + (n + y) = Tail.sumHelper (y + n) ys
```


This can be fixed by explicitly providing `y` and `n` as arguments to `Nat.add_comm`:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n []
intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []
rflAll goals completed! 🐙
| cons y ys ih unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ys=>
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
simp [NonTail.sum, Tail.sumHelper]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
rw [←Nat.add_assocconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys
rw [Nat.add_comm y nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ysconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)`


```lean
unsolved goals
consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ys
```


The goal now matches the induction hypothesis.
In particular, the induction hypothesis's type is a dependent function type.
Applying `ih` to `n + y` results in exactly the desired type.
The `exact` tactic completes a proof goal if its argument has exactly the desired type:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) :
(n : Nat) → n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Nat⊢ ∀ (n : Nat), n + NonTail.sum xs = Tail.sumHelper n xs
induction xs with
| nil =>nil⊢ ∀ (n : Nat), n + NonTail.sum [] = Tail.sumHelper n [] intro nniln:Nat⊢ n + NonTail.sum [] = Tail.sumHelper n []; rflAll goals completed! 🐙
| cons y ys ih =>consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ys⊢ ∀ (n : Nat), n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
intro nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper n (y :: ys)
simp [NonTail.sum, Tail.sumHelper]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
rw [←Nat.add_assocconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys
rw [Nat.add_comm y nconsy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ys]consy:Natys:List Natih:∀ (n : Nat), n + NonTail.sum ys = Tail.sumHelper n ysn:Nat⊢ n + y + NonTail.sum ys = Tail.sumHelper (n + y) ys
exact ih (n + y)All goals completed! 🐙`

The actual proof requires only a little additional work to get the goal to match the helper's type.
The first step is still to invoke function extensionality:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sum xsby⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs`


```lean
unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sum xs
```


The next step is unfold `Tail.sum`, exposing `Tail.sumHelper`:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sumHelper 0 xsby⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
simp [Tail.sum]xs:List Nat⊢ NonTail.sum xs = Tail.sumHelper 0 xs`


```lean
unsolved goals
xs:List Nat⊢ NonTail.sum xs = Tail.sumHelper 0 xs
```


Having done this, the types almost match.
However, the helper has an additional addend on the left side.
In other words, the proof goal is `NonTail.sum xs = Tail.sumHelper 0 xs`, but applying `non_tail_sum_eq_helper_accum` to `xs` and `0` yields the type `0 + NonTail.sum xs = Tail.sumHelper 0 xs`.
Another standard library proof, `Nat.zero_add`, has type `(n : Nat) → 0 + n = n`.
Applying this function to `NonTail.sum xs` results in an expression with type `0 + NonTail.sum xs = NonTail.sum xs`, so rewriting from right to left results in the desired goal:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := unsolved goals
xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xsby⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
simp [Tail.sum]xs:List Nat⊢ NonTail.sum xs = Tail.sumHelper 0 xs
rw [←Nat.zero_add (NonTail.sum xs)xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xs]xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xs`


```lean
unsolved goals
xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xs
```


Finally, the helper can be used to complete the proof:

`theorem non_tail_sum_eq_tail_sum : NonTail.sum = Tail.sum := by⊢ NonTail.sum = Tail.sum
funext xsxs:List Nat⊢ NonTail.sum xs = Tail.sum xs
simp [Tail.sum]xs:List Nat⊢ NonTail.sum xs = Tail.sumHelper 0 xs
rw [←Nat.zero_add (NonTail.sum xs)xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xs]xs:List Nat⊢ 0 + NonTail.sum xs = Tail.sumHelper 0 xs
exact non_tail_sum_eq_helper_accum xs 0All goals completed! 🐙`

This proof demonstrates a general pattern that can be used when proving that an accumulator-passing tail-recursive function is equal to the non-tail-recursive version.
The first step is to discover the relationship between the starting accumulator argument and the final result.
For instance, beginning `Tail.sumHelper` with an accumulator of `n` results in the final sum being added to `n`, and beginning `Tail.reverseHelper` with an accumulator of `ys` results in the final reversed list being prepended to `ys`.
The second step is to write down this relationship as a theorem statement and prove it by induction.
While the accumulator is always initialized with some neutral value in practice, such as `0` or `[]`, this more general statement that allows the starting accumulator to be any value is what's needed to get a strong enough induction hypothesis.
Finally, using this helper theorem with the actual initial accumulator value results in the desired proof.
For example, in `non_tail_sum_eq_tail_sum`, the accumulator is specified to be `0`.
This may require rewriting the goal to make the neutral initial accumulator values occur in the right place.

## 8.2.3. Functional Induction[🔗](find/?domain=Verso.Genre.Manual.section&name=fun-induction "Permalink")

The proof of `non_tail_sum_eq_helper_accum` follows the implementation of `Tail.sumHelper` closely.
There is not, however, a perfect match between the implementation and the structure expected by mathematical induction, which makes it necessary to manage the assumption `n` carefully.
This is a small amount of work in the case of `non_tail_sum_eq_helper_accum`, but proofs about functions whose definitions are further from the structure expected by `induction` require more bookkeeping.

In addition to proving theorems about recursive functions by induction on one of the arguments, Lean supports proofs by induction on the recursive call structure of functions.
This *functional induction* results in a base case for each branch of the function's control flow that does not include a recursive call, and inductive steps for each branch that does.
A proof by functional induction should demonstrate that the theorem holds for the non-recursive branches, and that if the theorem holds for the result of each recursive call, then it also holds for the result of the recursive branch.

Using functional induction simplifies `non_tail_sum_eq_helper_accum`:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) (n : Nat) :
n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Natn:Nat⊢ n + NonTail.sum xs = Tail.sumHelper n xs
fun_induction Tail.sumHelper with
| case1 n unsolved goals
case1n:Nat⊢ n + NonTail.sum [] = n=> skipcase1n:Nat⊢ n + NonTail.sum [] = n
| case2 n y ys ih unsolved goals
case2n y:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper (y + n) ys=> skipcase2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper (y + n) ys`

Each branch of the proof matches the corresponding branch of `Tail.sumHelper`:

`def Tail.sumHelper (soFar : Nat) : List Nat → Nat
| [] => soFar
| x :: xs => sumHelper (x + soFar) xs`

In the first, `case1`, the right side of the equality is the accumulator value, called `n` in the proof:


```lean
unsolved goals
case1n:Nat⊢ n + NonTail.sum [] = n
```


In the second, `case2`, the right side of the equality is the next step in the tail-recursive loop:


```lean
unsolved goals
case2n y:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper (y + n) ys
```


The resulting proof can be simpler.
The fundamentals of the argument, including the properties of addition that are used, are the same; however, the bookkeeping has been removed.
It is no longer necessary to manually juggle the accumulator value, and the induction hypothesis can be used directly instead of requiring instantiation:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) (n : Nat) :
n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Natn:Nat⊢ n + NonTail.sum xs = Tail.sumHelper n xs
fun_induction Tail.sumHelper with
| case1 n =>case1n:Nat⊢ n + NonTail.sum [] = n simp [NonTail.sum]All goals completed! 🐙
| case2 n y ys ih =>case2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + NonTail.sum (y :: ys) = Tail.sumHelper (y + n) ys
simp [NonTail.sum]case2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + (y + NonTail.sum ys) = Tail.sumHelper (y + n) ys
rw [←Nat.add_assoccase2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys]case2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ n + y + NonTail.sum ys = Tail.sumHelper (y + n) ys
rw [Nat.add_comm n ycase2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys]case2n:Naty:Natys:List Natih:y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys⊢ y + n + NonTail.sum ys = Tail.sumHelper (y + n) ys
assumptionAll goals completed! 🐙`

The `grind` tactic is very well suited to this kind of goal.
Unlike `simp` and `rw`, it is not directional; internally, it accumulates a collection of facts until it either proves the goal completely or fails to do so.
It is preconfigured to use basic facts about arithmetic, such as the associativity and commutativity of addition, and it automatically uses local assumptions such as the induction hypothesis.
Using `grind`, this proof becomes short and to-the-point:

`theorem non_tail_sum_eq_helper_accum (xs : List Nat) (n : Nat) :
n + NonTail.sum xs = Tail.sumHelper n xs := byxs:List Natn:Nat⊢ n + NonTail.sum xs = Tail.sumHelper n xs
fun_induction Tail.sumHelpercase1soFar✝:Nat⊢ soFar✝ + NonTail.sum [] = soFar✝case2soFar✝:Natx✝:Natxs✝:List Natih1✝:x✝ + soFar✝ + NonTail.sum xs✝ = Tail.sumHelper (x✝ + soFar✝) xs✝⊢ soFar✝ + NonTail.sum (x✝ :: xs✝) = Tail.sumHelper (x✝ + soFar✝) xs✝ <;>case1soFar✝:Nat⊢ soFar✝ + NonTail.sum [] = soFar✝case2soFar✝:Natx✝:Natxs✝:List Natih1✝:x✝ + soFar✝ + NonTail.sum xs✝ = Tail.sumHelper (x✝ + soFar✝) xs✝⊢ soFar✝ + NonTail.sum (x✝ :: xs✝) = Tail.sumHelper (x✝ + soFar✝) xs✝ grind [NonTail.sum]All goals completed! 🐙`

This proof also matches the way the proof might be explained to a skilled programmer: “Just check both branches of `Tail.sumHelper`!”

## 8.2.4. Exercise[🔗](find/?domain=Verso.Genre.Manual.section&name=tail-recursion-proof-exercises "Permalink")

### 8.2.4.1. Warming Up[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming___-Proving___-and-Performance--Proving-Equivalence--Exercise--Warming-Up "Permalink")

Write your own proofs for `Nat.zero_add`, `Nat.add_assoc`, and `Nat.add_comm` using the `induction` tactic.

### 8.2.4.2. More Accumulator Proofs[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming___-Proving___-and-Performance--Proving-Equivalence--Exercise--More-Accumulator-Proofs "Permalink")

#### 8.2.4.2.1. Reversing Lists[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming___-Proving___-and-Performance--Proving-Equivalence--Exercise--More-Accumulator-Proofs--Reversing-Lists "Permalink")

Adapt the proof for `sum` into a proof for `NonTail.reverse` and `Tail.reverse`.
The first step is to think about the relationship between the accumulator value being passed to `Tail.reverseHelper` and the non-tail-recursive reverse.
Just as adding a number to the accumulator in `Tail.sumHelper` is the same as adding it to the overall sum, using `List.cons` to add a new entry to the accumulator in `Tail.reverseHelper` is equivalent to some change to the overall result.
Try three or four different accumulator values with pencil and paper until the relationship becomes clear.
Use this relationship to prove a suitable helper theorem.
Try proving this helper theorem both using induction on lists and via functional induction.
Then, write down the overall theorem.
Because `NonTail.reverse` and `Tail.reverse` are polymorphic, stating their equality requires the use of `@` to stop Lean from trying to figure out which type to use for `α`.
Once `α` is treated as an ordinary argument, `funext` should be invoked with both `α` and `xs`:

`theorem non_tail_reverse_eq_tail_reverse :
@NonTail.reverse = @Tail.reverse := unsolved goals
α:Type u_1xs:List α⊢ NonTail.reverse xs = Tail.reverse xsby⊢ @NonTail.reverse = @Tail.reverse
funext α xsα:Type u_1xs:List α⊢ NonTail.reverse xs = Tail.reverse xs`

This results in a suitable goal:


```lean
unsolved goals
α:Type u_1xs:List α⊢ NonTail.reverse xs = Tail.reverse xs
```


#### 8.2.4.2.2. Factorial[🔗](find/?domain=Verso.Genre.Manual.section&name=Functional-Programming-in-Lean--Programming___-Proving___-and-Performance--Proving-Equivalence--Exercise--More-Accumulator-Proofs--Factorial "Permalink")

Prove that `NonTail.factorial` from the exercises in the previous section is equal to your tail-recursive solution by finding the relationship between the accumulator and the result and proving a suitable helper theorem.

[←8.1. Tail Recursion](Programming___-Proving___-and-Performance/Tail-Recursion/#tail-recursion "8.1. Tail Recursion")[8.3. Arrays and Termination→](Programming___-Proving___-and-Performance/Arrays-and-Termination/#array-termination "8.3. Arrays and Termination")


> **Review needed:** The following headings have no short source sentence: 8.2.4. Exercise 🔗, 8.2.4.2. More Accumulator Proofs 🔗