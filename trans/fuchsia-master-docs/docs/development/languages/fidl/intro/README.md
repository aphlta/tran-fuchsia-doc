 
# Overview  总览 

This document is a description of the Fuchsia Interface Definition Language (FIDL) purpose, high-level goals, and requirements. 本文档是对Fuchsia接口定义语言（FIDL）的目的，高级目标和要求的描述。

 
## Related Documents  相关文件 

 
*   [Wire Format Specification]  * [线格式规格]
*   [Language Specification]  * [语言规范]
*   [Compiler Specification]  * [编译器规格]
*   [Style Guide]  *   [时尚指南]
*   [API Rubric]  * [API专栏]
*   [Linter to check API Readability / Style]  * [Linter检查API的可读性/样式]
*   [C Language Bindings]  * [C语言绑定]
*   [Low-Level C++ Language Bindings]  * [低级C ++语言绑定]
*   [High-Level C++ Language Bindings]  * [高级C ++语言绑定]
*   [C/Low-Level/High-Level C++ Bindings Comparison]  * [C /低级/高级C ++绑定比较]
*   [Examples]: Some small example code used during development  * [示例]：开发过程中使用的一些小示例代码
*   [Tutorial]: A tutorial on using FIDL services in several languages  * [教程]：有关使用多种语言的FIDL服务的教程

<!-- Reference links because these are used again below. -->  <！-参考链接，因为下面再次使用这些链接。 ->

[Wire Format Specification]: ../reference/wire-format/README.md [Language Specification]: ../reference/language.md[Compiler Specification]: ../reference/compiler.md[Style Guide]: ../style.md[API Rubric]: ../../../api/fidl.md[Linter to Check API Readability / Style]: ../reference/linter.md[C Language Bindings]: ../tutorial/tutorial-c.md[Low-Level C++ Language Bindings]: ../tutorial/tutorial-llcpp.md[High-Level C++ Language Bindings]: ../tutorial/tutorial-cpp.md[C/Low-Level/High-Level C++ Bindings Comparison]: ../tutorial/c-family-comparison.md[Examples]: /zircon/tools/fidl/examples[Tutorial]: ../tutorial/README.md [Wire Format Specification]：../reference/wire-format/README.md [Language Specification]：../reference/language.md[Compiler Specification]：../reference/compiler.md[Style Guide]：。 ./style.md[API专栏]：../../../api/fidl.md[Lint检查API可读性/样式]：../reference/linter.md[C语言绑定]：.. /tutorial/tutorial-c.md [低级C ++语言绑定]：../ tutorial / tutorial-llcpp.md [高级C ++语言绑定]：../tutorial/tutorial-cpp.md[C/Low级别/高级C ++绑定比较]：../ tutorial / c-family-comparison.md [示例]：/ zircon / tools / fidl / examples [教程]：../tutorial/README.md

[TOC]  [目录]

The Fuchsia Interface Definition Language (FIDL) is the language used to describe interprocess communication (IPC) protocols used by programs running onthe Fuchsia Operating System. FIDL is supported by a toolchain (compiler) andruntime support libraries (bindings) to help developers use IPC effectively. 紫红色接口定义语言（FIDL）是一种语言，用于描述在紫红色操作系统上运行的程序所使用的进程间通信（IPC）协议。 FIDL由工具链（编译器）和运行时支持库（绑定）支持，以帮助开发人员有效地使用IPC。

 
## Goals  目标 

Fuchsia extensively relies on IPC since it has a microkernel architecture wherein most functionality is implemented in user space outside of the kernel,including privileged components such as device drivers. Consequently the IPCmechanism must be efficient, deterministic, robust, and easy to use. Fuchsia广泛依赖IPC，因为它具有微内核架构，其中大多数功能在内核外部的用户空间中实现，包括特权组件（例如设备驱动程序）。因此，IPC机制必须高效，确定性，强大且易于使用。

**IPC efficiency** pertains to the computational overhead required to generate, transfer, and consume messages between processes. IPC will be involved in allaspects of system operation so it must be efficient. The FIDL compiler mustgenerate tight code without excess indirection or hidden costs. It should be atleast as good as hand-rolled code would be where it matters most. ** IPC效率**涉及在进程之间生成，传输和使用消息所需的计算开销。 IPC将涉及系统操作的所有方面，因此它必须高效。 FIDL编译器必须生成紧凑的代码，而不会产生过多的间接或隐藏成本。在最重要的地方，它应该至少与手工编写的代码一样好。

**IPC determinism** pertains to the ability to perform transactions within a known resource envelope. IPC will be used extensively by critical systemservices such as filesystems which serve many clients and which must perform inpredictable ways. The FIDL wire format must offer strong static guarantees suchas ensuring that structure size and layout is invariant thereby alleviating theneed for dynamic memory allocation or complex validation rules. ** IPC确定性**涉及在已知资源范围内执行事务的能力。 IPC将由关键系统服务（例如为许多客户端提供服务且必须执行不可预测方式的文件系统）广泛使用。 FIDL线格式必须提供强大的静态保证，例如确保结构大小和布局不变，从而减轻了对动态内存分配或复杂验证规则的需求。

**IPC robustness** pertains to the need to consider IPC as an essential part of the operating system's ABI. Maintaining binary stability is crucial. Mechanismsfor protocol evolution must be designed conservatively so as not to violate theinvariants of existing services and their clients, particularly when the needfor determinism is also considered. The FIDL bindings must perform effective,lightweight, and strict validation. ** IPC健壮性**与需要将IPC视为操作系统ABI的重要组成部分有关。保持二进制稳定性至关重要。协议演化的机制必须谨慎设计，以免违反现有服务及其客户的不变性，尤其是在还考虑确定性需求的情况下。 FIDL绑定必须执行有效，轻量且严格的验证。

**IPC ease of use** pertains to the fact that IPC protocols are an essential part of the operating system's API. It is important to provide good developerergonomics for accessing services via IPC. The FIDL code generator removes theburden of writing IPC bindings by hand. Moreover, the FIDL code generator canproduce different bindings to suit the needs of different audiences and theiridioms. ** IPC的易用性**与IPC协议是操作系统API的重要组成部分有关。为通过IPC访问服务提供良好的开发人员工程学非常重要。 FIDL代码生成器消除了手工编写IPC绑定的负担。此外，FIDL代码生成器可以产生不同的绑定，以满足不同受众及其习惯的需求。

TODO: express goal of meeting the needs of different audiences using appropriately tailored bindings, eg. system programming native vs. event-drivendispatch vs. async calls, etc... say more things about FIDL as our system API,SDK concerns, etc. TODO：表达目标，即使用适当定制的绑定来满足不同受众的需求。系统编程本机vs.事件驱动调度vs.异步调用等...更多关于FIDL的信息，例如我们的系统API，SDK问题等。

 
# Requirements  要求 

 
## Purpose  目的 

 
*   Describe data structures and protocols used by IPC on Zircon.  *描述IPC在Zircon上使用的数据结构和协议。
*   Optimized for interprocess communication only; FIDL must not be persisted to disk or used for network transfer across device boundaries. *仅针对进程间通信进行了优化； FIDL不得持久保存到磁盘或用于跨设备边界的网络传输。
*   Efficiently transport messages consisting of data (bytes) and capabilities (handles) over Zircon channels between processes running on the samedevice. *在同一设备上运行的进程之间，通过Zircon通道有效地传输包含数据（字节）和功能（句柄）的消息。
*   Designed specifically to facilitate effective use of Zircon primitives; not intended for use on other platforms; not portable. *专为促进有效使用Zircon原语而设计；不适用于其他平台；不便携。
*   Offers convenient APIs for creating, sending, receiving, and consuming messages. *提供方便的API，用于创建，发送，接收和使用消息。
*   Perform sufficient validation to maintain protocol invariants (but no more than that). *执行足够的验证以保持协议不变性（但不超过此数量）。

 
## Efficiency  效率 

 
*   Just as efficient (speed and memory) as using hand-rolled data structures would be. *和使用手动滚动数据结构一样高效（速度和内存）。
*   Wire format uses uncompressed native datatypes with little-endianness and correct alignment to support in-place access of message contents. *有线格式使用具有低字节序和正确对齐方式的未压缩本机数据类型，以支持就地访问消息内容。
*   No dynamic memory allocation is required to produce or to consume messages when their size is statically known or bounded. *当静态地知道或限制消息的大小时，不需要动态内存分配来产生或使用消息。
*   Explicitly handle ownership with move-only semantics.  *使用仅移动语义明确处理所有权。
*   Data structure packing order is canonical, unambiguous, and has minimum padding. *数据结构的打包顺序规范，明确，并且填充最少。
*   Avoid back-patching pointers.  *避免回补指针。
*   Avoid expensive validation.  *避免进行昂贵的验证。
*   Avoid calculations which may overflow.  *避免可能会溢出的计算。
*   Leverage pipelining of protocol requests for asynchronous operation.  *利用协议请求的流水线进行异步操作。
*   Structures are fixed size; variable-size data is stored out-of-line.  *结构尺寸固定；可变大小的数据脱机存储。
*   Structures are not self-described; FIDL files describe their contents.  *结构不是自我描述的； FIDL文件描述其内容。
*   No versioning of structures, but protocols can be extended with new methods for evolution. *没有结构的版本控制，但是可以使用新的演化方法扩展协议。

 
## Ergonomics  人机工程学 

 
*   Programming language bindings maintained by Fuchsia team:  *紫红色团队维护的编程语言绑定：
    *   C, Low-Level C++, High-Level C++, Dart, Go, Rust  * C，低级C ++，高级C ++，Dart，Go，Rust
*   Keeping in mind we might want to support other languages in the future, such as: *请记住，我们将来可能希望支持其他语言，例如：
    *   Java, JavaScript, etc.  * Java，JavaScript等
*   The bindings and generated code are available in native or idiomatic flavors depending on the intended application. *绑定和生成的代码以本机或惯用的方式提供，具体取决于预期的应用程序。
*   Use compile-time code generation to optimize message serialization, deserialization, and validation. *使用编译时代码生成来优化消息序列化，反序列化和验证。
*   FIDL syntax is familiar, easily accessible, and programming language agnostic. * FIDL语法很熟悉，易于访问，并且与编程语言无关。
*   FIDL provides a library system to simplify deployment and use by other developers. * FIDL提供了一个库系统来简化其他开发人员的部署和使用。
*   FIDL expresses the most common data types needed for system APIs; it does not seek to provide a comprehensive one-to-one mapping of all types offeredby all programming languages. * FIDL表示系统API所需的最常见数据类型；它并不试图提供所有编程语言提供的所有类型的全面的一对一映射。

 
## Implementation  实作 

 
*   Compiler is written in C++ to be usable by components built in Zircon.  *编译器使用C ++编写，可用于Zircon内置的组件。
*   Compiler is portable and can be built with a host toolchain.  *编译器是可移植的，可以使用主机工具链构建。
*   We will not support FIDL bindings for any platform other than Fuchsia.  *除紫红色以外，我们不支持FIDL绑定。

 
## Where to Find the Code  在哪里找到代码 

 
- [The compiler](/zircon/tools/fidl)  -[编译器]（/ zircon / tools / fidl）
- [C and low-level C++ bindings](/zircon/system/ulib/fidl)  -[C和低级C ++绑定]（/ zircon / system / ulib / fidl）
- [High-level C++ bindings](/sdk/lib/fidl/cpp)  -[高级C ++绑定]（/ sdk / lib / fidl / cpp）
- [Go bindings](https://fuchsia.googlesource.com/third_party/go/+/master/src/syscall/zx/fidl/)  -[绑定]（https://fuchsia.googlesource.com/third_party/go/+/master/src/syscall/zx/fidl/）
- [Rust bindings](/garnet/public/lib/fidl/rust)  -[铁锈绑定]（/ garnet / public / lib / fidl / rust）

 
## Constituent Parts of Specification  规范的组成部分 

 
### FIDL Wire Format  FIDL线格式 

The FIDL wire format specified how FIDL messages are represented in memory for transmission over IPC. FIDL有线格式规定了如何在内存中表示FIDL消息以通过IPC传输。

The FIDL wire format is documented [Wire Format Specification].  FIDL有线格式记录在[Wire Format Specification]中。

 
### FIDL Language  FIDL语言 

The FIDL language is the syntax by which protocols are described in ***.fidl** files. FIDL语言是在***。fidl **文件中描述协议的语法。

The FIDL language is documented [Language Specification].  FIDL语言已记录在[语言规范]中。

 
### FIDL Compiler  FIDL编译器 

The FIDL compiler generates code for programs to use and implement protocols described by the FIDL language. FIDL编译器为程序使用和实现FIDL语言描述的协议生成代码。

The FIDL compiler is documented [Compiler Specification].  FIDL编译器记录在[编译器规范]中。

 
### FIDL Bindings  FIDL绑定 

FIDL bindings are language-specific runtime support libraries and code generators which provide APIs for manipulating FIDL data structures andprotocols. FIDL绑定是特定于语言的运行时支持库和代码生成器，它们提供用于处理FIDL数据结构和协议的API。

Languages-specific topics:  特定语言的主题：

 
*   [C Language Bindings]  * [C语言绑定]
*   [Low-Level C++ Language Bindings]  * [低级C ++语言绑定]
*   [High-Level C++ Language Bindings]  * [高级C ++语言绑定]

Bindings are available in various flavors depending on the language:  根据语言的不同，可以提供各种样式的绑定：

 
*   **Native bindings**: designed for highly sensitive contexts such as device drivers and high-throughput servers, leverage in-place access, avoid memoryallocation, but may require somewhat more awareness of the constraints ofthe protocol on the part of the developer. * **本地绑定**：专为设备驱动程序和高吞吐量服务器等高度敏感的上下文而设计，可利用就地访问，避免内存分配，但可能需要开发人员更多地了解协议的约束。
*   **Idiomatic bindings**: designed to be more developer-friendly by copying data from the wire format into easier to use data types (such as heap-backedstrings or vectors), but correspondingly somewhat less efficient as aresult. * **惯用绑定**：旨在通过将数据从有线格式复制到更易于使用的数据类型（例如堆支持的字符串或向量）中，从而对开发人员更友好，但因此效率相对较低。

Bindings offer several various ways of invoking protocol methods depending on the language: 绑定提供了几种不同的方法来调用协议方法，具体取决于语言：

 
*   **Send/receive**: read or write messages directly to a channel, no built-in wait loop (C) * **发送/接收**：直接将消息读取或写入通道，无内置等待循环（C）
*   **Callback-based**: received messages are dispatched asynchronously as callbacks on an event loop (C++, Dart) * **基于回调**：接收到的消息作为事件循环（C ++，Dart）上的回调异步分发
*   **Port-based**: received messages are delivered to a port or future (Rust)  * **基于端口**：接收到的消息将传递到端口或将来（Rust）
*   **Synchronous call**: waits for reply and return it (Go, C++ unit tests)  * **同步调用**：等待回复并返回（Go，C ++单元测试）

Bindings provide some or all of the following principal operations:  绑定提供以下一些或全部主要操作：

 
*   **Encode**: in-place transform native data structures into the wire format (coupled with validation) * **编码**：将本地数据结构就地转换为有线格式（与验证结合）
*   **Decode**: in-place transform wire format data into native data structures (coupled with validation) * **解码**：将有线格式数据就地转换为本地数据结构（与验证结合）
*   **Copy/Move To Idiomatic Form**: copy contents of native data structures into idiomatic data structures, handles are moved * **复制/移动到惯用格式**：将本机数据结构的内容复制到惯用数据结构中，将句柄移动
*   **Copy/Move To Native Form**: copy contents of idiomatic data structures into native data structures, handles are moved * **复制/移动到本机表单**：将惯用数据结构的内容复制到本机数据结构中，将句柄移动
*   **Clone**: copy native or idiomatic data structures (that do not contain move-only types) * **克隆**：复制本机或惯用数据结构（不包含仅移动类型）
*   **Call**: invoke protocol method  * ** Call **：调用协议方法

 
## Workflow  工作流程 

This section describes the workflow of authors, publishers, and consumers of IPC protocols described using FIDL. 本节介绍使用FIDL描述的IPC协议的作者，发布者和使用者的工作流程。

 
# Authoring FIDL  创作FIDL 

The author of a FIDL based protocol creates one or more ***.fidl files** to describe their data structures, protocols, and methods. 基于FIDL的协议的作者创建一个或多个***。fidl文件**，以描述其数据结构，协议和方法。

FIDL files are grouped into one or more **FIDL libraries** by the author. Each library represents a group of logically related functionality with a uniquelibrary name. FIDL files within the same library implicitly have access to allother declarations within the same library. The order of declarations within theFIDL files that make up a library is not significant. 作者将FIDL文件分为一个或多个** FIDL库**。每个库代表一组具有唯一库名称的逻辑相关功能。同一库中的FIDL文件隐式有权访问同一库中的所有其他声明。构成库的FIDL文件中的声明顺序并不重要。

FIDL files of one library can access declarations within another FIDL library by **importing** the other FIDL module. Importing other FIDL libraries makes theirsymbols available for use thereby enabling the construction of protocols derivedfrom them. Imported symbols must be qualified by the library name or by an aliasto prevent namespace collisions. 一个库的FIDL文件可以通过“导入”另一个FIDL模块来访问另一个FIDL库中的声明。导入其他FIDL库可使用它们的符号，从而能够构造从它们衍生的协议。导入的符号必须通过库名或别名来限定，以防止名称空间冲突。

 
# Publishing FIDL  发布FIDL 

The publisher of a FIDL based protocol is responsible for making FIDL libraries available to consumers. For example, the author may disseminate FIDL librariesin a public source repository or distribute them as part of an SDK. 基于FIDL的协议的发布者负责使FIDL库可供消费者使用。例如，作者可以在公共资源库中分发FIDL库，也可以将它们作为SDK的一部分进行分发。

Consumers need only point the FIDL compiler at the directory which contains the FIDL files for a library (and its dependencies) to generate code for thatlibrary. The precise details for how this is done will generally be addressed bythe consumer's build system. 使用者只需要将FIDL编译器指向包含库FIDL文件（及其依赖项）的目录即可为该库生成代码。消费者的构建系统通常会解决如何完成此操作的确切细节。

 
# Consuming FIDL  消费FIDL 

The consumer of a FIDL based protocol uses the FIDL compiler to generate code suitable for use with their language runtime specific bindings. For certainlanguage runtimes, the consumer may have a choice of a few different flavors ofgenerated code all of which are interoperable at the wire format level butperhaps not at the source level. 基于FIDL的协议的使用者使用FIDL编译器生成适用于其语言运行时特定绑定的代码。对于某些语言的运行时，使用者可以选择几种不同风格的生成代码，所有这些风格都可以在有线格式级别互操作，而在源代码级别则不能互操作。

In the Fuchsia world build environment, generating code from FIDL libraries will be done automatically for all relevant languages by individual FIDL buildtargets for each library. 在Fuchsia世界构建环境中，将通过每个库的单独FIDL构建目标为所有相关语言自动从FIDL库生成代码。

