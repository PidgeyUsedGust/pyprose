import pyprose


if __name__ == "__main__":

    import pkgutil
    import pyprose.dll

    # get all dependencies
    dependencies = set()
    for importer, modname, is_pkg in pkgutil.walk_packages(
        pyprose.__path__, pyprose.__name__ + "."
    ):
        if not is_pkg:
            module = importer.find_module(modname).load_module(modname)
            if hasattr(module, "dependencies"):
                new_dependencies = getattr(module, "dependencies")
                for new_dependency in new_dependencies:
                    dependencies.add(new_dependency)
                    dependencies.update(new_dependencies[new_dependency])

    print("> Found {} dependencies. Trying to find them.".format(len(dependencies)))
    for dependency in dependencies:
        pyprose.dll.load_dll(dependency)
