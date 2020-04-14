import sys
from typing import List, Optional, Dict, Tuple

import pyprose
import pyprose.dependencies

dependencies = {
    "Microsoft.ProgramSynthesis.Split.Text": [
        "System.Collections.Immutable",
        "Newtonsoft.Json",
        "Microsoft.ProgramSynthesis.Common",
    ]
}

pyprose.dependencies.load(dependencies)

from Microsoft.ProgramSynthesis.Split.Text import (
    DelimiterStringsConstraint,
    FillStrategyConstraint,
    FixedWidthConstraint,
    IncludeDelimitersInOutput,
    NthExampleConstraint,
    ProgramProperties,
    QuotingConfigurationConstraint,
    SimpleDelimiter,
    SimpleDelimitersOrFixedWidth,
    SplitSession,
    SplitInputOutputExample,
    SplitProgram,
)
from Microsoft.ProgramSynthesis.Split.Text.Semantics import (
    FillStrategy,
    QuotingConfiguration,
    QuotingStyle,
    SplitCell,
)


class TextSplittingProgram(pyprose.ProseProgram):
    """Text splitting program."""

    @property
    def delimiter(self) -> str:
        return self._program.Properties.Delimiter

    @property
    def n_columns(self) -> int:
        return self._program.Properties.ColumnCount


def learn_program(
    examples: List[str],
    delimiters: Optional[List[str]] = None,
    fill_strategy: Optional[str] = None,
    fixed_width: bool = False,
    include_delimiters_in_output: bool = False,
    nth_examples: Optional[Dict[str, Dict[int, str]]] = None,
    quoting_configuration: Tuple[str, str, str] = None,
    simple_delimiter: bool = False,
    simple_delimiters_or_fixed_width: bool = False,
) -> TextSplittingProgram:
    """Learn splitting program."""
    return TextSplittingProgram(
        _learn_programs(
            examples,
            delimiters,
            fill_strategy,
            fixed_width,
            include_delimiters_in_output,
            nth_examples,
            quoting_configuration,
            simple_delimiter,
            simple_delimiters_or_fixed_width,
            k=1
        )[0],
        _run_program
    )


def _learn_programs(
    examples: List[str],
    delimiters: Optional[List[str]] = None,
    fill_strategy: Optional[str] = None,
    fixed_width: bool = False,
    include_delimiters_in_output: bool = False,
    nth_examples: Optional[Dict[str, Dict[int, str]]] = None,
    quoting_configuration: Tuple[str, str, str] = None,
    simple_delimiter: bool = False,
    simple_delimiters_or_fixed_width: bool = False,
    k=1
) -> List[SplitProgram]:
    """Learn a text splitting program from a set of examples.
    
    Args:
        examples (iterable): List of input examples.
        delimiters (iterable): List of possible delimiters.
        fill_strategy (str): Strategy to use for filling cells in columns
            with fewer cells than expected. One of "left", "right" or "null".
        fixed_width (boolean): Whether to learn fixed width programs.
        include_delimiters_in_output (boolean): Indicate whether splitting
            program should include delimiter cells in output.
        nth_example (dict): Mapping of input examples to positions
            to output cells.
        quoting_configuration (tuple): Tuple of `(quotechar, doublequote, escapechar)`
            that controls quoting. For now, only `QuotingStyle.Standard` is
            supported, which only allows quoting at the begin and end
            of a field. See `csv.Dialect` for more information.
        simple_delimiter (boolean): Whether single delimiter program should be learnt.
        simple_delimiters_or_fixed_width (boolean): 


    Returns:
        A `ProseProgram` that splits strings.

    """

    session = SplitSession()

    for example in examples:
        session.Inputs.Add(session.CreateStringRegion(example))

    if delimiters is not None:
        session.Constraints.Add(DelimiterStringsConstraint(list(delimiters)))

    if fill_strategy is not None:
        strategy = {
            "null": FillStrategy.null,
            "left": FillStrategy.LeftToRight,
            "right": FillStrategy.RightToLeft,
        }.get(fill_strategy)
        session.Constraints.Add(FillStrategyConstraint(strategy))

    if fixed_width:
        session.Constraints.Add(FixedWidthConstraint())

    # seems to be always added
    session.Constraints.Add(IncludeDelimitersInOutput(include_delimiters))

    if nth_examples is not None:
        for example_input in nth_examples:
            if example_input in examples:
                for position, output in nth_examples[example_input].items():
                    session.Constraints.Add(
                        NthExampleConstraint(example_input, position, output)
                    )

    if quoting_configuration is not None and len(quoting_configuration) == 3:
        session.Constraints.Add(QuotingConfigurationConstraint(*quoting_configuration))

    if simple_delimiter:
        session.Constraints.Add(SimpleDelimiter())

    if simple_delimiters_or_fixed_width:
        session.Constraints.Add(SimpleDelimitersOrFixedWidth())

    programs = session.LearnTopK(k)

    return programs


def _run_program(program: SplitProgram, example: str):
    return [
        s.CellValue.Value for s in program.Run(SplitSession.CreateStringRegion(example))
    ]
