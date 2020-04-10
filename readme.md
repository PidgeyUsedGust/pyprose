# pyprose

Python wrapper around the Microsoft PROSE framework. This package only provides easy wrappers around compiled DSLs, not the option for creating new DSLs.

## installation

### requirements

The main requirements are pythonnet and PROSE. Below are instructions to get these up and running. 

#### pythonnet

This package depends on pythonnet for calling PROSE. Here are some instructions for installing it on different operating systems.

#### PROSE

This package requires the [Microsoft.ProgramSynthesis](https://www.nuget.org/packages/Microsoft.ProgramSynthesis/) package. By default, pyprose will look in the [global package cache](https://docs.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders) and should find the appropriate files if it was installed in any project. This can be done by either adding it to any project in Visual Studio, or by using `nuget.exe` and downloading it to any directory.

You can check whether (and which) dependencies are correctly detected by running the following command.

```console
python -m pyprose.dll check
```

## how to use

The goal of pyprose is to make it as easy as possible to use the powerful PROSE system.

### constraints

Most constraints have been added as arguments in their respective `learn_program` functions.

As an example, take `Split.Text`. Many constraints can be added in order to aid the splitting learner. The following is a simplified excerpt from the `Split.Text` sample project.

```C#
splitSession = new SplitSession();
var inputs = new List<StringRegion>
{
    SplitSession.CreateStringRegion("PE5 Leonard"),
    SplitSession.CreateStringRegion("U109 Adam"),
    SplitSession.CreateStringRegion("R342 Carrie")
};
splitSession.Inputs.Add(inputs);
splitSession.Constraints.Add(new IncludeDelimitersInOutput(false));
splitSession.Constraints.Add(new NthExampleConstraint(inputs[0].Value, 0, "PE5"));
splitSession.Constraints.Add(new NthExampleConstraint(inputs[0].Value, 1, "Leonard"));
splitSession.Constraints.Add(new NthExampleConstraint(inputs[1].Value, 0, "U109"));
splitSession.Constraints.Add(new NthExampleConstraint(inputs[1].Value, 1, "Adam"));
SplitProgram programFromExamples = splitSession.Learn();
```

In pyprose, the same can be achieved as follows.

```python
from pyprose.split.text import learn_program

program = learn_program(["PE5 Leonard", "U109 Adam", "R342 Carrie"],
                        include_delimiters_in_output=False,
                        nth_examples={"PE5 Leonard": {0: "PE5", 1: "Leonard"},
                                      "U109 Adam": {0: "U109", 1: "Adam"}})
```

All supported constraint arguments should be properly documented.

## progress

Progress on implementation of DSLs.

- [ ] Transformation.Text
- [ ] Split.Text
