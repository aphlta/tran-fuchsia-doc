 
# Linter Interface  林特接口 

This document describes the command-line interface to the FIDL linter.  本文档介绍了FIDL linter的命令行界面。

For more information about FIDL's overall purpose, goals, and requirements, see [Overview](../intro/README.md). 有关FIDL总体目的，目标和要求的更多信息，请参见[概述]（../ intro / README.md）。

 
## Overview  总览 

The FIDL linter is a command line program that processes one or more FIDL files, and prints warnings about content that compiles (technically valid FIDL),but appears to violate rules from the [FIDL Style Rubric][fidl-style].Readability is important, and style is a component of that, but the FIDL Rubricalso defines rules that help ensure the FIDL API does not include things that areknown to hamper cross-language portability. FIDL linter是一个命令行程序，处理一个或多个FIDL文件，并打印有关已编译内容的警告（技术上有效的FIDL），但似乎违反了[FIDL Style Rubric] [fidl-style]的规则。可读性很重要，而样式是其中的一个组成部分，但FIDL Rubric还定义了规则，以确保FIDL API不包含已知会妨碍跨语言可移植性的内容。

 
## Use `fx lint`  使用`fx lint` 

Fuchsia includes the `fx lint` command that automatically selects and runs the appropriate code linter for each of a set of specified files. `fx lint` bundlesthe files with a `.fidl` extension, and passes all of them, together, to the FIDLlinter command `fidl-lint`. 紫红色包含“ fx lint”命令，该命令会自动为一组指定文件的每个文件选择并运行适当的代码文件。 fx lint将扩展名为.fidl的文件捆绑在一起，并将所有文件一起传递给FIDLlinter命令fidl-lint。

`fx lint` is the recommended way to invoke the FIDL linter, and ideally should be run before uploading new FIDL librarys or changes to existing FIDL. Without anyarguments, `fx lint` will run all available linters on all files in your mostrecent `git commit`. 建议使用fx lint调用FIDL linter，最好在上载新FIDL库或更改现有FIDL之前运行。没有任何争论，`fx lint`将在最近的`git commit`中的所有文件上运行所有可用的linter。

```sh
fx lint
```
 

To review other available options, run:  要查看其他可用选项，请运行：

```sh
fx lint --help
```
 

