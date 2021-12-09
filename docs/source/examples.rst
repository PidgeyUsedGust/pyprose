Examples
========

``Transformation.Text``
-----------------------

The most basic form to run FlashFill is to give it a list of :class:`Example <pyprose.transformation.text.Example>` objects.

::

   p = learn_program([
      Example(("Greta", "Hermansson"), "Hermansson, G."),
      Example(("Kettil", "Hansson"), "Hansson, K.")
   ])

When tabular data is available as a list of lists, the :func:`make_examples <pyprose.transformation.text.make_examples>` function can be used. It also supports a list of `(input, output)` tuples and it supports detecting input only examples.

::

   e = make_examples([
      ["Greta", "Hermansson", "Hermansson, G."],
      ["Kettil", "Hansson", "Hansson, K."],
      ["Myron", "Lampros"]
   ])
   p = learn_program(e)

Finally, the :func:`flashfill <pyprose.transformation.text.flashfill>` convenience function emulates a spreadsheet environment by detecting rows that lack an output value and using a learned program to fill them.

Invoking

::

   flashfill([
      ["Greta", "Hermansson", "Hermansson, G."],
      ["Kettil", "Hansson", "Hansson, K."],
      ["Myron", "Lampros"]
   ])

will add a cell ``"Lampros, Myron"`` to the final row.

``Matching.Text``
-----------------

This DSL allows to profile a list of strings by learning a small set of regular expressions that cover the strings.

:: 

   from pyprose.matching.text import learn_patterns

   examples = [
      "21-Feb-73",
      "2 January 1920",
      "4 July 1767",
      "11 August 1897",
      "11 November 1889",
      "09-Jul-01",
   ]
   patterns = learn_patterns(examples)

This yields two patterns that we can vizualise through ``pattern.description``::

   [Digit]{1} & [Space]{1} & TitleWord & [Space]{1} & Const[1] & [Digit]{3}
   [Digit]{2} & [Any]+

We can see that more emphasis is put on the first digit token having the same length. We can force some strings to be matched by the same pattern as follows::

   learn_patterns(
      examples,
      in_same_clusters=[["21-Feb-73", "09-Jul-01"]]
   )

yielding

::

   [Digit]+ & [Space]{1} & TitleWord & [Space]{1} & [Digit]{4}
   [Digit]{2} & Const[-] & TitleWord & Const[-] & [Digit]{2}

which makes more sense. Conversely, we can also disable strings from being matched by the same pattern::

   patterns = learn_patterns(
      ["1992", "2001", "1995"],
      in_different_clusters=[["1992", "2001"]]
   )

which yields patterns ``Const[199] & [Digit]{1}`` and ``Const[2001]``.

Besides descriptions, the :class:`Pattern <pyprose.matching.text.Pattern>` object also supports generating a regular expression::

   >>> pattern.regex
   '^199[0-9]$'

and matching and extraction capabilities.::

   >>> pattern.matches("1991")
   True

   >>> pattern.matches("2001")
   False

   >>> pattern.extract("I was born in 1992.")
   ["1992"]

Finally, we can get some statistics from the learning process.::

   >>> pattern.matching_fraction
   0.6666666666666666

   >>> pattern.examples
   ['1992', '1995']
