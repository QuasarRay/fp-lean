# Study guide: 8.4. More Inequalities 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **8.4. More Inequalities 🔗** — Lean's built-in proof automation is sufficient to check that arrayMapHelper and findHelper terminate.
- **8.4.1. Merge Sort 🔗** — One example of a function whose termination proof is non-trivial is merge sort on List .
- **8.4.2. Splitting a List Makes it Shorter 🔗** — It will also be necessary to prove that (splitList xs).snd.length < xs.length .
- **8.4.2.1. Adding One to the Greater Side 🔗** — The inequality needed to prove splitList_shorter_le is ∀ ( n m : Nat ) , n ≤ m → n ≤ m + 1 .
- **8.4.2.2. Finishing the Proof 🔗** — Now that both helper theorems have been proved, the rest of splitList_shorter_le will be completed quickly.
- **8.4.2.3. A Simpler Proof 🔗** — Instead of using ordinary induction, splitList_shorter_le can be proved using functional induction, resulting in one case for each branch of splitList :
- **8.4.3. Merge Sort Terminates 🔗** — Merge sort has two recursive calls, one for each sub-list returned by splitList .
- **8.4.4. Division as Iterated Subtraction 🔗** — Just as multiplication is iterated addition and exponentiation is iterated multiplication, division can be understood as iterated subtraction.
- **8.4.5. Exercises 🔗** — Prove the following theorems without using grind :

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←8.3. Arrays and Termination](Programming___-Proving___-and-Performance/Arrays-and-Termination/#array-termination "8.3. Arrays and Termination")[8.5. Bounded Numbers→](Programming___-Proving___-and-Performance/Bounded-Numbers/#Fin "8.5. Bounded Numbers")

# 8.4. More Inequalities[🔗](find/?domain=Verso.Genre.Manual.section&name=more-inequalities "Permalink")

Lean's built-in proof automation is sufficient to check that `arrayMapHelper` and `findHelper` terminate.
All that was needed was to provide an expression whose value decreases with each recursive call.
However, Lean's built-in automation is not magic, and it often needs some help.

## 8.4.1. Merge Sort[🔗](find/?domain=Verso.Genre.Manual.section&name=merge-sort "Permalink")

One example of a function whose termination proof is non-trivial is merge sort on `List`.
Merge sort consists of two phases: first, a list is split in half.
Each half is sorted using merge sort, and then the results are merged using a function that combines two sorted lists into a larger sorted list.
The base cases are the empty list and the singleton list, both of which are already considered to be sorted.

To merge two sorted lists, there are two basic cases to consider:

1. If one of the input lists is empty, then the result is the other list.
2. If both lists are non-empty, then their heads should be compared. The result of the function is the smaller of the two heads, followed by the result of merging the remaining entries of both lists.

This is not structurally recursive on either list.
The recursion terminates because an entry is removed from one of the two lists in each recursive call, but it could be either list.
Behind the scenes, Lean uses this fact to prove that it terminates:

`def merge [Ord α] (xs : List α) (ys : List α) : List α :=
match xs, ys with
| [], _ => ys
| _, [] => xs
| x'::xs', y'::ys' =>
match Ord.compare x' y' with
| .lt | .eq => x' :: merge xs' (y' :: ys')
| .gt => y' :: merge (x'::xs') ys'`

A simple way to split a list is to add each entry in the input list to two alternating output lists:

`def splitList (lst : List α) : (List α × List α) :=
match lst with
| [] => ([], [])
| x :: xs =>
let (a, b) := splitList xs
(x :: b, a)`

This splitting function is structurally recursive.

Merge sort checks whether a base case has been reached.
If so, it returns the input list.
If not, it splits the input, and merges the result of sorting each half:

`` def fail to show termination for
mergeSort
with errors
failed to infer structural recursion:
Not considering parameter α of mergeSort:
it is unchanged in the recursive calls
Not considering parameter #2 of mergeSort:
it is unchanged in the recursive calls
Cannot use parameter xs:
failed to eliminate recursive application
mergeSort halves.fst


Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
xs #1
1) 70:11-31 ? ?
2) 70:34-54 _ _
#1: xs.length
Please use `termination_by` to specify a decreasing measure.mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
merge (mergeSort halves.fst) (mergeSort halves.snd) ``

Lean's pattern match compiler is able to tell that the assumption `h` introduced by the `if` that tests whether `xs.length < 2` rules out lists longer than one entry, so there is no “missing cases” error.
However, even though this program always terminates, it is not structurally recursive, and Lean is unable to automatically discover a decreasing measure:


```lean
fail to show termination for
  mergeSort
with errors
failed to infer structural recursion:
Not considering parameter α of mergeSort:
  it is unchanged in the recursive calls
Not considering parameter #2 of mergeSort:
  it is unchanged in the recursive calls
Cannot use parameter xs:
  failed to eliminate recursive application
    mergeSort halves.fst


Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
            xs #1
1) 70:11-31  ?  ?
2) 70:34-54  _  _

#1: xs.length

Please use `termination_by` to specify a decreasing measure.
```


The reason it terminates is that `splitList` always returns lists that are shorter than its input, at least when applied to lists that contain at least two elements.
Thus, the length of `halves.fst` and `halves.snd` are less than the length of `xs`.
This can be expressed using a `termination_by` clause:

`` def mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
merge (failed to prove termination, possible solutions:
 - Use `have`-expressions to prove the remaining goals
 - Use `termination_by` to specify a different well-founded relation
 - Use `decreasing_by` to specify your own tactic for discharging this kind of goal
α:Type u_1xs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ (splitList xs).fst.length < xs.lengthmergeSort halves.fst) (mergeSort halves.snd)
termination_by xs.length ``

With this clause, the error message changes.
Instead of complaining that the function isn't structurally recursive, Lean instead points out that it was unable to automatically prove that `(splitList xs).fst.length < xs.length`:


```lean
failed to prove termination, possible solutions:
  - Use `have`-expressions to prove the remaining goals
  - Use `termination_by` to specify a different well-founded relation
  - Use `decreasing_by` to specify your own tactic for discharging this kind of goal
α:Type u_1xs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ (splitList xs).fst.length < xs.length
```


## 8.4.2. Splitting a List Makes it Shorter[🔗](find/?domain=Verso.Genre.Manual.section&name=splitting-shortens "Permalink")

It will also be necessary to prove that `(splitList xs).snd.length < xs.length`.
Because `splitList` alternates between adding entries to the two lists, it is easiest to prove both statements at once, so the structure of the proof can follow the algorithm used to implement `splitList`.
In other words, it is easiest to prove that `∀(lst : List α), (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length`.

Unfortunately, the statement is false.
In particular, `splitList []` is `([], [])`. Both output lists have length `0`, which is not less than `0`, the length of the input list.
Similarly, `splitList ["basalt"]` evaluates to `(["basalt"], [])`, and `["basalt"]` is not shorter than `["basalt"]`.
However, `splitList ["basalt", "granite"]` evaluates to `(["basalt"], ["granite"])`, and both of these output lists are shorter than the input list.

It turns out that the lengths of the output lists are always less than or equal to the length of the input list, but they are only strictly shorter when the input list contains at least two entries.
It turns out to be easiest to prove the former statement, then extend it to the latter statement.
Begin with a theorem statement:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := unsolved goals
α:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.lengthbyα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
skipα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length`


```lean
unsolved goals
α:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
```


Because `splitList` is structurally recursive on the list, the proof should use induction.
The structural recursion in `splitList` fits a proof by induction perfectly: the base case of the induction matches the base case of the recursion, and the inductive step matches the recursive call.
The `induction` tactic gives two goals:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil unsolved goals
nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length=> skipnilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length
| cons x xs ih unsolved goals
consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length=> skipconsα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length`


```lean
unsolved goals
nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length
```



```lean
unsolved goals
consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length
```


The goal for the `nil` case can be proved by invoking the simplifier and instructing it to unfold the definition of `splitList`, because the length of the empty list is less than or equal to the length of the empty list.
Similarly, simplifying with `splitList` in the `cons` case places `Nat.succ` around the lengths in the goal:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil =>nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length simp [splitList]All goals completed! 🐙
| cons x xs ih unsolved goals
consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1=>
simp [splitList]consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length`


```lean
unsolved goals
consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
```


This is because the call to `List.length` consumes the head of the list `x :: xs`, converting it to a `Nat.succ`, in both the length of the input list and the length of the first output list.

Writing `A ∧ B` in Lean is short for `And A B`.
`And` is a structure type in the `Prop` universe:

`structure And (a b : Prop) : Prop where
intro ::
left : a
right : b`

In other words, a proof of `A ∧ B` consists of the `And.intro` constructor applied to a proof of `A` in the `left` field and a proof of `B` in the `right` field.

The `cases` tactic allows a proof to consider each constructor of a datatype or each potential proof of a proposition in turn.
It corresponds to a `match` expression without recursion.
Using `cases` on a structure results in the structure being broken apart, with an assumption added for each field of the structure, just as a pattern match expression extracts the field of a structure for use in a program.
Because structures have only one constructor, using `cases` on a structure does not result in additional goals.

Because `ih` is a proof of `List.length (splitList xs).fst ≤ List.length xs ∧ List.length (splitList xs).snd ≤ List.length xs`, using `cases ih` results in an assumption that `List.length (splitList xs).fst ≤ List.length xs` and an assumption that `List.length (splitList xs).snd ≤ List.length xs`:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil =>nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length simp [splitList]All goals completed! 🐙
| cons x xs ih unsolved goals
cons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1=>
simp [splitList]consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
cases ihcons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length`


```lean
unsolved goals
cons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
```


Because the goal of the proof is also an `And`, the `constructor` tactic can be used to apply `And.intro`, resulting in a goal for each argument:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil =>nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length simp [splitList]All goals completed! 🐙
| cons x xs ih unsolved goals
cons.intro.leftα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length

cons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1=>
simp [splitList]consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
cases ihcons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
constructorcons.intro.leftα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.lengthcons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length`


```lean
unsolved goals
cons.intro.leftα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length

cons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
```


The `left` goal is identical to the `left✝` assumption, so the `assumption` tactic dispatches it:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil =>nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length simp [splitList]All goals completed! 🐙
| cons x xs ih unsolved goals
cons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1=>
simp [splitList]consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
cases ihcons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
constructorcons.intro.leftα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.lengthcons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
case left =>α:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length assumptionAll goals completed! 🐙consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length`


```lean
unsolved goals
cons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
```


The `right` goal resembles the `right✝` assumption, except the goal adds a `+ 1` only to the length of the input list.
It's time to prove that the inequality holds.

### 8.4.2.1. Adding One to the Greater Side[🔗](find/?domain=Verso.Genre.Manual.section&name=le-succ-of-le "Permalink")

The inequality needed to prove `splitList_shorter_le` is `∀(n m : Nat), n ≤ m → n ≤ m + 1`.
The incoming assumption that `n ≤ m` essentially tracks the difference between `n` and `m` in the number of `Nat.le.step` constructors.
Thus, the proof should add an extra `Nat.le.step` in the base case.

Starting out, the statement reads:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := unsolved goals
n m:Nat⊢ n ≤ m → n ≤ m + 1byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
skipn:Natm:Nat⊢ n ≤ m → n ≤ m + 1`


```lean
unsolved goals
n m:Nat⊢ n ≤ m → n ≤ m + 1
```


The first step is to introduce a name for the assumption that `n ≤ m`:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := unsolved goals
n m:Nath:n ≤ m⊢ n ≤ m + 1byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1`


```lean
unsolved goals
n m:Nath:n ≤ m⊢ n ≤ m + 1
```


The proof is by induction on this assumption:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl unsolved goals
refln m:Nat⊢ n ≤ n + 1=> skiprefln:Natm:Nat⊢ n ≤ n + 1
| step _ ih unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1=> skipstepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1`

In the case for `refl`, where `n = m`, the goal is to prove that `n ≤ n + 1`:


```lean
unsolved goals
refln m:Nat⊢ n ≤ n + 1
```


In the case for `step`, the goal is to prove that `n ≤ m + 1` under the assumption that `n ≤ m`:


```lean
unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1
```


For the `refl` case, the `step` constructor can be applied:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl unsolved goals
refln m:Nat⊢ n.le n=> constructorrefln:Natm:Nat⊢ n.le nrefln:Natm:Nat⊢ n ≤ n + 1
| step _ ih unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1=> skipstepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1`


```lean
unsolved goals
refln m:Nat⊢ n.le n
```


After `step`, `refl` can be used, which leaves only the goal for `step`:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl =>refln:Natm:Nat⊢ n ≤ n + 1 constructorrefln:Natm:Nat⊢ n.le n; constructorAll goals completed! 🐙
| step _ ih unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1=> skipstepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1`


```lean
unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1
```


For the step, applying the `step` constructor transforms the goal into the induction hypothesis:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl =>refln:Natm:Nat⊢ n ≤ n + 1 constructorrefln:Natm:Nat⊢ n.le n; constructorAll goals completed! 🐙
| step _ ih unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n.le (m✝ + 1)=> constructorstepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n.le (m✝ + 1)stepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1`


```lean
unsolved goals
stepn m m✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n.le (m✝ + 1)
```


The final proof is as follows:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl =>refln:Natm:Nat⊢ n ≤ n + 1 constructorrefln:Natm:Nat⊢ n.le n; constructorAll goals completed! 🐙
| step =>stepn:Natm:Natm✝:Nata✝:n.le m✝a_ih✝:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1 constructorstepn:Natm:Natm✝:Nata✝:n.le m✝a_ih✝:n ≤ m✝ + 1⊢ n.le (m✝ + 1); assumptionAll goals completed! 🐙`

To reveal what's going on behind the scenes, the `apply` and `exact` tactics can be used to indicate exactly which constructor is being applied.
The `apply` tactic solves the current goal by applying a function or constructor whose return type matches, creating new goals for each argument that was not provided, while `exact` fails if any new goals would be needed:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1 := byn:Natm:Nat⊢ n ≤ m → n ≤ m + 1
intro hn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction h with
| refl =>refln:Natm:Nat⊢ n ≤ n + 1 apply Nat.le.steprefln:Natm:Nat⊢ n.le n; exact Nat.le.reflAll goals completed! 🐙
| step _ ih =>stepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1 apply Nat.le.stepstepn:Natm:Natm✝:Nata✝:n.le m✝ih:n ≤ m✝ + 1⊢ n.le (m✝ + 1); exact ihAll goals completed! 🐙`

The proof can be golfed:

`theorem Nat.le_succ_of_le (h : n ≤ m) : n ≤ m + 1:= byn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
induction hrefln:Natm:Nat⊢ n ≤ n + 1stepn:Natm:Natm✝:Nata✝:n.le m✝a_ih✝:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1 <;>refln:Natm:Nat⊢ n ≤ n + 1stepn:Natm:Natm✝:Nata✝:n.le m✝a_ih✝:n ≤ m✝ + 1⊢ n ≤ m✝.succ + 1 repeat (first | constructorstepn:Natm:Natm✝:Nata✝:n.le m✝a_ih✝:n ≤ m✝ + 1⊢ n.le m✝ | assumptionAll goals completed! 🐙)`

In this short tactic script, both goals introduced by `induction` are addressed using `repeat (first | constructor | assumption)`.
The tactic `first | T1 | T2 | ... | Tn` means to use try `T1` through `Tn` in order, using the first tactic that succeeds.
In other words, `repeat (first | constructor | assumption)` applies constructors as long as it can, and then attempts to solve the goal using an assumption.

The proof can be shortened even further by using `grind`, which includes a solver for linear arithmetic:

`theorem Nat.le_succ_of_le (h : n ≤ m) : n ≤ m + 1:= byn:Natm:Nath:n ≤ m⊢ n ≤ m + 1
grindAll goals completed! 🐙`

Finally, the proof can be written as a recursive function:

`theorem Nat.le_succ_of_le : n ≤ m → n ≤ m + 1
| .refl => .step .refl
| .step h => .step (Nat.le_succ_of_le h)`

Each style of proof can be appropriate to different circumstances.
The detailed proof script is useful in cases where beginners may be reading the code, or where the steps of the proof provide some kind of insight.
The short, highly-automated proof script is typically easier to maintain, because automation is frequently both flexible and robust in the face of small changes to definitions and datatypes.
The recursive function is typically both harder to understand from the perspective of mathematical proofs and harder to maintain, but it can be a useful bridge for programmers who are beginning to work with interactive theorem proving.

### 8.4.2.2. Finishing the Proof[🔗](find/?domain=Verso.Genre.Manual.section&name=finishing-splitList-shorter-proof "Permalink")

Now that both helper theorems have been proved, the rest of `splitList_shorter_le` will be completed quickly.
The current proof state has one goal remaining:


```lean
unsolved goals
cons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
```


Using `Nat.le_succ_of_le` together with the `right✝` assumption completes the proof:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
induction lst with
| nil =>nilα:Type u_1⊢ (splitList []).fst.length ≤ [].length ∧ (splitList []).snd.length ≤ [].length simp [splitList]All goals completed! 🐙
| cons x xs ih =>consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList (x :: xs)).fst.length ≤ (x :: xs).length ∧ (splitList (x :: xs)).snd.length ≤ (x :: xs).length
simp [splitList]consα:Type u_1x:αxs:List αih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
cases ihcons.introα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length ∧ (splitList xs).fst.length ≤ xs.length + 1
constructorcons.intro.leftα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.lengthcons.intro.rightα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
case left =>α:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).snd.length ≤ xs.length assumptionAll goals completed! 🐙
case right =>α:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length + 1
apply Nat.le_succ_of_leα:Type u_1x:αxs:List αleft✝:(splitList xs).fst.length ≤ xs.lengthright✝:(splitList xs).snd.length ≤ xs.length⊢ (splitList xs).fst.length ≤ xs.length
assumptionAll goals completed! 🐙`

The next step is to return to the actual theorem that is needed to prove that merge sort terminates: that so long as a list has at least two entries, both results of splitting it are strictly shorter.

`theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length ∧
(splitList lst).snd.length < lst.length := unsolved goals
α:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.lengthbyα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
skipα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length`


```lean
unsolved goals
α:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
```


Pattern matching works just as well in tactic scripts as it does in programs.
Because `lst` has at least two entries, they can be exposed with `match`, which also refines the type through dependent pattern matching:

`theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length ∧
(splitList lst).snd.length < lst.length := byα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
match lst with
| x :: y :: xs unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
(splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length=>
skipα:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
(splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length`


```lean
unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
  (splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length
```


Simplifying using `splitList` removes `x` and `y`, resulting in the computed lengths of lists each gaining a `+ 1`:

`theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length ∧
(splitList lst).snd.length < lst.length := byα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
match lst with
| x :: y :: xs unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length < xs.length + 1 ∧ (splitList xs).snd.length < xs.length + 1=>
simp [splitList]α:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length < xs.length + 1 ∧ (splitList xs).snd.length < xs.length + 1α:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
(splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length`


```lean
unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length < xs.length + 1 ∧ (splitList xs).snd.length < xs.length + 1
```


Replacing `simp` with `simp +arith` removes these `+ 1`s, because `simp +arith` makes use of the fact that `n + 1 < m + 1` implies `n < m`:

`theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length ∧
(splitList lst).snd.length < lst.length := byα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
match lst with
| x :: y :: xs unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length=>
simp +arith [splitList]α:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.lengthα:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
(splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length`


```lean
unsolved goals
α:Type u_1lst:List αx y:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length
```


This goal now matches `splitList_shorter_le`, which can be used to conclude the proof:

`theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length ∧
(splitList lst).snd.length < lst.length := byα:Type u_1lst:List αx✝:lst.length ≥ 2⊢ (splitList lst).fst.length < lst.length ∧ (splitList lst).snd.length < lst.length
match lst with
| x :: y :: xs =>α:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList (x :: y :: xs)).fst.length < (x :: y :: xs).length ∧
(splitList (x :: y :: xs)).snd.length < (x :: y :: xs).length
simp +arith [splitList]α:Type u_1lst:List αx:αy:αxs:List αx✝:(x :: y :: xs).length ≥ 2⊢ (splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length
apply splitList_shorter_leAll goals completed! 🐙`

The facts needed to prove that `mergeSort` terminates can be pulled out of the resulting `And`:

`theorem splitList_shorter_fst (lst : List α) (h : lst.length ≥ 2) :
(splitList lst).fst.length < lst.length :=
splitList_shorter lst h |>.left
theorem splitList_shorter_snd (lst : List α) (h : lst.length ≥ 2) :
(splitList lst).snd.length < lst.length :=
splitList_shorter lst h |>.right`

### 8.4.2.3. A Simpler Proof[🔗](find/?domain=Verso.Genre.Manual.section&name=splitList-shorter-le-simpler-proof "Permalink")

Instead of using ordinary induction, `splitList_shorter_le` can be proved using functional induction, resulting in one case for each branch of `splitList`:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
fun_induction splitList with
| case1 unsolved goals
case1α:Type u_1⊢ ([], []).fst.length ≤ [].length ∧ ([], []).snd.length ≤ [].length=> skipcase1α:Type u_1⊢ ([], []).fst.length ≤ [].length ∧ ([], []).snd.length ≤ [].length
| case2 x xs a b splitEq ih unsolved goals
case2α:Type u_1x:αxs a b:List αsplitEq:splitList xs = (a, b)ih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (x :: b, a).fst.length ≤ (x :: xs).length ∧ (x :: b, a).snd.length ≤ (x :: xs).length=> skipcase2α:Type u_1x:αxs:List αa:List αb:List αsplitEq:splitList xs = (a, b)ih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (x :: b, a).fst.length ≤ (x :: xs).length ∧ (x :: b, a).snd.length ≤ (x :: xs).length`

The first case matches the base case of `splitList`.
*Both* applications of `splitList` have been replaced by the result of this first branch:


```lean
unsolved goals
case1α:Type u_1⊢ ([], []).fst.length ≤ [].length ∧ ([], []).snd.length ≤ [].length
```


The second case matches the recursive branch of `splitList`.
In addition to the induction hypothesis, the value of the `let` in `splitList` is tracked in an assumption:


```lean
unsolved goals
case2α:Type u_1x:αxs a b:List αsplitEq:splitList xs = (a, b)ih:(splitList xs).fst.length ≤ xs.length ∧ (splitList xs).snd.length ≤ xs.length⊢ (x :: b, a).fst.length ≤ (x :: xs).length ∧ (x :: b, a).snd.length ≤ (x :: xs).length
```


While the second case looks a bit complicated, everything needed to complete the proof is present.
Indeed, `grind` can prove both goals immediately:

`theorem splitList_shorter_le (lst : List α) :
(splitList lst).fst.length ≤ lst.length ∧
(splitList lst).snd.length ≤ lst.length := byα:Type u_1lst:List α⊢ (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length
fun_induction splitListcase1α:Type u_1⊢ ([], []).fst.length ≤ [].length ∧ ([], []).snd.length ≤ [].lengthcase2α:Type u_1x✝¹:αxs✝:List αa✝:List αb✝:List αx✝:splitList xs✝ = (a✝, b✝)ih1✝:(splitList xs✝).fst.length ≤ xs✝.length ∧ (splitList xs✝).snd.length ≤ xs✝.length⊢ (x✝¹ :: b✝, a✝).fst.length ≤ (x✝¹ :: xs✝).length ∧ (x✝¹ :: b✝, a✝).snd.length ≤ (x✝¹ :: xs✝).length <;>case1α:Type u_1⊢ ([], []).fst.length ≤ [].length ∧ ([], []).snd.length ≤ [].lengthcase2α:Type u_1x✝¹:αxs✝:List αa✝:List αb✝:List αx✝:splitList xs✝ = (a✝, b✝)ih1✝:(splitList xs✝).fst.length ≤ xs✝.length ∧ (splitList xs✝).snd.length ≤ xs✝.length⊢ (x✝¹ :: b✝, a✝).fst.length ≤ (x✝¹ :: xs✝).length ∧ (x✝¹ :: b✝, a✝).snd.length ≤ (x✝¹ :: xs✝).length grindAll goals completed! 🐙`

## 8.4.3. Merge Sort Terminates[🔗](find/?domain=Verso.Genre.Manual.section&name=merge-sort-terminates "Permalink")

Merge sort has two recursive calls, one for each sub-list returned by `splitList`.
Each recursive call will require a proof that the length of the list being passed to it is shorter than the length of the input list.
It's usually convenient to write a termination proof in two steps: first, write down the propositions that will allow Lean to verify termination, and then prove them.
Otherwise, it's possible to put a lot of effort into proving the propositions, only to find out that they aren't quite what's needed to establish that the recursive calls are on smaller inputs.

The `sorry` tactic can prove any goal, even false ones.
It isn't intended for use in production code or final proofs, but it is a convenient way to “sketch out” a proof or program ahead of time.
Any definitions or theorems that use `sorry` are annotated with a warning.

The initial sketch of `mergeSort`'s termination argument that uses `sorry` can be written by copying the goals that Lean couldn't prove into `have`-expressions.
In Lean, `have` is similar to `let`.
When using `have`, the name is optional.
Typically, `let` is used to define names that refer to interesting values, while `have` is used to locally prove propositions that can be found when Lean is searching for evidence that an array lookup is in-bounds or that a function terminates.

`` declaration uses `sorry`def declaration uses `sorry`declaration uses `sorry`mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
have : halves.fst.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ halves.fst.length < xs.length
sorryAll goals completed! 🐙
have : halves.snd.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:halves.fst.length < xs.length⊢ halves.snd.length < xs.length
sorryAll goals completed! 🐙
merge (mergeSort halves.fst) (mergeSort halves.snd)
termination_by xs.length ``

The warning is located on the name `mergeSort`:


```lean
declaration uses `sorry`
```


Because there are no errors, the proposed propositions are enough to establish termination.

The proofs begin by applying the helper theorems:

`def mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
have : halves.fst.length < xs.length := unsolved goals
α:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := ⋯⊢ xs.length ≥ 2byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ halves.fst.length < xs.length
apply splitList_shorter_fstα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ xs.length ≥ 2
have : halves.snd.length < xs.length := unsolved goals
α:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := ⋯this:halves.fst.length < xs.length⊢ xs.length ≥ 2byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:halves.fst.length < xs.length⊢ halves.snd.length < xs.length
apply splitList_shorter_sndα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:halves.fst.length < xs.length⊢ xs.length ≥ 2
merge (mergeSort halves.fst) (mergeSort halves.snd)
termination_by xs.length`

Both proofs fail, because `splitList_shorter_fst` and `splitList_shorter_snd` both require a proof that `xs.length ≥ 2`:


```lean
unsolved goals
α:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := ⋯⊢ xs.length ≥ 2
```


To check that this will be enough to complete the proof, add it using `sorry` and check for errors:

`` declaration uses `sorry`def declaration uses `sorry`declaration uses `sorry`mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
have : xs.length ≥ 2 := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ xs.length ≥ 2 sorryAll goals completed! 🐙
have : halves.fst.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:xs.length ≥ 2⊢ halves.fst.length < xs.length
apply splitList_shorter_fstα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:xs.length ≥ 2⊢ xs.length ≥ 2
assumptionAll goals completed! 🐙
have : halves.snd.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis✝:xs.length ≥ 2this:halves.fst.length < xs.length⊢ halves.snd.length < xs.length
apply splitList_shorter_sndα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis✝:xs.length ≥ 2this:halves.fst.length < xs.length⊢ xs.length ≥ 2
assumptionAll goals completed! 🐙
merge (mergeSort halves.fst) (mergeSort halves.snd)
termination_by xs.length ``

Once again, there is only a warning.


```lean
declaration uses `sorry`
```


There is one promising assumption available: `h : ¬List.length xs < 2`, which comes from the `if`.
Clearly, if it is not the case that `xs.length < 2`, then `xs.length ≥ 2`.
The `grind` tactic solves this goal, and the program is now complete:

`def mergeSort [Ord α] (xs : List α) : List α :=
if h : xs.length < 2 then
match xs with
| [] => []
| [x] => [x]
else
let halves := splitList xs
have : xs.length ≥ 2 := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xs⊢ xs.length ≥ 2
grindAll goals completed! 🐙
have : halves.fst.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:xs.length ≥ 2⊢ halves.fst.length < xs.length
apply splitList_shorter_fstα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis:xs.length ≥ 2⊢ xs.length ≥ 2
assumptionAll goals completed! 🐙
have : halves.snd.length < xs.length := byα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis✝:xs.length ≥ 2this:halves.fst.length < xs.length⊢ halves.snd.length < xs.length
apply splitList_shorter_sndα:Type ?u.3inst✝:Ord αxs:List αh:¬xs.length < 2halves:List α × List α := splitList xsthis✝:xs.length ≥ 2this:halves.fst.length < xs.length⊢ xs.length ≥ 2
assumptionAll goals completed! 🐙
merge (mergeSort halves.fst) (mergeSort halves.snd)
termination_by xs.length`

The function can be tested on examples:

`["geode", "limestone", "mica", "soapstone"]#eval mergeSort ["soapstone", "geode", "mica", "limestone"]`


```lean
["geode", "limestone", "mica", "soapstone"]
```


`[3, 5, 15, 22]#eval mergeSort [5, 3, 22, 15]`


```lean
[3, 5, 15, 22]
```


## 8.4.4. Division as Iterated Subtraction[🔗](find/?domain=Verso.Genre.Manual.section&name=division-as-iterated-subtraction "Permalink")

Just as multiplication is iterated addition and exponentiation is iterated multiplication, division can be understood as iterated subtraction.
The [very first description of recursive functions in this book](Getting-to-Know-Lean/Datatypes-and-Patterns/#recursive-functions) presents a version of division that terminates when the divisor is not zero, but that Lean does not accept.
Proving that division terminates requires the use of a fact about inequalities.

Lean cannot prove that this definition of division terminates:

`` def fail to show termination for
div
with errors
failed to infer structural recursion:
Not considering parameter k of div:
it is unchanged in the recursive calls
Cannot use parameter n:
failed to eliminate recursive application
div (n - k) k


failed to prove termination, possible solutions:
 - Use `have`-expressions to prove the remaining goals
 - Use `termination_by` to specify a different well-founded relation
 - Use `decreasing_by` to specify your own tactic for discharging this kind of goal
k n:Nath✝:¬n < k⊢ n - k < ndiv (n k : Nat) : Nat :=
if n < k then
0
else
1 + div (n - k) k ``


```lean
fail to show termination for
  div
with errors
failed to infer structural recursion:
Not considering parameter k of div:
  it is unchanged in the recursive calls
Cannot use parameter n:
  failed to eliminate recursive application
    div (n - k) k


failed to prove termination, possible solutions:
  - Use `have`-expressions to prove the remaining goals
  - Use `termination_by` to specify a different well-founded relation
  - Use `decreasing_by` to specify your own tactic for discharging this kind of goal
k n:Nath✝:¬n < k⊢ n - k < n
```


That's a good thing, because it doesn't!
When `k` is `0`, value of `n` does not decrease, so the program is an infinite loop.

Rewriting the function to take evidence that `k` is not `0` allows Lean to automatically prove termination:

`def div (n k : Nat) (ok : k ≠ 0) : Nat :=
if h : n < k then
0
else
1 + div (n - k) k ok`

This definition of `div` terminates because the first argument `n` is smaller on each recursive call.
This can be expressed using a `termination_by` clause:

`def div (n k : Nat) (ok : k ≠ 0) : Nat :=
if h : n < k then
0
else
1 + div (n - k) k ok
termination_by n`

## 8.4.5. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=inequalities-exercises "Permalink")

Prove the following theorems without using `grind`:

- For all natural numbers `n`, `0 < n + 1`.
- For all natural numbers `n`, `0 \leq n`.
- For all natural numbers `n` and `k`, `(n + 1) - (k + 1) = n - k`
- For all natural numbers `n` and `k`, if `k < n` then `n \neq 0`
- For all natural numbers `n`, `n - n = 0`
- For all natural numbers `n` and `k`, if `n + 1 < k` then `n < k`

[←8.3. Arrays and Termination](Programming___-Proving___-and-Performance/Arrays-and-Termination/#array-termination "8.3. Arrays and Termination")[8.5. Bounded Numbers→](Programming___-Proving___-and-Performance/Bounded-Numbers/#Fin "8.5. Bounded Numbers")
