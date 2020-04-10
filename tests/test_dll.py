import pyprose


def test_find_dll_global():
    pyprose._find_dll_global("microsoft.programsynthesis.transformation.text")
    pyprose._find_dll_global("transformation.text")
    assert pyprose._find_dll_global("transformation.nothing") == (None, None)

def test_find_dll_local():
    pyprose._find_dll_local("Microsoft.ProgramSynthesis.Transformation.Text")
    pyprose._find_dll_local("Transformation.Text")
    assert pyprose._find_dll_local("Transformation.Nothing") == (None, None)

def test_find_dll():
    pass


if __name__ == "__main__":

    test_find_dll_global()
    test_find_dll_local()
    test_find_dll()
