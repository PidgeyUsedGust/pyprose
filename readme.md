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

The learned program can be ran on new inputs—a list of two strings in this case. In this case, calling `p(["Etelka", "Bala"])` then returns a new string `"Bala, E."`.

More information and examples can be found in the documentation.

## Installation

This package requires ``pythonnet`` and compiled PROSE assemblies. The documentation contains detailed instructions for installing these dependencies.

Once the dependencies are installed, a simple

```pip install git+https://github.com/pidgeyusedgust/pyprose``

should suffice.

## Progress

Progress on implementation of DSLs.

- [x] Transformation.Text (FlashFill)
- [x] Matching.Text (FlashProfile)
- [ ] Split.Text **(in progress)**

If you are interested in seeing a specific DSL integrated sooner, don't hesitate to contact me!

## Contact

Questions or feedback? Don't hesitate to contact me at `gust.verbruggen@kuleuven.be`!
