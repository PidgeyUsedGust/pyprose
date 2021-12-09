import pyprose.dependencies


def test_find_dll_global():
    print(pyprose.dependencies._find_dll_global("microsoft.programsynthesis.transformation.text"))
    print(pyprose.dependencies._find_dll_global("transformation.text"))
    print(pyprose.dependencies._find_dll_global("transformation.nothing"))
    assert pyprose.dependencies._find_dll_global("transformation.nothing") == None


if __name__ == "__main__":

    test_find_dll_global()
