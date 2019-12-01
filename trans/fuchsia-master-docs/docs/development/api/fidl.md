 
# FIDL API Rubric  FIDL API专栏 

[TOC]  [目录]

 
## General Advice  一般建议 

This section presents techniques, best practices, and general advice about defining protocols in the [Fuchsia Interface DefinitionLanguage](/docs/development/languages/fidl/README.md). 本节介绍了有关在[Fuchsia Interface DefinitionLanguage]（/ docs / development / languages / fidl / README.md）中定义协议的技术，最佳实践和一般建议。

 
### Protocols not objects  协议不是对象 

FIDL is a language for defining interprocess communication protocols.  Although the syntax resembles a definition of an object-oriented interface, the designconsiderations are more akin to network protocols than to object systems.  Forexample, to design a high-quality protocol, you need to consider bandwidth,latency, and flow control.  You should also consider that a protocol is morethan just a logical grouping of operations: a protocol also imposes a FIFOordering on requests and breaking a protocol into two smaller protocols meansthat requests made on the two different protocols can be reordered with respectto each other. FIDL是用于定义进程间通信协议的语言。尽管语法类似于面向对象接口的定义，但设计注意事项更类似于网络协议，而不是对象系统。例如，要设计高质量协议，您需要考虑带宽，延迟和流量控制。您还应该考虑一个协议，不仅仅是一个逻辑上的操作分组：一个协议还对请求强加了FIFO排序，并且将一个协议分成两个较小的协议意味着可以对两个不同协议上的请求进行重新排序。

 
### Focus on the types  专注于类型 

A good starting point for designing your FIDL protocol is to design the data structures your protocol will use.  For example, a FIDL protocol aboutnetworking would likely contain data structures for various types of IPaddresses and a FIDL protocol about graphics would likely contain datastructures for various geometric concepts.  You should be able to look at thetype names and have some intuition about the concepts the protocol manipulatesand how those concepts might be structured. 设计FIDL协议的一个很好的起点是设计协议将使用的数据结构。例如，关于网络的FIDL协议可能会包含各种IP地址类型的数据结构，关于图形的FIDL协议可能会包含各种几何概念的数据结构。您应该能够查看类型名称，并对协议操作的概念以及如何构造这些概念有一些直觉。

 
### Language neutrality  语言中立 

There are FIDL back ends for many different languages.  You should avoid over-specializing your FIDL definitions for any particular target language.Over time, your FIDL protocol is likely to be used by many different languages,perhaps even some languages that are not even supported today.  FIDL is theglue that holds the system together and lets Fuchsia support a wide variety oflanguages and runtimes.  If you over-specialize for your favorite language, youundermine that core value proposition. FIDL后端支持许多不同的语言。您应该避免针对任何特定目标语言过度专门化FIDL定义。随着时间的流逝，您的FIDL协议可能会被许多不同的语言使用，甚至某些语言甚至今天都不被支持。 FIDL是将系统结合在一起的胶水，它使Fuchsia支持多种语言和运行时。如果您过度专业化自己喜欢的语言，则会破坏该核心价值主张。

 
### Ordinals  普通人 

Protocols contain a number of methods.  Each method is automatically assigned a unique 32 bit identifier, called an ordinal.  Servers use the ordinal valueto determine which protocol method should be dispatched. 协议包含许多方法。每个方法都会自动分配一个唯一的32位标识符，称为序数。服务器使用序数值确定应调度哪种协议方法。

The compiler determines the ordinal value by hashing the library, protocol, and method name.  In rare cases, ordinals in the same protocol may collide.  Ifthis happens, you can use the `Selector` attribute to change the name of themethod the compiler uses for hashing.  The following example will use the methodname "C" instead of the method name "B" for calculating the hash: 编译器通过散列库，协议和方法名称来确定序数值。在极少数情况下，同一协议中的普通字符可能会发生冲突。如果发生这种情况，则可以使用“选择器”属性来更改编译器用于散列的方法的名称。下面的示例将使用方法名称“ C”而不是方法名称“ B”来计算哈希值：

```fidl
protocol A {
    [ Selector = "C" ]
    B(string s, bool b);
};
```
 

Selectors can also be used to maintain backwards compatibility with the wire format in cases where developers wish to change the name of a method. 在开发人员希望更改方法名称的情况下，选择器还可用于保持与有线格式的向后兼容性。

 
### Library structure  图书馆结构 

Carefully consider how you divide your type and protocol definitions into libraries.  How you decompose these definitions into libraries has a largeeffect on the consumers of these definitions because a FIDL library is the unitof dependency and distribution for your protocols. 仔细考虑如何将类型和协议定义划分为库。将这些定义分解为库的方式对这些定义的使用者有很大的影响，因为FIDL库是协议的依赖性和分布的单位。

The FIDL compiler requires that the dependency graph between libraries is a DAG, which means you cannot create a circular dependency across library boundaries.However, you can create (some) circular dependencies within a library. FIDL编译器要求库之间的依赖关系图是DAG，这意味着您无法跨库边界创建循环依赖关系，但是可以在库中创建（某些）循环依赖关系。

To decide whether to decompose a library into smaller libraries, consider the following questions: 要决定是否将一个库分解为较小的库，请考虑以下问题：

 
 * Do the customers for the library break down into separate roles that would want to use a subset of the functionality or declarations in the library?  Ifso, consider breaking the library into separate libraries that target eachrole. *库的客户是否分解为想要使用库中功能或声明子集的单独角色？如果是这样，请考虑将库分成针对每个角色的单独的库。

 
 * Does the library correspond to an industry concept that has a generally understood structure?  If so, consider structuring your library to match theindustry-standard structure.  For example, Bluetooth is organized into`fuchsia.bluetooth.le` and `fuchsia.bluetooth.gatt` to match how theseconcepts are generally understood in the industry.  Similarly,`fuchsia.net.http` corresponds to the industry-standard HTTP networkprotocol. *库是否符合具有公认结构的行业概念？如果是这样，请考虑构建您的库以匹配行业标准结构。例如，蓝牙被组织为“ fuchsia.bluetooth.le”和“ fuchsia.bluetooth.gatt”，以匹配业界对这些概念的一般理解。类似地，“ fuchsia.net.http”对应于行业标准的HTTP网络协议。

 
 * Do many other libraries depend upon the library?  If so, check whether those incoming dependencies really need to depend on the whole library or whetherthere is a "core" set of definitions that could be factored out of thelibrary to receive the bulk of the incoming dependencies. *是否还有许多其他图书馆依赖该图书馆？如果是这样，请检查这些传入依赖项是否真的需要依赖整个库，或者是否存在可以从库中分解出来以接收大量传入依赖项的“核心”定义集。

Ideally, we would produce a FIDL library structure for Fuchsia as a whole that is a global optimum.  However, Conway's law states that "organizations whichdesign systems \[...\] are constrained to produce designs which are copies ofthe communication structures of these organizations."  We should spend amoderate amount of time fighting Conway's law. 理想情况下，我们将为紫红色整体创建FIDL库结构，这是全球最佳的。但是，康韦定律指出“设计系统受其约束的组织只能制作出这些组织的通信结构的副本。”我们应该花一些时间与康威定律作斗争。

 
## Types  种类 

As mentioned under "general advice," you should pay particular attention to the types you used in your protocol definition. 如“一般建议”中所述，您应该特别注意协议定义中使用的类型。

 
### Be consistent  始终如一 

Use consistent types for the same concept.  For example, use a uint32 or a int32 for a particular concept consistently throughout your library.  If you create astruct for a concept, be consistent about using that struct to represent theconcept. 对同一概念使用一致的类型。例如，在整个库中始终对特定概念使用uint32或int32。如果您为一个概念创建一个结构，请在使用该结构表示该概念时保持一致。

Ideally, types would be used consistently across library boundaries as well. Check related libraries for similar concepts and be consistent with thoselibraries.  If there are many concepts shared between libraries, considerfactoring the type definitions for those concepts into a common library.  Forexample, `fuchsia.mem` and `fuchsia.math` contain many commonly used types forrepresenting memory and mathematical concepts, respectively. 理想情况下，类型也应跨库边界一致使用。检查相关的库以了解类似的概念，并与这些库保持一致。如果在库之间共享许多概念，请考虑将这些概念的类型定义分解为公共库。例如，“ fuchsia.mem”和“ fuchsia.math”包含许多常用类型，分别表示内存和数学概念。

 
### Prefer semantic types  首选语义类型 

Create structs to name commonly used concepts, even if those concepts could be represented using primitives.  For example, an IPv4 address is an importantconcept in the networking library and should be named using a struct eventhrough the data can be represented using a primitive: 创建结构以命名常用的概念，即使可以使用基元表示这些概念。例如，IPv4地址是网络库中的重要概念，即使可以使用原语表示数据，也应使用结构来命名它：

```fidl
struct Ipv4Address {
    array<uint8>:4 octets;
};
```
 

In performance-critical target languages, structs are represented in line, which reduces the cost of using structs to name important concepts. 在对性能至关重要的目标语言中，结构以行形式表示，这降低了使用结构命名重要概念的成本。

 
### Consider using fuchsia.mem.Buffer  考虑使用fuchsia.mem.Buffer 

A Virtual Memory Object (VMO) is a kernel object that represents a contiguous region of virtual memory.  VMOs track memory on a per-page basis, which means aVMO by itself does not track its size at byte-granularity.  When sending memoryin a FIDL message, you will often need to send both a VMO and a size.  Ratherthan sending these primitives separately, consider using `fuchsia.mem.Buffer`,which combines these primitives and names this common concept. 虚拟内存对象（VMO）是一个内核对象，代表虚拟内存的连续区域。 VMO每页跟踪一次内存，这意味着aVMO本身不会以字节粒度跟踪其大小。在FIDL消息中发送内存时，通常需要同时发送VMO和大小。与其单独发送这些原语，不如考虑使用“ fuchsia.mem.Buffer”，它结合了这些原语并命名了这个通用概念。

 
### Specify bounds for vector and string  指定向量和字符串的界限 

All `vector` and `string` declarations should specify a length bound. Declarations generally fall into one of two categories: 所有的`vector`和`string`声明都应指定长度限制。声明通常分为两类之一：

 
* There is a constraint inherent to the data. For example, a string containing a filesystem name component must not be longer than`fuchsia.io.MAX_FILENAME`. *数据固有的约束。例如，包含文件系统名称组件的字符串不得超过`fuchsia.io.MAX_FILENAME`。
* There is no constraint other than "as much as possible." In these cases, you should use the built-in constant `MAX`. *除了“尽可能”以外没有其他限制。在这种情况下，您应该使用内置的常量“ MAX”。

Whenever you use `MAX`, consider whether the receiver of the message would really want to process arbitrarily long sequences or whether extremely longsequences represent abuse. 每当您使用“ MAX”时，请考虑消息的接收者是否真的想处理任意长序列，或者极端长序列是否表示滥用。

Bear in mind that all declarations are implicitly bounded by the maximum message length when sent over a `zx::channel`. If there really are use cases forarbitrarily long sequences, simply using `MAX` might not address those use casesbecause clients that attempt to provide extremely long sequences might hit themaximum message length. 请记住，在通过`zx :: channel`发送时，所有声明都以最大消息长度为隐式限制。如果确实存在任意长序列的用例，则仅使用MAX可能无法解决这些用例，因为尝试提供极长序列的客户端可能会达到最大消息长度。

To address use cases with arbitrarily large sequences, consider breaking the sequence up into multiple messages using one of the pagination patternsdiscussed below or consider moving the data out of the message itself, forexample into a `fuchsia.mem.Buffer`. 为了处理具有任意大序列的用例，请考虑使用下面讨论的一种分页模式将序列分解为多条消息，或者考虑将数据移出消息本身，例如移至“ fuchsia.mem.Buffer”中。

 
### String encoding, string contents, and length bounds  字符串编码，字符串内容和长度范围 

FIDL `string`s are encoded in [UTF-8](https://en.wikipedia.org/wiki/UTF-8), a variable-width encoding that uses 1, 2, 3, or 4 bytes per[Unicode code point](http://unicode.org/glossary/#code_point). FIDL`string's编码为[UTF-8]（https://en.wikipedia.org/wiki/UTF-8），一种可变宽度编码，每个[Unicode使用1、2、3或4个字节代码点]（http://unicode.org/glossary/code_point）。

Bindings enforce valid UTF-8 for strings, and strings are therefore not appropriate for arbitrary binary data. See[Should I use string or vector?](#should-i-use-string-or-vector). 绑定对字符串强制使用有效的UTF-8，因此字符串不适用于任意二进制数据。请参阅[我应该使用字符串还是向量？]（我应该使用字符串还是向量）。

Because the purpose of length bound declarations is to provide an easily calculable upper bound on the total byte size of a FIDL message, `string` boundsspecify the maximum _number of bytes_ in the field. To be on the safe side, youwill generally want to budget <code>(4 bytes · <var>code points instring</var>)</code>. (If you know for certain that the text only uses codepoints in the single-byte ASCII range, as in the case of phone numbers or creditcard numbers, 1 byte per code point will be sufficient.) 因为长度限制声明的目的是在FIDL消息的总字节大小上提供易于计算的上限，所以“ string”界限指定字段中的最大字节数。为了安全起见，通常需要预算<code>（4字节·<var> instring </ var>个代码点）</ code>。 （如果您确定文本仅使用单字节ASCII范围内的代码点，例如电话号码或信用卡号，则每个代码点1个字节就足够了。）

How many code points are in a string? This question can be complicated to answer, particularly for user-generated string contents, because there is notnecessarily a one-to-one correspondence between a Unicode code point and whatusers might think of as "characters". 字符串中有多少个代码点？这个问题的回答可能很复杂，尤其是对于用户生成的字符串内容而言，因为Unicode代码点与用户可能认为的“字符”之间不一定存在一一对应的关系。

For example, the string  例如，字符串

```none
á
```
 

is rendered as a single user-perceived "character", but actually consists of two code points: 呈现为单个用户感知的“字符”，但实际上包含两个代码点：

```
1. LATIN SMALL LETTER A (U+0061)
2. COMBINING ACUTE ACCENT (U+0301)
```
 

In Unicode terminology, this kind of user-perceived "character" is known as a [grapheme cluster](https://unicode.org/reports/tr29/#Grapheme_Cluster_Boundaries). 在Unicode术语中，这种用户感知的“字符”被称为[字素群集]（https://unicode.org/reports/tr29/Grapheme_Cluster_Boundaries）。

A single grapheme cluster can consist of arbitrarily many code points. Consider this longer example: 单个字素簇可以包含任意多个代码点。考虑下面的示例：

```none
á🇨🇦b👮🏽‍♀️
```
 

If your system and fonts support it, you should see **four grapheme clusters** above: 如果您的系统和字体支持它，您应该在上面看到“四个字素簇”：

```
1. 'a' with acute accent
2. emoji of Canadian flag
3. 'b'
4. emoji of a female police officer with a medium skin tone
```
 

These four grapheme clusters are encoded as **ten code points**:  这四个字素簇编码为“十个代码点”：

```
 1. LATIN SMALL LETTER A (U+0061)
 2. COMBINING ACUTE ACCENT (U+0301)
 3. REGIONAL INDICATOR SYMBOL LETTER C (U+1F1E8)
 4. REGIONAL INDICATOR SYMBOL LETTER A (U+1F1E6)
 5. LATIN SMALL LETTER B (U+0062)
 6. POLICE OFFICER (U+1F46E)
 7. EMOJI MODIFIER FITZPATRICK TYPE-4 (U+1F3FD)
 8. ZERO WIDTH JOINER (U+200D)
 9. FEMALE SIGN (U+2640)
10. VARIATION SELECTOR-16 (U+FE0F)
```
 

In UTF-8, this string takes up **28 bytes**.  在UTF-8中，此字符串占用** 28个字节**。

From this example, it should be clear that if your application's UI displays a text input box that allows _N_ arbitrary grapheme clusters (what users think ofas "characters"), and you plan to transport those user-entered strings overFIDL, you will have to budget _some multiple_ of <code>4·<var>N</var></code> inyour FIDL `string` field. 从此示例中可以清楚地看到，如果您的应用程序的UI显示一个文本输入框，该输入框允许_N_个任意字形簇（用户认为是“字符”），并且您计划通过FIDL传输这些用户输入的字符串，在FIDL“字符串”字段中，预算为<code> 4·<var> N </ var> </ code>的某个倍数。

What should that multiple be? It depends on your data. If you're dealing with a fairly constrained use case (e.g. human names, postal addresses, credit cardnumbers), you might be able to assume 1-2 code points per grapheme cluster. Ifyou're building a chat client where emoji use is rampant, 4-5 code points pergrapheme cluster might be safer. In any case, your input validation UI shouldshow clear visual feedback so that users aren't surprised if they run out ofroom. 这个倍数应该是多少？这取决于您的数据。如果您要处理相当有限的用例（例如人名，邮政地址，信用卡号），则每个字素簇可以假设1-2个代码点。如果您要建立一个聊天客户端，其中表情符号的使用非常普遍，那么4-5个代码点的字母字形群集可能会更安全。无论如何，您的输入验证UI都应该显示清晰的视觉反馈，以便用户在没有空间的情况下也不会感到惊讶。

 
### Integer types  整数类型 

Select an integer type appropriate for your use case and be consistent about how you use them.  If your value is best thought of as a byte of data, use `byte`.If a negative value has no meaning, use an unsigned type.  As a rule of thumb ifyou're unsure, use 32-bit values for small quantities and 64-bit values forlarge ones. 选择适合您的用例的整数类型，并在使用方式上保持一致。如果最好将您的值视为数据的字节，则使用`byte`。如果负值无意义，请使用无符号类型。根据经验，如果不确定，请对少量使用32位值，对于较大的使用64位值。

 
### How should I represent errors?  我应该如何表示错误？ 

Select the appropriate error type for your use case and be consistent about how you report errors. 为您的用例选择适当的错误类型，并在报告错误方面保持一致。

Use the `status` type for errors related to kernel objects or IO.  For example, `fuchsia.process` uses `status` because the library is largely concerned withmanipulating kernel objects.  As another example, `fuchsia.io` uses `status`extensively because the library is concerned with IO. 使用`status'类型来处理与内核对象或IO相关的错误。例如，`fuchsia.process`使用`status`，因为该库在很大程度上与操纵内核对象有关。再举一个例子，因为库与IO有关，fuchsia.io广泛使用status。

Use a domain-specific enum error type for other domains.  For example, use an enum when you expect clients to receive the error and then stop rather thanpropagate the error to another system. 对其他域使用特定于域的枚举错误类型。例如，当您希望客户端收到错误时使用一个枚举，然后停止而不是传播错误到另一个系统。

There are two patterns for methods that can return a result or an error:  可以返回结果或错误的方法有两种模式：

 
 * Prefer using the `error` syntax to clearly document and convey a possible erroneous return, and take advantage of tailored target languagebindings; *首选使用“错误”语法来清楚地记录和传达可能的错误返回，并利用量身定制的目标语言绑定；

 
 * Use the [optional value with error enum](#using-optional-value-with-error-enum)for cases when you need maximal performance. *如果需要最大性能，请使用[带有错误枚举的可选值]（使用带有错误枚举的可选值）。

The performance difference between the [error syntax](#using-the-error-syntax) vs [optional value with error enum](#using-optional-value-with-error-enum) aresmall: [错误语法]（使用错误语法）与[带有错误枚举的可选值]（使用带有错误枚举的可选值）之间的性能差异很小：

 
  * Slightly bigger payload (8 extra bytes for values, 16 extra bytes for errors); *有效负载稍大（值多8个字节，错误多16个字节）；
  * Since the value and error will be in an envelope, there is additional work to record/verify the number of bytes and number of handles; *由于值和错误将包含在信封中，因此需要进行额外的工作来记录/验证字节数和句柄数；
  * Both will represent the value out-of-line, and therefore require a pointer indirection. *两者都将代表离线值，因此需要间接指针。

 
#### Using the error syntax  使用错误语法 

Methods can take an optional `error <type>` specifier to indicate that they return a value, or error out and produce `<type>`. Here is an example: 方法可以使用可选的`error <type>`指示符来指示它们返回一个值，或者出错并产生`<type>`。这是一个例子：

```fidl
// Only erroneous status are listed
enum MyErrorCode {
    MISSING_FOO = 1;  // avoid using 0
    NO_BAR = 2;
    ...
};

protocol Frobinator {
    1: Frobinate(...) -> (FrobinateResult value) error MyErrorCode;
};
```
 

When using this pattern, you can either use an `int32`, `uint32`, or an enum thereof to represent the kind of error returned. In most cases, returning anenum is the preferred approach. As noted in the [enum](#enum) section, it is bestto avoid using the value `0`. 使用此模式时，可以使用`int32`，`uint32`或其枚举来表示返回的错误类型。在大多数情况下，首选的方法是返回肛门。如[enum]（enum）部分所述，最好避免使用值“ 0”。

 
#### Using optional value with error enum  使用带有错误枚举的可选值 

When maximal performance is required, defining a method with two returns, an optional value and an error code, is common practice. See for instance: 当需要最佳性能时，通常的做法是定义一个带有两个返回值，可选值和错误代码的方法。参见例如：

```fidl
enum MyErrorCode {
    OK = 0;               // The success value should be 0,
    MISSING_FOO = 1;      // with erroneous status next.
    NO_BAR = 2;
    ...
};

protocol Frobinator {
    1: Frobinate(...) -> (FrobinateResult? value, MyErrorCode err);
};
```
 

When using this pattern, returning an enum is the preferred approach. Here, defining the `0` value as the "success" is best. For further details, referto the [enum](#enum) section. 使用此模式时，返回枚举是首选方法。这里，最好将“ 0”值定义为“成功”。有关更多详细信息，请参见[enum]（enum）部分。

 
#### Avoid messages and descriptions in errors  避免错误的消息和描述 

In some unusual situations, protocols may include a string description of the error in addition to a `status` or enum value if the range of possible errorconditions is large and descriptive error messages are likely to be useful toclients.  However, including a string invites difficulties.  For example,clients might try to parse the string to understand what happened, which meansthe exact format of the string becomes part of the protocol, which isespecially problematic when the strings are[localized](#localizing-strings-and-error-messages). 在某些不常见的情况下，如果可能的错误条件的范围很大并且描述性错误消息可能对客户端有用，则协议除了“状态”或枚举值外还可能包含错误的字符串描述。但是，包含字符串会带来困难。例如，客户可能尝试解析字符串以了解发生了什么，这意味着字符串的确切格式成为协议的一部分，当字符串被[localized]（localizing-strings-and-error-messages）时，这尤其成问题。

*Security note:* Similarly, reporting stack traces or exception messages to the client canunintentionally leak privileged information. *安全说明：*同样，向客户端报告堆栈跟踪或异常消息可能会无意间泄露特权信息。

 
### Localizing strings and error messages  本地化字符串和错误消息 

If you are building a service that acts as a backend for a UI, use structured, typed messages, and leave the rendering to the UI layer. 如果您要构建充当UI后端的服务，请使用结构化的类型化消息，并将呈现内容留给UI层。

If all your messages are simple and unparameterized, use `enum`s for error reporting and general UI strings. For more detailed messages, with parameterssuch as names, numbers, and locations, use `table`s or `xunion`s, and passthe parameters as string or numeric fields. 如果所有消息都是简单且未参数化的，请使用`enum`进行错误报告和常规UI字符串。有关带有名称，数字和位置等参数的更详细的消息，请使用“ table”或“ xunion”，并将参数作为字符串或数字字段传递。

It may be tempting to generate messages (in English) in the service and provide them to the UI as strings—the UI just receives a string and pops up anotification or error dialog box. 在服务中生成消息（英文）并将它们作为字符串提供给UI可能很诱人-UI仅接收字符串并弹出通知或错误对话框。

However, this simpler approach has some serious drawbacks:  但是，这种较简单的方法存在一些严重的缺点：

 
* Does your service know what locale (language and region) is being used in the UI? You would either have to pass the locale with each request (see[example][locale-passing-example]), or keep track of state for each connectedclient, in order to provide messages in the right language. *您的服务是否知道UI中使用的语言环境（语言和区域）？您可能必须随每个请求传递语言环境（请参阅[example] [locale-passing-example]），或跟踪每个已连接客户端的状态，以便以正确的语言提供消息。
* Does your service's development environment have good support for localization? If you're writing in C++, you have easy access to the<abbr title="International Components for Unicode">ICU</abbr> library and`MessageFormat`, but if you're using Rust, library support is currently muchmore limited. *您的服务的开发环境是否对本地化提供了良好的支持？如果您使用C ++编写，则可以轻松访问<abbr title =“ Unicode的国际组件”> ICU </ abbr>库和MessageFormat，但是，如果您使用的是Rust，则库支持目前受到限制。
* Do any of your error messages need to include parameters that are known to the UI but not to the service? *您的任何错误消息是否都需要包含UI已知但服务不知道的参数？
* Does your service only serve a single UI implementation? Does the service know how much space the UI has to display a message? *您的服务仅服务于单个UI实现吗？服务是否知道UI显示消息需要多少空间？
* Are errors only displayed as text? You might also need error-specific alert icons, sound effects, or text-to-speech hints. *错误仅显示为文本吗？您可能还需要特定于错误的警报图标，声音效果或文本语音转换提示。
* Could the user change the display locale while the UI is still running? If this happens, pre-localized strings might be difficult to update to the newlocale, particularly if they were the result of some non-idempotent operation. *用户可以在UI仍在运行时更改显示区域设置吗？如果发生这种情况，预本地化的字符串可能很难更新到新的语言环境，尤其是如果它们是某些非幂等操作的结果。

Unless you are building a highly specialized service that is tightly coupled to a _single UI implementation_, you probably shouldn't expose user-visible UIstrings in your FIDL service. 除非您要构建与_single UI实施紧密结合的高度专业化的服务，否则您不应该在FIDL服务中公开用户可见的UIstring。

 
### Should I define a struct to encapsulate method parameters (or responses)?  我应该定义一个结构来封装方法参数（或响应）吗？ 

Whenever you define a method, you need to decide whether  to pass parameters individually or to encapsulate the parameters in a struct.  Making the bestchoice involves balancing several factors.  Consider the questions below to helpguide your decision making: 无论何时定义方法，都需要决定是单独传递参数还是将参数封装在结构中。做出最佳选择涉及平衡多个因素。考虑以下问题，以帮助指导您的决策：

 
 * Is there a meaningful encapsulation boundary?  If a group of parameters makes sense to pass around as a unit because they have some cohesion beyond thismethod, you might want to encapsulate those parameters in a struct.(Hopefully, you have already identified these cohesive groups when youstarted designing your protocol because you followed the "general advice"above and focused on the types early on.) *是否有有意义的封装边界？如果一组参数可以作为一个单元传递，因为它们具有超出此方法的内聚性，则您可能希望将这些参数封装在一个结构中。（希望您在开始设计协议时就已经确定了这些内聚性组，因为您遵循上方的“一般建议”，并着重于早期的类型。）

 
 * Would the struct be useful for anything beyond the method being called?  If not, consider passing the parameters separately. *该结构对除调用方法之外的任何其他东西有用吗？如果不是，请考虑分别传递参数。

 
 * Are you repeating the same groups of parameters in many methods?  If so, consider grouping those parameters into one or more structures.  You mightalso consider whether the repetition indicates that these parameters arecohesive because they represent some important concept in your protocol. *您是否在许多方法中重复相同的参数组？如果是这样，请考虑将这些参数分组为一个或多个结构。您可能还会考虑重复是否表明这些参数是内聚的，因为它们代表了协议中的一些重要概念。

 
 * Are there a large number of parameters that are optional or otherwise are commonly given a default value?  If so, consider using use a struct to reduceboilerplate for callers. *是否有大量可选参数，否则通常会给其默认值？如果是这样，请考虑使用结构减少调用者的样板。

 
 * Are there groups of parameters that are always null or non-null at the same time?  If so, consider grouping those parameters into a nullable struct toenforce that invariant in the protocol itself.  For example, the`FrobinateResult` struct defined above contains values that are always nullat the same time when `error` is not `MyError.OK`. *是否存在同时总是为null或非null的参数组？如果是这样，请考虑将这些参数分组为可为空的结构，以增强协议本身的不变性。例如，上面定义的“ FrobinateResult”结构包含的值总是在“ error”不是“ MyError.OK”时同时为空。

 
### Should I use string or bytes?  我应该使用字符串还是字节？ 

In FIDL, `string` data must be valid UTF-8, which means strings can represent sequences of Unicode code points but cannot represent arbitrary binary data.  Incontrast, `bytes` or `array<uint8>` can represent arbitrary binary data and donot imply Unicode. 在FIDL中，“字符串”数据必须是有效的UTF-8，这意味着字符串可以表示Unicode代码点的序列，但不能表示任意二进制数据。相反，“字节”或“数组<uint8>”可以表示任意二进制数据，并不表示Unicode。

Use `string` for text data:  将`string`用于文本数据：

 
 * Use `string` to represent package names because package names are required to be valid UTF-8 strings (with certain excluded characters). *使用“字符串”来表示软件包名称，因为软件包名称必须是有效的UTF-8字符串（带有某些排除的字符）。

 
 * Use `string` to represent file names within packages because file names within packages are required to be valid UTF-8 strings (with certain excludedcharacters). *使用“字符串”来表示软件包中的文件名，因为软件包中的文件名必须是有效的UTF-8字符串（带有某些排除的字符）。

 
 * Use `string` to represent media codec names because media codec names are selected from a fixed vocabulary of valid UTF-8 strings. *使用“字符串”来表示媒体编解码器名称，因为媒体编解码器名称是从有效的UTF-8字符串的固定词汇表中选择的。

 
 * Use `string` to represent HTTP methods because HTTP methods are comprised of a fixed selection of characters that are always valid UTF-8. *使用`string`表示HTTP方法，因为HTTP方法由固定选择的字符组成，这些字符始终是有效的UTF-8。

Use `bytes` or `array<uint8>` for small non-text data:  对于小型非文本数据，请使用“字节”或“数组<uint8>”：

 
 * Use `bytes` for HTTP header fields because HTTP header fields do not specify an encoding and therefore cannot necessarily be represented in UTF-8. *对HTTP标头字段使用“字节”，因为HTTP标头字段未指定编码，因此不一定以UTF-8表示。

 
 * Use `array<uint8>:6` for MAC addresses because MAC address are binary data.  *对MAC地址使用`array <uint8>：6`，因为MAC地址是二进制数据。

 
 * Use `array<uint8>:16` for UUIDs because UUIDs are (almost!) arbitrary binary data. *对UUID使用`array <uint8>：16`，因为UUID是（几乎！）任意二进制数据。

Use shared-memory primitives for blobs:  对blob使用共享内存原语：

 
 * Use `fuchsia.mem.Buffer` for images and (large) protobufs, when it makes sense to buffer the data completely. *当有意义地完全缓冲数据时，对图像和（大型）protobuf使用`fuchsia.mem.Buffer`。
 * Use `handle<socket>` for audio and video streams because data may arrive over time, or when it makes sense to process data before completely written oravailable. *对音频和视频流使用`handle <socket>`，因为数据可能会随时间到达，或者在完全写入或可用之前处理数据有意义。

 
### Should I use vector or array?  我应该使用向量还是数组？ 

A `vector` is a variable-length sequence that is represented out-of-line in the wire format.  An `array` is a fixed-length sequence that is represented in-linein the wire format. “ vector”是一个可变长度序列，以有线格式离线表示。 “ array”是固定长度的序列，以wire格式在线表示。

Use `vector` for variable-length data:  对可变长度数据使用`vector`：

 
 * Use `vector` for tags in log messages because log messages can have between zero and five tags. *对日志消息中的标签使用`vector`，因为日志消息可以具有零到五个标签。

Use `array` for fixed-length data:  将`array`用于固定长度的数据：

 
 * Use `array` for MAC addresses because a MAC address is always six bytes long.  *对MAC地址使用`array`，因为MAC地址总是6个字节长。

 
### Should I use a struct or a table?  我应该使用结构还是表格？ 

Both structs and tables represent an object with multiple named fields. The difference is that structs have a fixed layout in the wire format, which meansthey *cannot* be modified without breaking binary compatibility. By contrast,tables have a flexible layout in the wire format, which means fields *can* beadded to a table over time without breaking binary compatibility. 结构和表都代表具有多个命名字段的对象。不同之处在于，结构以有线格式具有固定的布局，这意味着*在不破坏二进制兼容性的情况下不能对其进行修改。相比之下，表具有有线格式的灵活布局，这意味着可以在不破坏二进制兼容性的情况下将字段*随时间添加到表中。

Use structs for performance-critical protocol elements or for protocol elements that are very unlikely to change in the future. For example, use a struct torepresent a MAC address because the structure of a MAC address is very unlikelyto change in the future. 将结构用于对性能至关重要的协议元素或将来不太可能更改的协议元素。例如，使用结构体表示MAC地址，因为MAC地址的结构将来极不可能更改。

Use tables for protocol elements that are likely to change in the future.  For example, use a table to represent metadata information about camera devicesbecause the fields in the metadata are likely to evolve over time. 将表用于将来可能更改的协议元素。例如，使用表来表示有关相机设备的元数据信息，因为元数据中的字段可能会随时间变化。

 
### How should I represent constants?  我应该如何表示常数？ 

There are three ways to represent constants, depending on the flavor of constant you have: 有三种表示常量的方式，具体取决于您拥有的常量的种类：

 
1. Use `const` for special values, like **PI**, or **MAX_NAME_LEN**.  1.使用const作为特殊值，例如** PI **或** MAX_NAME_LEN **。
2. Use `enum` when the values are elements of a set, like the repeat mode of a media player: **OFF**, **SINGLE_TRACK**, or **ALL_TRACKS**. 2.当值是集合的元素时，请使用“枚举”，例如媒体播放器的重复模式：** OFF **，** SINGLE_TRACK **或** ALL_TRACKS **。
3. Use `bits` for constants forming a group of flags, such as the capabilities of an interface: **WLAN**, **SYNTH**, and **LOOPBACK**. 3.将“位”用于构成一组标志的常量，例如接口的功能：WLAN，** SYNTH **和** LOOPBACK **。

 
#### const  const 

Use a `const` when there is a value that you wish to use symbolically rather than typing the value every time.The classical example is **PI** &mdash; it's often coded as a `const`because it's convenient to not have to type `3.141592653589` every timeyou want to use this value. 当您希望使用一个象征性的值而不是每次都键入该值时，请使用const。经典示例是** PI ** mdash;。它通常被编码为const，因为每次使用此值时不必键入3.141592653589都很方便。

Alternatively, you may use a `const` when the value may change, but needs to otherwise be used consistently throughout.A maximum number of characters that can be supplied in a given field isa good example (e.g., **MAX_NAME_LEN**).By using a `const`, you centralize the definition of that number, andthus don't end up with different values throughout your code. 另外，当值可能改变时，您可以使用const，但是在整个过程中都必须一致使用。在给定字段中可以提供的最大字符数就是一个很好的示例（例如** MAX_NAME_LEN **）。通过使用const，您可以集中定义该数字，因此在整个代码中最终不会得到不同的值。

Another reason to choose `const` is that you can use it both to constrain a message, and then later on in code.For example: 选择const的另一个原因是可以同时使用它来约束一条消息，然后再在代码中使用它，例如：

```fidl
const int32 MAX_BATCH_SIZE = 128;

protocol Sender {
    Emit(vector<uint8>:MAX_BATCH_SIZE batch);
};
```
 

You can then use the constant `MAX_BATCH_SIZE` in your code to assemble batches. 然后，您可以在代码中使用常量MAX_BATCH_SIZE来组装批处理。

 
#### enum  枚举 

Use an enum if the set of enumerated values is bounded and controlled by the Fuchsia project.  For example, the Fuchsia project defines the pointer eventinput model and therefore controls the values enumerated by `PointerEventPhase`. 如果枚举值集受Fuchsia项目限制和控制，请使用枚举。例如，紫红色项目定义了指针事件输入模型，因此控制了PointerEventPhase枚举的值。

In some scenarios, you should use an enum even if the Fuchsia project itself does not control the set of enumerated values if we can reasonably expect thatpeople who will want to register new values will submit a patch to the Fuchsiasource tree to register their values.  For example, texture formats need to beunderstood by the Fuchsia graphics drivers, which means new texture formats canbe added by developers working on those drivers even if the set of textureformats is controlled by the graphics hardware vendors.  As a counter example,do not use an enum to represent HTTP methods because we cannot reasonably expectpeople who use novel HTTP methods to submit a patch to the Platform Source Tree. 在某些情况下，即使Fuchsia项目本身不控制枚举值的集合，您也应该使用一个枚举，如果我们可以合理地期望那些想要注册新值的人将向Fuchsiasource树提交补丁来注册其值。例如，Fuchsia图形驱动程序需要理解纹理格式，这意味着即使纹理格式集由图形硬件供应商控制，开发人员也可以通过使用这些驱动程序的开发人员添加新的纹理格式。作为反例，请勿使用枚举来表示HTTP方法，因为我们不能合理地期望使用新颖HTTP方法的人向平台源树提交补丁。

For _a priori_ unbounded sets, a `string` might be a more appropriate choice if you foresee wanting to extend the set dynamically.  For example, use a `string`to represent media codec names because intermediaries might be able to dosomething reasonable with a novel media codec name. 对于先验的无边界集合，如果您希望动态扩展集合，则“字符串”可能是更合适的选择。例如，使用“字符串”来表示媒体编解码器名称，因为中介可能可以使用新颖的媒体编解码器名称来做一些合理的事情。

If the set of enumerated values is controlled by an external entity, use an integer (of an appropriate size) or a `string`.  For example, use an integer (ofsome size) to represent USB HID identifiers because the set of USB HIDidentifiers is controlled by an industry consortium.  Similarly, use a `string`to represent a MIME type because MIME types are controlled (at least in theory)by an IANA registry. 如果一组枚举值由外部实体控制，则使用整数（适当大小）或“字符串”。例如，使用整数（一定大小）来表示USB HID标识符，因为USB HIDidentifier的集合由行业协会控制。类似地，使用“字符串”来表示MIME类型，因为MIME类型（至少在理论上）是由IANA注册机构控制的。

We recommend that, where possible, developers avoid use of `0` as an enum value. Because many target languages use `0` as the default value for integers, it canbe difficult for to distinguish whether a `0` value was set intentionally, orinstead was set because it is the default. For instance, the`fuchsia.module.StoryState` defines three values:  `RUNNING` with value `1`,`STOPPING` with value `2`, and `STOPPED` with value `3`. 我们建议开发人员尽可能避免将“ 0”用作枚举值。由于许多目标语言使用“ 0”作为整数的默认值，因此很难区分是故意设置还是“ 0”值是默认设置。例如，`fuchsia.module.StoryState`定义了三个值：具有值1的RUNNING，具有值2的STOPPING和具有值3的STOPPED。

There are two cases where using the value `0` is appropriate:  在两种情况下，使用值'0'是合适的：

 
  * The enum has a natural default, initial, or unknown state;  *枚举具有自然的默认，初始或未知状态；

 
  * The enum defines an error code used in the [optional value with error enum](#using-optional-value-with-error-enum)pattern. *枚举定义了在[带错误枚举的可选值]（使用带有错误枚举的可选值）模式中使用的错误代码。

 
#### bits  位 

If your protocol has a bitfield, represent its values using `bits` values (for details, see [`FTP-025`: "Bit Flags."][ftp-025]) 如果您的协议具有位字段，请使用“位”值表示其值（有关详细信息，请参见[FTP-025：“位标志”。] [ftp-025]）

For example:  例如：

```fidl
// Bit definitions for Info.features field

bits InfoFeatures : uint32 {
    WLAN = 0x00000001;      // If present, this device represents WLAN hardware
    SYNTH = 0x00000002;     // If present, this device is synthetic (not backed by h/w)
    LOOPBACK = 0x00000004;  // If present, this device receives all messages it sends
};
```
 

This indicates that the `InfoFeatures` bit field is backed by an unsigned 32-bit integer, and then goes on to define the three bits that are used. 这表明“ InfoFeatures”位字段由一个无符号的32位整数支持，然后继续定义所使用的三个位。

You can also express the values in binary (as opposed to hex) using the `0b` notation: 您还可以使用`0b`表示法以二进制形式（而不是十六进制）表示值：

```fidl
bits InfoFeatures : uint32 {
    WLAN =     0b00000001;  // If present, this device represents WLAN hardware
    SYNTH =    0b00000010;  // If present, this device is synthetic (not backed by h/w)
    LOOPBACK = 0b00000100;  // If present, this device receives all messages it sends
};
```
 

This is the same as the previous example.  这与前面的示例相同。

 
## Good Design Patterns  好的设计模式 

This section describes several good design patterns that recur in many FIDL protocols. 本节描述了许多FIDL协议中重复出现的几种良好的设计模式。

 
### Protocol request pipelining  协议请求流水线 

One of the best and most widely used design patterns is _protocol request pipelining_.  Rather than returning a channel that supports a protocol, theclient sends the channel and requests the server to bind an implementation ofthe protocol to that channel: 最佳和最广泛使用的设计模式之一是_protocol request pipelining_。客户端不返回支持协议的通道，而是发送该通道并请求服务器将协议的实现绑定到该通道：

```fidl
GOOD:
protocol Foo {
    GetBar(string name, request<Bar> bar);
};

BAD:
protocol Foo {
    GetBar(string name) -> (Bar bar);
};
```
 

This pattern is useful because the client does not need to wait for a round-trip before starting to use the `Bar` protocol.  Instead, the client can queuemessages for `Bar` immediately.  Those messages will be buffered by the kerneland processed eventually once an implementation of `Bar` binds to the protocolrequest.  By contrast, if the server returns an instance of the `Bar` protocol,the client needs to wait for the whole round-trip before queuing messages for`Bar`. 这种模式很有用，因为客户端在开始使用Bar协议之前不需要等待往返。相反，客户端可以立即将“ Bar”的消息排队。这些消息将由内核缓冲，并在将“ Bar”的实现绑定到协议请求后最终进行处理。相反，如果服务器返回Bar协议的实例，则客户端需要等待整个往返，然后再为Bar消息排队。

If the request is likely to fail, consider extending this pattern with a reply that describes whether the operation succeeded: 如果请求可能失败，请考虑通过描述操作是否成功的回复扩展此模式：

```fidl
protocol CodecProvider {
    TryToCreateCodec(CodecParams params, request<Codec> codec) -> (bool succeed);
};
```
 

To handle the failure case, the client waits for the reply and takes some other action if the request failed.  Another approach is for the protocol to have anevent that the server sends at the start of the protocol: 为了处理失败情况，客户端等待答复，如果请求失败，则采取其他措施。协议的另一种方法是让服务器在协议开始时发送一个事件：

```fidl
protocol Codec2 {
    -> OnReady();
};

protocol CodecProvider2 {
    TryToCreateCodec(CodecParams params, request<Codec2> codec);
};
```
 

To handle the failure case, the client waits for the `OnReady` event and takes some other action if the `Codec2` channel is closed before the event arrives. 为了处理故障情况，客户端等待OnReady事件，如果在事件到达之前关闭Codec2通道，则采取其他措施。

However, if the request is likely to succeed, having either kind of success signal can be harmful because the signal allows the client to distinguishbetween different failure modes that often should be handled in the same way.For example, the client should treat a service that fails immediately afterestablishing a connection in the same way as a service that cannot be reached inthe first place.  In both situations, the service is unavailable and the clientshould either generate an error or find another way to accomplishing its task. 但是，如果请求很可能成功，则使用任何一种成功信号都可能是有害的，因为该信号使客户端可以区分通常应以相同方式处理的不同失败模式，例如，客户端应将服务视为在建立连接后立即失败，其连接方式与最初无法到达的服务相同。在这两种情况下，服务均不可用，客户端应生成错误或找到另一种方法来完成其任务。

 
### Flow Control  流量控制 

FIDL messages are buffered by the kernel.  If one endpoint produces more messages than the other endpoint consumes, the messages will accumulate in thekernel, taking up memory and making it more difficult for the system to recover.Instead, well-designed protocols should throttle the production of messages tomatch the rate at which those messages are consumed, a property known as _flowcontrol_. FIDL消息由内核缓冲。如果一个端点产生的消息多于另一端点消耗的消息，则这些消息将在内核中累积，占用内存，并使系统更难以恢复，相反，设计良好的协议应限制消息的产生以匹配速率这些消息被消耗，称为_flowcontrol_的属性。

The kernel provides some amount of flow control in the form of back pressure on channels.  However, most protocols should have protocol-level flow control anduse channel back pressure as a backstop to protect the rest of the system whenthe protocol fails to work as designed. 内核以通道背压的形式提供了一些流量控制。但是，大多数协议都应具有协议级别的流量控制，并在协议无法按设计工作时使用通道背压作为支撑，以保护系统的其余部分。

Flow control is a broad, complex topic, and there are a number of effective design patterns.  This section discusses some of the more popular flow controlpatterns but is not exhaustive. The patterns are listed in descending order ofpreference. If one of these patterns works well for a particular use case itshould be used but if not protocols are free to use alternative flow controlmechanisms that are not listed below. 流量控制是一个广泛而复杂的主题，并且有许多有效的设计模式。本节讨论一些较流行的流量控制模式，但并不详尽。模式按优先顺序降序列出。如果这些模式之一对于特定用例运行良好，则应使用它，但如果没有，则协议可以自由使用未在下面列出的替代流控制机制。

 
#### Prefer pull to push  更喜欢拉推 

Without careful design, protocols in which the server pushes data to the client often have poor flow control.  One approach to providing better flow control isto have the client pull one or a range from the server.  Pull models havebuilt-in flow control since the client naturally limits the rate at which theserver produces data and avoids getting overwhelmed by messages pushed from theserver. 如果不进行仔细的设计，服务器将数据推送到客户端的协议通常会具有较差的流控制。提供更好的流控制的一种方法是让客户端从服务器拉一个或一个范围。 Pull模型具有内置的流控制功能，因为客户端自然会限制服务器生成数据的速率，并避免被服务器推送的消息淹没。

 
#### Delay responses using hanging gets  使用悬挂获取延迟响应 

A simple way to implement a pull-based protocol is to "park a callback" with the server using the _hanging get pattern_: 实现基于请求的协议的一种简单方法是使用_hanging get pattern_在服务器上“驻留回调”：

```fidl
protocol FooProvider {
    WatchFoo(...) -> (Foo foo);
};
```
 

In this pattern, the client sends a `WatchFoo` message but the server does not reply until it has new information to send to the client. The client consumesthe foo and immediately sends another hanging get.  The client and server eachdo one unit of work per data item, which means neither gets ahead of the other. 在这种模式下，客户端发送“ WatchFoo”消息，但是服务器只有在有新信息要发送给客户端时才会回复。客户端使用foo并立即发送另一个挂起的get。客户端和服务器每个数据项都执行一个工作单元，这意味着两者都不比另一个更先进。

The hanging get pattern works well when the set of data items being transferred is bounded in size and the server-side state is simple, but does not work wellin situations where the client and server need to synchronize their work. 当要传输的数据项集有大小限制并且服务器端状态很简单时，悬挂获取模式会很好地工作，但是在客户端和服务器需要同步其工作的情况下，该方法不能很好地工作。

For example, a server might implement the hanging get pattern for some mutable state foo using a "dirty" bit for each client. It would initialize this bit totrue, clear it on each `WatchFoo` response, and set it on each change of foo.The server would only respond to a `WatchFoo` message when the dirty bit is set. 例如，服务器可能为每个客户端使用“脏”位来实现某​​些可变状态foo的悬挂获取模式。它将初始化此位为true，在每个“ WatchFoo”响应中将其清除，并在每次foo更改时将其设置。服务器仅在设置了脏位时才响应“ WatchFoo”消息。

 
#### Throttle push using acknowledgements  使用确认进行油门推 

One approach to providing flow control in protocols that use the push, is the _acknowledgment pattern_, in which the caller provides an acknowledgementresponse that the caller uses for flow control.  For example, consider thisgeneric listener protocol: 在使用推送的协议中提供流控制的一种方法是_acknowledgment pattern_，其中调用方提供一个确认响应，调用方将其用于流控制。例如，考虑以下通用侦听器协议：

```fidl
protocol Listener {
    OnBar(...) -> ();
};
```
 

The listener is expected to send an empty response message immediately upon receiving the `OnBar` message.  The response does not convey any data to thecaller.  Instead, the response lets the caller observe the rate at which thecallee is consuming messages.  The caller should throttle the rate at which itproduces messages to match the rate at which the callee consumes them.  Forexample, the caller might arrange for only one (or a fixed number) of messagesto be in flight (i.e., waiting for acknowledgement). 侦听器应在收到OnBar消息后立即发送空响应消息。该响应不会将任何数据传达给呼叫者。相反，响应使呼叫者可以观察被呼叫者使用消息的速率。呼叫者应限制其产生消息的速率，以匹配被呼叫者消耗消息的速率。例如，呼叫者可能只安排一条消息（或固定数量的消息）进行传输（即等待确认）。

 
#### Push bounded data using events  使用事件推送边界数据 

In FIDL, servers can send clients unsolicited messages called _events_. Protocols that use events need to provide particular attention to flow controlbecause the event mechanism itself does not provide any flow control. 在FIDL中，服务器可以向客户端发送称为_events_的未经请求的消息。使用事件的协议需要特别注意流控制，因为事件机制本身不提供任何流控制。

A good use case for events is when at most one instance of the event will be sent for the lifetime of the channel.  In this pattern, the protocol does notneed any flow control for the event: 事件的一个很好的用例是，在整个通道的生命周期内最多发送一个事件实例。在这种模式下，协议不需要对该事件进行任何流控制：

```fidl
protocol DeathWish {
    -> OnFatalError(status error_code);
};
```
 

Another good use case for events is when the client requests that the server produce events and when the overall number of events produced by the server isbounded.  This pattern is a more sophisticated version of the hanging getpattern in which the server can respond to the "get" request a bounded number oftimes (rather than just once): 事件的另一个很好的用例是，当客户端请求服务器产生事件时，以及服务器产生的事件总数受限制时。此模式是悬挂getpattern的更复杂的版本，在该模式中，服务器可以响应“ get”请求的次数有限（而不是一次）：

```fidl
protocol NetworkScanner {
    ScanForNetworks();
    -> OnNetworkDiscovered(string network);
    -> OnScanFinished();
};
```
 

 
#### Throttle events using acknowledgements  节气门事件使用确认 

If there is no a priori bound on the number of events, consider having the client acknowledge the events by sending a message.  This pattern is a moreawkward version of the throttle push using acknowledgements pattern in which theroles of client and server are switched.  As in the other pattern, the servershould throttle event production to match the rate at which the client consumesthe events: 如果事件数量没有先验约束，请考虑让客户端通过发送消息来确认事件。此模式是使用确认模式的节气门推送的更尴尬的版本，在该模式中，客户端和服务器的角色被切换。与其他模式一样，服务器应限制事件的产生，以匹配客户端使用事件的速率：

```fidl
protocol View {
    -> OnInputEvent(InputEvent event);
    NotifyInputEventHandled();
};
```
 

One advantage to this pattern over the normal acknowledgement pattern is that the client can more easily acknowledge multiple events with a single messagebecause the acknowledgement is disassociated from the event being acknowledged.This pattern allows for more efficient batch processing by reducing the volumeof acknowledgement messages and works well for in-order processing of multipleevent types: 与正常确认模式相比，此模式的一个优势是，客户端可以通过一条消息更轻松地确认多个事件，因为确认与被确认的事件无关，此模式可通过减少确认消息和工作量的方式来进行更有效的批处理。适用于多种事件类型的有序处理：

```fidl
protocol View {
    -> OnInputEvent(InputEvent event, uint64 seq);
    -> OnFocusChangedEvent(FocusChangedEvent event, uint64 seq);
    NotifyEventsHandled(uint64 last_seq);
};
```
 

Unlike throttle push using acknowledgements, this pattern does not express the relationship between the request and the response in FIDL syntax and thereforeit is prone to misuse. Flow control will only work when clients correctlyimplement sending of the notification message. 与使用确认的节流推送不同，此模式不以FIDL语法表示请求和响应之间的关系，因此容易被滥用。仅当客户端正确实现通知消息的发送时，流控制才起作用。

 
### Feed-forward dataflow  前馈数据流 

Some protocols have _feed-forward dataflow_, which avoids round-trip latency by having data flow primarily in one direction, typically from client to server.The protocol only synchronizes the two endpoints when necessary.  Feed-forwarddataflow also increases throughput because fewer total context switches arerequired to perform a given task. 某些协议具有“前馈数据流”，它通过使数据流主要在一个方向上（通常是从客户端到服务器）流向，从而避免了往返延迟。该协议仅在必要时才同步两个端点。前馈数据流还增加了吞吐量，因为执行给定任务所需的总上下文切换较少。

The key to feed-forward dataflow is to remove the need for clients to wait for results from prior method calls before sending subsequent messages.  Forexample, protocol request pipelining removes the need for the client to waitfor the server to reply with a protocol before the client can use theprotocol.  Similarly, client-assigned identifiers (see below) remove the needfor the client to wait for the server to assign identifiers for state held bythe server. 前馈数据流的关键是消除客户端在发送后续消息之前等待先前方法调用的结果的需求。例如，协议请求流水线消除了客户端在客户端可以使用协议之前等待服务器响应协议的需求。同样，客户端分配的标识符（请参见下文）消除了客户端等待服务器分配服务器所持有状态的标识符的需要。

Typically, a feed-forward protocol will involve the client submitting a sequence of one-way method calls without waiting for a response from the server.  Aftersubmitting these messages, the client explicitly synchronizes with the server bycalling a method such as `Commit` or `Flush` that has a reply.  The reply mightbe an empty message or might contain information about whether the submittedsequence succeeded.  In more sophisticated protocols, the one-way messages arerepresented as a union of command objects rather than individual method calls,see the _command union pattern_ below. 通常，前馈协议将涉及客户端提交一系列单向方法调用，而无需等待服务器的响应。提交这些消息后，客户端通过调用诸如“ Commit”或“ Flush”之类的具有回复的方法与服务器显式同步。回复可能是空消息，也可能包含有关提交序列是否成功的信息。在更复杂的协议中，单向消息表示为命令对象的并集，而不是单独的方法调用，请参见下面的“命令并集模式”。

Protocols that use feed-forward dataflow work well with optimistic error handling strategies.  Rather than having the server reply to every method with astatus value, which encourages the client to wait for a round trip between eachmessage, instead include a status reply only if the method can fail for reasonsthat are not under the control of the client.  If the client sends a messagethat the client should have known was invalid (e.g., referencing an invalidclient-assigned identifier), signal the error by closing the connection.  If theclient sends a message the client could not have known was invalid, eitherprovide a response that signals success or failure (which requires the client tosynchronize) or remember the error and ignore subsequent dependent requestsuntil the client synchronizes and recovers from the error in some way. 使用前馈数据流的协议可与乐观错误处理策略配合使用。服务器不要让服务器回复具有状态值的每个方法，而是鼓励客户端等待每个消息之间的往返，而仅当该方法因客户端无法控制的原因而失败时，才包括状态回复。如果客户端发送一条消息，表明客户端应该知道该消息无效（例如，引用了无效的客户端分配的标识符），请通过关闭连接来发出错误信号。如果客户端发送了一个消息，客户端可能不知道该消息无效，请提供一个响应来指示成功或失败（这需要客户端进行同步）或记住错误并忽略后续的相关请求，直到客户端以某种方式进行同步并从错误中恢复过来。

Example:  例：

```fidl
protocol Canvas {
    Flush() -> (status code);
    Clear();
    UploadImage(uint32 image_id, Image image);
    PaintImage(uint32 image_id, float x, float y);
    DiscardImage(uint32 image_id);
    PaintSmileyFace(float x, float y);
    PaintMoustache(float x, float y);
};
```
 

 
### Privacy by Design  设计隐私 

The client and server in a protocol frequently have access to different sets of sensitive data. Privacy or security problems can be caused by unintentionallyleaking more data than necessary over the protocol. 协议中的客户端和服务器经常可以访问不同的敏感数据集。私密性或安全性问题可能是由于无意间泄露了超出协议所需数量的数据所致。

When designing a protocol pay particular attention to fields in your protocol that: 设计协议时，请特别注意协议中的字段：

 
* Contain personally identifiable information such as names, email addresses, or payment details. *包含个人身份信息，例如姓名，电子邮件地址或付款明细。
* Are supplied by the user so potentially contain personal information. Examples include device names and comment fields. *由用户提供，因此可能包含个人信息。示例包括设备名称和注释字段。
* Act as a unique identifier that can be correlated across vendors, users, devices, or resets. Examples include serial numbers, MAC addresses, IPaddresses and global account IDs. *充当可以在供应商，用户，设备或重置之间关联的唯一标识符。示例包括序列号，MAC地址，IP地址和全局帐户ID。

These types of fields are reviewed thoroughly and the availability of protocols that include them may be restricted. Make sure that your protocols don't containmore information than is needed. 会对这些类型的字段进行彻底的检查，并且可能会限制包含它们的协议的可用性。确保您的协议所包含的信息不超过所需的信息。

If a use case for an API requires personal or linkable data and other use cases do not, consider using two different protocols so that access to the moresensitive use case may be controlled separately. 如果API的用例需要个人或可链接的数据，而其他用例则不需要，请考虑使用两种不同的协议，以便可以分别控制对更敏感用例的访问。

Consider two hypothetical examples that illustrate privacy violations caused by API design choices: 考虑两个假设的示例，这些示例说明了由API设计选择引起的侵犯隐私的行为：

 
* [Example 1 - Serial numbers in a peripheral control API](#privacy-example-1)  * [示例1-外围控件API中的序列号]（privacy-example-1）
* [Example 2 - Device names in a device setup API](#privacy-example-2)  * [示例2-设备设置API中的设备名称]（privacy-example-2）

 
#### Example 1 - Serial numbers in a peripheral control API {#privacy-example-1}  示例1-外围控件API {privacy-example-1}中的序列号 

Consider a peripheral control API that includes the serial numbers of USB peripherals. A serial number does not contain personal data but it is a verystable identifier that is easy to correlate. Including the serial number in thisAPI leads to many privacy concerns: 考虑一个包含USB外设序列号的外设控制API。序列号不包含个人数据，但是它是一个非常稳定的标识符，易于关联。在此API中包含序列号会引起许多隐私问题：

 
* Any client with access to the API could correlate the different accounts using the same Fuchsia device. *任何有权使用该API的客户端都可以使用相同的Fuchsia设备关联不同的帐户。
* Any client with access to the API could correlate the different personae within an account. *任何有权访问API的客户端都可以将帐户中的不同角色关联起来。
* Different software vendors could collude to learn whether they are being used by the same users or on the same device. *不同的软件供应商可能会合谋了解它们是由同一用户使用还是在同一设备上使用。
* If a peripheral is moved between devices, any client with access to the API could correlate the set of devices and users the peripheral is shared between. *如果外围设备在设备之间移动，则任何有权访问该API的客户端都可以将外围设备之间共享的设备和用户集相关联。
* If a peripheral is sold, clients with access to the API could correlate the old and new owner of the peripheral. *如果出售了外围设备，则有权访问API的客户可以将外围设备的新老所有者关联起来。
* Some manufacturers encode information in their serial numbers. This may let clients with access to the API deduce where or when the user purchased theperipheral. *一些制造商在其序列号中编码信息。这可以让有权访问API的客户端推断出用户在何处或何时购买外围设备。

In this example, the intent of the serial number is to allow clients to detect when the same USB peripheral is reconnected. Meeting this intent does require astable identifier but it does not require a global identifier. Different clientsdo not need to receive the same identifier, the same client does not need toreceive the same identifier across different Fuchsia devices, and the identifierdoes not need to remain constant across factory reset events. 在此示例中，序列号的目的是允许客户端检测何时重新连接了相同的USB外设。满足此意图确实需要使用不稳定的标识符，但不需要全局标识符。不同的客户端不需要接收相同的标识符，相同的客户端不需要在不同的紫红色设备上接收相同的标识符，并且在出厂重置事件中标识符不需要保持恒定。

In this example, a good alternative is to send an identifier that is only guaranteed to be stable for a single client on a single device. This identifiercould potentially be a hash of the peripheral's serial number, the Fuchsiadevice identifier, and the moniker of the connection. 在此示例中，一个很好的选择是发送仅保证对单个设备上的单个客户端稳定的标识符。该标识符可能是外围设备序列号，Fuchsiadevice标识符和连接名称的哈希。

 
#### Example 2 - Device names in a device setup API {#privacy-example-2}  示例2-设备设置API {privacy-example-2}中的设备名称 

Consider a device setup API that includes the model of the phone that is used to assist in the setup of a device. In most cases a phone's model string is set bythe OEM, but some phones report a user-supplied device name as their model. Thisleads to many model strings containing the real names or pseudonyms of theirusers. Therefore, this API risks associating a user across identities or acrossdevices. A rare or pre-release model string might reveal sensitive informationeven when it isn't supplied by the user. 考虑一个设备设置API，其中包括用于协助设备设置的电话型号。在大多数情况下，手机的型号字符串是由OEM设置的，但是某些手机会报告用户提供的设备名称作为其型号。这导致许多模型字符串包含其用户的真实姓名或假名。因此，此API冒着将用户跨身份或跨设备关联的风险。罕见的或预发行的模型字符串可能会泄露敏感信息，即使用户未提供它也是如此。

In some cases, it might be appropriate to use the model string but restrict which clients can access the API. Alternatively, the API could use fields thatare never controlled by the user such as the manufacturer string. Anotheralternative is to sanitize the model string by comparing it to an allowlist ofpopular phone models and replacing rare model strings with a generic string. 在某些情况下，使用模型字符串但限制哪些客户端可以访问API可能是合适的。或者，API可以使用用户从未控制过的字段，例如制造商字符串。另一种选择是通过将模型字符串与流行电话模型的允许列表进行比较来净化模型字符串，并用通用字符串替换稀有模型字符串。

 
### Client-assigned identifiers  客户端分配的标识符 

Often a protocol will let a client manipulate multiple pieces of state held by the server.  When designing an object system, the typical approach to thisproblem is to create separate objects for each coherent piece of state held bythe server.  However, when designing a protocol, using separate objects for eachpiece of state has several disadvantages. 通常，协议将允许客户端操纵服务器所持有的多个状态。设计对象系统时，解决此问题的典型方法是为服务器保存的每个相关状态创建单独的对象。但是，在设计协议时，为每个状态使用单独的对象有几个缺点。

Creating separate protocol instances for each logical object consumes kernel resources because each instance requires a separate channel object.Each instance maintains a separate FIFO queue of messages.  Usingseparate instances for each logical object means that messages sentto different objects can be reordered with respect to each other, leading toout-of-order interactions between the client and the server. 为每个逻辑对象创建单独的协议实例会消耗内核资源，因为每个实例都需要一个单独的通道对象。每个实例维护一个单独的FIFO消息队列。对每个逻辑对象使用单独的实例意味着发送到不同对象的消息可以相对于彼此重新排序，从而导致客户端和服务器之间的无序交互。

The _client-assigned identifier pattern_ avoids these problems by having the client assign `uint32` or `uint64` identifiers to objects retained by the server.All the messages exchanged between the client and the server are funnelledthrough a single protocol instance, which provides a consistent FIFO orderingfor the whole interaction. _client-signed identifier pattern_避免了这些问题，方法是让客户端为服务器保留的对象分配uint32或uint64标识符。客户端和服务器之间交换的所有消息都通过一个协议实例进行漏斗处理，从而提供一致的整个交互的FIFO顺序。

Having the client (rather than the server) assign the identifiers allows for feed-forward dataflow because the client can assign an identifier to an objectand then operate on that object immediately without waiting for the server toreply with the object's identifier.  In this pattern, the identifiers are validonly within the scope of the current connection, and typically the zeroidentifier is reserved as a sentinel.  *Security note:* Clients should not useaddresses in their address space as their identifiers because these addressescan leak the layout of their address space. 让客户端（而不是服务器）分配标识符可以进行前馈数据流，因为客户端可以将标识符分配给对象，然后立即对该对象进行操作，而无需等待服务器用对象的标识符进行回复。在这种模式下，标识符仅在当前连接的范围内有效，并且通常将零标识符保留为标记。 *安全说明：*客户端不应将其地址空间中的地址用作其标识符，因为这些地址可能会泄漏其地址空间的布局。

The client-assigned identifier pattern has some disadvantages.  For example, clients are more difficult to author because clients need to manage their ownidentifiers.  Developers commonly want to create a client library that providesan object-oriented facade for the service to hide the complexity of managingidentifiers, which itself is an anti-pattern (see _client libraries_ below). 客户端分配的标识符模式有一些缺点。例如，客户更难以编写，因为客户需要管理自己的标识符。开发人员通常希望创建一个客户端库，该库为服务提供面向对象的外观，以隐藏管理标识符的复杂性，而标识符本身就是一种反模式（请参见下面的_client library_）。

A strong signal that you should create a separate protocol instance to represent an object rather than using a client-assigned identifier is when youwant to use the kernel's object capability system to protect access to thatobject.  For example, if you want a client to be able to interact with an objectbut you do not want the client to be able to interact with other objects,creating a separate protocol instance means you can use the underlying channelas a capability that controls access to that object. 当您要使用内核的对象功能系统来保护对该对象的访问时，强烈建议您创建一个单独的协议实例来表示一个对象而不是使用客户端分配的标识符。例如，如果您希望客户端能够与对象进行交互，但又不希望客户端能够与其他对象进行交互，则创建单独的协议实例意味着您可以将基础通道用作控制对该对象的访问的功能宾语。

 
### Command union  指挥联合 

In protocols that use feed-forward dataflow, the client often sends many one-way messages to the server before sending a two-way synchronization message.  If theprotocol involves a particularly high volume of messages, the overhead forsending a message can become noticeable.  In those situations, consider usingthe _command union pattern_ to batch multiple commands into a single message. 在使用前馈数据流的协议中，客户端通常在发送双向同步消息之前向服务器发送许多单向消息。如果该协议涉及大量消息，则发送消息的开销会变得很明显。在这种情况下，请考虑使用_command union pattern_将多个命令批处理为一条消息。

In this pattern, the client sends a `vector` of commands rather than sending an individual message for each command.  The vector contains a union of all thepossible commands, and the server uses the union tag as the selector for commanddispatch in addition to using the method ordinal number: 在这种模式下，客户端发送命令的“向量”，而不是为每个命令发送单独的消息。向量包含所有可能命令的并集，并且服务器除了使用方法序号之外，还使用并集标记作为命令调度的选择器：

```fidl
struct PokeCmd { int32 x; int32 y; };

struct ProdCmd { string:64 message; };

union MyCommand {
    PokeCmd poke;
    ProdCmd prod;
};

protocol HighVolumeSink {
  Enqueue(vector<MyCommand> commands);
  Commit() -> (MyStatus result);
};
```
 

Typically the client buffers the commands locally in its address space and sends them to the server in a batch.  The client should flush the batch to the serverbefore hitting the channel capacity limits in either bytes and handles. 通常，客户端在其地址空间中本地缓存命令，然后将它们批量发送到服务器。客户端应在达到字节和句柄中的通道容量限制之前将批处理刷新到服务器。

For protocols with even higher message volumes, consider using a ring buffer in a `zx::vmo` for the data plane and an associated `zx::fifo` for the controlplane.  Such protocols place a higher implementation burden on the client andthe server but are appropriate when you need maximal performance.  For example,the block device protocol uses this approach to optimize performance. 对于消息量更大的协议，考虑在数据平面的zx :: vmo中使用环形缓冲区，在控制平面使用相关的zx :: fifo。这样的协议给客户端和服务器带来了更高的实现负担，但是在您需要最大性能时才是合适的。例如，块设备协议使用此方法来优化性能。

 
### Pagination  分页 

FIDL messages are typically sent over channels, which have a maximum message size.  In many cases, the maximum message size is sufficient to transmitreasonable amounts of data, but there are use cases for transmitting large (oreven unbounded) amounts of data.  One way to transmit a large or unboundedamount of information is to use a _pagination pattern_. FIDL消息通常通过具有最大消息大小的通道发送。在许多情况下，最大消息大小足以传输合理数量的数据，但是存在用于传输大量（甚至无限量）数据的用例。传输大量或无限制信息的一种方法是使用_pagination pattern_。

 
#### Paginating Writes  分页写 

A simple approach to paginating writes to the server is to let the client send data in multiple messages and then have a "finalize" method that causes theserver to process the sent data: 对服务器写分页的一种简单方法是让客户端以多条消息发送数据，然后使用“ finalize”方法使服务器处理发送的数据：

```fidl
protocol Foo {
    AddBars(vector<Bar> bars);
    UseTheBars() -> (...);
};
```
 

For example, this pattern is used by `fuchsia.process.Launcher` to let the client send an arbitrary number of environment variables. 例如，`fuchsia.process.Launcher`使用此模式让客户端发送任意数量的环境变量。

A more sophisticated version of this pattern creates a protocol that represents the transaction, often called a _tear-off protocol_: 此模式的更高级版本创建代表交易的协议，通常称为_tear-off protocol_：

```fidl
protocol BarTransaction {
    Add(vector<Bar> bars);
    Commit() -> (...);
};

protocol Foo {
    StartBarTransaction(request<BarTransaction> transaction);
};
```
 

This approach is useful when the client might be performing many operations concurrently and breaking the writes into separate messages loses atomicity.Notice that `BarTransaction` does not need an `Abort` method.  The betterapproach to aborting the transaction is for the client to close the`BarTransaction` protocol. 当客户端可能同时执行许多操作并且将写入拆分为单独的消息会丢失原子性时，此方法很有用。请注意，“ BarTransaction”不需要“ Abort”方法。中止交易的更好方法是让客户端关闭BarTransaction协议。

 
#### Paginating Reads  分页阅读 

A simple approach to paginating reads from the server is to let the server send multiple responses to a single request using events: 分页来自服务器的读取的一种简单方法是让服务器使用事件向单个请求发送多个响应：

```fidl
protocol EventBasedGetter {
    GetBars();
    -> OnBars(vector<Bar> bars);
    -> OnBarsDone();
};
```
 

Depending on the domain-specific semantics, this pattern might also require a second event that signals when the server is done sending data.  This approachworks well for simple cases but has a number of scaling problems.  For example,the protocol lacks flow control and the client has no way to stop the server ifthe client no longer needs additional data (short of closing the wholeprotocol). 根据特定于域的语义，此模式可能还需要第二个事件，该事件在服务器完成数据发送时发出信号。这种方法在简单情况下效果很好，但存在许多扩展问题。例如，该协议缺少流控制，并且如果客户端不再需要其他数据（缺少关闭整个协议），则客户端将无法停止服务器。

A more robust approach uses a tear-off protocol to create an iterator:  一种更可靠的方法是使用分离协议创建迭代器：

```fidl
protocol BarIterator {
    GetNext() -> (vector<Bar> bars);
};

protocol ChannelBasedGetter {
    GetBars(request<BarIterator> iterator);
};
```
 

After calling `GetBars`, the client uses protocol request pipelining to queue the first `GetNext` call immediately.  Thereafter, the client repeatedly calls`GetNext` to read additional data from the server, bounding the number ofoutstanding `GetNext` messages to provide flow control.  Notice that theiterator need not require a "done" response because the server can reply with anempty vector and then close the iterator when done. 调用GetBars之后，客户端使用协议请求管道将第一个GetNext调用立即排队。此后，客户端反复调用“ GetNext”以从服务器读取其他数据，以限制未完成的“ GetNext”消息的数量以提供流控制。请注意，迭代器不需要“完成”响应，因为服务器可以使用空向量进行响应，然后在完成后关闭迭代器。

Another approach to paginating reads is to use a token.  In this approach, the server stores the iterator state on the client in the form of an opaque token,and the client returns the token to the server with each partial read: 分页读取的另一种方法是使用令牌。在这种方法中，服务器以不透明令牌的形式将迭代器状态存储在客户端上，并且每次读取部分内容时，客户端会将令牌返回给服务器：

```fidl
struct Token { array<uint8>:16 opaque; }
protocol TokenBasedGetter {
    // If token is null, fetch the first N entries. If token is not null, return
    // the N items starting at token. Returns as many entries as it can in
    // results and populates next_token if more entries are available.
    GetEntries(Token? token) -> (vector<Entry> entries, Token? next_token);
}
```
 

This pattern is especially attractive when the server can escrow all of its pagination state to the client and therefore no longer need to maintainpaginations state at all.  The server should document whether the client canpersist the token and reuse it across instances of the protocol.  *Securitynote:* In either case, the server must validate the token supplied by the clientto ensure that the client's access is limited to its own paginated results anddoes not include results intended for another client. 当服务器可以将其所有分页状态都托管给客户端，因此根本不再需要保持分页状态时，此模式特别有吸引力。服务器应记录客户端是否可以持久令牌并在协议实例之间重用它。 *安全说明：*在这两种情况下，服务器都必须验证客户端提供的令牌，以确保客户端的访问仅限于其自身的分页结果，并且不包括用于其他客户端的结果。

 
### Eventpair correlation  事件对关联 

When using client-assigned identifiers, clients identify objects held by the server using identifiers that are meaningful only in the context of their ownconnection to the server.  However, some use cases require correlating objectsacross clients.  For example, in `fuchsia.ui.scenic`, clients largely interactwith nodes in the scene graph using client-assigned identifiers.  However,importing a node from another process requires correlating the reference to thatnode across process boundaries. 当使用客户端分配的标识符时，客户端使用仅在其自身与服务器的连接的上下文中才有意义的标识符来标识服务器拥有的对象。但是，某些用例需要跨客户端关联对象。例如，在“ fuchsia.ui.scenic”中，客户端使用客户端分配的标识符在很大程度上与场景图中的节点进行交互。但是，从另一个过程中导入一个节点需要跨该过程边界关联对该节点的引用。

The _eventpair correlation pattern_ solves this problem using a feed-forward dataflow by relying on the kernel to provide the necessary security.  First, theclient that wishes to export an object creates a `zx::eventpair` and sends oneof the entangled events to the server along with its client-assigned identifierof the object.  The client then sends the other entangled event to the otherclient, which forwards the event to the server with its own client-assignedidentifier for the now-shared object: _事件对关联模式_通过依赖内核提供必要的安全性，使用前馈数据流解决了此问题。首先，希望导出对象的客户端创建一个“ zx :: eventpair”，并将纠缠的事件之一及其由客户端分配的对象标识符发送到服务器。然后，客户端将另一个纠缠的事件发送给另一个客户端，另一个事件将事件转发给服务器，该服务器使用自己的客户端分配的标识符来共享现在共享的对象：

```fidl
protocol Foo {
    ExportThing(uint32 client_assigned_id, ..., handle<eventpair> export_token);
};

protocol Bar {
    ImportThing(uint32 some_other_client_assigned_id, ..., handle<eventpair> import_token);
};
```
 

To correlate the objects, the server calls `zx_object_get_info` with `ZX_INFO_HANDLE_BASIC` and matches the `koid` and `related_koid` properties fromthe entangled event objects. 为了关联对象，服务器用ZX_INFO_HANDLE_BASIC调用`zx_object_get_info`并匹配纠缠事件对象的`koid`和`related_koid`属性。

 
### Eventpair cancellation  取消事件对 

When using tear-off protocol transactions, the client can cancel long-running operations by closing the client end of the protocol.  The server should listen for`ZX_CHANNEL_PEER_CLOSED` and abort the transaction to avoid wasting resources. 使用剥离协议事务时，客户端可以通过关闭协议的客户端来取消长时间运行的操作。服务器应侦听ZX_CHANNEL_PEER_CLOSED并中止事务以避免浪费资源。

There is a similar use case for operations that do not have a dedicated channel. For example, the `fuchsia.net.http.Loader` protocol has a `Fetch` method thatinitiates an HTTP request.  The server replies to the request with the HTTPresponse once the HTTP transaction is complete, which might take a significantamount of time.  The client has no obvious way to cancel the request short ofclosing the entire `Loader` protocol, which might cancel many other outstandingrequests. 没有专用通道的操作也有类似的用例。例如，“ fuchsia.net.http.Loader”协议具有“ Fetch”方法，该方法会启动HTTP请求。 HTTP事务完成后，服务器将使用HTTP响应来回复请求，这可能会花费大量时间。除非关闭整个“ Loader”协议，否则客户端没有明显的取消请求的方法，这可能会取消许多其他未完成的请求。

The _eventpair cancellation pattern_ solves this problem by having the client include one of the entangled events from a `zx::eventpair` as a parameter to themethod.  The server then listens for `ZX_EVENTPAIR_PEER_CLOSED` and cancels theoperation when that signal is asserted.  Using a `zx::eventpair` is better thanusing a `zx::event` or some other signal because the `zx::eventpair` approachimplicitly handles the case where the client crashes or otherwise tears downbecause the `ZX_EVENTPAIR_PEER_CLOSED` is generated automatically by the kernelwhen the entangled event retained by the client is destroyed. _eventpair取消模式_通过让客户端包括来自zx :: eventpair的纠缠事件之一作为方法的参数来解决此问题。然后，服务器侦听“ ZX_EVENTPAIR_PEER_CLOSED”，并在声明该信号时取消该操作。使用`zx :: eventpair`优于使用`zx :: event`或其他信号，因为`zx :: eventpair`可以隐式处理客户端崩溃或崩溃的情况，因为`ZX_EVENTPAIR_PEER_CLOSED`是由客户端保留的纠缠事件被销毁时的内核。

 
### Empty protocols  空协议 

Sometimes an empty protocol can provide value.  For example, a method that creates an object might also receive a `request<FooController>` parameter.  Thecaller provides an implementation of this empty protocol: 有时，空协议可以提供价值。例如，创建对象的方法可能还会收到一个`request <FooController>`参数。调用方提供了此空协议的实现：

```fidl
protocol FooController {};
```
 

The `FooController` does not contain any methods for controlling the created object, but the server can use the `ZX_CHANNEL_PEER_CLOSED` signal on theprotocol to trigger destruction of the object.  In the future, the protocolcould potentially be extended with methods for controlling the created object. “ FooController”不包含任何控制所创建对象的方法，但是服务器可以使用协议上的“ ZX_CHANNEL_PEER_CLOSED”信号来触发对象的破坏。将来，该协议可能会使用控制创建对象的方法进行扩展。

 
### Controlling settings-like data  控制类似设置的数据 

Often, servers will expose settings which the client can modify. Prefer using a `table` to represent such settings. For instance, the `fuchsia.accessibility`library defines: 通常，服务器会公开客户端可以修改的设置。首选使用“表”来表示此类设置。例如，`fuchsia.accessibility`库定义：

```fidl
table Settings {
    1: bool magnification_enabled;
    2: float32 magnification_zoom_factor;
    3: bool screen_reader_enabled;
    4: bool color_inversion_enabled;
    5: ColorCorrection color_correction;
    6: array<float32>:9 color_adjustment_matrix;
}
```
(Comments are omitted for readability.)  （为了便于阅读，省略了注释。）

There are various ways to provide clients the ability to change these settings.  有多种方法可以为客户提供更改这些设置的功能。

The **partial update** approach exposes an `Update` method taking a partial settings value, and changes fields _only_ if they are present in the partialvalue. “部分更新”方法公开了一个带有部分设置值的“更新”方法，并更改字段_only_（如果它们存在于partialvalue中）。

```fidl
protocol TheManagerOfSomeSorts {
    /// Description how the update modifies the behavior.
    ///
    /// Only fields present in the settings value will be changed.
    Update(Settings settings) -> ...;
};
```
 

The **replace** approach exposes a `Replace` method taking a complete settings value, and changes the settings to the newly provided one. ** replace **方法公开了采用完整设置值的`Replace`方法，并将设置更改为新提供的设置。

```fidl
protocol TheManagerOfSomeSorts {
    /// Description how the override modifies the behavior.
    ///
    /// This replaces the setting.
    Replace(Settings settings) -> ...;
};
```
 

Things to avoid:  避免的事情：

 
 * Avoid using the verb `Set` or `Override` for either the partial update or the replace approach since what semantics are offered will be ambiguous. *避免对部分更新或替换方法使用动词“设置”或“覆盖”，因为提供的语义将是模棱两可的。

 
 * Avoid individual methods to update settings' fields such as `SetMagnificationEnabled`. Such individal methods are more burdensome tomaintain, and callers rarely want to update a single value. *避免使用诸如SetMagnificationEnabled之类的更新设置的单独方法。这种单独的方法维护起来比较麻烦，并且调用者很少希望更新单个值。

 
## Antipatterns  反模式 

This section describes several antipatterns: design patterns that often provide negative value.  Learning to recognize these patterns is the first step towardsavoiding using them in the wrong ways. 本节描述了几种反模式：通常提供负值的设计模式。学习识别这些模式是避免以错误的方式使用它们的第一步。

 
### Client libraries  客户端库 

Ideally, clients interface with protocols defined in FIDL using language-specific client libraries generated by the FIDL compiler.While this approach lets Fuchsia provide high-quality support for a largenumber of target languages, sometimes the protocol is too low-level to program directly.In such cases, it's appropriate to provide a hand-written client library thatinterfaces to the same underlying protocol, but is easier to use correctly. 理想情况下，客户端使用FIDL编译器生成的特定于语言的客户端库与FIDL中定义的协议进行交互。尽管这种方法可以让Fuchsia为大量目标语言提供高质量的支持，但有时该协议的底层级别太低而无法直接进行编程。在这种情况下，提供一个手写的客户端库是合适的，该客户端库可以连接到相同的基础协议，但更易于正确使用。

For example, `fuchsia.io` has a client library, `libfdio.so`, which provides a POSIX-like frontend to the protocol.  Clients that expect a POSIX-style`open`/`close`/`read`/`write` interface can link against `libfdio.so` and speakthe `fuchsia.io` protocol with minimal modification.  This client libraryprovides value because the library adapts between an existing library interfaceand the underlying FIDL protocol. 例如，“ fuchsia.io”具有一个客户端库“ libfdio.so”，该库为该协议提供了类似于POSIX的前端。期望使用POSIX风格的open / close / read / write接口的客户可以链接libfdio.so并以最小的改动说出fuchsia.io协议。该客户端库提供了价值，因为该库可在现有库接口和基础FIDL协议之间进行调整。

Another kind of client library that provides positive value is a framework.  A framework is an extensive client library that provides a structure for a largeportion of the application.  Typically, a framework provides a significantamount of abstraction over a diverse set of protocols.  For example, Flutter isa framework that can be viewed as an extensive client library for the`fuchsia.ui` protocols. 提供正面价值的另一种客户端库是框架。框架是一个广泛的客户端库，它为大部分应用程序提供结构。通常，框架通过各种协议集提供大量的抽象。例如，Flutter isa框架可以看作是fuchsia.ui协议的扩展客户端库。

FIDL protocols should be fully documented regardless of whether the protocol has an associated client library.  An independent group of software engineers shouldbe able to understand and correctly use the protocol directly given itsdefinition without need to reverse-engineer the client library.  When theprotocol has a client library, aspects of the protocol that are low-level andsubtle enough to motivate you to create a client library should be documentedclearly. 无论该协议是否具有关联的客户端库，都应完整记录FIDL协议。一个独立的软件工程师小组应该能够直接根据协议的定义来理解和正确使用协议，而无需对客户端库进行反向工程。当该协议具有客户端库时，应清楚记录协议的底层和足以激发您创建客户端库的方面。

The main difficulty with client libraries is that they need to be maintained for every target language, which tends to mean client libraries are missing (orlower quality) for less popular languages.  Client libraries also tend to ossifythe underlying protocols because they cause every client to interact with theserver in exactly the same way.  The servers grow to expect this exactinteraction pattern and fail to work correctly when clients deviate from thepattern used by the client library. 客户端库的主要困难在于，每种目标语言都需要维护它们，这往往意味着缺少流行语言的客户端库（质量较低）。客户端库还倾向于使底层协议更加僵化，因为它们导致每个客户端以完全相同的方式与服务器交互。当客户端偏离客户端库使用的模式时，服务器会逐渐期望这种精确的交互模式，并且无法正常工作。

In order to include the client library in the Fuchsia SDK, we should provide implementations of the library in at least two languages. 为了在Fuchsia SDK中包含客户端库，我们应该至少以两种语言提供该库的实现。

 
### Service hubs {#service_hubs}  服务中心{service_hubs} 

A _service hub_ is a `Discoverable` protocol that simply lets you discover a number of other protocols, typically with explicit names: _service hub_是一个“可发现”协议，可以让您发现许多其他协议，通常使用显式名称：

```fidl
BAD:
[Discoverable]
protocol ServiceHub {
    GetFoo(request<Foo> foo);
    GetBar(request<Bar> bar);
    GetBaz(request<Baz> baz);
    GetQux(request<Qux> qux);
};
```
 

Particularly if stateless, the `ServiceHub` protocol does not provide much value over simply making the individual protocol services discoverable directly: 尤其是在无状态的情况下，`ServiceHub`协议并没有提供太多的价值，而仅仅是简单地使单个协议服务可直接发现：

```fidl
[Discoverable]
protocol Foo { ... };

[Discoverable]
protocol Bar { ... };

[Discoverable]
protocol Baz { ... };

[Discoverable]
protocol Qux { ... };
```
 

Either way, the client can establish a connection to the enumerated services. In the latter case, the client can discover the same services through the normalmechanism used throughout the system to discover services.  Using the normalmechanism lets the core platform apply appropriate policy to discovery. 无论哪种方式，客户端都可以建立与枚举服务的连接。在后一种情况下，客户端可以通过整个系统中用来发现服务的正常机制来发现相同的服务。使用正常机制可以使核心平台将适当的策略应用于发现。

However, service hubs can be useful in some situations.  For example, if the protocol were stateful or was obtained through some process more elaborate thannormal service discovery, then the protocol could provide value by transferringstate to the obtained services.  As another example, if the methods forobtaining the services take additional parameters, then the protocol couldprovide value by taking those parameters into account when connecting to theservices. 但是，服务中心在某些情况下可能很有用。例如，如果协议是有状态的，或者是通过比正常服务发现更复杂的过程获得的，则协议可以通过将状态转移到获得的服务来提供价值。作为另一示例，如果用于获得服务的方法采用附加参数，则协议可以通过在连接至服务时考虑这些参数来提供价值。

 
### Overly object-oriented design  过度的面向对象设计 

Some libraries create separate protocol instances for every logical object in the protocol, but this approach has a number of disadvantages: 一些库为协议中的每个逻辑对象创建单独的协议实例，但是这种方法有许多缺点：

 
 * Message ordering between the different protocol instances is undefined. Messages sent over a single protocol are processed in FIFO order (in eachdirection), but messages sent over different channels race.  When theinteraction between the client and the server is spread across many channels,there is a larger potential for bugs when messages are unexpectedlyreordered. *不同协议实例之间的消息顺序是不确定的。通过单个协议发送的消息按FIFO顺序（在每个方向上）进行处理，但是通过不同通道发送的消息会竞争。当客户端和服务器之间的交互分布在许多渠道上时，如果消息意外地重新排序，则存在更大的潜在错误。

 
 * Each protocol instance has a cost in terms of kernel resources, waiting queues, and scheduling.  Although Fuchsia is designed to scale to largenumbers of channels, the costs add up over the whole system and creating ahuge proliferation of objects to model every logical object in the systemplaces a large burden on the system. *每个协议实例在内核资源，等待队列和调度方面都有代价。尽管紫红色被设计为可扩展到大量通道，但成本在整个系统上加起来，并且创建大量对象以建模系统中的每个逻辑对象，这给系统带来了沉重负担。

 
* Error handling and teardown is much more complicated because the number of error and teardown states grows exponentially with the number of protocolinstances involved in the interaction.  When you use a single protocolinstance, both the client and the server can cleanly shut down the interactionby closing the protocol.  With multiple protocol instances, the interactioncan get into states where the interaction is partially shutdown or where thetwo parties have inconsistent views of the shutdown state. *错误处理和拆除的复杂性要高得多，因为错误和拆除状态的数量会随着交互中涉及的协议实例的数量呈指数增长。当您使用单个协议实例时，客户端和服务器都可以通过关闭协议来干净地关闭交互。在具有多个协议实例的情况下，交互可以进入交互被部分关闭的状态，或者双方对关闭状态的看法不一致的状态。

 
 * Coordination across protocol boundaries is more complex than within a single protocol because multiple protocols need to allowfor the possibility that different protocols will be used by differentclients, who might not completely trust each other. *跨协议边界的协调比在单个协议中更为复杂，因为多个协议需要考虑不同客户端可能会使用不同协议的可能性，这些客户端可能不会完全相互信任。

However, there are use cases for separating functionality into multiple protocols: 但是，有一些将功能分成多个协议的用例：

 
 * Providing separate protocols can be beneficial for security because some clients might have access to only one of the protocols and thereby berestricted in their interactions with the server. *提供单独的协议可能对安全性有益，因为某些客户端可能只能访问其中一种协议，从而限制了它们与服务器的交互。

 
 * Separate protocols can also more easily be used from separate threads.  For example, one protocol might be bound to one thread and another protocolmight be bound to another thread. *也可以从单独的线程中更轻松地使用单独的协议。例如，一个协议可能绑定到一个线程，而另一个协议可能绑定到另一个线程。

 
 * Clients and servers pay a (small) cost for each method in a protocol. Having one giant protocol that contains every possible method can be lessefficient than having multiple smaller protocols if only a few of thesmaller protocols are needed at a time. *客户端和服务器为协议中的每种方法支付（少量）费用。如果一次只需要几个较小的协议，那么拥有一个包含所有可能方法的巨型协议可能会比拥有多个较小的协议效率低。

 
 * Sometimes the state held by the server factors cleanly along method boundaries.  In those cases, consider factoring the protocol into smallerprotocols along those same boundaries to provide separate protocols forinteracting with separate state. *有时，服务器保持的状态会沿着方法边界清晰地分解。在那些情况下，请考虑将协议分解为沿着相同边界的较小协议，以提供用于与单独状态进行交互的单独协议。

A good way to avoid over object-orientation is to use client-assigned identifiers to model logical objects in the protocol.  That pattern lets clientsinteract with a potentially large set of logical objects through a singleprotocol. 避免过度面向对象的一种好方法是使用客户端分配的标识符在协议中对逻辑对象进行建模。这种模式使客户可以通过一个协议与一组可能很大的逻辑对象进行交互。

