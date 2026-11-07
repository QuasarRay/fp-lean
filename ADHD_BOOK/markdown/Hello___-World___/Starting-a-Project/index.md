# Study guide: 2.3. Starting a Project 🔗

> This page is a companion transcription. The authoritative, complete rendered book is in `site/original/`.
> The ADHD website in `site/adhd/` retains every original rendered paragraph and code block.

## Quick concept reference (source excerpts)

- **2.3. Starting a Project 🔗** — As a program written in Lean becomes more serious, an ahead-of-time compiler-based workflow that results in an executable becomes more attractive.
- **2.3.1. First steps 🔗** — To get started with a project that uses Lake, use the command lake new greeting in a directory that does not already contain a file or directory called greeting .
- **2.3.2. Lakefiles 🔗** — A lakefile.toml describes a package , which is a coherent collection of Lean code for distribution, analogous to an npm or nuget package or a Rust crate.
- **2.3.3. Libraries and Imports 🔗** — A Lean library consists of a hierarchically organized collection of source files from which names can be imported, called modules .

## One-section checklist

- [ ] Read one subsection of the full lesson.
- [ ] Run all Lean examples, including examples that intentionally produce errors.
- [ ] Attempt every original exercise.
- [ ] Explain the main idea using one sentence.

---

## Complete source lesson

[←2.2. Step By Step](Hello___-World___/Step-By-Step/#step-by-step "2.2. Step By Step")[2.4. Worked Example: cat→](Hello___-World___/Worked-Example___--cat/#example-cat "2.4. Worked Example: cat")

# 2.3. Starting a Project[🔗](find/?domain=Verso.Genre.Manual.section&name=starting-a-project "Permalink")

As a program written in Lean becomes more serious, an ahead-of-time compiler-based workflow that results in an executable becomes more attractive.
Like other languages, Lean has tools for building multiple-file packages and managing dependencies.
The standard Lean build tool is called Lake (short for “Lean Make”).
Lake is typically configured using a TOML file that declaratively specifies dependencies and describes what is to be built.
For advanced use cases, Lake can also be configured in Lean itself.

## 2.3.1. First steps[🔗](find/?domain=Verso.Genre.Manual.section&name=lake-new "Permalink")

To get started with a project that uses Lake, use the command `lake new greeting` in a directory that does not already contain a file or directory called `greeting`.
This creates a directory called `greeting` that contains the following files:

- `Main.lean` is the file in which the Lean compiler will look for the `main` action.
- `Greeting.lean` and `Greeting/Basic.lean` are the scaffolding of a support library for the program.
- `lakefile.toml` contains the configuration that `lake` needs to build the application.
- `lean-toolchain` contains an identifier for the specific version of Lean that is used for the project.

Additionally, `lake new` initializes the project as a Git repository and configures its `.gitignore` file to ignore intermediate build products.
Typically, the majority of the application logic will be in a collection of libraries for the program, while `Main.lean` will contain a small wrapper around these pieces that does things like parsing command lines and executing the central application logic.
To create a project in an already-existing directory, run `lake init` instead of `lake new`.

By default, the library file `Greeting/Basic.lean` contains a single definition:

File: `Greeting/Basic.lean``def hello := "world"`

The library file `Greeting.lean` imports `Greeting/Basic.lean`:

File: `Greeting.lean``` -- This module serves as the root of the `Greeting` library. ```-- Import modules here that should be built as part of the library.``import Greeting.Basic`

This means that everything defined in `Greeting/Basic.lean` is also available to files that import `Greeting.lean`.
In `import` statements, dots are interpreted as directories on disk.

The executable source `Main.lean` contains:

File: `Main.lean``import Greeting``def main : IO Unit :=` `IO.println s!"Hello, {hello}!"`

Because `Main.lean` imports `Greeting.lean` and `Greeting.lean` imports `Greeting/Basic.lean`, the definition of `hello` is available in `main`.

To build the package, run the command `lake build`.
After a number of build commands scroll by, the resulting binary has been placed in `.lake/build/bin`.
Running `./.lake/build/bin/greeting` results in `Hello, world!`.
Instead of running the binary directly, the command `lake exe` can be used to build the binary if necessary and then run it.
Running `lake exe greeting` also results in `Hello, world!`.

## 2.3.2. Lakefiles[🔗](find/?domain=Verso.Genre.Manual.section&name=lakefiles "Permalink")

A `lakefile.toml` describes a *package*, which is a coherent collection of Lean code for distribution, analogous to an `npm` or `nuget` package or a Rust crate.
A package may contain any number of libraries or executables.
The [documentation for Lake](https://lean-lang.org/doc/reference/latest/find/?domain=Verso.Genre.Manual.section&name=lake-config-toml) describes the available options in a Lake configuration.
The generated `lakefile.toml` contains the following:

File: `lakefile.toml``name = "greeting"``version = "0.1.0"``defaultTargets = ["greeting"]``[[lean_lib]]``name = "Greeting"``[[lean_exe]]``name = "greeting"``root = "Main"`

This initial Lake configuration consists of three items:

- *package* settings, at the top of the file,
- a *library* declaration, named `Greeting`, and
- an *executable*, named `greeting`.

Each Lake configuration file will contain exactly one package, but any number of dependencies, libraries, or executables.
By convention, package and executable names begin with a lowercase letter, while libraries begin with an uppercase letter.
Dependencies are declarations of other Lean packages (either locally or from remote Git repositories)
The items in the Lake configuration file allow things like source file locations, module hierarchies, and compiler flags to be configured.
Generally speaking, however, the defaults are reasonable.
Lake configuration files written in the Lean format may additionally contain *external libraries*, which are libraries not written in Lean to be statically linked with the resulting executable, *custom targets*, which are build targets that don't fit naturally into the library/executable taxonomy, and *scripts*, which are essentially `IO` actions (similar to `main`), but that additionally have access to metadata about the package configuration.

Libraries, executables, and custom targets are all called *targets*.
By default, `lake build` builds those targets that are specified in the `defaultTargets` list.
To build a target that is not a default target, specify the target's name as an argument after `lake build`.

## 2.3.3. Libraries and Imports[🔗](find/?domain=Verso.Genre.Manual.section&name=libraries-and-imports "Permalink")

A Lean library consists of a hierarchically organized collection of source files from which names can be imported, called *modules*.
By default, a library has a single root file that matches its name.
In this case, the root file for the library `Greeting` is `Greeting.lean`.
The first line of `Main.lean`, which is `import Greeting`, makes the contents of `Greeting.lean` available in `Main.lean`.

Additional module files may be added to the library by creating a directory called `Greeting` and placing them inside.
These names can be imported by replacing the directory separator with a dot.
For instance, creating the file `Greeting/Smile.lean` with the contents:

File: `Greeting/Smile.lean``def Expression.happy : String := "a big smile"`

means that `Main.lean` can use the definition as follows:

File: `Main.lean``import Greeting``import Greeting.Smile``open Expression``def main : IO Unit :=` `IO.println s!"Hello, {hello}, with {happy}!"`

The module name hierarchy is decoupled from the namespace hierarchy.
In Lean, modules are units of code distribution, while namespaces are units of code organization.
That is, names defined in the module `Greeting.Smile` are not automatically in a corresponding namespace `Greeting.Smile`.
In particular, `happy` is in the `Expression` namespace.
Modules may place names into any namespace they like, and the code that imports them may `open` the namespace or not.
`import` is used to make the contents of a source file available, while `open` makes names from a namespace available in the current context without prefixes.

The line `open Expression` makes the name `Expression.happy` accessible as `happy` in `main`.
Namespaces may also be opened *selectively*, making only some of their names available without explicit prefixes.
This is done by writing the desired names in parentheses.
For example, `Nat.toFloat` converts a natural number to a `Float`.
It can be made available as `toFloat` using `open Nat (toFloat)`.

[←2.2. Step By Step](Hello___-World___/Step-By-Step/#step-by-step "2.2. Step By Step")[2.4. Worked Example: cat→](Hello___-World___/Worked-Example___--cat/#example-cat "2.4. Worked Example: cat")
