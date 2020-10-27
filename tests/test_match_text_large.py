from pathlib import Path
from pyprose.matching.text import learn_patterns, Token


def test_many_strings():

    import json
    import time

    with open(Path(__file__).parent / "resources" / "strings.json") as f:
        strings = json.load(f)

    start = time.time()
    patterns = learn_patterns(strings, outlier_limit=1.0, include_outlier_patterns=True)
    end = time.time()


if __name__ == "__main__":
    test_many_strings()
