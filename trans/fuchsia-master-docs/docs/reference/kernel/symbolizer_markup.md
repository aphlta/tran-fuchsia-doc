 
# Symbolizer markup format #  符号器标记格式 

This document defines a text format for log messages that can be processed by a _symbolizing filter_.  The basic idea is that loggingcode emits text that contains raw address values and so forth, withoutthe logging code doing any real work to convert those values tohuman-readable form.  Instead, logging text uses the markup formatdefined here to identify pieces of information that should be convertedto human-readable form after the fact.  As with other markup formats,the expectation is that most of the text will be displayed as is, whilethe markup elements will be replaced with expanded text, or convertedinto active UI elements, that present more details in symbolic form. 本文档定义了可以由_symbolizing filter_处理的日志消息的文本格式。基本思想是，日志记录代码发出包含原始地址值等的文本，而日志记录代码无需做任何实际工作即可将这些值转换为人类可读的形式。相反，日志记录文本使用此处定义的标记格式来标识应在事实发生后转换为人类可读形式的信息。与其他标记格式一样，期望大多数文本将按原样显示，而标记元素将替换为扩展的文本或转换为活动的UI元素，从而以符号形式显示更多详细信息。

This means there is no need for symbol tables, DWARF debugging sections, or similar information to be directly accessible at runtime.  There isalso no need at runtime for any logic intended to compute human-readablepresentation of information, such as C++ symbol demangling.  Instead,logging must include markup elements that give the contextualinformation necessary to make sense of the raw data, such as memorylayout details. 这意味着不需要在运行时直接访问符号表，DWARF调试部分或类似信息。在运行时也不需要用于计算信息的人类可读表示的任何逻辑，例如C ++符号分解。取而代之的是，日志必须包含标记元素，这些标记元素会提供有意义的上下文信息，以使原始数据有意义，例如内存布局细节。

This format identifies markup elements with a syntax that is both simple and distinctive.  It's simple enough to be matched and parsed withstraightforward code.  It's distinctive enough that character sequencesthat look like the start or end of a markup element should rarely ifever appear incidentally in logging text.  It's specifically intendednot to require sanitizing plain text, such as the HTML/XML requirementto replace `<` with `&lt;` and the like. 此格式使用简单且与众不同的语法来标识标记元素。它非常简单，可以使用直接代码进行匹配和解析。它非常独特，以至于看起来像标记元素的开头或结尾的字符序列几乎永远不会偶然出现在日志文本中。专门不要求清理纯文本，例如HTML / XML要求用lt;`替换`<`等。

 
## Scope and assumptions ##  范围和假设 

This specification defines a format standard for Zircon and Fuchsia. But there is nothing specific to Zircon or Fuchsia about the markupformat.  A symbolizing filter implementation will be independent both ofthe _target_ operating system and machine architecture where the logsare generated and of the _host_ operating system and machinearchitecture where the filter runs. 该规范定义了锆石和紫红色的格式标准。但是关于markupformat，Zircon或Fuchsia并没有特定的含义。一个象征性的过滤器实现将独立于生成日志的_target_操作系统和机器体系结构以及运行过滤器的_host_操作系统和机器体系结构。

This format assumes that the symbolizing filter processes intact whole lines.  If long lines might be split during some stage of a loggingpipeline, they must be reassembled to restore the original line breaksbefore feeding lines into the symbolizing filter.  Most markup elementsmust appear entirely on a single line (often with other text beforeand/or after the markup element).  There are some markup elements thatare specified to span lines, with line breaks in the middle of theelement.  Even in those cases, the filter is not expected to handle linebreaks in arbitrary places inside a markup element, but only insidecertain fields. 此格式假定符号过滤器处理完整的整行。如果在测井管道的某个阶段可能会分开长线，则必须重新组装它们以恢复原始的换行符，然后再将行输入到符号过滤器中。大多数标记元素必须完全出现在一行上（通常与其他文本一起出现在标记元素之前和/或之后）。指定了一些标记元素来跨越线，在元素的中间有换行符。即使在这种情况下，也不能期望过滤器处理标记元素内任意位置的换行符，而只能处理某些字段。

This format assumes that the symbolizing filter processes a coherent stream of log lines from a single process address space context.  If alogging stream interleaves log lines from more than one process, thesemust be collated into separate per-process log streams and each streamprocessed by a separate instance of the symbolizing filter.  Because thekernel and user processes use disjoint address regions in most operatingsystems (including Zircon), a single user process address space plusthe kernel address space can be treated as a single address space forsymbolization purposes if desired. 此格式假定符号过滤器处理来自单个进程地址空间上下文的一致的日志行流。如果阻塞流交错来自多个进程的日志行，则必须将它们整理为单独的按进程日志流，并且每个流都由符号过滤器的单独实例处理。由于内核和用户进程在大多数操作系统（包括Zircon）中使用不相交的地址区域，因此，如果需要，可以将单个用户进程地址空间加上内核地址空间视为单个地址空间，以实现符号化目的。

 
## Dependence on Build IDs ##  对构建ID的依赖 

The symbolizer markup scheme relies on contextual information about runtime memory address layout to make it possible to convert markupelements into useful symbolic form.  This relies on having anunmistakable identification of which binary was loaded at each address. 符号化器标记方案依赖于有关运行时内存地址布局的上下文信息，从而可以将标记元素转换为有用的符号形式。这取决于对每个地址加载哪个二进制文件的明确标识。

An ELF Build ID is the payload of an ELF note with name `"GNU"` and type `NT_GNU_BUILD_ID`, a unique byte sequence that identifies a particularbinary (executable, shared library, loadable module, or driver module).The linker generates this automatically based on a hash that includesthe complete symbol table and debugging information, even if this islater stripped from the binary. ELF构建ID是名称为“ GNU”，类型为NT_GNU_BUILD_ID的ELF注释的有效载荷，NT_GNU_BUILD_ID是标识特定二进制文件（可执行文件，共享库，可加载模块或驱动程序模块）的唯一字节序列。链接器会生成此文件。即使包含二进制符号表中的最新信息，它也会自动基于包含完整符号表和调试信息的哈希值。

This specification uses the ELF Build ID as the sole means of identifying binaries.  Each binary relevant to the log must have beenlinked with a unique Build ID.  The symbolizing filter must have somemeans of mapping a Build ID back to the original ELF binary (either thewhole unstripped binary, or a stripped binary paired with a separatedebug file). 本规范使用ELF构建ID作为识别二进制文件的唯一方法。与日志相关的每个二进制文件都必须已链接有唯一的内部版本ID。符号过滤器必须具有一些将Build ID映射回原始ELF二进制文件的手段（整个未剥离的二进制文件，或与分离的ebug文件配对的剥离二进制文件）。

 
## Colorization ##  显色 

The markup format supports a restricted subset of ANSI X3.64 SGR (Select Graphic Rendition) control sequences.  These are unlike other markupelements: 标记格式支持ANSI X3.64 SGR（选择图形呈现）控制序列的受限子集。这些不同于其他标记：
 * They specify presentation details (**bold** or colors) rather than semantic information.  The association of semantic meaning with color(e.g. red for errors) is chosen by the code doing the logging, ratherthan by the UI presentation of the symbolizing filter.  This is aconcession to existing code (e.g. LLVM sanitizer runtimes) that usespecific colors and would require substantial changes to generatesemantic markup instead. *它们指定演示文稿的详细信息（粗体或彩色），而不是语义信息。语义与颜色的关联（例如，红色表示错误）是通过进行记录的代码来选择的，而不是通过符号过滤器的UI表示来选择的。这是对使用特定颜色的现有代码（例如LLVM sanitizer运行时）的让步，而需要进行实质性更改以生成语义标记。
 * A single control sequence changes "the state", rather than being an hierarchical structure that surrounds affected text. *单个控制序列会更改“状态”，而不是围绕受影响文本的层次结构。

The filter processes ANSI SGR control sequences only within a single line.  If a control sequence to enter a **bold** or color state isencountered, it's expected that the control sequence to reset to defaultstate will be encountered before the end of that line.  If a "dangling"state is left at the end of a line, the filter may reset to defaultstate for the next line. 该过滤器仅在一行内处理ANSI SGR控制序列。如果遇到进入“粗体”或颜色状态的控制序列，则预期在该行的结尾之前会遇到重置为默认状态的控制序列。如果在行尾留有“悬挂”状态，则过滤器可能会重置为下一行的默认状态。

An SGR control sequence is not interpreted inside any other markup element. However, other markup elements may appear between SGR control sequences andthe color/**bold** state is expected to apply to the symbolic output thatreplaces the markup element in the filter's output. SGR控制序列不会在任何其他标记元素中解释。但是，其他标记元素可能会出现在SGR控制序列之间，并且希望将color / ** bold **状态应用于将过滤器输出中的标记元素替换掉的符号输出。

The accepted SGR control sequences all have the form `"\033[%um"` (expressed here using C string syntax), where `%u` is one of these: 可接受的SGR控制序列都具有“ \ 033 [％um””的形式（此处使用C字符串语法表示），其中“％u”是其中之一：

| Code | Effect | Notes | |:----:|:------:|-------|| `0`  | Reset to default formatting. | || `1`  | Use **bold text**  | Combines with color states, doesn't reset them.|| `30` | Black foreground   | || `31` | Red foreground     | || `32` | Green foreground   | || `33` | Yellow foreground  | || `34` | Blue foreground    | || `35` | Magenta foreground | || `36` | Cyan foreground    | || `37` | White foreground   | | |代码效果|注意事项|：----：|：------：| ------- || `0` |重置为默认格式。 | || `1` |使用**粗体** |与颜色状态结合使用，请勿重置它们。 `30` |黑色前景| || `31` |红色前景| || `32` |绿色前景| || `33` |黄色前景| || `34` |蓝色前景| || `35` |洋红色前景| || `36` |青色前景| || `37` |白色前景| |

 
## Common markup element syntax ##  通用标记元素语法 

{# Disable variable substition to avoid {{ being interpreted by the template engine #} {% verbatim %} {禁用变量替换以避免{{被模板引擎解释} {逐字％}

All the markup elements share a common syntactic structure to facilitate simple matching and parsing code.  Each element has the form: 所有标记元素共享一个共同的语法结构，以简化简单的匹配和解析代码。每个元素具有以下形式：

```
{{{tag:fields}}}
```
 

`tag` identifies one of the element types described below, and is always a short alphabetic string that must be in lower case.  The rest of theelement consists of one or more fields.  Fields are separated by `:` andcannot contain any `:` or `}` characters.  How many fields must be ormay be present and what they contain is specified for each element type. “ tag”标识下面描述的元素类型之一，并且始终是短字母字符串，必须小写。其余元素由一个或多个字段组成。字段由`：`分隔，并且不能包含任何`：`或`}`字符。为每种元素类型指定必须存在或可以存在多少个字段以及它们包含的字段。

No markup elements or ANSI SGR control sequences are interpreted inside the contents of a field. 在字段的内容内不会解释任何标记元素或ANSI SGR控制序列。

In the descriptions of each element type, `printf`-style placeholders indicate field contents: 在每种元素类型的描述中，`printf`样式的占位符指示字段内容：

 
* `%s`  *`％s`

  A string of printable characters, not including `:` or `}`.  一串可打印的字符，不包括`：`或`}`。

 
* `%p`  *`％p`

  An address value represented by `0x` followed by an even number of hexadecimal digits (using either lower-case or upper-case for`A`..`F`).  If the digits are all `0` then the `0x` prefix may beomitted.  No more than 16 hexadecimal digits are expected to appear ina single value (64 bits). 用“ 0x”表示的地址值，后跟偶数个十六进制数字（“ A” ..“ F”使用小写或大写）。如果数字全为“ 0”，则可以省略“ 0x”前缀。单个值（64位）中最多应出现16个十六进制数字。

 
* `%u`  *`％u`

  A nonnegative decimal integer.  非负十进制整数。

 
* `%x`  *`％x`

  A sequence of an even number of hexadecimal digits (using either lower-case or upper-case for `A`..`F`), with no `0x` prefix.This represents an arbitrary sequence of bytes, such as an ELF Build ID. 偶数个十六进制数字的序列（对于“ A” ..“ F”使用小写或大写），没有前缀“ 0x”。这表示任意字节序列，例如ELF Build ID。

 
## Presentation elements ##  演示元素 

These are elements that convey a specific program entity to be displayed in human-readable symbolic form. 这些是传达要以人类可读符号形式显示的特定程序实体的元素。

 
* `{{{symbol:%s}}}`  *`{{{symbol：％s}}}`

  Here `%s` is the linkage name for a symbol or type.  It may require demangling according to language ABI rules.  Even for unmangled names,it's recommended that this markup element be used to identify a symbolname so that it can be presented distinctively. 这里的“％s”是符号或类型的链接名称。可能需要根据语言ABI规则进行拆除。即使对于未修饰的名称，也建议将该标记元素用于标识符号名，以便可以区别显示。

  Examples:  例子：

  ```
  {{{symbol:_ZN7Mangled4NameEv}}}
  {{{symbol:foobar}}}
  ```
 

 
* `{{{pc:%p}}}`  *`{{{pc：％p}}}`

  Here `%p` is the memory address of a code location. It might be presented as a function name and source location. 这里的“％p”是代码位置的内存地址。它可能显示为函数名称和源位置。

  Examples:  例子：

  ```
  {{{pc:0x12345678}}}
  {{{pc:0xffffffff9abcdef0}}}
  ```
 

 
* `{{{data:%p}}}`  *`{{{data：％p}}}`

  Here `%p` is the memory address of a data location. It might be presented as the name of a global variable at that location. 这里的“％p”是数据位置的内存地址。它可能表示为该位置的全局变量的名称。

  Examples:  例子：

  ```
  {{{data:0x12345678}}}
  {{{data:0xffffffff9abcdef0}}}
  ```
 

 
* `{{{bt:%u:%p}}}`  *`{{{bt：％u：％p}}}`

  This represents one frame in a backtrace.  It usually appears on a line by itself (surrounded only by whitespace), in a sequence of suchlines with ascending frame numbers.  So the human-readable outputmight be formatted assuming that, such that it looks good for asequence of `bt` elements each alone on its line with uniformindentation of each line.  But it can appear anywhere, so the filtershould not remove any non-whitespace text surrounding the element. 这表示回溯中的一帧。它通常单独出现在一行中（仅由空白包围），并以这样的序列出现，并以递增的帧号显示。因此，可以假定以下内容来格式化人类可读的输出，以使得它看起来很适合单独使用`bt`元素的行，并在每行上具有统一的缩进。但是它可以出现在任何地方，因此过滤器不应删除元素周围的任何非空白文本。

  Here `%u` is the frame number, which starts at zero for the location of the fault being identified, increments to one for the caller offrame zero's call frame, to two for the caller of frame one, etc.`%p` is the memory address of a code location. 这里'％u'是帧号，对于已确定故障的位置，它从零开始，对于帧零的调用者的调用者，递增为1，对于帧一的调用者，递增为2，依此类推。％p是代码位置的内存地址。

  In frames after frame zero, this code location identifies a call site. Some emitters may subtract one byte or one instruction length from theactual return address for the call site, with the intent that theaddress logged can be translated directly to a source location for thecall site and not for the apparent return site thereafter (which canbe confusing).  It's recommended that emitters _not_ do this, so thateach frame's code location is the exact return address given to itscallee and e.g. could be highlighted in instruction-level disassembly.The symbolizing filter can do the adjustment to the address ittranslates into a source location.  Assuming that a call instructionis longer than one byte on all supported machines, applying the"subtract one byte" adjustment a second time still results in anaddress somewhere in the call instruction, so a little sloppiness heredoes no harm. 在零帧之后的帧中，此代码位置标识一个呼叫站点。一些发射器可能会从呼叫站点的实际返回地址中减去一个字节或一个指令长度，目的是记录的地址可以直接转换为呼叫站点的源位置，而不是此后的明显返回站点的源位置（这可能会造成混淆）。建议发射器_not_执行此操作，以使每个帧的代码位置都是给itscallee和e.g.的确切返回地址。可以在指令级反汇编中突出显示。符号过滤器可以对其转换为源位置的地址进行调整。假设在所有支持的机器上调用指令的长度超过一个字节，那么第二次应用“减去一个字节”的调整仍然会在调用指令的某处产生一个地址，因此一点点草率都不会造成任何危害。

  Examples:  例子：

  ```
  {{{bt:0:0x12345678}}}
  {{{bt:1:0xffffffff9abcdef0}}}
  ```
 

 
* `{{{hexdict:...}}}`  *`{{{hexdict：...}}}`

  This element can span multiple lines.  Here `...` is a sequence of key-value pairs where a single `:` separates each key from its value,and arbitrary whitespace separates the pairs.  The value (right-handside) of each pair either is one or more `0` digits, or is `0x`followed by hexadecimal digits.  Each value might be a memory addressor might be some other integer (including an integer that looks like alikely memory address but actually has an unrelated purpose).  Whenthe contextual information about the memory layout suggests that agiven value could be a code location or a global variable dataaddress, it might be presented as a source location or variable nameor with active UI that makes such interpretation optionally visible. 该元素可以跨越多行。在这里，...是一系列键值对，其中单个`：`将每个键与其值分开，任意空格将这对键分开。每对的值（右侧）是一个或多个“ 0”数字，或者是“ 0x”，后跟十六进制数字。每个值可能是一个内存地址，也可能是其他一些整数（包括一个看起来类似的内存地址，但实际上具有不相关目的的整数）。当有关内存布局的上下文信息表明给定的值可以是代码位置或全局变量数据地址时，它可以显示为源位置或变量名称，或具有活动的UI，使该解释可选可见。

  The intended use is for things like register dumps, where the emitter doesn't know which values might have a symbolic interpretation but apresentation that makes plausible symbolic interpretations availablemight be very useful to someone reading the log.  At the same time,a flat text presentation should usually avoid interfering too muchwith the original contents and formatting of the dump.  For example,it might use footnotes with source locations for values that appearto be code locations.  An active UI presentation might show the dumptext as is, but highlight values with symbolic information availableand pop up a presentation of symbolic details when a value is selected. 预期用途是用于寄存器转储之类的，发射器不知道哪些值可能具有符号解释，但是使合理的符号解释可用的表示对于阅读日志的人可能非常有用。同时，纯文本显示通常应避免过多干扰原始内容和转储格式。例如，它可能使用带有源位置的脚注来表示似乎是代码位置的值。活动的UI演示文稿可能会按原样显示转储文本，但是会突出显示具有可用符号信息的值，并在选择值时弹出符号详细信息的演示文稿。

  Example:  例：

  ```
  {{{hexdict:
    CS:                   0 RIP:     0x6ee17076fb80 EFL:            0x10246 CR2:                  0
    RAX:      0xc53d0acbcf0 RBX:     0x1e659ea7e0d0 RCX:                  0 RDX:     0x6ee1708300cc
    RSI:                  0 RDI:     0x6ee170830040 RBP:     0x3b13734898e0 RSP:     0x3b13734898d8
     R8:     0x3b1373489860  R9:         0x2776ff4f R10:     0x2749d3e9a940 R11:              0x246
    R12:     0x1e659ea7e0f0 R13: 0xd7231230fd6ff2e7 R14:     0x1e659ea7e108 R15:      0xc53d0acbcf0
  }}}
  ```
 

 
## Trigger elements ##  触发元素 

These elements cause an external action and will be presented to the user in a human readable form. Generally they trigger an externalaction to occur that results in a linkable page. The link or someother informative information about the external action can then bepresented to the user. 这些元素引起外部动作，并将以人类可读的形式呈现给用户。通常，它们触发外部动作发生，从而导致可链接页面。然后可以将关于外部动作的链接或其他信息性信息呈现给用户。

 
* `{{{dumpfile:%s:%s}}}`  *`{{{dumpfile：％s：％s}}}`

  Here the first `%s` is an identifier for a type of dump and the second `%s` is an identifier for a particular dump that's just beenpublished.  The types of dumps, the exact meaning of "published",and the nature of the identifier are outside the scope of the markupformat per se.  In general it might correspond to writing a file bythat name or something similar. 在这里，第一个“％s”是转储类型的标识符，第二个“％s”是刚刚发布的特定转储的标识符。转储的类型，“已发布”的确切含义以及标识符的性质超出了markupformat本身的范围。通常，它可能对应于用该名称或类似名称编写文件。

  This element may trigger additional post-processing work beyond symbolizing the markup. It indicates that a dump file of some sorthas been published.  Some logic attached to the symbolizing filter mayunderstand certain types of dump file and trigger additionalpost-processing of the dump file upon encountering this element (e.g.generating visualizations, symbolization).  The expectation is that theinformation collected from contextual elements (described below) in thelogging stream may be necessary to decode the content of the dump.  Soif the symbolizing filter triggers other processing, it may need tofeed some distilled form of the contextual information to thoseprocesses. 除了符号化标记之外，此元素还可能触发其他后处理工作。它表示已发布某种转储文件。附加到符号过滤器的某些逻辑可能会理解某些类型的转储文件，并在遇到此元素时触发转储文件的其他后处理（例如，生成可视化效果，符号化）。期望从日志流中的上下文元素（如下所述）收集的信息对于解码转储的内容可能是必需的。因此，如果符号过滤器触发其他处理，则可能需要将某些形式的上下文信息馈送到这些处理中。

  On Zircon and Fuchsia in particular, "publish" means to call the `__sanitizer_publish_data` function from `<zircon/sanitizer.h>`with the "type" identifier as the "sink name" string.  The "dumpidentifier" is the name attached to the Zircon VMO whose handlewas passed in the call to `__sanitizer_publish_data`.**TODO(mcgrathr): Link to docs about `__sanitizer_publish_data` andgetting data dumps off the device.** 特别是在Zircon和Fuchsia上，“发布”是指从“ <zircon / sanitizer.h>”中调用“ __sanitizer_publish_data”函数，并将“类型”标识符作为“接收器名称”字符串。 “ dumpidentifier”是附加到Zircon VMO的名称，该Zircon VMO的句柄已在对__sanitizer_publish_data的调用中传递。** TODO（mcgrathr）：链接到有关__sanitizer_publish_data的文档，并从设备中获取数据转储。**

  An example of a type identifier is `sancov`, for dumps from LLVM [SanitizerCoverage](https://clang.llvm.org/docs/SanitizerCoverage.html). 类型标识符的一个示例是“ sancov”，用于从LLVM [SanitizerCoverage]（https://clang.llvm.org/docs/SanitizerCoverage.html）进行转储。

  Example:  例：

  ```
  {{{dumpfile:sancov:sancov.8675}}}
  ```
 

 
## Contextual elements ##  上下文元素 

These are elements that supply information necessary to convert presentation elements to symbolic form.  Unlike presentation elements,they are not directly related to the surrounding text.  Contextualelements should appear alone on lines with no other non-whitespacetext, so that the symbolizing filter might elide the whole line fromits output without hiding any other log text. 这些元素提供将表示元素转换为符号形式所需的信息。与表示元素不同，它们与周围的文本没有直接关系。上下文元素应该单独出现在没有其他非空白文本的行上，以便符号过滤器可以从其输出中删除整行而不会隐藏任何其他日志文本。

The contextual elements themselves do not necessarily need to be presented in human-readable output.  However, the information theyimpart may be essential to understanding the logging text even aftersymbolization.  So it's recommended that this information be preservedin some form when the original raw log with markup may no longer bereadily accessible for whatever reason. 上下文元素本身不一定需要以人类可读的输出形式呈现。但是，即使在符号化之后，它们所提供的信息对于理解日志文本也可能是必不可少的。因此，建议无论出于何种原因都无法再访问带有标记的原始原始日志时，以某种形式保留此信息。

Contextual elements should appear in the logging stream before they are needed.  That is, if some piece of context may affect how thesymbolizing filter would interpret or present a later presentationelement, the necessary contextual elements should have appearedsomewhere earlier in the logging stream.  It should always be possiblefor the symbolizing filter to be implemented as a single pass over theraw logging stream, accumulating context and massaging text as it goes. 上下文元素应在需要之前出现在日志记录流中。也就是说，如果某段上下文可能会影响符号过滤器解释或呈现后续呈现元素的方式，则必要的上下文元素应该已经出现在日志记录流中的某个较早位置。符号筛选器应该始终可以作为原始日志流上的一次传递来实现，从而累积上下文并在处理文本时对其进行按摩。

 
* `{{{reset}}}`  *`{{{reset}}}`

  This should be output before any other contextual element. The need for this contextual element is to support implementations that handlelogs coming from multiple processes. Such implementations might notknow when a new process starts or ends. Because some identifyinginformation (like process IDs) might be the same between old and newprocesses, a way is needed to distinguish two processes with suchidentical identifying information. This element informs suchimplementations to reset the state of a filter so that informationfrom a previous process's contextual elements is not assumed for newprocess that just happens have the same identifying information. 这应该在任何其他上下文元素之前输出。此上下文元素的需要是支持处理来自多个进程的日志的实现。这样的实现可能不知道新进程何时开始或结束。由于旧进程和新进程之间的某些标识信息（如进程ID）可能相同，因此需要一种方法来区分具有这种相同标识信息的两个进程。该元素通知此类实现以重置过滤器的状态，以便对于刚刚发生的具有相同标识信息的新过程，不假定来自先前过程的上下文元素的信息。

 
* `{{{module:%i:%s:%s:...}}}`  *`{{{module：％i：％s：％s：...}}}`

  This element represents a so called "module". A "module" is a single linked binary, such as a loaded ELF file. Usually each module occupiesa contiguous range of memory (always does on Zircon). 该元素代表一个所谓的“模块”。 “模块”是单个链接的二进制文件，例如已加载的ELF文件。通常，每个模块占用连续的内存范围（在Zircon上始终如此）。

  Here `%i` is the module ID which is used by other contextual elements to refer to this module.  The first `%s` is a human-readable identifier forthe module, such as an ELF `DT_SONAME` string or a file name; but itmight be empty.  It's only for casual information.  Only the module ID isused to refer to this module in other contextual elements, never the `%s`string.  The `module` element defining a module ID must always be emittedbefore any other elements that refer to that module ID, so that a filternever needs to keep track of dangling references.  The second `%s` is themodule type and it determines what the remaining fields are.  Thefollowing module types are supported: 这里的“％i”是模块标识，其他上下文元素使用它来引用此模块。第一个％s是模块的人类可读标识符，例如ELF`DT_SONAME`字符串或文件名；但它可能是空的。仅用于休闲信息。在其他上下文元素中，仅使用模块ID来引用该模块，而不会使用％s字符串。定义模块ID的`module`元素必须始终在引用该模块ID的任何其他元素之前发出，因此过滤器无需跟踪悬挂的引用。第二个“％s”是模块类型，它确定剩余的字段是什么。支持以下模块类型：

 
  * `elf:%x`  *`elf：％x`

    Here `%x` encodes an ELF Build ID. The Build ID should refer to a single linked binary. The Build ID string is the sole way to identifythe binary from which this module was loaded. 这里的'％x'对ELF内部版本号进行编码。 Build ID应该引用单个链接的二进制文件。 Build ID字符串是识别从中加载该模块的二进制文件的唯一方法。

  Example:  例：

  ```
  {{{module:1:libc.so:elf:83238ab56ba10497}}}
  ```
 

 
* `{{{mmap:%p:%x:...}}}`  *`{{{mmap：％p：％x：...}}}`

  This contextual element is used to give information about a particular region in memory. `%p` is the starting address and `%x` gives the sizein hex of the region of memory. The `...` part can take different formsto give different information about the specified region of memory. Theallowed forms are the following: 此上下文元素用于提供有关内存中特定区域的信息。 “％p”是起始地址，“％x”给出了内存区域的十六进制大小。 “ ...”部分可以采用不同的形式来提供有关指定内存区域的不同信息。允许的形式如下：

 
  * `load:%i:%s:%p`  *`load：％i：％s：％p`

    This subelement informs the filter that a segment was loaded from a module. The module is identified by its module id `%i`. The `%s` isone or more of the letters 'r', 'w', and 'x' (in that order and ineither upper or lower case) to indicate this segment of memory isreadable, writable, and/or executable. The symbolizing filter can usethis information to guess whether an address is a likely code addressor a likely data address in the given module. The remaining `%p` givesthe module relative address. For ELF files the module relative addresswill be the `p_vaddr` of the associated program header. For example ifyour module's executable segment has `p_vaddr=0x1000`, `p_memsz=0x1234`,and was loaded at 0x7acba69d5000 then you need to subtract 0x7acba69d4000from any address between 0x7acba69d5000 and 0x7acba69d6234 to get themodule relative address. The starting address will usually have beenrounded down to the active page size, and the size rounded up. 该子元素通知过滤器某个段是从模块加载的。该模块由其模块ID“％i”标识。 “％s”是字母“ r”，“ w”和“ x”中的一个或多个（以该顺序以及大写或小写形式），以指示该内存段是可读，可写和/或可执行的。符号过滤器可以使用此信息来猜测地址是给定模块中的可能的代码地址还是可能的数据地址。其余的'％p'给出模块的相对地址。对于ELF文件，模块的相对地址将是关联程序头的`p_vaddr'。例如，ifyour模块的可执行段具有“ p_vaddr = 0x1000”，“ p_memsz = 0x1234”，并加载到0x7acba69d5000，那么您需要从0x7acba69d5000和0x7acba69d6234之间的任何地址中减去0x7acba69d4000，以获取模块相对地址。起始地址通常会四舍五入为活动页面大小，并且将大小四舍五入。

  Example:  例：

  ```
  {{{mmap:0x7acba69d5000:0x5a000:load:1:rx:0x1000}}}
  ```
 

