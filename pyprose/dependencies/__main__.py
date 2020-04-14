import pyprose


if __name__ == "__main__":

    import pkgutil
    import pyprose.dependencies

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
    found = list()
    for dependency in dependencies:
        dll = pyprose.dependencies._find_dll_global(dependency)
        if dll is not None:
            found.append(dll)
    print("> Found {} in the global package cache.".format(len(found)))
