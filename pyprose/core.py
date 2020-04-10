from typing import Callable, Any
import pyprose.dependencies

dependencies = {
    "Microsoft.ProgramSynthesis.Common": [
        "System.Collections.Immutable",
        "Newtonsoft.Json",
    ]
}
pyprose.dependencies.load(dependencies)

from Microsoft.ProgramSynthesis import Program


class ProseProgram:
    """Wrapper around PROSE programs."""

    def __init__(self, program: Program, runner: Callable[[Program, Any], Any]):
        self._program = program
        self._runner = runner

    def __call__(self, i: Any):
        return self._runner(self._program, i)

    @property
    def score(self) -> float:
        return self._program.Score