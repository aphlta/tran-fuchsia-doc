 
# CLI Tool Help Requirements  CLI工具帮助要求 

 

 
## Overview  总览 

Command line help, as often provided via `--help` is an important means of communication with the user. It provides a shorthand for more detaileddocumentation and feature discovery. 命令行帮助（通常通过--help提供）是与用户通信的重要手段。它为更详细的文档说明和功能发现提供了捷径。

 

 
## Guide  指南 

Help documentation must include a usage section written in [Usage](#bookmark=id.yv0npmd9oldw) format, followed by brief written prosedescribing the command, and the following sections (as needed): Options,Commands, Examples, Notes, and Error codes. 帮助文档必须包括以[用法]（bookmark = id.yv0npmd9oldw）格式编写的用法部分，其后是简短的书面说明该命令的内容，以及以下部分（根据需要）：选项，命令，示例，注释和错误代码。

Let's start with a full example before digging into the specifics.  让我们先从完整的示例开始，然后再深入探讨具体细节。

 
### Example  例 

Each section of this example is described in detail later in this document. (Note that `blast` is not a real tool). 本文档后面将详细介绍此示例的每个部分。 （请注意，blast不是真正的工具）。

```text
Usage: blast [-f] [-s <scribble>] <command> [<args>]

Destroy the contents of <file>.

Options:
  -f                force, ignore minor errors. This description
                    is so long that it wraps to the next line.
  -s <scribble>     write <scribble> repeatedly
  -v, --verbose     say more. Defaults to $BLAST_VERBOSE.

Commands:
  blow-up         explosively separate
  grind           make smaller by many small cuts
  help            get help on other commands e.g. `blast help grind`

Examples:
  Scribble 'abc' and then run |grind|.
  $ blast -s 'abc' grind old.txt taxes.cp

Notes:
  Use `blast help <command>` for details on [<args>] for a subcommand.

Error codes:
  2 The blade is too dull.
  3 Out of fuel.
```
 

 
#### General layout and style  总体布局和风格 

See above for an example that follows these requirements.  请参阅上面的示例，这些示例遵循这些要求。

Several sections call for **English prose**. This means writing in proper sentences using English grammar with US English spelling (as opposed to BritishEnglish or others). Use one space between sentences, and adhere to the "Oxfordcomma" style. E.g. the Description and Notes sections are written in Englishprose. 有几个部分要求“英语散文”。这意味着使用英语语法和美国英语拼写（而不是BritishEnglish或其他）来编写适当的句子。在句子之间使用一个空格，并坚持“牛津逗号”风格。例如。 “说明”和“注释”部分以Englishprose编写。

**Layout**  **布局**

 
- Each section is separated by one blank line.  -每个部分用一个空白行分隔。
- Section contents are indented two spaces.  -节内容缩进两个空格。
- Single line contents will be written on the same line as the label with one space separating the colon and the command name. E.g. "`Usage: blast <file>`". -单行内容将与标签写在同一行上，并用一个空格分隔冒号和命令名称。例如。 “`用法：blast <file>`”。
- Multi-line sections will be written immediately following the label (without a blank line). Each line after the label will be indented two spaces. -多行部分将立即写在标签后面（无空行）。标签后的每一行将缩进两个空格。
- All output is a single column of text with the exception of Options, Commands, and Error codes which are two column tables. -所有输出均为单列文本，但选项，命令和错误代码是两列表，例外。
- Use spaces for indentation or alignment. Do not output tab characters.  -使用空格进行缩进或对齐。不输出制表符。
- Wrap text at 80 columns. When wrapping Option or Command descriptions, align the subsequent lines with the start of the description (e.g. about 20characters in). -在80列处换行。在包装Option或Command描述时，将后续行与描述的开头对齐（例如，大约20个字符）。

**Style**  **样式**

 
- Section titles appear in title-case: capitalize the first and last words. All words in between are also capitalized except for articles (a, an, the),conjunctions (e.g., and, but, or), and prepositions (e.g., on, in, with). -章节标题以大写字母出现：大写第一个和最后一个单词。除冠词（a，an，the），接词（例如and，but，or）和介词（例如on，in，with）外，中间的所有单词也都大写。
- Short description fragments (the second column in Options or Commands) begin with a lowercase letter and are not expected to be full sentences. Any textbeyond the short description should be complete sentences, with a period afterthe fragment. -简短描述片段（选项或命令的第二列）以小写字母开头，并且不应为完整的句子。简短描述以外的任何文本均应为完整的句子，在句段后加上句点。
- Try to keep each section concise. If there is more to say, direct the user to use `--verbose` when running `--help` or direct them to the fulldocumentation. -尽量保持每个部分的简洁。如果还有更多要说的话，请指示用户在运行--help时使用--verbose或将其定向到完整文档。
- Unicode (UTF-8) characters are allowed in descriptive text (prose). The command name and usage text will only contain portable ASCII characters(without Unicode). -描述性文字（散文）中允许使用Unicode（UTF-8）字符。命令名称和用法文本将仅包含可移植的ASCII字符（不带Unicode）。

 
### Usage  用法 

Usage is required and includes the "`Usage:`" header.  使用是必需的，并且包括“ Usage：”标题。

```text
Usage: blast [-f] [-s <scribble>] <command> [<args>]
```
 

Usage will commonly be a single line, though multiple lines can be used to clarify when options are mutually exclusive. If the number of lines needed topresent all the mutually exclusive scenarios becomes excessive, limit the linesto some common cases and give more details in the full docs. If there are manymutually exclusive options, consider making subcommands or separate tools toreduce the complexity. 用法通常是单行，但是可以使用多行来说明选项何时互斥。如果表示所有相互排斥的场景所需的行数过多，请将行限制为某些常见情况，并在完整文档中提供更多详细信息。如果有许多互斥的选项，请考虑使用子命令或单独的工具来降低复杂性。

 
#### Usage syntax  使用语法 

The command name is listed first. The command name is not hardcoded: it will be dynamically pulled from the command name, i.e. the last element on the `argv[0]`path. This allows a single binary to operate as multiple different tools. 命令名称列在最前面。命令名称不是硬编码的：它将动态地从命令名称中拉出，即argv [0]路径上的最后一个元素。这允许单个二进制文件用作多个不同的工具。

The name and usage text will contain portable ASCII characters only. All long form commands are entirely lowercase, i.e. never all-caps or mixed-case. Singleletter switches should prefer lowercase, but uppercase is allowed. 名称和用法文本将仅包含可移植的ASCII字符。所有长格式命令都完全是小写字母，即绝不要全部大写或大小写混合。单字母开关应首选小写字母，但允许使用大写字母。

Use meaningful words for options and placeholders. Avoid abbreviations. Prefer single words. When more than one word is used, separate words with a hyphen(`-`), i.e. do not use underscores, camel-case, or run words together. 为选项和占位符使用有意义的词。避免缩写。优先使用单个单词。当使用多个单词时，请使用连字符（`-`）分隔单词，即不要同时使用下划线，驼峰大小写或连续单词。

Aside from the command name there are several kinds of arguments (as described in [Fuchsia Tool Requirements](http://go.corp.google.com/fuchsia-tool-requirements)). 除了命令名称外，还有几种自变量（如[Fuchsia工具要求]（http://go.corp.google.com/fuchsia-tool-requirements）中所述）。

 
- Exact text  -确切的文字
- Arguments  -参数
- Options (Switches and Keys)  -选项（开关和按键）
- Keyed options  -键控选项
- Option delimiter  -选项定界符

 
##### Exact Text Syntax  确切的文字语法 

Exact text is written as-is in the usage line. In the example "`Usage: copy <from> to <destination>`", the word `to` is required exact text. If exact textis optional, it will be enclosed in brackets (`[]`) in the usage line: "`Usage:copy <from> [to] <destination>`". 确切的文本按原样写在用法行中。在示例“用法：将<from>复制到<目标>”中，单词“ to”是必填文本。如果确切的文本是可选的，它将用在用法行中的方括号（`[]`）中：“`Usage：copy <from> [to] <destination>`”。

 
##### Argument Syntax  参数语法 

Arguments are enclosed in angle brackets (<>) to differentiate them from explicit text. In the example `Usage: copy <from> <destination>`, both `<from>`and `<destination>` are arguments. If an argument is optional, it will beenclosed in brackets (`[]`) such as: `Usage: copy <from> [<destination>]`. Seealso [Option Delimiter](./cli.md#option_delimiter). 将参数括在尖括号（<>）中，以将其与显式文本区分开。在示例“用法：复制<from> <destination>”中，“ <from>”和“ <destination>”都是参数。如果参数是可选的，则将其括在方括号（[[]`）中，例如：`用法：copy <from> [<destination>]`。另请参见[选项分隔符]（./ cli.mdoption_delimiter）。

 
##### Mutually Exclusive Option Syntax  互斥选项语法 

There are a couple choices when illustrating mutually exclusive options.  说明互斥选项时有两个选择。

If more than one usage line is provided, each will show a mutually exclusive set of commands. For example: 如果提供了多个使用行，则每个使用行将显示一组互斥的命令。例如：

```text
Usage:
  swizzle [-z] <file>
  swizzle --reset
```
 

Indicates that `--reset` and usage with a `<file>` are mutually exclusive options. 表示“ --reset”和与“ <file>”一起使用是互斥的选项。

Another way to specify mutually exclusive options is using a vertical bar ('|') between the options. Note that when a vertical bar is used to indicate data flowbetween processes it is called a "Pipe." When used to separate options it isread as "Or". 指定互斥选项的另一种方法是在选项之间使用竖线（'|'）。注意，当使用竖线表示进程之间的数据流时，它称为“管道”。当用于分隔选项时，将其读取为“或”。

For example:  例如：

```text
Usage: froth [-y|-z] <file>
```
 

Indicates that `-y` **_or_** `-z` switches can be used (or neither, since they are optional), but it's senseless to use both together (they are mutuallyexclusive options). To indicate that either value must be used, but not both,wrap the choices in parentheses, e.g. "`Usage: froth (-a|-b) <file>`" means that`-a` **_or_** `-b` must be passed. 表示可以使用`-y` ** _ or _ **`-z`开关（或者都不使用，因为它们是可选的），但是将它们一起使用是没有意义的（它们是互斥的选项）。为了表示必须使用其中一个值，但不能同时使用两个值，请在括号中将选项括起来，例如“`用法：泡沫（-a | -b）<文件>`”表示必须传递`-a` ** _ or _ **`-b`。

Note that it's common that `--version` or `--help` causes other arguments to be ignored and is seldom listed as such. Listing them as separate usage lines isconsidered unnecessary. 注意，通常使用--version或--help导致其他参数被忽略，因此很少列出。将它们列为单独的使用行被认为是不必要的。

 
##### Grouping (implied) options  分组（隐含）选项 

There is no specific syntax to indicate when enabling one option will also affect another option. When an option implies that another option is enabled ordisabled, specify that in the Options. E.g. "`passing -e implies -f`" means thatif `-e` is enabled, `-f` will be enabled as if it were passed on the commandline (regardless of whether `-f` was explicitly passed). The redundant passingof the implied value is harmless (not an error). 没有特定的语法指示何时启用一个选项也会影响另一选项。当某个选项暗示另一个选项已启用或禁用时，请在“选项”中指定该选项。例如。 “`传递-e意味着-f`”表示如果启用了-e，则将启用-f就像在命令行上传递一样（无论是否显式传递了-f）。隐式值的冗余传递是无害的（不是错误）。

Document the implication in the primary switch. E.g. if `-x implies -c and -p` place that note in the description of `-x` but not in `-c` and `-p`. This is tokeep the `--help` output concise (this rule can be relaxed in the fulldocumentation). 记录下主交换机中的含义。例如。如果`-x暗示-c和-p`将该注释放在`-x`的描述中，而不是在`-c`和`-p`的描述中。这是为了使“ --help”输出保持简洁（在完整文档中可以放宽此规则）。

 
##### Optional Keys  可选键 

To create the appearance of a keyed option with an optional Key, create optional exact text followed by an argument. For example "`Usage: copy [from] <from> [to]<destination>`". In the example, all of these are valid: "`copy a b`", "`copyfrom a b`", "`copy from a to b`", "`copy a to b`". 要使用可选的Key创建带有键的选项的外观，请创建可选的精确文本，后跟一个参数。例如“`用法：复制[from] <from> [to] <目的地>`”。在示例中，所有这些都是有效的：“从a复制到b”，“从a复制到b”，“从a复制到b”，“从a复制到b”。

 
##### Repeating Options  重复选项 

If the same positional argument may be repeated, indicate that with an ellipsis ('...'). Rather than a Unicode ellipsis, use three consecutive periods. Forexample: "`Usage: copy <from> [<from>...] <to>`" means the last argument isalways interpreted as the `<to>`, while the preceding values are multiple`<from>` entries. Note that "`<from> [<from>...]`" means there is one or more`<from>` entries, while "`Usage: copy [<from>...] <to>`" means zero or more`<from>` entries are accepted. 如果可以重复相同的位置参数，请用省略号（'...'）表示。而不是Unicode省略号，请使用三个连续的句点。例如：“`用法：复制<from> [<from> ...] <to>`”表示最后一个参数总是解释为`<to>`，而前面的值是多个<from>条目。请注意，“`<from> [<from> ...]`”表示存在一个或多个“ <from>”条目，而“`用法：复制[<from> ...] <to>`”表示接受零个或多个“ <from>”条目。

For Key/Value pairs which may be repeated, group them with brackets (if the pair is optional) or parentheses (if the pair is not optional) and add an ellipsis tothe group, e.g. `[--input <file>]...` or `(--input <file>)...` respectively. 对于可能重复的键/值对，将其用方括号（如果该对是可选的）或括号（如果该对不是可选的）进行分组，然后在该组中添加省略号，例如分别是[--input <file>] ......或（--input <file>）...

 
##### Brackets  括号 

Angle brackets (`<>`), brackets (`[]`), and parentheses (`()`) will not have spaces immediately inside. 尖括号（`<>`），方括号（`[]`）和括号（`（）`）内不能有空格。

```text
[from] # correct
<to> # correct
(-a|-b) # correct

[ from ] # incorrect
< to > # incorrect
( -a|-b ) # incorrect
```
 

Angle brackets (<>) wrap Arguments or Key values.  尖括号（<>）包装参数或键值。

Brackets (`[]`) wrap optional elements. With nested angle brackets, such as `[<file>]`, interpret the `<file>` as an Argument that is optional. The nested"`[<`" is not a separate bracket style, it is a "`[`" with a "`<`" within it.When nesting, the brackets (`[`) will be outermost (do not use `<[file]>`). 方括号（`[]`）包装可选元素。对于嵌套的尖括号，例如`[<file>]`，将`<file>`解释为可选参数。嵌套的“`[<`”不是单独的括号样式，它是其中包含“`<`”的“`[`”。嵌套时，括号（`[`）将位于最外面（请勿使用`<[文件]>`）。

Parentheses (`()`) are used to group elements. Use parentheses when they improve clarity, such as with required mutually exclusive options. 括号（`（）`）用于对元素进行分组。当括号可以提高清晰度时，请使用括号，例如带有必需的互斥选项。

Braces (`{}`) are reserved for future use. This guide intentionally leaves open the possibility for braces to have special meaning in a future revision of thisdocument. 括号（`{}`）保留供将来使用。本指南有意使括号在本文档的将来修订版中具有特殊含义的可能性。

 
### Description  描述 

The description is required and does not include a header. I.e. the description area is not labeled "description". E.g. 该描述是必需的，并且不包括标题。即描述区域未标记为“描述”。例如。

```text
Destroy the contents of <file>.
```
 

The description is written in US English prose (complete sentences using US English grammar, spelling, and punctuation). 描述使用美国英语散文（使用美国英语语法，拼写和标点的完整句子）编写。

Every tool should tell you what it does and this is the section to do that.  每个工具都应告诉您它的功能，这是执行此操作的部分。

The Description section should describe  说明部分应说明

 
- what the tool does (required)  -该工具的功能（必填）
- the platform configuration used  -使用的平台配置
- schemes, data formats, or protocols used  -使用的方案，数据格式或协议
- golden workflows (critical developer journeys)  -黄金工作流程（关键的开发人员旅程）
- a broad URL to documentation (e.g. fuchsia.com/docs or similar, avoid deep links that go stale to easily) -指向文档的宽泛网址（例如fuchsia.com/docs或类似网址，请避免使用容易过时的深层链接）

The Description section can also contain a "see also" referring to another tool by name (avoid using a URL). “描述”部分还可以包含“另请参见”，其名称通过名称引用（避免使用URL）。

What not to put in the Description section  在说明部分不放的内容

 
- environment variables used, other than those already listed in Options (provide this in Options or Notes) -使用的环境变量，而不是已在“选项”中列出的变量（在“选项”或“注释”中提供）
- security hazards (explain these in the Notes section)  -安全隐患（在“注释”部分中进行解释）
- error codes (put those in an Error codes section)  -错误代码（将这些内容放入“错误代码”部分）
- copyright (don't include this in the `--help`)  -版权（请勿在`--help`中添加）
- author (don't include this in the `--help`)  -作者（请勿在`--help`中加入）
- how to get help on subcommands (put this in the short description for the `help` subcommand) -如何获得有关子命令的帮助（将其放在“ help”子命令的简短描述中）
- how to update the tool (that should be in the documentation for the tool package, if applicable) -如何更新工具（如果适用，应包含在工具包的文档中）
- release notes (use a separate file)  -发行说明（使用单独的文件）

 
### Options  选件 

An Options section is required if the program accepts arguments. E.g.  如果程序接受参数，则需要“选项”部分。例如。

```text
Options:
  -f              force, ignore minor errors
  -s <scribble>   write <scribble> repeatedly. Defaults to $BLAST_SCRIBBLE.
```
 

The listed options apply to the tool itself and not to a subcommand. Options for individual subcommands are listed when requesting help for that subcommand, e.g.when using `blast help grind` or `blast grind --help`. 列出的选项适用于工具本身，而不适用于子命令。在请求该子命令的帮助时，将列出各个子命令的选项，例如，在使用“ blast help grind”或“ blast grind --help”时。

Try to keep options to a single, complete word. If two words are needed, separate the words with a hyphen (`-`). Avoid uncommon abbreviations. 尝试将选项保留为一个完整的单词。如果需要两个单词，请用连字符（`-`）分隔。避免使用不常用的缩写。

Present the list of options in alphabetical order.  按字母顺序显示选项列表。

Options will list each argument, switch, and keyed option on separate lines with the exception of arguments that have both a short and long form. If an argumenthas both a short and long form they are listed on the same line, short formfirst, and separated by `, ` (comma space), e.g. `-f, --force`. 选项将在单独的行上列出每个参数，开关和键控选项，但参数的形式既简短又长。如果参数同时具有短格式和长格式，则它们会在同一行上列出，短格式在前，并以`，`（逗号空格）分隔，例如-f，--force

Exact text arguments will not be listed in the Options section. They are shown in the Usage section. 确切的文本参数将不会在“选项”部分中列出。它们显示在“用法”部分。

Text that will be typed as-is is not wrapped in brackets, while variable entries appear in angle brackets (`<>`) and optional entries appear in square brackets(`[]`). When listing options, the Key is never optional. For example: 将原样输入的文本未括在方括号中，而变量条目则出现在尖括号（`<>`）中，而可选项则出现在方括号（`[]）中。列出选项时，密钥永远不是可选的。例如：

```text
  -a                   a good example
  [-b]                 a bad example, to use -b it must be typed as-is
```
 

A short description will follow each option. There's no limit on the length of this description, but be concise. Try to put more details in the overall tooldescription, the Examples, or the Notes instead of creating a lengthy optiondescription. 每个选项后面都会有简短说明。此说明的长度没有限制，但要简明扼要。尝试在整体工具描述，示例或注释中放置更多详细信息，而不要创建冗长的选项描述。

What to describe  描述什么

 
- a brief reminder of what the option implies, e.g. `ignore minor errors`  -简要提醒该选项的含义，例如忽略小错误
- if the option overrides another option, e.g. `-x implies -c and -p`  -如果选项优先于另一个选项，例如-x表示-c和-p
- default value, e.g. `defaults to $BLAST_SCRIBBLE`  -默认值，例如默认为$ BLAST_SCRIBBLE

The column on which the description sentence fragment begins may vary depending on the needs of the tool. Use 20 characters from the left edge if it looks okay,but adjust if a bit more or less reads better. 描述语句片段开始的列可能会根据工具的需求而有所不同。如果看起来还可以，请从左边缘开始使用20个字符，但如果稍稍好一点，请进行调整。

If there is a large number of options, consider showing a useful subset and explaining how to get further help to see all of them, e.g. by passing`--verbose` along with `--help`. 如果有大量选项，请考虑显示一个有用的子集，并说明如何获得进一步的帮助以查看所有选项，例如通过传递“ --verbose”和“ --help”。

 
### Commands  指令 

A commands section is required if the program has subcommands. If present it will be labeled, "Commands:". E.g. 如果程序具有子命令，则必须有一个命令部分。如果存在，它将被标记为“命令：”。例如。

```text
Commands:
  blow-up         explosively separate
  grind           make smaller by many small cuts
  help            get help on other commands e.g. `blast help grind`
```
 

If the program does not have subcommands, the commands section will not be present. 如果程序没有子命令，则将不显示命令部分。

When a tool has subcommands, it will also have a `help` command to get further help on the subcommands, i.e.` blast help grind`. 当工具具有子命令时，它还将具有一个“帮助”命令，以获取有关子命令的进一步帮助，即“ blast help grind”。

Try to keep subcommands to a single, complete word. If two words are needed, separate the words with a hyphen (`-`). Avoid uncommon abbreviations. Presentthe list of commands in alphabetical order. 尝试将子命令保留为一个完整的单词。如果需要两个单词，请用连字符（`-`）分隔。避免使用不常用的缩写。按字母顺序显示命令列表。

Each command name appears with a short description on a separate line. For a more lengthy command description, the user will specifically ask for help onthat command. This description serves as a short reminder of the command and toassist in discovery of commands. 每个命令名称在单独的行上带有简短描述。对于更长的命令描述，用户将特别要求该命令的帮助。此描述只是对命令的简短提醒，并有助于发现命令。

If there is a large number of commands, consider showing a useful subset and explaining how to get further help to see all of them, e.g. by passing`--verbose` along with `--help`. 如果有大量命令，请考虑显示一个有用的子集，并说明如何获得进一步的帮助以查看所有命令，例如通过传递“ --verbose”和“ --help”。

 
### Examples  例子 

An examples section is optional. If present it will be labeled, "Examples:". E.g. 示例部分是可选的。如果存在，它将被标记为“示例：”。例如。

```text
Examples:
  Scribble 'abc' and then run |grind|.
  $ blast -s 'abc' grind old.txt taxes.cp
```
 

Each example will have US English prose (i.e. complete sentences using US English grammar, spelling, and punctuation) describing the example, followed byan example command line. Each line that would be entered on the command lineliterally will be prefixed with a "`$ `" to mimic a command prompt. 每个示例都会有描述该示例的美式英语散文（即使用美式英语语法，拼写和标点符号的完整句子），然后是示例命令行。在命令行上逐行输入的每一行都将以“ $$”作为前缀，以模仿命令提示符。

To wrap an example that is overly long, end the previous line with "`\ `" and begin subsequent lines with "`  `" (spaces) to indicate line continuation. 要包装一个过长的示例，请在前一行以“`\`”结束，在后续行以“``”（空格）开始以指示行继续。

```text
  This example wraps onto multiple lines.
  $ blast -s 2332 some/long/path/cats.o \
    more/long/path/dogs.o more/long/path/bears.o \
    more/long/path/deer.o
```
 

If it is helpful to show some of the output from the example command, write the output immediately following the example. 如果有助于显示example命令的某些输出，请在示例之后立即编写输出。

Separate examples with one blank line.  用一个空白行分隔示例。

If the Examples section is getting overly long, move examples to a help doc. Interactive help examples are for quick reference and discoverability ratherthan exhaustive documentation. 如果“示例”部分过长，请将示例移至帮助文档。交互式帮助示例用于快速参考和发现，而不是详尽的文档。

 
### Notes  笔记 

Notes are optional and begin with a "Notes:" header. E.g.  注释是可选的，并以“注释：”标题开头。例如。

```text
Notes:
  Use `blast help <command>` for details on [<args>] for a subcommand.
```
 

The notes are written in US English prose (i.e. complete sentences using US English grammar, spelling, and punctuation). 注释以美式英语散文（即使用美式英语语法，拼写和标点符号的完整句子）书写。

What to put in the Notes  注意事项

 
- environment variables used, other than those already listed in Options (for default values) -使用的环境变量，但“选项”中已列出的变量除外（用于默认值）
- security hazards  -安全隐患
- reminders to help the user  -提醒帮助用户

What not to put in the Notes  注意事项

 
- error codes (put those in an Error codes section)  -错误代码（将这些内容放入“错误代码”部分）
- copyright (don't include this in the `--help`)  -版权（请勿在`--help`中添加）
- author (don't include this in the `--help`)  -作者（请勿在`--help`中加入）
- how to get help on subcommands (put this in the short description for the `help` subcommand) -如何获得有关子命令的帮助（将其放在“ help”子命令的简短描述中）
- how to update the tool (that should be in the documentation for the tool package, if applicable) -如何更新工具（如果适用，应包含在工具包的文档中）
- release notes (use a separate file)  -发行说明（使用单独的文件）

 
### Error codes  错误代码 

The Error codes section is required if codes other than `0` or `1` are generated. E.g. 如果生成的不是“ 0”或“ 1”以外的代码，则需要“错误代码”部分。例如。

```text
Error codes:
  2  The blade is too dull.
  3  Out of fuel.
```
 

This section is omitted if only `0` or `1` results are generated by the program.  如果程序仅生成“ 0”或“ 1”结果，则忽略此部分。

Error code `0` is always treated as "no error" and error code `1` is always a "general error". Neither are documented in the `--help` output. Every error codeother than `0` or `1` that may be generated by the tool must be documented. 错误代码“ 0”始终被视为“无错误”，错误代码“ 1”始终被视为“一般错误”。两者均未在“ --help”输出中记录。该工具可能产生的除0或1之外的所有错误代码都必须记录在案。

 
### Platform specifics  平台细节 

Some platforms (e.g. DOS) use a different option prefix (e.g. `/`) or may allow case insensitive switches. Tools will use a dash prefix (`-`) and case sensitiveoptions regardless of the platform. This means that the documentation for a toolgenerally doesn't need to consider the platform being used. 某些平台（例如DOS）使用不同的选项前缀（例如`/`），或者可能允许不区分大小写的开关。无论平台如何，工具都会使用破折号（`-`）和区分大小写的选项。这意味着工具的文档通常不需要考虑所使用的平台。

 
### What not to include in --help output  --help输出中不包括的内容 

Do not show Key/Value pairs with an equals sign (`=`), e.g. `--scribble=abc`. The Key and Value are parsed using whitespace as a delimiter (`--scribble abc`).Showing the equals in the help is potentially confusing. 不要显示带有等号（`=`）的键/值对，例如`--scribble = abc`。键和值使用空格作为分隔符（`--scribble abc`）进行解析。在帮助中显示等号可能会造成混淆。

Do not implement a pager (something like the `more` program that pauses output on each screenful of text). 不要实现寻呼机（类似于`more`程序，该程序会在每个屏幕文本上暂停输出）。

Do not include  不包括

 
- a copyright in the help output (put that where legal specifies)  -帮助输出中的版权（法律规定的地方）
- release notes (put that in release notes)  -发行说明（在发行说明中注明）
- full documentation (put that in the markdown documentation)  -完整的文档（在降价文档中放入）
- version information (output that from `--version`)  -版本信息（从`--version`输出）
- documentation on result codes `0` or `1` (put in .md docs)  -关于结果代码“ 0”或“ 1”的文档（放在.md docs中）
