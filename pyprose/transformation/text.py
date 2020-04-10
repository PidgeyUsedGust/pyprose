# import clr
import sys
from typing import List, Tuple, Optional, Union

import pyprose
import pyprose.dependencies

dependencies = {
    "Microsoft.ProgramSynthesis.Transformation.Text": [
        "System.Collections.Immutable",
        "Newtonsoft.Json",
        "Microsoft.ProgramSynthesis.Common",
    ]
}
pyprose.dependencies.load(dependencies)

from Microsoft.ProgramSynthesis.Transformation.Text import (
    Example as _Example,
    InputRow,
    Session,
    Program,
)

# from Microsoft.ProgramSynthesis.Transformation.Text.Semantics import IRow
from Microsoft.ProgramSynthesis.Transformation.Text.Translation.Python import (
    PythonTranslator,
    PythonModule,
)
from Microsoft.ProgramSynthesis.Translation import OptimizeFor
from Microsoft.ProgramSynthesis.Translation.Python import PythonHeaderModule


class Example:
    """Input-output example."""

    def __init__(self, I: Union[List[str], str], O: str):
        if isinstance(I, str):
            I = [I]
        self._input = I
        self._output = O

    def to_prose(self) -> _Example:
        return _Example(InputRow(self._input), self._output)


class TransformationProgram(pyprose.ProseProgram):
    """Transformation program.
    
    Adds some additional information such as which columns
    are used. 

    """

    def used_columns(self) -> List[int]:
        """Columns used by this program.
        
        As these are always the column indices, we cast them
        to integers, which allows for easily extracting them
        from the input.
    
        Returns:
            Indices of the columns used by this program.
    
        """
        return list(map(int, self._program.ColumnsUsed))

    def n_columns(self) -> int:
        """Number of inputs used."""
        return len(self._program.ColumnsUsed)


def learn_program(
    examples: List[Example], additional_input: Optional[List[List[str]]] = None
) -> TransformationProgram:
    """Learn a program.
    
    Args:
        examples (iterable): List of (input, output) examples where input
            is a tuple and output is a string.
        additional_input (iterable): List of additional input tuples.

    Returns:
        A `ProseProgram` that transforms input into output.
        
    """
    return TransformationProgram(
        _learn_programs(examples, additional_input, k=1)[0], _run_program
    )


def learn_programs(
    examples: List[Example],
    additional_input: Optional[List[List[str]]] = None,
    k: int = 1,
) -> List[Program]:
    """Learn multiple programs.
    
    As per PROSE, `k` differently ranked programs are learned,
    so more programs may be returned.

    May return fewer than `k` programs if less are found.

    Args:
        k (int): Minimal number of differently ranked programs
            to learn.

    """
    return [
        pyprose.ProseProgram(program, _run_program)
        for program in _learn_programs(examples, additional_input, k)
    ]


def _learn_programs(
    examples: List[Example],
    additional_input: Optional[List[List[str]]] = None,
    k: int = 1,
) -> List[Program]:
    """Learn a transformation program from a set of examples.

    Args:
        examples (iterable): List of Example objects.
        additional_input (iterable): List of additional input columns.
        k (int): Number of programs to lean.

    Returns:
        A list of Programs.

    """
    # initialise session
    session = Session()
    # feed examples
    for example in examples:
        session.Constraints.Add(example.to_prose())
    # feed additional input
    if additional_input is not None:
        for input_ in additional_input:
            session.Inputs.Add(InputRow(input_))
    # learn program
    programs = session.LearnTopK(k)
    return programs


def _run_program(program: Program, i: Union[List[str], str]):
    """Run a program.
    
    Args:
        i (iterable): List of input values.
    
    Returns:
        Result of program(i) as a string.
    
    """
    if isinstance(i, str):
        i = [i]
    return program.Run(InputRow(i))


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
