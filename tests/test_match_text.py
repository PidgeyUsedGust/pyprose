from pathlib import Path
from pyprose.matching.text import learn_patterns, Token


def test_match_dates():
    patterns = learn_patterns(
        [
            "21-Feb-73",
            "2 January 1920a",
            "4 July 1767",
            "1892",
            "11 August 1897",
            "11 November 1889",
            "9-Jul-01",
            "17-Sep-08",
            "10-May-35",
            "7-Jun-52",
            "24 July 1802",
            "25 April 1873",
            "24 August 1850",
            "Unknown",
            "1058",
            "8 August 1876",
            "26 July 1165",
            "28 December 1843",
            "22-Jul-46",
            "17 January 1871",
            "17-Apr-38",
            "28 February 1812",
            "1903",
            "1915",
            "1854",
            "9 May 1828",
            "28-Jul-32",
            "25-Feb-16",
            "19-Feb-40",
            "10-Oct-50",
            "5 November 1880",
            "1928",
            "13-Feb-03",
            "8-Oct-43",
            "1445",
            "8 July 1859",
            "25-Apr-27",
            "25 November 1562",
            "2-Apr-10",
        ]
    )
    assert len(patterns) == 6

    extracted = set()
    for pattern in patterns:
        extracted.update(
            pattern.extract("I was born on 25 December 1992 and not in 1993")
        )
    assert extracted == {"1992", "1993", "25 December 1992"}


def test_tokens():
    assert "whitespace" in Token.default_tokens()
    assert Token.default_token_score("whitespace") == -6.0

    for pattern in patterns:
        assert pattern.tokens[0].Name == "P"


def test_same_cluster():

    strings = ["1992", "2003", "January"]

    patterns1 = learn_patterns(strings)
    assert len(patterns1) == 2

    patterns2 = learn_patterns(strings, in_same_clusters=[["1992", "January"]])
    assert len(patterns2) == 1
    assert patterns2[0].matches("Anything2001")


def test_different_cluster():

    strings = ["1992", "2001", "1995"]

    patterns1 = learn_patterns(strings)
    assert len(patterns1) == 1
    assert patterns1[0].matches("2020")
    assert patterns1[0].matches("1885")

    patterns2 = learn_patterns(strings, in_different_clusters=[["1992", "2001"]])
    assert len(patterns2) == 2


if __name__ == "__main__":
    test_match_dates()
    test_tokens()
    test_same_cluster()
    test_different_cluster()
