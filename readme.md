# pyprose

Python wrapper around the Microsoft PROSE framework. This package only provides easy wrappers around compiled DSLs, not the option for creating new DSLs.

## how to use

The goal of pyprose is to make it as easy as possible to use the powerful PROSE system.

### basic example

As a simple example, we show how to use `Transformation.Text`, which implements the FlashFill system for learning string  transformation programs (example taken from  [here](https://microsoft.github.io/prose/documentation/transformation-text/intro/)).

```python
from pyprose.transformation.text import learn_program, Example

p = learn_program([
    Example(["Greta", "Hermansson"], "Hermansson, G."),
    Example(["Kettil", "Hansson"], "Hansson, K.")
])

# or with implicit examples

p = learn_program([
    (["Greta", "Hermansson"], "Hermansson, G."),
    (["Kettil", "Hansson"], "Hansson, K.")
])
```

The learned program can be ran on new inputs—a list of two strings in this case—as `p(["Etelka", "Bala"])` which returns a new string `Bala, E.`.

### constraints

Most constraints have been added as arguments in their respective `learn_program` functions.

All supported constraint arguments should be properly documented.

### FlashProfile

The FlashProfile system is implemented as `Match.Text` and yields patterns instead of programs.

## installation

There are two main requirements.

* [`pythonnet`](http://pythonnet.github.io/), which requires Mono, is used for loading the compiled PROSE DLSs.
* The required PROSE binaries for a specific DSL. For example, Microsoft.ProgramSynthesis.Transformation.Text is required in order to use `pyprose.transformation.text` (FlashFill). By default, `pyprose` will look for these in the [global NuGet package cache](https://docs.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders) and copy them to its own directory as they are needed. Adding the DSL to any project through Visual Studio or downloading the package using `nuget.exe` should therefore be sufficient. Dependencies for all DLS can be verified using `python -m pyprose.dependencies`.

Installing these dependencies is not as trivial as it should be. As we want to make `pyprose` as accessible as possible, detailed instructions that we have verified to work on different operating systems are therefore given below. If anyone chooses a different path for installing either requirements or is able to successfully follow these instructions on untested OS versions, please let me know in order to update this readme.

### macOS

Tested on Catalina (10.15.4).

#### pythonnet

* Install mono through homebrew
  ```command
  brew install pkg-config
  brew install glib --universal
  brew install mono
  ```
* Set  `PKG_CONFIG_PATH` and `DYLD_LIBRARY_PATH` accordingly. 
  ```command
  export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Versions/Current/lib/pkgconfig
  export DYLD_LIBRARY_PATH=/Library/Frameworks/Mono.framework/Versions/Current/lib
  ```
* Install `pythonnet` from GitHub.
  ```command
  USE_OSX_FRAMEWORKS=0 ARCHFLAGS="-arch x86_64" pip install git+https://github.com/pythonnet/pythonnet
  ```

#### PROSE

There are a few options.

* Install [Visual Studio](https://visualstudio.microsoft.com/vs/mac/) and create a new project or download the PROSE sample project. Under *Project > Manage NuGet Packages* search for Microsoft.ProgramSynthesis and install it.
* Install NuGet through homebrew (`brew install nuget`) and install the Microsoft.ProgramSynthesis package to any directory.
  ```command
  nuget install Microsoft.ProgramSynthesis -Outputdir <anything>
  ```

### Linux

Tested on Ubuntu 19.10.

We discovered that Mono 5.20 is the only version of Mono that works for both installing `pythonnet` and using `nuget.exe`.

#### pythonnet

* Install Mono 5.20 as per [these instructions](https://www.mono-project.com/download/stable/#download-lin) but with the correct version in the third step.
  ```command
  sudo apt install gnupg ca-certificates
  sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
  echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic/snapshots/5.20 main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
  sudo apt update
  ```
  For other Linux distributions, find the correct version [here](http://download.mono-project.com/repo/).
* Install pythonnet.
  ```command
  pip install pythonnet
  ```

#### PROSE

1. Download the lastext `nuget.exe` from [this link](https://dist.nuget.org/win-x86-commandline/latest/nuget.exe).
   ```command
   wget https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
   ```
2. Install the package to any directory.
   ```command
   mono nuget.exe install Microsoft.ProgramSynthesis -OutputDirectory <anywhere>
   ```

### Windows

#### pythonnet

#### PROSE

## progress

Progress on implementation of DSLs.

- [x] Transformation.Text (FlashFill)
- [x] Match.Text (FlashProfile)
- [ ] Split.Text **(in progress)**
