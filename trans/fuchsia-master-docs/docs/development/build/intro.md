 
# A Short Introduction to GN  GN简介 

This is a quick introduction to GN's terms and way of thinking.  This should be sufficient background to get your bearings in GN and how it's used in Zircon.GN (and the Zircon build) are more complicated than the below will discuss, butthe average developer will not need to understand most of it on a deeper level. 这是GN术语和思维方式的快速介绍。这应该有足够的背景知识来使您了解GN，以及如何在Zircon.GN（以及Zircon版本）中使用它，比下面的讨论要复杂得多，但是一般的开发人员无需更深入地了解其中的大部分内容。

The GN documentation pages [QuickStart] and [Language] give more detailed background on GN, and [Reference] has the full language documentation.  Usethe `gn help` command to print out the reference interactively for individualtopics.  [Ninja] has its own documentation as well. GN文档页面[QuickStart]和[Language]提供了有关GN的更多详细背景信息，并且[Reference]具有完整的语言文档。使用gn help命令以交互方式打印出各个主题的参考。 [忍者]也有自己的文档。

In the Zircon checkout after running `scripts/download-prebuilt`, `scripts/gn` and `scripts/ninja` provide access to the prebuilt binaries. 在运行`scripts / download-prebuilt`之后的Zircon签出中，`scripts / gn`和`scripts / ninja`提供对预编译二进制文件的访问。

[Ninja]: https://ninja-build.org/manual.html [QuickStart]: https://gn.googlesource.com/gn/+/master/docs/quick_start.md[Language]: https://gn.googlesource.com/gn/+/master/docs/language.md[Reference]: https://gn.googlesource.com/gn/+/master/docs/reference.md [忍者]：https://ninja-build.org/manual.html [快速入门]：https://gn.googlesource.com/gn/+/master/docs/quick_start.md [语言]：https：// gn.googlesource.com/gn / + / master / docs / language.md [参考]：https://gn.googlesource.com/gn/+/master/docs/reference.md

 
## Two-phase operation: `gn` and `ninja`  两阶段操作：`gn`和`ninja` 

Unlike `make`, `gn` is only ever half the story.  It's in the name: GN stands for Generate [Ninja].  There's a division of responsibilities between thetools that corresponds to a separation of running the build into two steps: 与`make`不同，`gn`只是故事的一半。它的名称是：GN代表Generate [Ninja]。工具之间存在责任划分，对应于将构建分为两个步骤运行：

 
1. `gn gen` takes all the configuration choices and makes all the decisions. All it really does is generate the `.ninja` files in the build directory.This step only has to be done by hand when you change the configuration orcompletely nuke the build directory.  In general, it only needs to be donewhen the GN files change, and in incremental builds it happensautomatically if the GN files or configuration change. 1.`gn gen`接受所有配置选择并做出所有决定。它真正要做的只是在构建目录中生成`.ninja`文件。仅当您更改配置或完全取消构建目录时，才需要手动执行此步骤。通常，仅当GN文件发生更改时才需要执行此操作，而在增量构建中，如果GN文件或配置发生更改，则它会自动发生。

 
1. `ninja` runs the commands to compile and link, etc.  It handles incremental builds and parallelism.  This is the step you do every time you've changeda source file, like running `make`.  GN automatically emits rules tore-generate the Ninja files by running gn gen again when a relevant`BUILD.gn` file (or some other relevant files) has changed, so for mostchanges after the first time you've built, `ninja` does it all. 1.`ninja`运行命令进行编译和链接等。它处理增量构建和并行性。这是您每次更改源文件时都执行的步骤，例如运行`make`。当相关的BUILD.gn文件（或其他一些相关的文件）发生更改时，GN会自动发出规则，通过再次运行gn gen来重新生成Ninja文件，因此对于大多数更改，在您首次构建后，ninja会执行这一切。

Ninja is very stupid compared to something like GNU `make`.  It just compares times and runs commands and its input files are written by machines, nothumans.  However, it builds in some useful things that we bend over backwardto accomplish in `make`: 与GNU make这样的东西相比，Ninja非常愚蠢。它只是比较时间并运行命令，其输入文件是由机器而不是人类编写的。但是，它建立了一些有用的东西，我们将向后弯腰以在make中完成：

 
 - Rebuild each file when the command line changes.  Command lines will only really change when GN runs again.  But after that, Ninja is smart aboutincremental builds re-doing commands for files that have changed and notre-running commands that haven't changed. -当命令行更改时，重建每个文件。仅当GN重新运行时，命令行才会真正改变。但是在那之后，Ninja很聪明，可以为已更改的文件执行重新构建命令，而不重新运行未更改的命令。
 - Handle compiler-generated dependency files.  Ninja knows about the makefile subset that compilers emit in `.d` files and consumes them directly whendirected to by GN. -处理编译器生成的依赖文件。 Ninja知道编译器会在.d文件中生成的makefile子集，并在被GN定向时直接使用它们。
 - Run with `-j$(getconf _NPROCESSORS_ONLN)` by default.  You can pass `-j1` to serialize or `-j1024` when using Goma, but out of the box it does theparallelism you usually want. -默认情况下使用-j $（getconf _NPROCESSORS_ONLN）运行。您可以在使用Goma时传递`-j1`进行序列化，也可以传递`-j1024`，但是开箱即用，它可以实现您通常想要的并行度。
 - Prevent interleaved `stdout`/`stderr` output from parallel jobs.  Ninja buffers the output so that error messages don't get garbled by spew frommultiple processes. -防止并行作业输出交错的`stdout` /`stderr`。 Ninja会对输出进行缓冲，以使错误消息不会因来自多个进程的溢出而乱码。
 - Support terse/verbose command output.  By default, Ninja emits short `Kbuild`-style messages for each command it runs, in a wordy-progress-meterstyle.  The -v switch is like V=1 in `Kbuild`, to show each actual command. -支持简洁/详细命令输出。默认情况下，Ninja会以其冗长的进度表样式为运行的每个命令发出简短的“ Kbuild”样式消息。 -v开关类似于`Kbuild`中的V = 1，以显示每个实际命令。

GN was developed as part of the Chromium project to replace older build systems.  Fuchsia inherited it from them, and it is now used across the tree asthe primary build system. GN是Chromium项目的一部分，目的是取代旧的构建系统。紫红色是从它们那里继承而来的，现在它在树上被用作主要的构建系统。

 
## Build directories and `args.gn`  建立目录和`args.gn` 

Ninja always runs in the build directory.  All commands Ninja runs are run from the root of the build directory.  The common thing is `ninja -C build-dir`. Ninja始终在构建目录中运行。 Ninja运行的所有命令均从构建目录的根目录运行。常见的是`ninja -C build-dir`。

Neither GN nor Ninja cares what build directory you use.  It's common practice to use a subdirectory of the source directory, and since file paths areusually rebased to be relative to the build directory, the file names given tothe compiler will have a whole lot of `../` in them if you put your builddirectory elsewhere; but it should work.  It's long been common practice inChromium (predating GN itself) to use `out/_something_` in the sourcedirectory, and Fuchsia inherited that default.  But nothing cares what builddirectory names you choose, though the `build-*` subdirectory name pattern isin the `.gitignore` for Zircon and the `out` subdirectory is in the top-level`.gitignore` file for Fuchsia. GN和Ninja都不关心您使用的构建目录。通常使用源目录的子目录，并且由于通常将文件路径重新建立为相对于构建目录的相对路径，因此，如果您将构建目录放入编译器，则赋予编译器的文件名中会包含很多`../`。别处;但应该可以。在Chromium（早于GN本身）中，在源目录中使用`out / _something_`一直是很常见的做法，而Fuchsia继承了该默认值。但是没有什么在乎您选择什么构建目录名称，尽管Zircon的.buildignore子目录位于build- *子目录中，而倒挂金钟的out子目录位于顶级.gitignore文件中。

The basic command is `gn gen build-dir`.  This creates `build-dir/` if needed, and populates it with Ninja files for the current configuration.  If`build-dir/args.gn` exists, then `gn gen` will read that file to set GN buildarguments (see below).  `args.gn` is a file in GN syntax that can assign valuesto GN build arguments that override any hardcoded defaults.  This means justrepeating `gn gen build-dir` preserves what you did last time. 基本命令是“ gn gen build-dir”。这会在需要时创建`build-dir /`，并使用当前配置的Ninja文件进行填充。如果存在build-dir / args.gn，那么gn gen将读取该文件以设置GN buildarguments（请参见下文）。 args.gn是GN语法中的文件，可以为GN构建参数分配值，这些参数会覆盖所有硬编码的默认值。这意味着只需重复执行gn gen build-dir即可保留您上次执行的操作。

You can also add `--args=...` to gn gen or use the `gn args` command to configure your build arguments.  The` gn args` command gives you a way to runyour $EDITOR on the `args.gn` file, and upon exiting the editor the commandwill re-run `gn gen` for you with the new arguments.  You can also just edit`args.gn `any time, and the next Ninja run will re-generate the build files. 您还可以在gn gen上添加`--args = ...`或使用`gn args`命令来配置构建参数。 gn args命令为您提供了一种在args.gn文件上运行$ EDITOR的方法，退出编辑器后，该命令将使用新参数为您重新运行gn gen。您也可以随时编辑args.gn，下一次Ninja运行将重新生成构建文件。

 
## GN syntax and formatting  GN语法和格式 

GN syntax is whitespace-insensitive. `x=1 y=2` is the same as:  GN语法对空格不敏感。 x = 1 y = 2与以下内容相同：

```gn
x = 1
y = 2
```
 

However, there is *one true indentation and formatting style* for GN code.  The `gn format` command reformats syntactically valid GN code into the canonicalstyle.  There is editor syntax support for Emacs and Vim.  Canonical formattingwill be enforced by Tricium and mass reformatting will be done.  If you don'tlike the formatting, file bugs or make a change in upstream GN and if it landswe'll mass reformat everyone to conform to the new one truth. 但是，GN代码有*一种真正的缩进和格式样式*。 gn格式命令将语法上有效的GN代码重新格式化为规范样式。 Emacs和Vim具有编辑器语法支持。标准格式将由Tricium强制执行，并且将进行大量重新格式化。如果您不喜欢这种格式，请提交文件错误或对上游GN进行更改，如果它不适合我们，我们将重新格式化所有人以符合新的真理。

 
## Source paths and GN labels  源路径和GN标签 

GN uses POSIX-style paths (always in represented as strings) both for files and to refer to GN-defined entities.  Paths can be relative, which means relativeto the directory containing the `BUILD.gn` file where the path string appears.They can also be "source-absolute", meaning relative to the root of the sourcetree.  Source-absolute paths begin with `//` in GN. GN使用POSIX样式的路径（始终以字符串表示）既用于文件又用于引用GN定义的实体。路径可以是相对的，即相对于包含路径字符串所在目录的“ BUILD.gn”文件的目录。它们也可以是“ source-absolute”，即相对于sourcetree的根目录。绝对源路径在GN中以`//`开头。

**TODO(BLD-353): _This is a hold-over from the "layer cake" design and will probably change soon:_** Generically, an absolute path will look like`//path/to/dir`.  However, in order to maintain both the standalone Zirconbuild and the integrated Fuchsia build, *all absolute paths in Zircon will looklike `$zx/path/to/dir`*.  This allows us to use expand `$zx` to `//` in thecase of the standalone build and `//zircon/` in the case of the integratedbuild. ** TODO（BLD-353）：_这是“分层蛋糕”设计的保留，可能很快就会改变：_ **通常，绝对路径看起来像是“ // path / to / dir”。但是，为了同时维护独立的Zirconbuild和集成的Fuchsia版本，* Zircon中的所有绝对路径都将类似于$ zx / path / to / dir` *。对于独立构建，这使我们可以使用将`$ zx`扩展为`//`，而对于集成构建，则可以使用`// zircon /。

When source paths are eventually used in commands, they are translated into OS-appropriate paths that are either absolute or relative to the builddirectory (where commands run). 当最终在命令中使用源路径时，它们会转换为与操作系统相对应的路径，这些路径是绝对路径或相对于builddirectory的路径（运行命令的位置）。

Predefined variables are used in source path contexts to locate parts of the build directory: 在源路径上下文中使用预定义的变量来查找构建目录的各个部分：

 
 - `$root_build_dir` is the build directory itself  -`$ root_build_dir`是构建目录本身
 - `$root_out_dir` is the subdirectory for the current toolchain (see below)  -`$ root_out_dir`是当前工具链的子目录（见下文）
   - This is where all "top-level" targets go.  In many GN builds, all executables and libraries go here.  But it is not used directly veryoften in the Zircon build. -这是所有“顶级”目标的去向。在许多GN版本中，所有可执行文件和库都在这里。但是它在Zircon版本中并不经常直接使用。
 - `$target_out_dir` is the subdirectory of `$root_out_dir` for files built by targets in the current `BUILD.gn` file.  This is where the object files go.In the Zircon build, this is where executables and libraries go as well. -`$ target_out_dir`是$ root_out_dir`的子目录，用于由目标在当前`BUILD.gn`文件中构建的文件。这是目标文件所在的位置。在Zircon构建中，这也是可执行文件和库所在的位置。
 - `$target_gen_dir` is a corresponding place recommended to put generated code  -`$ target_gen_dir`是建议放置生成代码的对应位置
 - `$root_gen_dir` is a place for generated code needed outside this subdirectory -$ root_gen_dir是该子目录外部所需的生成代码的地方

GN labels are how we refer to things defined in a `BUILD.gn` file.  They are based on source paths, and always appear inside GN strings.  The full syntax ofa GN label is `"dir:name"` where the `dir` part is a source path that names theparticular `BUILD.gn` file.  The `name` refers to a target defined in that filewith `target_type("name") { ... }`.  As a shorthand, you can define a targetwith the same name as its directory.  The label `"//path/to/dir"` with no `:`part is a shorthand for `"//path/to/dir:dir"`.  This is the most common case. GN标签是我们引用“ BUILD.gn”文件中定义的内容的方式。它们基于源路径，并且始终出现在GN字符串中。 GN标签的完整语法为“ dir：name”，其中dir部分是命名特定BUILD.gn文件的源路径。 “名称”指的是在该文件中使用“ target_type（“ name”）{...}`”定义的目标。简而言之，您可以定义一个与目录相同名称的目标。没有“：”部分的标签“” // path / to / dir”是“” // path / to / dir：dir”的简写。这是最常见的情况。

 
## Dependency graph and `BUILD.gn` files  依赖图和`BUILD.gn`文件 

Everything in GN is rooted in the dependency graph.  There is one root `BUILD.gn` file.  The only way other `BUILD.gn` files are even read is if thereis a dependency on a label in that directory. GN中的所有内容都植根于依赖关系图中。有一个根目录“ BUILD.gn”。甚至读取其他`BUILD.gn`文件的唯一方法是，如果该目录中的标签存在依赖性。

There are no wildcards.  Every target must be named as a dependency of some other target to get built.  You can give individual targets on the `ninja`command line to explicitly get them built.  Otherwise they must be in the graphfrom the `//:default` target (named `default` in the root `BUILD.gn` file). 没有通配符。必须将每个目标命名为要构建的其他目标的依赖项。您可以在`ninja`命令行上给各个目标明确地构建它们。否则，它们必须在//：default目标（在根PUILD.gn文件中命名为default）的图形中。

There is a generic meta-target type called `group()` that doesn't correspond to a file produced by the build but is rather a way to structure your dependencygraph nicely.  Top-level targets like `default` are usually groups.  You canhave a group for all the drivers for a piece of hardware, a group for all thebinaries in a use case, etc. 有一个称为“ group（）”的通用元目标类型，它与构建生成的文件不对应，而是一种很好地构造依赖关系图的方式。诸如“ default”之类的顶级目标通常是组。您可以为一个硬件的所有驱动程序提供一个组，为一个用例为所有二进制文件提供一个组，等等。

When some code uses something at runtime (a data file, another executable, etc.)  but doesn't use it as a direct input at build time, that file belongs inthe `data_deps` list of target that uses it.  In the Zircon build, that will beenough to get the thing into the BOOTFS image at its appointed place. 当某些代码在运行时使用某些内容（数据文件，另一个可执行文件等），但在构建时未将其用作直接输入时，该文件属于使用该文件的目标的“ data_deps”列表。在Zircon构建中，将其放入指定位置的BOOTFS映像中已经很困难了。

Targets can also be labeled with `testonly = true` to indicate that the target contains tests. GN prevents targets that are not `testonly` from depending ontargets that are, allowing for some level of control over where test binariesend up. 目标也可以标记为“ testonly = true”，以指示目标包含测试。 GN防止非testonly目标依赖于目标，从而可以对测试二进制文件的最终位置进行某种程度的控制。

The whole Zircon build is driven from one or more `zbi()` targets.  This will make a ZBI by building and using the ZBI host tool. Targets can be placed inthis image by existing within its dependency graph, and so you can give itdependencies on the kernel and any drivers or executables you want in theimage. 整个Zircon构建都是由一个或多个`zbi（）`目标驱动的。这将通过构建和使用ZBI宿主工具来创建ZBI。目标可以通过存在于其映像中的依赖关系图中而放置在该映像中，因此您可以使其依赖于内核以及映像中所需的任何驱动程序或可执行文件。

Note that getting targets defined in Ninja files is at the granularity of `BUILD.gn` files, though the dependency graph from default or any other targetis at the granularity of an individual target.  So having some target in the`BUILD.gn` file in the graph from default makes all targets in that file (andtoolchain, see below) available as targets on the Ninja command line eventhough they are not built by default. 请注意，获得忍者文件中定义的目标的粒度为`BUILD.gn`文件，尽管来自默认目标或任何其他目标的依赖关系图为单个目标的粒度。因此，默认情况下，在图形的BUILD.gn文件中具有某些目标时，即使默认情况下未构建目标，该文件中的所有目标（以及工具链，请参见下文）也可以用作Ninja命令行上的目标。

 
## More Advanced Concepts  更高级的概念 

 
### GN expression language and GN scopes  GN表达语言和GN范围 

GN is a simple, dynamically-typed, imperative language whose sole purpose at the end of the day is to produce declarative Ninja rules.  Everything revolvesaround scopes, which is both the lexical binding construct of the language anda data type. GN是一种简单的动态类型的命令式语言，其最终目的只是产生声明性的Ninja规则。一切都围绕作用域，这既是语言的词汇绑定构造，也是数据类型。

GN values can take any of several types:  GN值可以采用以下几种类型中的任何一种：

 
 - Boolean, either `true` or `false`  -布尔值，“ true”或“ false”
 - Integer, signed with normal decimal syntax; not used much  -整数，使用常规十进制语法签名；用的不多
 - String, always in "double-quotes" (note below about `$` expansion)  -字符串，始终以“双引号”引起（以下有关$扩展的注释）
 - Scope, in curly braces:  `{ ... }`; see below.  -范围，用大括号括起来：`{...}`;见下文。
 - List of values, in square brackets: `[ 1, true, "foo", { x=1 y=2 } ]` is a list of four elements. -值列表，用方括号括起来：`[1，true，“ foo”，{x = 1 y = 2}]`是四个元素的列表。

Values are dynamically-typed and there is no kind of implicit type coercion, but there is never type-checking as such.  Values of different types nevercompare as equal, but it's not an error to compare them. 值是动态类型的，没有任何隐式类型强制，但是从来没有这样的类型检查。不同类型的值永远不会相等，但是比较它们不是错误。

String literals expand simple `$var` or `${var}` expressions inside the double-quotes.  This is an immediate expansion: `x${var}y` is the same as `x +var + y` when var is a string.  In this way, any value can be rendered as apretty-printed string. 字符串文字在双引号内扩展了简单的$ var或$ {var}表达式。这是一个立即扩展：当var是一个字符串时，x $ {var} y与x + var + y相同。这样，任何值都可以呈现为漂亮打印的字符串。

Identifiers made up of alphanumerics and underscores can populate a scope via assignment operators.  Imperative assignment with `=` and modification via `+=`are really all the GN language does (there are also some special ways to haveside effects like `print()`, used for debugging; and `write_file()`, usedsparingly). 由字母数字和下划线组成的标识符可以通过赋值运算符填充作用域。强制使用`=`进行赋值并通过`+ =`进行修改实际上是GN语言所做的（还有一些特殊的副作用，例如用于调试的`print（）`和用于单独使用的`write_file（）`）。 。

Each file is internally represented as a scope, and there is no global scope. Shared "globals" can be defined in a `.gni` file and imported where they areused (`import("//path/to/something.gni")`).  Each `.gni file is processed onceper toolchain (see below for information about toolchains), and the resultingscope is copied into the importing file scope. 每个文件在内部均表示为作用域，并且没有全局作用域。可以在.gni文件中定义共享的“全局变量”，并将其导入使用它们的位置（“ import（“ // path / to / something.gni”））。每个`.gni文件每个工具链都会处理一次（有关工具链的信息，请参阅下文），并将结果范围复制到导入文件作用域中。

Target declarations introduce a sub-scope:  目标声明引入了一个子范围：

```gn
foo = true
executable("target") {
  foo = 12
}
# Outside the target, foo == true
```
 

GN is very strict in diagnosing errors when a variable is defined but never used within a scope.  The scope inside a target acts like a keyword argumentlist for the target with checking that the argument names were spelledcorrectly.  The target-defining code can also use `assert()` to diagnose anerror if a required argument was omitted. 当定义了变量但从未在范围内使用变量时，GN在诊断错误时非常严格。目标内部的作用域就像目标的关键字参数列表一样，它检查参数名称是否拼写正确。如果省略了必需的参数，则目标定义代码也可以使用“ assert（）”来诊断错误。

A value can also be a scope.  Then it's acting like a struct when you use it: `value.member`.  But a scope is always a block of GN code that executes toyield its set of names and values: 值也可以是范围。然后，当您使用它时，它就像一个结构：value.member。但是，作用域始终是GN代码块，执行该代码块会产生其名称和值集：

```gn
foo = {
  x = global_tuning + 42
  If (some_global && other_thing == "foobar") {
    y = 2
  }
}
```
 

This always defines `foo.x` but only sometimes defines `foo.y`.  这总是定义`foo.x`，但有时只定义`foo.y`。

 
### GN toolchains  GN工具链 

GN has a concept called a "toolchain".  This will all be happening behind the scenes and Zircon hackers shouldn't need to deal with it directly, but it helpsto understand the mechanism. GN有一个称为“工具链”的概念。这一切都将在幕后发生，Zircon黑客不需要直接处理它，但是它有助于了解这种机制。

This is what encapsulates the compilers and default compilation switches.  It's also the only real way to get the same things compiled twice in differentways. In Zircon there will be several toolchains: 这就是封装编译器和默认编译开关的原因。这也是使相同的内容以不同的方式进行两次编译的唯一真实方法。在Zircon中，将有几个工具链：

 
 - Host  -主持人
 - Vanilla userland (compiled with default `-fPIE`)  -Vanilla用户区（与默认`-fPIE`一起编译）
 - Shared libraries in userland (compiled with `-fPIC`)  -用户区中的共享库（与-fPIC一起编译）
 - `userboot`  -`userboot`
 - Kernel  - 核心
 - Kernel physical-address mode for ARM64 (compiled with `-mstrict-align`)  -ARM64的内核物理地址模式（与`-mstrict-align`编译）
 - Multiboot for x86 (compiled with `-m32`)  -适用于x86的Multiboot（与`-m32`一起编译）
 - UEFI for Gigaboot  -Gigaboot的UEFI
 - Toolchains are also used in the ["variants" scheme](/docs/gen/zircon_build_arguments.md#variants) that is how we allow selectivelyenabling ASan or the like for parts of userland. -工具链也用于[“ variants”方案]（/ docs / gen / zircon_build_arguments.mdvariants）中，这是我们允许部分用户土地选择性启用ASan或类似功能的方式。

Each toolchain is identified by a GN label.  The full syntax for target labels is actually `//path/to/dir:name(//path/to/toolchain/label)`.  Usually thetoolchain is omitted and this is expanded to `label($current_toolchain)`,i.e. label references are usually within the same toolchain. 每个工具链均由GN标签标识。目标标签的完整语法实际上是`// path / to / dir：name（// path / to / toolchain / label）`。通常会省略工具链，并将其扩展为`label（$ current_toolchain）`，即。标签引用通常在同一工具链中。

