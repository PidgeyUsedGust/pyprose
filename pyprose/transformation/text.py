"""Implements the FlashFill algorithm [1]_.

.. [1] Gulwani, Sumit. "Automating string processing in spreadsheets using input-output
   examples." ACM Sigplan Notices 46.1 (2011): 317-330.

"""
from typing import List, Optional, Union, Any

from ..core import ProseProgram
from ..dependencies import load

dependencies = {
    "Microsoft.ProgramSynthesis.Transformation.Text": [
        "System.Collections.Immutable",
        "Newtonsoft.Json",
        "Microsoft.ProgramSynthesis.Common",
    ]
}
load(dependencies)

from Microsoft.ProgramSynthesis.Wrangling import Example as ProseExample, InputRow  # type: ignore
from Microsoft.ProgramSynthesis.Transformation.Text import Session, Program  # type: ignore
from Microsoft.ProgramSynthesis.Transformation.Text.Translation.Python import (  # type: ignore
    PythonTranslator,
    PythonModule,
)
from Microsoft.ProgramSynthesis.Translation import OptimizeFor  # type: ignore
from Microsoft.ProgramSynthesis.Translation.Python import PythonHeaderModule  # type: ignore


class Example:
    """An input-output or input example."""

    def __init__(self, I: Union[List[str], str], O: Optional[str] = None):
        """

        Args:
            I: Row of input values.
            O: Output to which `I` should be transformed. If not given,
                considered as an input only example that can be used
                to help the synthesizer.

        """
        if isinstance(I, str):
            I = [I]
        self.input = I
        self.output = O

    def __str__(self):
        return "{} -> {}".format(", ".join(self.input), self.output)

    def to_prose(self) -> Union[ProseExample, InputRow]:
        if self.output is not None:
            return ProseExample(InputRow(self.input), self.output)
        return InputRow(self.input)

    def has_output(self):
        return self.output is not None


class TextTransformationProgram(ProseProgram):
    """A callable text transformation program."""

    def __call__(self, row: Union[List[str], str, Example]):
        """Transform input row.

        Args:
            row: Can be represented as a list of values, a single
                value or an example.

        """
        return super().__call__(row)

    @property
    def uses_columns(self) -> List[int]:
        """Indices of input columns used by this transformation program."""
        return list(map(int, self._program.ColumnsUsed))


def make_examples(data: Any) -> List[Example]:
    """Convenience function for creating examples from data.

    The following formats for input data are currently supported.

        * A list of rows representing a table. Rows that don't have
          the last element are considered input only examples.
        * List of `(input, output)` tuples where `input` can be a single
          string or a list of values.

    Pandas dataframes can be easily converted to a suitable format
    using `df.values.tolist()`.

    Returns:
        Examples found in the input.

    """
    examples = list()

    # example given as ((input,) output) tuples.
    if all(isinstance(line, tuple) for line in data):
        for line in data:
            if len(line) == 2:
                examples.append(Example(line[0], line[1]))
            elif len(line) == 1:
                examples.append(Example(line[0]))

    # example given as list of strings
    elif all(all(isinstance(e, str) for e in line) for line in data):
        n = max(map(len, data))
        for line in data:
            if len(line) == n and line[-1] != "" and line[-1] != None:
                examples.append(Example(line[:-1], line[-1]))
            elif len(line) == n:
                examples.append(Example(line[:-1]))
            elif len(line) + 1 == n:
                examples.append(Example(line))

    return examples


def learn_program(examples: List[Example]) -> Optional[TextTransformationProgram]:
    """Learn a single program.

    Args:
        examples: List of examples.

    Returns:
        A transformation program if one is found, `None` otherwise.

    """
    program = _make_session(examples).Learn()
    if program is None:
        return None
    return TextTransformationProgram(program, _run_program)


def learn_programs(
    examples: List[Example], k: int = 1
) -> List[TextTransformationProgram]:
    """Learn multiple programs and return top-`k` ranked ones.

    As per PROSE, `k` differently ranked programs are learned,
    so more programs may be returned. May return fewer than `k`
    programs if not enough are found.

    """
    return [
        TextTransformationProgram(program, _run_program)
        for program in _make_session(examples).LearnTopK(k)
    ]


def flashfill(data: List[List[str]]) -> List[List[str]]:
    """Emulate spreadsheet environment.

    Rows that are incomplete are filled by learning a program
    on other rows.

    Args:
        data: A table as a list of lists.

    Returns:
        The input data, but with incomplete rows filled.

    """
    examples = make_examples(data)
    program = learn_program(examples)
    for i, example in enumerate(examples):
        if not example.has_output():
            output = program(example)
            line = data[i]
            if len(line) == len(example.input):
                line.append(output)
            else:
                line[-1] = output
    return data


def _make_session(examples: List[Example]) -> List[Program]:
    session = Session()
    for example in examples:
        if example.has_output():
            session.Constraints.Add(example.to_prose())
        else:
            session.Inputs.Add(example.to_prose())
    return session


def _run_program(program: Program, i: Union[List[str], str, Example]):
    """Run a program.

    Args:
        i: Input row. For convenience, we also allow raw inputs
            to be given, rather than only examples.

    Returns:
        Result of program(i).

    """
    if not isinstance(i, Example):
        i = Example(i)
    return program.Run(i.to_prose())


def _to_python(program, column_names=None):
    """Convert a program to Python.

    Returns a header with PROSE wrapper code and a
    string with the python code itself.

    Based off the ToPythonExtensions helper class,
    but we want to be able to reuse the header.

    WIP.

    """

    optimise = OptimizeFor.Performance

    translator = PythonTranslator()

    header = translator.GenerateHeaderModule(program, "prose_semantics")
    module = translator.CreateModule("transformation_text", "prose_semantics")
    method = translator.Translate(program, module, None, optimise)

    generated = method.GenerateCode("prose_semantics", optimise)

    module.Bind("transform_text", method)

    print(module.GenerateUnisolatedCode(optimise))
    # return ToPythonExtensions.ToPython(
    #     program, optimise, isolated=False, useProseLib=True
    # )
