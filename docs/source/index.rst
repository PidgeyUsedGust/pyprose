pyprose
=======

Python wrapper around the Microsoft `PROSE <https://microsoft.github.io/prose/>`_ framework.
The goal of ``pyprose`` is providing easy access to existing DSLs implemented in this framework.

As a simple example, the following snippet demonstrates how to learn programs
with FlashFill, implemented in PROSE as **Transformation.Text**. 

::

   from pyprose.transformation.text import learn_program, make_examples

   p = learn_program(make_examples([
      ["Greta", "Hermansson", "Hermansson, G."],
      ["Kettil", "Hansson", "Hansson, K."]
   ]))

This program can then be used on new examples.

::

   >>> p(["Etelka", "Bala"])
   Bala, E.

The ``make_examples`` function supports conversion of many different input data formats
to examples that can be used with ``learn_program``.

Contents
========

.. toctree::
   :maxdepth: 2

   install
   examples
   modules

Progress
========

The following DSLs have been fully implemented and all documented arguments tested.

* ``Transformation.Text`` (FlashFill)
* ``Matching.Text`` (FlashProfile)

The following DSLs are currently in development.

* ``Split.Text`` (predictive text splitting)