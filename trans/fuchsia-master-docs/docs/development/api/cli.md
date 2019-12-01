 
# Command-line Tools Rubric  命令行工具专栏 

 

 
## Overview  总览 

This document is for command line interface (CLI) tools. Graphical User Interfaces (GUI) are out of scope. 本文档适用于命令行界面（CLI）工具。图形用户界面（GUI）超出范围。

When developing tools for Fuchsia there are specific features and styles that will be used to create consistency. This document walks through thoserequirements. 开发用于紫红色的工具时，将使用特定的功能和样式来创建一致性。本文档涵盖了这些要求。

The goal is to maintain a uniform fit and finish for Fuchsia developer tools so that developers can know what to expect. They can most easily see how toaccomplish common tasks and there is a well lit path to discover rarer usedtools. 目标是为紫红色开发人员工具保持统一的贴合度和完成度，以便开发人员可以知道期望什么。他们最容易看到如何完成常见任务，并且有一条通明的路发现稀有的二手工具。

 

 
## Guide  指南 

The experience developers have writing software for Fuchsia will impact their general feelings toward writing for the platform and our tools are a significantpart of that experience. Providing tools that are inconsistent (with oneanother) creates a poor developer experience. 开发人员为Fuchsia编写软件的经验将影响他们对平台写作的总体感觉，而我们的工具是该经验的重要组成部分。提供不一致的工具（彼此）会给开发人员带来糟糕的体验。

This guide provides a rubric that Fuchsia tools must follow.  本指南提供了紫红色工具必须遵循的规则。

> **SDK** >> Some sections have an "SDK" call-out, like this one. These detail specific> rules that apply to tools included with the SDK distribution. > ** SDK ** >>某些部分带有“ SDK”标注，例如这一部分。这些适用于SDK发行版中包含的工具的特定于规则的详细规则。

 
## Considerations  注意事项 

Before embarking on the creation of a new tool, consider these factors to determine if the tool is a good fit for Fuchsia or the Fuchsia SDK. 在开始创建新工具之前，请考虑以下因素，以确定该工具是否适合Fuchsia或Fuchsia SDK。

> **SDK** >> SDK tools are specific to Fuchsia in some way. Generic tools or tools that are> widely available should not be part of Fuchsia and will not be included in the> Fuchsia SDK. For example, a tool that verifies generic JSON files would not be> a good addition. However a tool that verifies Fuchsia `.cmx` files, which> happen to use the JSON format, would be okay. > ** SDK ** >> SDK工具在某种程度上特定于紫红色。通用工具或广泛可用的工具不应该成为Fuchsia的一部分，也不会包含在Fuchsia SDK中。例如，验证通用JSON文件的工具不是很好的补充。但是，可以使用一种验证Fuchsia`.cmx`文件（恰好使用JSON格式）的工具。

 
### Audience  听众 

Tools may be used for different development tasks. On a large team these roles may be separate people. Some categories are: 工具可以用于不同的开发任务。在大型团队中，这些角色可能是分开的人。一些类别是：

 
- Component development (mods/agents)  -组件开发（mods /代理）
- Driver development (DDK)  -驱动程序开发（DDK）
- Fuchsia development (SDK)  -紫红色开发（SDK）
- Build integration (Blaze, Bazel, etc.)  -构建集成（Blaze，Bazel等）
- Quality assurance (QA)  -质量保证（QA）
- System integrators (e.g., on-device network tools)  -系统集成商（例如设备上的网络工具）
- Publishing (from dev host to server)  -发布（从开发主机到服务器）
- Deployment (from server to customers)  -部署（从服务器到客户）

Consider which users may use a tool and cater the tool to the audience.  考虑哪些用户可以使用该工具并将该工具迎合受众。

Tools may have different integration expectations. For example, a developer doing mod development may expect tools to integrate with their IntegratedDevelopment Environment (IDE), while a build integration tool may be called froma script. 工具可能具有不同的集成期望。例如，进行mod开发的开发人员可能希望工具与其集成开发环境（IDE）集成，而构建集成工具可能会从脚本中调用。

 
### Grouping Related Tools  分组相关工具 

Prefer to put related commands under a common tool, i.e. like `git` and `fx` do. This helps encourage the team toward a shared workflow and provides a point ofdiscovery. 最好将相关命令放在通用工具下，例如git和fx do。这有助于鼓励团队朝着共享工作流程发展，并提供发现点。

Prefer subcommands to multiple tools. E.g. don't create tools with hyphenated names like `package-create` and `package-publish`, instead create a `package`command that accepts create and publish subcommands. 子命令优先于多个工具。例如。不要使用带有连字符的名称的工具（例如“ package-create”和“ package-publish”）来创建工具，而是创建一个接受“ create”和“ publish”子命令的“ package”命令。

Keep the number of commands under a tool organized and reasonable. I.e. avoid adding unrelated commands to a tool and provide sensible organization of thecommands in the help and documentation. 在有条理和合理的工具下保持命令数量。即避免在工具中添加无关的命令，并在帮助和文档中合理地组织命令。

 
### Scope of Work  工作范围 

Command line tools can be divided into two groups: simple single purpose tools and larger more featureful tools. Create tools that are ergonomic for theirpurpose. Simple tools should be quick to start up, while more complex tools willlean toward the more featureful. 命令行工具可以分为两类：简单的单一目的工具和功能更大的较大工具。创建符合人体工程学的工具。简单的工具应能快速启动，而更复杂的工具将趋向于功能更强大。

Larger tools will encompass an entire task at the user (developer) level. Avoid making a tool that accomplishes one small step of a task; instead make a toolthat will perform a complete task. 较大的工具将涵盖用户（开发人员）级别的整个任务。避免制作能够完成一项任务的工具；而是制作一个可以执行完整任务的工具。

For example, when:  例如，当：

 
- developing a C++ application: run the preprocessor, run the compiler, run the linker, start the built executable. -开发C ++应用程序：运行预处理器，运行编译器，运行链接器，启动生成的可执行文件。
- working on a unit test: build the tests and run the tests being worked on  -进行单元测试：构建测试并运行正在进行的测试
- developing a mod: compile the code, move the code and resources to the device, start the mod (or hot-reload) -开发mod：编译代码，将代码和资源移至设备，启动mod（或热重装）

Lean toward a tool that will accomplish all the steps needed by default, but allow for an advanced user to do a partial step (for example, passing anargument to ask the C++ compiler to only run the preprocessor). 倾向于使用一种工具，该工具将完成默认情况下所需的所有步骤，但允许高级用户执行部分步骤（例如，传递参数要求C ++编译器仅运行预处理器）。

> **SDK** >> For SDK build integrators, separate tools. The build integrators will learn> each and piece them together to make a working system. > ** SDK ** >>对于SDK构建集成商，请使用单独的工具。构建集成商将学习>并将它们拼凑成一个工作系统。

 
#### Sharing common functionality  共享常用功能 

If a small step of a task will be needed by several tools, it doesn't make sense to duplicate that code. Consider making a small support tool or create a libraryto share the code. 如果几个工具需要完成一小步，那么复制该代码就没有意义了。考虑制作一个小型支持工具或创建一个库以共享代码。

Making a small tool that performs one step of the task can make sense to promote code reuse. If the user is not expected to run this small tool individually,place the support tool in a directory that is not added to the `$PATH`. I.e.avoid polluting the environment path unnecessarily. 制作一个执行任务一个步骤的小型工具可以促进代码重用。如果不希望用户单独运行此小工具，请将支持工具放置在未添加到$ PATH中的目录中。即避免不必要地污染环境路径。

Providing a library to share code may be preferable, so that a subprocess isn't needed. 提供共享代码的库可能是更可取的，因此不需要子进程。

 

 
## Implementation  实作 

Here is some guidance for the nuts and bolts of creating a tool. We'll cover which language to write the tool in, what style to use in that language, and soon. 这是有关创建工具的基本原则。我们将很快介绍使用哪种语言编写工具，以哪种风格使用该语言。

 
### Naming  命名 

The following applies to names of binaries, tools, sub-commands, and long parameter flags. 以下内容适用于二进制文件，工具，子命令和长参数标志的名称。

Use well-known US English terms or nouns for names. Well-known nouns includes those in common use for the subject matter, or the names of whole subsystems.If a name does not appear in documentation, it is likely not well-known. Ifit does not appear in any implementation, it is definitely not well-known. 使用著名的美国英语术语或名词作为名称。众所周知的名词包括主题中常用的名词或整个子系统的名称，如果名称未出现在文档中，则可能不是众所周知的。如果它没有出现在任何实现中，则它绝对不是众所周知的。

Only use lower-case characters in the US-ASCII character set and hyphens. A single hyphen (`-`) is used to separate words in a name. A Platformrequired extension is an exception (such as `.exe`). 在US-ASCII字符集和连字符中只能使用小写字符。单个连字符（`-`）用于分隔名称中的单词。 Platform所需的扩展名是一个例外（例如`.exe`）。

Name CLI tools with more than three characters. Keep the short file names available for user shortcuts (aliases). If you believe a tool should havea very short name, request approval from the Fuchsia API Council. 使用三个以上的字符来命名CLI工具。使简短文件名可用于用户快捷方式（别名）。如果您认为某个工具的名称应非常简短，请请求Fuchsia API委员会批准。

Keeping the points above in mind:  请牢记以上几点：

 
- Prefer whole words rather than abbreviations.  -优先选择完整的单词而不是缩写。
- Prefer shorter names where a user is expected type the name frequently. For less frequently typed names bias to more explicit names. -在需要用户输入的情况下，最好使用短名称。对于不太频繁键入的名称，请偏向更显式的名称。
- Prefer a single word to multiple words  -优先使用单个单词而不是多个单词
- Prefer subcommands to multiple tools that are hyphenated (e.g. avoid `foo-start`, `foo-stop`, `foo-reset`; instead have `foo` that acceptscommands `start|stop|reset`). -最好让子命令使用带连字符的多个工具（例如，避免使用“ foo-start”，“ foo-stop”，“ foo-reset”；而应使用具有接受命令“ start | stop | reset”的“ foo”）。
- Prefer symmetry (particularly in verbs) with other similar commands or sub-systems, unless that introduces a broken metaphor. -最好与其他类似的命令或子系统保持对称（尤其是动词），除非这样会引入隐喻。

 
### Programming Languages  编程语言 

Tools may be written in C++, Rust, and Go. For clarity, here are some languages not approved: Bash, Python, Perl, JavaScript, and Dart (see exceptions below). 工具可以用C ++，Rust和Go编写。为了清楚起见，以下是一些未经批准的语言：Bash，Python，Perl，JavaScript和Dart（请参见下面的例外）。

No language is preferred between C++, Rust, and Go. The choice between these languages is up to the author of the tool. 在C ++，Rust和Go之间没有语言是首选。这些语言之间的选择取决于工具的作者。

> **SDK** >> If a given flavor of SDK includes a specific language (e.g. Dart), that> language may be used for tools that are distributed with that SDK. I.e. do not> include a Dart tool in an SDK that wouldn't otherwise include the Dart> runtime, but if it's already there, that's okay. > ** SDK ** >> >>如果给定版本的SDK包含特定语言（例如Dart），则该语言可用于随该SDK分发的工具。即不要在SDK中包含Dart工具，否则该工具不会包含Dart>运行时，但是如果已经存在，那就可以了。

 
### Style Guides  风格指南 

Follow the corresponding [style guide](../README.md#languages) for the language and area of Fuchsia being developed.E.g. if the tool is included with Zircon and writtenin C++, use the style guide for C++ in Zircon. Specifically, avoid creating aseparate style guide for tools. 请遵循相应的[样式指南]（../ README.mdlanguages），了解所开发的紫红色的语言和区域。如果该工具包含在Zircon中并用C ++编写，请使用Zircon中的C ++样式指南。特别是，避免为工具创建单独的样式指南。

 
### Runtime Link Dependencies  运行时链接依赖项 

Try to minimize runtime link dependencies (statically link dependencies instead). On Linux it is acceptable to runtime link against the glibc suite oflibraries (libm, etc.); other runtime link dependencies are not allowed. 尝试最小化运行时链接依赖性（改为静态链接依赖性）。在Linux上，可以针对glibc套件库（libm等）进行运行时链接；不允许其他运行时链接依赖项。

 
### Building from Source  从源头建造 

Keep in mind that some developers will want to build the tools from source. Use the same build and dependency structure as the code in the Platform Source Tree.Do not make a separate system to build tools. 请记住，一些开发人员将希望从源代码构建工具。使用与平台源代码树中的代码相同的构建和依赖关系结构。请勿创建单独的系统来构建工具。

 

 
## Host Platforms  主机平台 

Keep an eye on how resource heavy a tool becomes and what OSes it will be expected to operate on. 密切关注工具的资源消耗量以及预期将在哪些操作系统上运行。

 
### Run on a Variety of Hardware  在各种硬件上运行 

Developer machines may range from a few CPU cores and moderate amount of RAM to dozens of CPU cores and huge amounts of RAM. Don't assume that host machines arevery powerful or that a server cluster is available to offload work to. 开发人员机器的范围从几个CPU内核和适量的RAM到数十个CPU内核和大量的RAM。不要以为主机功能强大，也不要以为服务器集群可以将工作分担给他人。

 
### Supported OSes  支持的操作系统 

This section is for the convenience of the reader. This document is not authoritative on which platforms are supported. 本节是为了方便读者。本文档并不支持所支持的平台。

We currently support  我们目前支持

 
- Linux  -Linux
- macOS  - 苹果系统

Tools written for developers must run on those platforms. There are other platforms to consider, and while these are not required at this time, it's goodto keep the platforms listed below in mind. 为开发人员编写的工具必须在这些平台上运行。还有其他平台需要考虑，尽管此时不需要这些平台，但最好记住以下列出的平台。

Tools should be built in a way that makes them easy to port to the following platforms: 工具的构建方式应使其易于移植到以下平台：

 
- Fuchsia (self-hosted)  -紫红色（自托管）
- Windows  -Windows

This is not an exhaustive list, we may support others.  这不是一个详尽的清单，我们可能会支持其他人。

 
### Case Insensitive File Systems  不区分大小写的文件系统 

Don't rely on case sensitivity in file paths. E.g. don't expect that `src/BUILD` and `src/build` are different files. Conversely, don't rely on caseinsensitivity since some platforms are case sensitive. 不要依赖文件路径中的区分大小写。例如。不要期望src / BUILD和src / build是不同的文件。相反，由于某些平台区分大小写，因此请勿依赖大小写不敏感。

 
### Development Hosts Using a Non-English Locale  使用非英语语言环境的开发主机 

There are several aspects to consider for non-English developers:  非英语开发人员应考虑以下几个方面：

 
- Whether the tool itself can be localized  -工具本身是否可以本地化
- Whether the documentation for the tool can be localized  -该工具的文档是否可以本地化
- Whether the tool can work with path names and data that include non-ASCII  -该工具是否可以使用包含非ASCII的路径名和数据
- Whether the tool works correctly on non-English OSes  -该工具在非英语操作系统上是否正常运行

Tools are provided in US English. It's not required that a tool be localized. (This may change in the future.) 工具以美国英语提供。不需要将工具本地化。 （将来可能会改变。）

The documentation for a tool will support non-ASCII characters. Both HTML and Markdown can support Unicode (UTF-8) characters, so these are both good choicesfor documentation. Doing the translation is not required, merely allow for thepossibility. 该工具的文档将支持非ASCII字符。 HTML和Markdown都可以支持Unicode（UTF-8）字符，因此它们都是文档的不错选择。不需要翻译，仅允许这种可能性。

Tools will function properly with file paths that contain binary sequences and white space. Use a library to work with file paths rather than manipulatingpaths as strings. (e.g. path.Join in Go.) 工具将正确处理包含二进制序列和空格的文件路径。使用库来处理文件路径，而不是将路径作为字符串来处理。 （例如path。加入Go。）

Tools will operate correctly on non-English platforms (e.g. Japanese or French). This means handling binary (e.g. UTF-8) data without corrupting it. E.g. don'tassume a text file is just ASCII characters. 工具可以在非英语平台（例如日语或法语）上正常运行。这意味着在不破坏数据的情况下处理二进制（例如UTF-8）数据。例如。不要假设文本文件只是ASCII字符。

 

 
## Execution  执行 

At runtime (or execution time) consider how the tool should behave.  在运行时（或执行时），请考虑该工具的行为。

 
### Optimize for No Work Needed  优化无需工作 

When appropriate, such as with a build tool, have the tool exit quickly if there is no work to do. If possible, go one step better by providing information tothe caller about the dependencies so that the caller can accurately determinewhether the tool needs to be called at all. 在适当的时候（例如使用构建工具），如果没有任何工作要做，请使该工具快速退出。如果可能的话，通过向调用者提供有关依赖项的信息来更好地迈出一步，以便调用者可以准确地确定是否需要调用该工具。

 
### Command Line Arguments  命令行参数 

There are three types of command line arguments:  命令行参数有三种类型：

 
- exact text  -确切的文字
- arguments  -参数
- options (i.e. switches and keys)  -选项（即开关和按键）

 
#### Exact text  确切的文字 

Exact text is placed as-is on the command line. A piece of exact text may be required or optional. Parsing exact text arguments should be restricted to caseswhere they are needed for disambiguation (i.e. for correctly parsing otherarguments). For example if a `copy` command accepted multiple source anddestination arguments, an exact text argument may be used to clarify which iswhich: `copy a b c` may be ambiguous; while `copy a to b c` may indicate that'`a`' is copied to two destinations. 确切的文本按原样放在命令行中。一段准确的文本可能是必需的，也可能是可选的。解析确切的文本参数应仅限于歧义消除（即正确解析其他参数）所需的情况。例如，如果一个“复制”命令接受了多个源和目标参数，则可以使用一个精确的文本参数来说明哪个是：“复制a b c”可能是模棱两可的；而“将a复制到b c”可能表示“ a”已复制到两个目的地。

 
#### Arguments  争论 

Arguments are like function parameters or slots for data to fit into. Often, their order matters. In the example `copy <from> <destination>`, both `<from>`and `<destination>` are ordered arguments. In cases where a single logicalargument is repeated the order may not matter, such as remove `<files>...` wherethe tool might process the `<files>` in an arbitrary order. 参数就像函数参数或数据适合的插槽。通常，它们的顺序很重要。在示例copy <from> <destination>中，<from>和`<destination>`都是有序参数。在重复单个逻辑参数的情况下，顺序可能无关紧要，例如删除`<files> ...`，其中该工具可能会以任意顺序处理`<files>'。

 
#### Options  选件 

Some arguments are known as options. Both switches and keyed (key/value pairs) are options. Options tend to modify the behavior of the tool or how the toolprocesses parameter arguments. Options consist of a dash prefixed letter orword. 一些参数称为选项。开关和键控（键/值对）都是选项。选项倾向于修改工具的行为或工具如何处理参数自变量。选项由带破折号的字母或单词组成。

Options must start with either one ('`-`') or two ('`--`') dashes followed by an alphanumeric label. In the case of a single dash, the length of the label mustbe 1. If the length of the label is two or more then two dashes must be used.For example: `-v` or `--help` are correct; `-help` is not valid. 选项必须以一个（'-`'）或两个（'`--`'）破折号开头，后跟一个字母数字标签。如果是单破折号，则标签的长度必须为1。如果标签的长度为两个或多个，则必须使用两个破折号。例如：-v或--help是正确的； -help无效。

All choices are required to have a (`--`) option. Providing single character shorthand (`-`) is optional. E.g. it's okay to provide just `--output`, or both`-o` and `--output`, but it's not ok to only provide an `-o` option without along option as well. 所有选项都必须具有（`--`）选项。提供单字符速记（`-`）是可选的。例如。可以只提供`--output`，或者同时提供`-o`和`--output`，但是也不能只提供`-o`选项而不附带选项。

Do not create numeric options, such as `-1` or `-2`. E.g. rather than having `-1` mean to do something once, add a `--once` option. If a numeric value isneeded, make a keyed option, like `--repeat <number>`. 不要创建数字选项，例如“ -1”或“ -2”。例如。而不是让-1意味着只做一次，而是增加一个--once选项。如果需要一个数字值，请输入一个键选项，例如`--repeat <number>`。

One (`-`) or two (`--`) dashes on their own are special cases and are not allowed as a key or switch. 单独的一个（`-`）或两个（`--`）破折号是特殊情况，不允许用作键或开关。

 
#### Switches  开关 

The presence of a switch means the feature it represents is 'on' while its absence means that it is 'off'. Switches default to 'off'. Unlike keyed options,a switch does not accept a value. E.g. `-v` is a common switch meaning verbose;it doesn't take a value, making it switch rather than a keyed value. 开关的存在表示其代表的功能处于“开启”状态，而开关的缺失则意味着其处于“关闭”状态。将默认设置切换为“关闭”。与键选项不同，开关不接受值。例如。 -v是一个普通的开关，意思是冗长；它不带值，而是开关而不是键值。

All switches must be documented (hidden switches are not allowed).  所有开关都必须记录在案（不允许使用隐藏开关）。

Running switches together is not allowed. E.g. `-xzf` or `-vv`, each must be separate: "`-x -z -f`" or "`-v -v`". 不允许同时运行开关。例如。 `-xzf`或`-vv`，每个必须分开：“`-x -z -f`”或“`-v -v`”。

 
#### Keyed Options  键控选项 

Keyed options consist of a key and a value. Keys are similar in syntax to switches except that a keyed option expects a value for the key.E.g. `-o <my_output_file>` has a key '`-o`' and a value of '`my_output_file`'. 键控选项由键和值组成。键的语法与开关相似，不同之处在于键选项需要键的值。 -o <my_output_file>具有键'-o`'和'my_output_file`'值。

Do not use an equals punctuation (or similar) to separate the key and value. E.g. do not do `-o=<my_output_file>`. 请勿使用等号标点（或类似标点）来分隔键和值。例如。不要做-o = <my_output_file>

Note about a rare case: Avoid making optional keys (where the value appears without its key) or optional values (where the key appears without itsvalue). It's clearer to consider the key/value pair optional, but inseparable.I.e. if the key is present a value is required and vice versa. Consider makingan argument instead of a keyed option with an optional key. E.g. rather than"`do-something [--config [<config_file>]]`" where not passing `[<config_file>]`means don't use a config file; instead do"`do-something [--config <config_file>|--no-config]`" where passing`--no-config` means don't load a config file. 请注意以下几种罕见情况：避免制作可选键（其中的值显示时没有键）或可选值（键中的显示时没有值）。考虑键/值对是可选的，但不可分割的，这显然是更清楚的。如果存在密钥，则需要一个值，反之亦然。考虑使用参数代替带可选键的键选项。例如。而不是“做某事[--config [<config_file>]]`”，其中不传递`[<config_file>]`的意思是不使用配置文件；而是执行“`do-something [--config <config_file> | --no-config]”，其中传递“ --no-config”表示不加载配置文件。

 
##### Mutually Exclusive Options  互斥选项 

Some options don't make sense with other options. We call the options mutually exclusive. 某些选项与其他选项没有任何意义。我们称这些选项互斥。

Passing mutually exclusive options is considered a user error. When this occurs the tool will do one of the following: 传递互斥选项被视为用户错误。发生这种情况时，该工具将执行以下操作之一：

 
- Write an error message explaining the issue and exit with a non-zero result code; doing no work (i.e. there was no data changed as a result of the call).This is the expected handling, so no further documentation or notes arerequired. -编写一条错误消息解释该问题并以非零结果代码退出；不执行任何操作（即呼叫后未更改任何数据），这是预期的处理方式，因此不需要进一步的文档或说明。
- Prioritize one option over another. E.g. "`passing -z will override -y`". In this case the handling will be documented in the `--help` output. -将一个选项优先于另一个选项。例如。 “`传递-z将覆盖-y`”。在这种情况下，处理将记录在“ --help”输出中。
- Other handling is possible (first takes precedence or last takes precedence or something else) though this is discouraged. In this case the handling willbe documented in the Description, Options, ***and*** Notes; though"`See Notes`" may be used in Description and Options with the full write-up in`Notes`. -尽管不建议这样做，但也可以进行其他处理（第一个优先或最后一个优先）。在这种情况下，处理将记录在“说明”，“选项”，“ ***”和“注释”中；不过，“说明”和“选项”中可能会使用“请参阅便笺”，而在便笺中则有完整的记载。

 
##### Grouping Options  分组选项 

There is no specific syntax to indicate when enabling one option will also affect another option. When an option implies that another option is enabled ordisabled, specify that in the Options. E.g. "`passing -e implies -f`" means thatif `-e` is enabled, `-f` will be enabled as if it were passed on the commandline (regardless of whether `-f` was explicitly passed). The redundant passingof the implied value is harmless (not an error). 没有特定的语法指示何时启用一个选项也会影响另一选项。当某个选项暗示另一个选项已启用或禁用时，请在“选项”中指定该选项。例如。 “`传递-e意味着-f`”表示如果启用了-e，则将启用-f就像在命令行上传递一样（无论是否显式传递了-f）。隐式值的冗余传递是无害的（不是错误）。

 
##### Option Delimiter  选项定界符 

Two dashes ('`--`') on their own indicates the end of argument options. All subsequent values are given to the tool as-is. For example, with"`Usage: foo [-a] <file>`", the command line "`foo -- -a`" may interpret `-a` asa file name rather than a switch. Further, "`foo -a -- -a`" enables the switch`-a` (the first `-a`, before the `--`) and passes the literal text `-a` (thesecond `-a`). 单独的两个破折号（'`--`'）表示参数选项的结尾。所有后续值均按原样提供给工具。例如，使用“`用法：foo [-a] <文件>”，命令行“`foo--a`”可以将-a解释为文件名而不是开关。此外，“ foo -a--a”启用开关-a（第一个-a，在-之前）并传递文字文本-a（第二个-a）。 ）。

 
##### Repeating Options  重复选项 

Repeating switches may be used to apply more emphasis (what more emphasis means is up to the tool, the description here is intentionally vague). A commonexample is increasing verbosity by passing more `-v` switches. 重复开关可用于施加更多的强调（更多的强调手段取决于工具，此处的描述是模糊的）。一个常见的例子是通过传递更多的-v开关来增加详细程度。

Repeating keyed options may be used to pass multiple values to the same command. Often this is done to avoid calling the same command multiple times. Commoncommands that accept repeating options are `cp`, `rm`, `cat`. Care must be takento ensure that repeating commands are unambiguous and clear. E.g. `cp` alwaysinterprets the last argument as the destination; if `cp` accepted multiplesource and destination arguments the parsing would become ambiguous or unclear. 重复键控选项可用于将多个值传递给同一命令。通常这样做是为了避免多次调用同一命令。接受重复选项的常见命令是`cp`，`rm`，`cat`。必须注意确保重复的命令是明确且清晰的。例如。 cp总是把最后一个参数解释为目的地。如果`cp`接受了多个源和目标参数，则解析将变得模棱两可或不清楚。

 
#### Standard Input Alias  标准输入别名 

In Fuchsia tools a single dash (`-`) is not interpreted as an alias to stdin. Use pipes to direct data into stdin or use `/dev/stdin` as an alias for stdin.(Note: `/dev/stdin` is not available on Fuchsia or Windows). 在Fuchsia工具中，单破折号（`-`）不会解释为stdin的别名。使用管道将数据导入stdin或使用`/ dev / stdin`作为stdin的别名（注意：`/ dev / stdin`在Fuchsia或Windows上不可用）。

 
#### Single Dash  单冲刺 

A single dash ('-') on its own is reserved for future use.  单独的破折号（'-'）保留供将来使用。

 
#### Subcommands  子指令 

Tools may contain sub-command that accept independent command line arguments. (Similar to the `git` tool). Subcommands do not begin with any dashes. E.g. in`fx build` the `build` argument is a subcommand. 工具可能包含接受独立命令行参数的子命令。 （类似于git工具）。子命令不以任何破折号开头。例如。在`fx build`中，`build`参数是一个子命令。

When a tool has many subcommands, it should also have a help subcommand that display help about other subcommands. E.g. "`fx help build`" will provide helpon the build subcommand. 当工具具有许多子命令时，它还应该具有一个help子命令，该命令显示有关其他子命令的帮助。例如。 “`fx help build`”将在build子命令上提供帮助。

Subcommands may have their own arguments that are not handled by the main tool. Arguments between the tool name and the subcommand are handled by the tool andarguments that follow the subcommand are handled by the subcommand. E.g. in`fx -a build -b` the `-a` is an argument for the `fx` tool, while the `-b`argument is handled by the `build` subcommand. 子命令可能具有其自己的参数，而主工具未处理这些参数。工具名称和子命令之间的参数由工具处理，子命令后的参数由子命令处理。例如。在`fx -a build -b`中，-a是`fx`工具的参数，而`-b`参数由`build`子命令处理。

 
### Common Features  共同特征 

Command line tools are expected to support some common switches:  命令行工具应该支持一些常见的开关：

 
- `--help`  -`-帮助`
- `--quiet`  -`-安静`
- `--verbose`  -`--verbose`
- `--version`  -`--version`

 
#### Interactive Help (--help)  交互式帮助（--help） 

A tool must accept a `--help` switch and provide usage information to the command line in that case. The layout and syntax of the help text is describedin a future document. 在这种情况下，工具必须接受“ --help”开关，并向命令行提供使用信息。帮助文本的布局和语法将在以后的文档中介绍。

The tool must not do other work (i.e. have side effects) when displaying help.  显示帮助时，该工具不得执行其他工作（即具有副作用）。

Use a library that can parse the arguments as well as present help information from the same source. Doing so keeps the two in sync. I.e. avoid writing commandline help as an independent paragraph of text. 使用可以解析参数以及提供来自同一来源的帮助信息的库。这样做可以使两者保持同步。即避免将命令行帮助作为独立的文本段落编写。

Keep the interactive help reasonably concise. Plan for a skilled reader, i.e. someone looking for a reminder on how to use the tool or a developer experiencedin reading interactive help. For the novice, provide a note referring them tothe Markdown documentation. 保持交互式帮助的合理简洁。规划熟练的读者，即寻找有关如何使用该工具的提醒的人或经验丰富的阅读交互式帮助的开发人员。对于新手，请提供注释以将他们引向Markdown文档。

Provide an option to generate machine parsable output.  提供一个选项来生成机器可分析的输出。

 
#### Verbosity (--quiet and --verbose)  详细程度（--quiet and --verbose） 

The `--quiet` and `--verbose` switches decrease or increase informational output to the user. Their implementation is optional, but all tools will accept them asarguments and must not use those terms for other purposes, e.g. don't use`--quiet` to turn off the audio output (use `--silence` or `--volume 0` or someother synonym). “ --quiet”和“ --verbose”开关减少或增加了向用户的信息输出。它们的实现是可选的，但是所有工具都会接受它们的参数，并且不得将这些术语用于其他目的，例如不要使用--quiet来关闭音频输出（使用--silence或--volume 0或其他同义词）。

 
#### Interactive Version (--version)  互动版本（-版本） 

A tool must accept a `--version` switch and provide an indication of the code used to build the tool in that case. The layout and syntax is not specified, butthe version will include a version number of some kind. 工具必须接受“ --version”开关，并在这种情况下提供用于构建工具的代码的指示。没有指定布局和语法，但是版本将包含某种版本号。

The tool must not do other work (have side effects) when reporting its version.  报告其版本时，该工具不得做其他工作（有副作用）。

 
### Logging  记录中 

Logging is distinct from normal output. The audience for logging is normally the tool developer or a power user trying to debug an issue. Logging may go tostdout in special cases, such as when `--verbose` output is requested. 日志记录不同于正常输出。记录的受众通常是工具开发人员或尝试调试问题的高级用户。在特殊情况下，例如当请求`--verbose`输出时，日志记录可能会消失。

Logging from multiple threads will not interlace words within a line, i.e. the minimum unit of output is a full text line. Each line will be prefixed with anindication of the severity of the line. The severity will be one of: detail,info, warning, error, fatal. 从多个线程进行日志记录将不会在一行中交错单词，即输出的最小单位是全文行。每行都将以行的严重性标记为前缀。严重性将是以下各项之一：详细信息，信息，警告，错误，致命。

 
## Metrics  指标 

Every tool must file a Privacy Design Document (PDD) in order to collect usage metrics. 每个工具都必须提交一份隐私设计文档（PDD），以收集使用情况指标。

Metrics are important to drive quality and business decisions. Questions we want to answer with metrics include: 指标对于推动质量和业务决策很重要。我们要用指标回答的问题包括：

 
- Which OS are our users using? - so we know how to prioritize work for various platforms -我们的用户正在使用哪个操作系统？ -因此，我们知道如何优先处理各种平台的工作
- Which tools are they using? - so we know how to prioritize investments, and to learn which workflows are currently being used so we can prioritizeinvestments or identify weak spots -他们使用哪些工具？ -因此，我们知道如何确定投资的优先顺序，并了解当前使用的工作流程，以便我们可以确定投资的优先顺序或确定薄弱环节
- How often do they use a tool? - so we know how to prioritize investments, and to learn which workflows are currently being used so we can prioritizeinvestments or identify weak spots -他们多久使用一次工具？ -因此，我们知道如何确定投资的优先顺序，并了解当前使用的工作流程，以便我们可以确定投资的优先顺序或确定薄弱环节
- Do our tools crash in the wild? How often? - so we know how to prioritize maintenance of tools -我们的工具会在野外崩溃吗？多常？ -我们是否知道如何优先维护工具
- How do they use a tool? - assuming that a tool can do one or more things, we'd like to learn how to prioritize investments in particular workflows of a tool -他们如何使用工具？ -假设某个工具可以完成一项或多项任务，我们将学习如何在该工具的特定工作流程中确定投资的优先级

The type and content of the metrics collected must be carefully chosen. We will go through the Google-standard PDD review process to ensure we are compliantwith Google's practices and policies. Tools must get approval on which metricsare collected before collection. 必须仔细选择收集的指标的类型和内容。我们将按照Google标准的PDD审核流程进行操作，以确保我们符合Google的惯例和政策。工具必须在收集之前就收集哪些度量标准获得批准。

 
## Configuration and Environment  配置与环境 

Tools often need to know something about the context they are running. Let's look at how that context should be gathered or stored. 工具通常需要了解有关它们正在运行的上下文的信息。让我们看一下如何收集或存储该上下文。

 
#### Reading Information  阅读信息 

Tools should not attempt to gather or intuit settings or other state directly from the environment. Information such as an attached target's IP address, theout directory for build products, or a directory for writing temporary fileswill be gathered from a platform agnostic source. Separating out the code thatperforms platform-specific work will allow tools to remain portable betweendisparate platforms. 工具不应尝试直接从环境中收集或了解设置或其他状态。诸如附加目标的IP地址，构建产品的输出目录或用于写入临时文件的目录之类的信息将从平台不可知的来源中收集。分离出执行平台特定工作的代码将使工具在不同平台之间保持可移植性。

Where practical, configuration information should be stored in a way familiar to the user of the host machine (e.g. on Windows, use the registry). Tools shouldgather information from SDK files or platform-specific tools that encapsulatethe work of reading from the Windows registry, Linux environment, or Macsettings. 在可行的情况下，配置信息应以主机用户熟悉的方式存储（例如，在Windows上，使用注册表）。工具应从SDK文件或平台专用工具收集信息，这些工具或工具封装了从Windows注册表，Linux环境或Macsettings读取的工作。

Tools will be build-system agnostic as well. Accessing a common file such as build input dependency file is okay. 工具也将与构建系统无关。可以访问诸如构建输入依赖项文件之类的通用文件。

 
#### Writing Information  写作信息 

Tools will not modify configuration or environment settings, except when the tool is clearly for the purpose of modifying an expected portion of theenvironment. 工具不会修改配置或环境设置，除非该工具明确用于修改环境的预期部分。

If modifying the environment outside of the tool's normal scope may help the user, the tool may do so with the express permission of the user. 如果在工具的正常范围之外修改环境可能对用户有所帮助，则该工具可以在用户的​​明确许可下进行操作。

 

 
## Execution Success and Failure  执行成功与失败 

Command line tools return an integer value in the range [0..127] when they exit. A zero represents success (no error) and 1-127 are various forms of error. Thevalue 1 is used as a general error. Any values other than 0 and 1 that may bereturned must be documented for the user. 命令行工具退出时会返回[0..127]范围内的整数值。零表示成功（无错误），而1-127是各种形式的错误。值1用作一般错误。必须为用户记录除0和1以外的任何其他值。

 
### Succeed with Grace  成功恩典 

If there were no errors encountered, return a result code of zero.  如果没有遇到错误，则返回结果代码零。

Avoid producing unnecessary output on success. Don't print "succeeded" (unless the user is asking for verbose output). 避免在成功时产生不必要的输出。不要打印“成功”（除非用户要求详细输出）。

 
### If Something is Unclear, Stop  如果不清楚，请停止 

If the tool encounters an ambiguous situation or is in danger of corrupting data, do not continue. E.g. if the path to the directory you're being asked todelete comes back as just "`/`", there was likely an error trying to get thatconfiguration information, avoid 'soldiering on' and removing everything under"`/`". 如果工具遇到模棱两可的情况或有损坏数据的危险，请不要继续。例如。如果要求您删除的目录路径返回为“`/`”，则可能是在尝试获取该配置信息时出错，避免“继续使用”并删除“`/`”下的所有内容。

 
### Do Not Fail Silently  不要默默地失败 

Tools must clearly indicate failure by returning a non-zero error code. If appropriate (if it makes sense for the tool or if the user explicitly asked forverbose output) print an error message explaining what went wrong. 工具必须通过返回非零错误代码来明确指示故障。如果合适（如果对工具有意义，或者用户明确要求详细输出），则打印一条错误消息，说明出了什么问题。

 
### Provide Direction on Failure  提供失败指导 

When a tool execution fails, be clear about whether the error came from bad inputs, missing dependencies, or bugs within the tool. Make error reportscomprehensible and actionable. 当工具执行失败时，请明确错误是由于错误的输入，缺少的依赖关系还是工具内部的错误引起的。使错误报告可理解且可行。

If the error came from bad inputs  如果错误来自错误的输入

 
1. If the user gave the tool bad data, give context about the error and guide the user toward fixing the input, e.g. print which input file (and linenumber if that's appropriate for the input) where the input error occurred. 1.如果用户向工具提供了错误的数据，请给出有关错误的上下文，并指导用户确定输入内容，例如打印发生输入错误的输入文件（如果适合输入，则打印行号）。
   - Prefer output that follows this format (for easy regex use): `file_name:line:column:description`. This is a common format used by manytools. Other formats are acceptable, but try to use something that is easyfor both humans and tools to parse. -更喜欢遵循这种格式的输出（为了易于使用正则表达式）：`file_name：line：column：description`。这是manytools常用的格式。其他格式也是可以接受的，但是请尝试使用易于人类和工具解析的内容。
2. Provide a reference to further information. E.g. if documentation is available, provide a link to documentation about the tool in general or todocumentation regarding the specific error. If the tool has the capacity toprovide more details, describe that (like how `gn` can explain how to run thetool to get more help). 2.提供更多信息的参考。例如。如果有可用的文档，请提供指向有关该工具的常规文档或有关特定错误的文档的链接。如果该工具有能力提供更多详细信息，请对其进行描述（例如gn可以解释如何运行该工具以获取更多帮助）。

If the error came from missing dependencies  如果错误来自缺少依赖项

 
1. Be clear that the error is from missing dependencies, i.e. don't leave the user trying to debug their input data if that is not the issue. 1.请明确指出错误是由于缺少依赖项引起的，也就是说，如果不是问题，请不要让用户尝试调试其输入数据。
2. Provide instruction on how to satisfy the dependencies. This can be an example command to run (e.g. `apt-get install foo`) or a link to furtherinstructions (e.g. "`see: http:example.com/how-to-install-foo`"). 2.提供有关如何满足依赖性的说明。这可以是要运行的示例命令（例如，“ apt-get install foo”），也可以是指向进一步说明的链接（例如，“请参阅：http：example.com/how-to-install-foo””）。

If the error came from an unexpected state (i.e. a bug) in the tool  如果错误来自工具中的意外状态（即错误）

 
1. Apologize. Explain that the tool got into an unexpected state. Don't leave the user trying to guess whether their input data was bad or they weremissing dependencies. 1.道歉。说明该工具进入了意外状态。不要让用户试图猜测他们的输入数据是错误的还是缺少依赖关系。
2. Suggest a mailing list or forum to get help. Help the user find out if the bug is fixed in the next tool version; or someone has found a workaround. 2.建议一个邮件列表或论坛以获取帮助。帮助用户找出该错误是否在下一工具版本中已修复；或有人找到了解决方法。
3. Invite the user to enter a bug report and make that as easy as possible. E.g. provide a link that goes to the bug database with the tool and platforminformation prepopulated. 3.邀请用户输入错误报告，并使其尽可能简单。例如。提供一个链接到错误数据库的链接，其中包含预先填充的工具和平台信息。

 

 
## Include Tests  包括测试 

Tools must include tests that guarantee its correct behavior. Include both unit tests and integration tests with each tool. Tests will run in Fuchsia continuousintegration. 工具必须包括保证其正确行为的测试。每个工具都包括单元测试和集成测试。测试将以倒挂金钟持续集成进行。

> **SDK** >> It's especially important that SDK tools imported from the Fuchsia build (pm,> etc.) have tests that run in Fuchsia continuous integration because the SDK> bot does not currently prevent breaking changes. > ** SDK ** >>从Fuchsia版本（pm等）中导入的SDK工具具有以Fuchsia持续集成运行的测试，这一点尤其重要，因为SDK>机器人当前无法阻止重大更改。

 
## Documentation  文献资料 

The Markdown documentation is the right place to put more verbose usage examples nd explanations. Markdown文档是放置更多详细用法示例和解释的正确位置。

> **SDK** >> All tools included in the SDK and intended to be executed directly by an end> user must have a corresponding Markdown documentation file. > ** SDK ** >> SDK中包含的所有旨在由最终用户直接执行的工具都必须具有相应的Markdown文档文件。

 
## User vs. Programmatic Interaction  用户与程序交互 

A tool may be run interactively by a human user or programmatically via a script (or other tool). 工具可以由人类用户交互式运行，也可以通过脚本（或其他工具）以编程方式运行。

While each tool will default to interactive or non-interactive mode if they can glean which is sensible, they must also accept explicit instruction to run in agiven mode (e.g. allow the user to execute the programmatic interface even ifthey are running in an interactive shell). 尽管每个工具都可以收集（如果明智的话）将默认设置为交互或非交互模式，但它们还必须接受明确的指令以在给定模式下运行（例如，即使它们在交互外壳中运行，也允许用户执行编程界面） 。

 
### Stdin  Stdin 

For tools that are not normally interactive, avoid requesting user input e.g. readline or linenoise). I.e. Don't suddenly put up an unexpected prompt toask the user a question. 对于通常不是交互式的工具，请避免请求用户输入，例如readline或linenoise）。即不要突然出现意想不到的提示来向用户提问。

For interactive tools (e.g. `zxdb`) prompting the user for input is expected.  对于交互式工具（例如`zxdb`），提示用户输入。

 
### Stdout  标准输出 

When sending output to the user on stdout use proper spelling, grammar, and avoid unusual abbreviations. If an unusual abbreviation is used, be sure it hasan entry in the [glossary.md](../../glossary.md). 在标准输出上将输出发送给用户时，请使用正确的拼写，语法，并避免使用不常见的缩写。如果使用了不寻常的缩写，请确保在[glossary.md]（../../ glossary.md）中有一个条目。

Try to check for output to terminal, i.e. see if a user is there or whether the receiver is a program. 尝试检查是否有输出到终端，即查看用户是否在那里或接收者是否为程序。

 
#### ANSI Color  ANSI颜色 

Use of color is allowed with the following caveats  下列注意事项允许使用颜色

 
- Enabling/disabling color output based on terminal information (i.e. whether it supports color) is encouraged, but that's not always possible (so it's notrequired) -鼓励根据终端信息（即是否支持颜色）启用/禁用颜色输出，但这并不总是可能的（因此不是必需的）
  - Always allow the user to override color use (they can disable it)  -始终允许用户覆盖颜色使用（可以将其禁用）
- When using color, be sure to use colors that are distinct for readers who may not be able to see a full range of color (e.g. color-blindness). -使用颜色时，请确保使用可能无法看到全部颜色的读者所专有的颜色（例如色盲）。
- Never rely on color to convey information. Only use color as an enhancement. Seeing the color must not be needed for correct interpretation of the output. -切勿依靠颜色来传达信息。仅将颜色用作增强。正确显示输出内容时，不必看到颜色。

 
### Stderr  斯特德 

Use stderr for reporting invalid operation (diagnostic output) i.e. when the tool is misbehaving. If the tool's purpose is to report issues (like a linter,where the tool is not failing) output those results to stdout instead of stderr. 使用stderr报告无效操作（诊断输出），即工具行为异常时。如果该工具的目的是报告问题（例如linter，则该工具不会失败），则将这些结果输出到stdout而不是stderr。

See Success and Failure for more information on reporting errors.  有关报告错误的更多信息，请参见成功和失败。

 
### Full-Screen  全屏 

Avoid creating full-screen terminal applications. Use a GUI application for such a tool. 避免创建全屏终端应用程序。将GUI应用程序用于此类工具。

 
### Non-interactive (Programmatic)  非互动式（程序化） 

Include a programmatic interface where reasonable to allow for automation.  在合理的范围内包括一个编程接口，以实现自动化。

If there is an existing protocol for that domain, try to follow suit (or have a good reason not to). Otherwise consider using manifest or JSON files formachine input. 如果该域已有协议，请尝试遵循（或有充分理由不这样做）。否则，请考虑使用清单文件或JSON文件进行机器输入。

 
### IDE (Semi-Programmatic)  IDE（半编程） 

Allow for tools to be used by an Integrated Development Environment. This generally involves accepting a manifest for input and generating a manifest. 允许集成开发环境使用工具。这通常涉及接受清单以进行输入并生成清单。

 
### Interactive (User)  互动式（用户） 

Interacting with the user while the tool is running is an uncommon case for many tools. Some tools may run interactively as an option, e.g. `rm -i` will promptthe user before each removal. 在工具运行时与用户进行交互对于许多工具而言并不常见。某些工具可以作为选项交互地运行，例如rm -i将在每次删除之前提示用户。

 
## State Files  状态文件 

State files encode information for data sharing between tools. PID file and lock files are examples of state files. 状态文件对信息进行编码，以便在工具之间共享数据。 PID文件和锁定文件是状态文件的示例。

Avoid using a PID file to contain the process ID of a running executable.  避免使用PID文件包含正在运行的可执行文件的进程ID。

