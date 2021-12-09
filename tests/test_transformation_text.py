from pyprose.transformation.text import (
    learn_program,
    learn_programs,
    make_examples,
    flashfill,
    Example,
)


def test_format_name():
    program = learn_program([Example("Kettil Hansson", "Hansson, K.")])
    assert program(["Etelka Bala"]) == "Bala, E."
    assert program(["Myron Lampros"]) == "Lampros, M."


def test_normalize_phone_number():
    examples = [
        Example("425-829-5512", "425-829-5512"),
        Example("(425) 829 5512", "425-829-5512"),
    ]
    program = learn_program(examples)
    assert program("425 233 1234") == "425-233-1234"
    assert program("(425) 777 3333") == "425-777-3333"


def test_merge_names():
    examples = [
        Example(["Kettil", "Hansson"], "Hansson, Kettil"),
        Example(["Greta", "Hermansson"]),
    ]
    program = learn_program(examples)
    assert program(["Etelka", "Bala"]) == "Bala, Etelka"
    assert program(["Myron", "Lampros"]) == "Lampros, Myron"


def test_top_10_normalize_phone_number():
    examples = [Example("(425) 829 5512", "425-829-5512")]
    programs = learn_programs(examples, k=10)
    assert len(programs) >= 10
    assert programs[0]("425 233 1234") == "425-233-1234"


def test_make_examples():
    examples1 = make_examples(
        [
            ["Greta", "Hermansson", "Hermansson, G."],
            ["Kettil", "Hansson", "Hansson, K."],
        ]
    )
    assert len(examples1) == 2
    assert examples1[0].has_output()
    assert examples1[1].has_output()

    examples2 = make_examples(
        [
            ["Greta", "Hermansson", "Hermansson, G."],
            ["Kettil", "Hansson"],
        ]
    )
    assert len(examples2) == 2
    assert examples2[0].has_output()
    assert not examples2[1].has_output()


def test_flashfill():
    table = [
        ["Greta", "Hermansson", "Hermansson, G."],
        ["Kettil", "Hansson", "Hansson, K."],
        ["Myron", "Lampros"],
    ]
    flashfill(table)
    assert table[2][2] == "Lampros, M."


if __name__ == "__main__":
    test_format_name()
    test_normalize_phone_number()
    test_merge_names()
    test_top_10_normalize_phone_number()
    test_make_examples()
    test_flashfill()
