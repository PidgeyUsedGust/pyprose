import re
import sys
from typing import List, Iterable, Union, Optional

import pyprose
import pyprose.dependencies

dependencies = {
    "Microsoft.ProgramSynthesis.Matching.Text": [
        "System.Collections.Immutable",
        "Microsoft.ProgramSynthesis.Common",
    ]
}

pyprose.dependencies.load(dependencies)

from System import Array
from System.Collections.Generic import List as _List
from Microsoft.ProgramSynthesis.Matching.Text import (
    Session,
    PatternInfo,
    AllowedTokens,
    InDifferentCluster,
    InSameCluster,
    OutlierLimit,
)
from Microsoft.ProgramSynthesis.Matching.Text.Semantics import (
    DefaultTokens,
    RegexToken,
    IToken,
)
from Microsoft.ProgramSynthesis.Matching.Text.Constraints import IncludeOutlierPatterns


class Pattern:
    """Wrapper around PatternInfo."""

    def __init__(self, pattern: PatternInfo):
        self._pattern = pattern

    def __call__(self, string: str) -> bool:
        return self.matches(string)

    def matches(self, string: str) -> bool:
        """Check if this pattern matches a given string.

        Will also ensure that none of the excluded regexes
        are matches.

        """
        return (re.match(self.regex, string) is not None) and not any(
            re.match(e, string) is not None for e in self.exclude
        )

    def extract(self, text: str) -> List[str]:
        """Extract all matches of this pattern from text.
        
        Args:
            text (str): Text to extract patterns from.

        """
        candidates = re.findall(self.regex[1:-1], text)
        return [
            candidate
            for candidate in candidates
            if not any(re.match(e, candidate) for e in self.exclude)
        ]

    @property
    def description(self) -> str:
        return self._pattern.Description

    @property
    def tokens(self) -> IToken:
        return self._pattern.DescriptionTokens

    @property
    def regex(self) -> str:
        return self._pattern.Regex

    @property
    def exclude(self) -> str:
        return self._pattern.RegexesToExclude

    @property
    def matching_fraction(self) -> float:
        return self._pattern.MatchingFraction

    @property
    def examples(self):
        return self._pattern.Examples

    @property
    def example(self):
        return next(iter(self.examples), None)


class Token:
    """Roughly a wrapper atound IToken.
    
    Rather than defining by character classes, we define them
    by the regex that should be matched.

    The default tokens used by FlashProfile have a generality
    score assigned to them. We allow the score to be set
    to a custom number or to the same generality as any
    existing token. The list of valid values for `score`
    can be obtained by `Token.default_tokens()`. The score for
    any of the default tokens can be obtained as follows.

    >>> Token.default_token_score('whitespace')
    -6.0

    """

    def __init__(self, regex, name: str = "", score: Union[float, str] = 0):
        self._regex = regex
        self._name = name
        if isinstance(score, str):
            score = self.default_token_score(score)
        self._score = score

    def __str__(self):
        return self._regex

    def to_prose(self) -> IToken:
        """Convert to an IToken.
        
        Uses RegexToken constructor as we only use
        regex based tokens.
        
        """
        return RegexToken(self._name, self._regex, self._score)

    @classmethod
    def default_tokens(cls):
        """Get list of default tokens."""
        return [t.Value for t in DefaultTokens.AllTokensPythonNames]

    @classmethod
    def default_token_score(cls, token: str) -> float:
        """Get score of any of the default tokens.
        
        Args:
            token (str): Any of the `Token.default_tokens`.
        """
        token = next(
            t.Key.Score for t in DefaultTokens.AllTokensPythonNames if t.Value == token
        )
        return token

    @classmethod
    def from_characters(
        cls, characters, name: str = "", score: Union[float, str] = 0.0
    ):
        return cls("[{}]+".format(characters), name, score)

    @classmethod
    def from_constant(cls, string, name: str = "", score: Union[float, str] = 0.0):
        return cls(string, name, score)


def learn_patterns(
    strings: Iterable[str],
    allowed_tokens: Optional[Iterable[Token]] = None,
    in_different_clusters: Optional[List[List[str]]] = None,
    in_same_clusters: Optional[List[List[str]]] = None,
    include_outlier_patterns: bool = False,
    outlier_limit: Optional[float] = None,
) -> List[Pattern]:
    """Learn patterns from strings.
    
    As presented in FlashProfile.

    Args:
        strings (iterable): A list of strings.
        allowed_tokens (iterable): List of tokens.

    """
    return [
        Pattern(pattern)
        for pattern in _learn_patterns(
            strings,
            allowed_tokens=allowed_tokens,
            in_different_clusters=in_different_clusters,
            in_same_clusters=in_same_clusters,
            include_outlier_patterns=include_outlier_patterns,
            outlier_limit=outlier_limit,
        )
    ]


def _learn_patterns(
    strings: Iterable[str],
    allowed_tokens: Optional[Iterable[Token]] = None,
    in_different_clusters: Optional[List[List[str]]] = None,
    in_same_clusters: Optional[List[List[str]]] = None,
    include_outlier_patterns: bool = False,
    outlier_limit: Optional[float] = None,
) -> List[PatternInfo]:
    """

    The input and output type of programs is assumed to be <str, bool>
    as based off the `InSameCluster` constraint.

    """
    session = Session()

    for string in strings:
        session.Inputs.Add(string)

    if allowed_tokens is not None:
        itokens = list()
        for tokens in allowed_tokens:
            itokens.append(tokens.to_prose())
        session.Constraints.Add(AllowedTokens[str, bool](Array[IToken](itokens)))

    if in_different_clusters is not None:
        for different in in_different_clusters:
            session.Constraints.Add(InDifferentCluster(Array[str](different)))

    if in_same_clusters is not None:
        for same in in_same_clusters:
            session.Constraints.Add(InSameCluster(Array[str](same)))

    if include_outlier_patterns:
        session.Constraints.Add(IncludeOutlierPatterns[str, bool]())

    if outlier_limit is not None:
        session.Constraints.Add(OutlierLimit[str, bool](outlier_limit))

    patterns = session.LearnPatterns()
    return patterns
