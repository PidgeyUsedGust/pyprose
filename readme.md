# pyprose

Python wrapper around the Microsoft PROSE framework. This package only provides easy wrappers around compiled DSLs, not the option for creating new DSLs.

## installation

### requirements

The main requirements are pythonnet and PROSE. Below are instructions to get these up and running. 

#### pythonnet

This package depends on pythonnet for calling PROSE. Here are some instructions for installing it on different operating systems.

(TODO)

#### PROSE

This package requires the [Microsoft.ProgramSynthesis](https://www.nuget.org/packages/Microsoft.ProgramSynthesis/) package. By default, pyprose will look in the [global package cache](https://docs.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders) and should find the appropriate files if it was installed in any project. This can be done by either adding it to any project in Visual Studio, or by using `nuget.exe` and downloading it to any directory.

You can check whether (and which) dependencies are correctly detected by running the following command.

```console
python -m pyprose.dependencies
```

## how to use

The goal of pyprose is to make it as easy as possible to use the powerful PROSE system.

### basic example

As a simple example, we show how to use `Transformation.Text`, which implements the FlashFill system for learning string  transformation programs (example taken from  [here](https://microsoft.github.io/prose/documentation/transformation-text/intro/)).

```python
from pyprose.transformation.text import learn_program, Example

p = learn_program([
    Example(["Greta", "Hermansson"], "Hermansson, G."),
    Example(["Kettil", "Hansson"], "Hansson, K.")
])

# or with implicit examples

p = learn_program([
    (["Greta", "Hermansson"], "Hermansson, G."),
    (["Kettil", "Hansson"], "Hansson, K.")
])
```

The learned program can be ran on new inputs—a list of two strings in this case—as `p(["Etelka", "Bala"])` which returns a new string `Bala, E.`.

### constraints

Most constraints have been added as arguments in their respective `learn_program` functions.

All supported constraint arguments should be properly documented.

### FlashProfile

The FlashProfile system is implemented as `Match.Text` and yields patterns instead of programs.

## progress

Progress on implementation of DSLs.

- [x] Transformation.Text (FlashFill)
- [x] Match.Text (FlashProfile)
- [ ] Split.Text **(in progress)**
