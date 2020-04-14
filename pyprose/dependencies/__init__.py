"""Loading DLL files.

Because the `clr.AddReference` method required all dependencies
to be in the same directory, they are copied over from nuget's
global cache.

"""

import re
import sys
from pathlib import Path
from shutil import copyfile
from distutils.version import LooseVersion
from typing import Optional
import clr
import pyprose

sys.path.append(str(Path(__file__).parent))


def load(dependencies):
    # ensure all dependencies are loaded
    for dependency in dependencies:
        load_dll(dependency)
        for subdependency in dependencies[dependency]:
            load_dll(subdependency)
    # add references
    for dependency in dependencies:
        clr.AddReference(dependency)


def load_dll(reference: str):
    """Ensure the specified reference can be imported.
    
    Args:
        name (str): Name of the reference to be imported.

    """
    dll_file = Path(__file__).parent / (reference + ".dll")
    if not dll_file.is_file():
        dll = _find_dll_global(reference)
        copyfile(dll, dll_file)


def _find_dll_global(dll: str) -> Optional[str]:
    """Find DLL in global NuGet package cache.
    
    Args:
        dll (str): Name of the DLL file that is needed.

    Returns:
        Tuple of (path, version) where path is the folder
        that contains the DLL and version is its version
        as a string.
    
    """

    folder = Path.home() / ".nuget" / "packages" / dll.lower()
    if folder.exists():
        versions = list()
        for version in folder.glob("*.*.*"):
            if version.is_dir():
                versions.append(version)
        max_version = max(versions, key=lambda v: LooseVersion(v.name))
        if (max_version / "lib" / "net45").is_dir():
            dll_folder = max_version / "lib" / "net45"
        else:
            dll_folder = next((max_version / "lib").glob("*net45*"))
        return next(dll_folder.glob(dll + ".dll"), None)


# def _find_dll_local(dll):
#     """Find DLL in local installed path."""
#     name = Path(dll)
#     if _nuget_local.exists():
#         versions = list()
#         for version in _nuget_local.glob("*{}*".format(name)):
#             version_number = re.findall(r"(?:\d+\.[\d+\.]*\d+)", str(version))[0]
#             versions.append((version / "lib" / "net45", version_number))
#         if len(versions) > 0:
#             return max(versions, key=lambda v: LooseVersion(v[1]))
#     return (None, None)