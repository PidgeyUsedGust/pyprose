from pyprose.transformation.text import learn_program, learn_programs, Example


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
    examples = [Example(["Kettil", "Hansson"], "Hansson, Kettil")]
    inputs = [["Greta", "Hermansson"]]
    program = learn_program(examples, additional_input=inputs)
    assert program(["Etelka", "Bala"]) == "Bala, Etelka"
    assert program(["Myron", "Lampros"]) == "Lampros, Myron"


def test_top_10_normalize_phone_number():
    examples = [Example("(425) 829 5512", "425-829-5512")]
    programs = learn_programs(examples, k=10)
    assert len(programs) >= 10
    assert programs[0]("425 233 1234") == "425-233-1234"


if __name__ == "__main__":
    test_format_name()
    test_normalize_phone_number()
    test_merge_names()
    test_top_10_normalize_phone_number()
