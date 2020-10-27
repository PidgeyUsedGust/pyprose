# pyprose

Python wrapper around the Microsoft PROSE framework. This package only provides easy wrappers around compiled DSLs, not the option for creating new DSLs.

## How to use

As a simple example, we show how to use `Transformation.Text`, which implements the FlashFill system for learning string  transformation programs (example taken from  [here](https://microsoft.github.io/prose/documentation/transformation-text/intro/)).

```python
from pyprose.transformation.text import learn_program, make_examples

p = learn_program(make_examples([
    (["Greta", "Hermansson"], "Hermansson, G."),
    (["Kettil", "Hansson"], "Hansson, K.")
]))
```

The learned program can be ran on new inputs—a list of two strings in this case. In this case, calling `p(["Etelka", "Bala"])` then returns a new string `Bala, E.`.

### Constraints

Most constraints have been added as arguments in their respective `learn_program` functions. All supported constraint arguments should be properly documented.

### FlashProfile

Most DSLs learn programs that are to be invoked on new input. The `Match.Text` DSL implements FlashProfile, which learns patterns. The `learn_patterns` function returns a list of `Pattern` objects instead of a program. This object can be matched on new strings and can be used to extract this pattern from other strings.

```python
pattern = learn_patterns(["1992", "2001", "1995"])[0]
pattern.matches("2020")
pattern.extract("I was born on 25 December 1992")
```

More information and examples can be found in the documentation.

## Installation

This package requires Python 3.7, ``pythonnet`` and compiled PROSE assemblies. The documentation contains detailed instructions for installing these dependencies.

Once the dependencies are installed, a simple `pip install pyprose` should suffice.

## Progress

Progress on implementation of DSLs.

- [x] Transformation.Text (FlashFill)
- [x] Match.Text (FlashProfile)
- [ ] Split.Text **(in progress)**
