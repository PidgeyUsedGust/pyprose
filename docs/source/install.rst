Installation
============

There are two main requirements in order to use ``pyprose``.

* Compiled PROSE assemblies. These are not shipped with ``pyprose`` but are easily
  obtained by installing the `Microsoft.ProgramSynthesis`_ package from NuGet using
  `Visual Studio`_ or the `NuGet CLI`_.
* `Python for .NET`_ (``pythonnet``) is used to load and run code from these assemblies.

These are unfortunately not trivial to install on all operating systems. In order to
make the process as seamless as possible, we provide detailed instructions that are
verified to work on specific operating systems.

We have found that Python 3.7 works for all dependencies and can be easily installed
using `pyenv`_.

.. _Microsoft.ProgramSynthesis: https://www.nuget.org/packages/Microsoft.ProgramSynthesis/
.. _Visual Studio: https://visualstudio.microsoft.com/
.. _NuGet CLI: https://docs.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli
.. _Python for .NET: http://pythonnet.github.io/
.. _pyenv: https://github.com/pyenv/pyenv

.. _install-macos:

macOS
-----

Tested on Catalina (10.15.4) under Python 3.7 installed though `pyenv`_.

.. _macospythonnet:

pythonnet
~~~~~~~~~

Install `Mono <https://www.mono-project.com/download/stable/>`_ and update the following
environment variables::

  export PATH=$PATH:/Library/Frameworks/Mono.framework/Versions/Current/bin
  export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Versions/Current/lib/pkgconfig

Install ``pycparser`` and ``pythonnet``::

  pip install pycparser
  pip install pythonnet

.. _macosprose:

PROSE
~~~~~
There are a few options.

* Install `Visual Studio`_ and create a new project or download the PROSE sample project. Under ``Project > Manage NuGet`` Packages search for ``Microsoft.ProgramSynthesis`` and install it.
* Mono should have installed the ``nuget`` command, which allows installing packages from the command line.::
      
      nuget install Microsoft.ProgramSynthesis -Outputdir <anything>

Linux
-----

Tested on Ubuntu 19.10.

We discovered that Mono 5.20 is the only version of Mono that works for both installing ``pythonnet`` and using ``nuget.exe``.

.. _linuxpythonnet:

pythonnet
~~~~~~~~~

* Install Mono 5.20 as per `these instructions <https://www.mono-project.com/download/stable/#download-lin>`_ but with the correct version in the third step::

    sudo apt install gnupg ca-certificates
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic/snapshots/5.20 main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    sudo apt update
    sudo apt install mono-complete 

For other Linux distributions, find the correct version `here <http://download.mono-project.com/repo/>`_.

* Install ``pythonnet`` dependencies::

    sudo apt-get install clang
    sudo apt-get install libglib2.0-dev
    sudo apt-get install python3-dev

* Install ``pythonnet``::

    pip install pycparser
    pip install pythonnet
  
.. _linuxprose:

PROSE
~~~~~

Download the latest ``nuget.exe``::

    wget https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
  
Run it with ``mono`` to install the package to any directory::

    mono nuget.exe install Microsoft.ProgramSynthesis -OutputDirectory <anywhere>

.. _install-windows:

Windows
-------

Tested on Windows 10.

.. _windowspythonnet:

pythonnet
~~~~~~~~~

Install through ``pip``::

    pip install pycparser
    pip install pythonnet

.. _windowsprose:

PROSE
~~~~~

There are two options.

* Install `Visual Studio`_ and create a new project or download the PROSE sample project. Under ``Project > Manage NuGet Packages`` search for *Microsoft.ProgramSynthesis* and install it.
* Download `nuget.exe <https://dist.nuget.org/win-x86-commandline/latest/nuget.exe>`_ and add it to PATH or move it to the current directory. Install the package to any directory::
      
      nuget.exe install Microsoft.ProgramSynthesis -Outputdir <anything>
