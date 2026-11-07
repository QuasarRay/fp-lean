# Study guide: 1.4. Structures 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **1.4. Structures 🔗** — The first step in writing a program is usually to identify the problem domain's concepts, and then find suitable representations for them in code.
- **1.4.1. Updating Structures 🔗** — Imagine a function zeroX that replaces the x field of a Point with 0 .
- **1.4.2. Behind the Scenes 🔗** — Every structure has a constructor .
- **1.4.3. Exercises 🔗** — Define a structure named RectangularPrism that contains the height, width, and depth of a rectangular prism, each as a Float .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←1.3. Functions and Definitions](Getting-to-Know-Lean/Functions-and-Definitions/#functions-and-definitions "1.3. Functions and Definitions")[1.5. Datatypes and Patterns→](Getting-to-Know-Lean/Datatypes-and-Patterns/#datatypes-and-patterns "1.5. Datatypes and Patterns")

# 1.4. Structures[🔗](find/?domain=Verso.Genre.Manual.section&name=structures "Permalink")

The first step in writing a program is usually to identify the problem domain's concepts, and then find suitable representations for them in code.
Sometimes, a domain concept is a collection of other, simpler, concepts.
In that case, it can be convenient to group these simpler components together into a single “package”, which can then be given a meaningful name.
In Lean, this is done using *structures*, which are analogous to `struct`s in C or Rust and `record`s in C#.

Defining a structure introduces a completely new type to Lean that can't be reduced to any other type.
This is useful because multiple structures might represent different concepts that nonetheless contain the same data.
For instance, a point might be represented using either Cartesian or polar coordinates, each being a pair of floating-point numbers.
Defining separate structures prevents API clients from confusing one for another.

Lean's floating-point number type is called `Float`, and floating-point numbers are written in the usual notation.

`#check 1.2`


```lean
1.2 : Float
```


`#check -454.2123215`


```lean
-454.2123215 : Float
```


`#check 0.0`


```lean
0.0 : Float
```


When floating point numbers are written with the decimal point, Lean will infer the type `Float`. If they are written without it, then a type annotation may be necessary.

`#check 0`


```lean
0 : Nat
```


`#check (0 : Float)`


```lean
0 : Float
```


A Cartesian point is a structure with two `Float` fields, called `x` and `y`.
This is declared using the `structure` keyword.

`structure Point where
x : Float
y : Float`

After this declaration, `Point` is a new structure type.
The typical way to create a value of a structure type is to provide values for all of its fields inside of curly braces.
The origin of a Cartesian plane is where `x` and `y` are both zero:

`def origin : Point := { x := 0.0, y := 0.0 }`

The result of `#eval origin` looks very much like the definition of `origin`.


```lean
{ x := 0.000000, y := 0.000000 }
```


Because structures exist to “bundle up” a collection of data, naming it and treating it as a single unit, it is also important to be able to extract the individual fields of a structure.
This is done using dot notation, as in C, Python, Rust, or JavaScript.

`#eval origin.x`


```lean
0.000000
```


`#eval origin.y`


```lean
0.000000
```


This can be used to define functions that take structures as arguments.
For instance, addition of points is performed by adding the underlying coordinate values.
It should be the case that

`#eval addPoints { x := 1.5, y := 32 } { x := -8, y := 0.2 }`

yields


```lean
{ x := -6.500000, y := 32.200000 }
```


The function itself takes two `Point`s as arguments, called `p1` and `p2`.
The resulting point is based on the `x` and `y` fields of both `p1` and `p2`:

`def addPoints (p1 : Point) (p2 : Point) : Point :=
{ x := p1.x + p2.x, y := p1.y + p2.y }`

Similarly, the distance between two points, which is the square root of the sum of the squares of the differences in their `x` and `y` components, can be written:

`def distance (p1 : Point) (p2 : Point) : Float :=
Float.sqrt (((p2.x - p1.x) ^ 2.0) + ((p2.y - p1.y) ^ 2.0))`

For example, the distance between `(1, 2)` and `(5, -1)` is `5`:

`#eval distance { x := 1.0, y := 2.0 } { x := 5.0, y := -1.0 }`


```lean
5.000000
```


Multiple structures may have fields with the same names.
A three-dimensional point datatype may share the fields `x` and `y`, and be instantiated with the same field names:

`structure Point3D where
x : Float
y : Float
z : Float``def origin3D : Point3D := { x := 0.0, y := 0.0, z := 0.0 }`

This means that the structure's expected type must be known in order to use the curly-brace syntax.
If the type is not known, Lean will not be able to instantiate the structure.
For example,

`#check { x := 0.0, y := 0.0 }`

leads to the error


```lean
invalid {...} notation, expected type is not known
```


As usual, the situation can be remedied by providing a type annotation.

`#check ({ x := 0.0, y := 0.0 } : Point)`


```lean
{ x := 0.0, y := 0.0 } : Point
```


To make programs more concise, Lean also allows the structure type annotation inside the curly braces.

`#check { x := 0.0, y := 0.0 : Point}`


```lean
{ x := 0.0, y := 0.0 } : Point
```


## 1.4.1. Updating Structures[🔗](find/?domain=Verso.Genre.Manual.section&name=updating-structures "Permalink")

Imagine a function `zeroX` that replaces the `x` field of a `Point` with `0`.
In most programming language communities, this sentence would mean that the memory location pointed to by `x` was to be overwritten with a new value.
However, Lean is a functional programming language.
In functional programming communities, what is almost always meant by this kind of statement is that a fresh `Point` is allocated with the `x` field pointing to the new value, and all other fields pointing to the original values from the input.
One way to write `zeroX` is to follow this description literally, filling out the new value for `x` and manually transferring `y`:

`def zeroX (p : Point) : Point :=
{ x := 0, y := p.y }`

This style of programming has drawbacks, however.
First off, if a new field is added to a structure, then every site that updates any field at all must be updated, causing maintenance difficulties.
Secondly, if the structure contains multiple fields with the same type, then there is a real risk of copy-paste coding leading to field contents being duplicated or switched.
Finally, the program becomes long and bureaucratic.

Lean provides a convenient syntax for replacing some fields in a structure while leaving the others alone.
This is done by using the `with` keyword in a structure initialization.
The source of unchanged fields occurs before the `with`, and the new fields occur after.
For example, `zeroX` can be written with only the new `x` value:

`def zeroX (p : Point) : Point :=
{ p with x := 0 }`

Remember that this structure update syntax does not modify existing values—it creates new values that share some fields with old values.
Given the point `fourAndThree`:

`def fourAndThree : Point :=
{ x := 4.3, y := 3.4 }`

evaluating it, then evaluating an update of it using `zeroX`, then evaluating it again yields the original value:

`#eval fourAndThree`


```lean
{ x := 4.300000, y := 3.400000 }
```


`#eval zeroX fourAndThree`


```lean
{ x := 0.000000, y := 3.400000 }
```


`#eval fourAndThree`


```lean
{ x := 4.300000, y := 3.400000 }
```


One consequence of the fact that structure updates do not modify the original structure is that it becomes easier to reason about cases where the new value is computed from the old one.
All references to the old structure continue to refer to the same field values in all of the new values provided.

## 1.4.2. Behind the Scenes[🔗](find/?domain=Verso.Genre.Manual.section&name=behind-the-scenes "Permalink")

Every structure has a *constructor*.
Here, the term “constructor” may be a source of confusion.
Unlike constructors in languages such as Java or Python, constructors in Lean are not arbitrary code to be run when a datatype is initialized.
Instead, constructors simply gather the data to be stored in the newly-allocated data structure.
It is not possible to provide a custom constructor that pre-processes data or rejects invalid arguments.
This is really a case of the word “constructor” having different, but related, meanings in the two contexts.

By default, the constructor for a structure named `S` is named `S.mk`.
Here, `S` is a namespace qualifier, and `mk` is the name of the constructor itself.
Instead of using curly-brace initialization syntax, the constructor can also be applied directly.

`#check Point.mk 1.5 2.8`

However, this is not generally considered to be good Lean style, and Lean even returns its feedback using the standard structure initializer syntax.


```lean
{ x := 1.5, y := 2.8 } : Point
```


Constructors have function types, which means they can be used anywhere that a function is expected.
For instance, `Point.mk` is a function that accepts two `Float`s (respectively `x` and `y`) and returns a new `Point`.

`#check (Point.mk)`


```lean
Point.mk : Float → Float → Point
```


To override a structure's constructor name, write it with two colons at the beginning.
For instance, to use `Point.point` instead of `Point.mk`, write:

`structure Point where
point ::
x : Float
y : Float`

In addition to the constructor, an accessor function is defined for each field of a structure.
These have the same name as the field, in the structure's namespace.
For `Point`, accessor functions `Point.x` and `Point.y` are generated.

`#check (Point.x)`


```lean
Point.x : Point → Float
```


`#check (Point.y)`


```lean
Point.y : Point → Float
```


In fact, just as the curly-braced structure construction syntax is converted to a call to the structure's constructor behind the scenes, the syntax `x` in the prior definition of `addPoints` is converted into a call to the `x` accessor.
That is, `#eval origin.x` and `#eval Point.x origin` both yield


```lean
0.000000
```


Accessor dot notation is usable with more than just structure fields.
It can also be used for functions that take any number of arguments.
More generally, accessor notation has the form `TARGET.f ARG1 ARG2 ...`.
If `TARGET` has type `T`, the function named `T.f` is called.
`TARGET` becomes its leftmost argument of type `T`, which is often but not always the first one, and `ARG1 ARG2 ...` are provided in order as the remaining arguments.
For instance, `String.append` can be invoked from a string with accessor notation, even though `String` is not a structure with an `append` field.

`#eval "one string".append " and another"`


```lean
"one string and another"
```


In that example, `TARGET` represents `"one string"` and `ARG1` represents `" and another"`.

The function `Point.modifyBoth` (that is, `modifyBoth` defined in the `Point` namespace) applies a function to both fields in a `Point`:

`def Point.modifyBoth (f : Float → Float) (p : Point) : Point :=
{ x := f p.x, y := f p.y }`

Even though the `Point` argument comes after the function argument, it can be used with dot notation as well:

`#eval fourAndThree.modifyBoth Float.floor`


```lean
{ x := 4.000000, y := 3.000000 }
```


In this case, `TARGET` represents `fourAndThree`, while `ARG1` is `Float.floor`.
This is because the target of the accessor notation is used as the first argument in which the type matches, not necessarily the first argument.

## 1.4.3. Exercises[🔗](find/?domain=Verso.Genre.Manual.section&name=structure-exercises "Permalink")

- Define a structure named `RectangularPrism` that contains the height, width, and depth of a rectangular prism, each as a `Float`.
- Define a function named `volume : RectangularPrism → Float` that computes the volume of a rectangular prism.
- Define a structure named `Segment` that represents a line segment by its endpoints, and define a function `length : Segment → Float` that computes the length of a line segment. `Segment` should have at most two fields.
- Which names are introduced by the declaration of `RectangularPrism`?
- Which names are introduced by the following declarations of `Hamster` and `Book`? What are their types?

  `structure Hamster where
  name : String
  fluffy : Bool``structure Book where
  makeBook ::
  title : String
  author : String
  price : Float`

[←1.3. Functions and Definitions](Getting-to-Know-Lean/Functions-and-Definitions/#functions-and-definitions "1.3. Functions and Definitions")[1.5. Datatypes and Patterns→](Getting-to-Know-Lean/Datatypes-and-Patterns/#datatypes-and-patterns "1.5. Datatypes and Patterns")
