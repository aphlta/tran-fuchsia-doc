 
# Tracing tutorial  跟踪教程 

A tutorial for enabling tracing in your code.  在代码中启用跟踪的教程。

 
## Overview  总览 

Tracing is used for a number of reasons, including:  使用跟踪的原因有很多，其中包括：

 
* to log unusual conditions,  *记录异常情况，
* to debug software,  *调试软件，
* to perform measurements,  *执行测量，
* to produce a timeline of events, and  *产生事件的时间表，以及
* to keep track of statistics.  *跟踪统计信息。

 
## Topics  话题 

In this tutorial, we'll examine tracing in Fuchsia and address the following topics: 在本教程中，我们将研究紫红色的跟踪并解决以下主题：

 
- What is tracing?  -什么是追踪？
- Why do I want to use it?  -为什么要使用它？
- What's the absolute simplest way to do a tracing "hello world"?  -进行“ hello world”追踪的最简单的绝对方法是什么？
- What are the "best practices" for tracing?  -跟踪的“最佳做法”是什么？
- How do I correlate trace data from disparate sources?  -如何关联来自不同来源的跟踪数据？

 
# Concepts  概念 

In the Fuchsia tracing system, three types of [components](/docs/glossary.md#component) cooperate in a distributed manner: 在紫红色的跟踪系统中，三种类型的[components]（/ docs / glossary.mdcomponent）以分布式方式进行协作：

 
* Trace Manager &mdash; an administrator that manages the overall tracing system  *跟踪管理器-管理整个跟踪系统的管理员
* Trace Provider &mdash; a program that generates trace data  *跟踪提供程序mdash;生成跟踪数据的程序
* Trace Client &mdash; a program that consumes trace data  *跟踪客户端mdash；消耗跟踪数据的程序

Let's suppose your program wants to create trace data. Your program would play the role of a trace provider &mdash; it generatestracing data.There can, of course, be many trace providers in a system. 假设您的程序要创建跟踪数据。您的程序将充当跟踪提供程序的角色–它会生成跟踪数据。系统中当然可以有许多跟踪提供程序。

Let's further suppose that a different program wants to process the data that your trace provider is generating.This program takes on the role of a trace client, and like the trace provider,there can be many trace clients in a system. 进一步假设另一个程序想要处理跟踪提供程序生成的数据。该程序担当跟踪客户端的角色，并且像跟踪提供程序一样，系统中可能有许多跟踪客户端。

> Note that there's currently just one trace client, with no immediate plans > to add more. We'll discuss this further below, in the> [Trace Client operation](#trace-client-operation) section. >请注意，当前只有一个跟踪客户端，没有立即计划>添加更多。我们将在下面的[Trace Client operation]（trace-client-operation）部分中对此进行进一步讨论。

What's interesting about Fuchsia's distributed implementation is that for efficiency, the trace provider writes the data directly into a sharedmemory segment (a Zircon [**VMO** &mdash; Virtual Memory Object](/docs/zircon/objects/vm_object.md)).The data isn't copied anywhere, it's stored in memory as it's generated. Fuchsia的分布式实现有趣的是，为了提高效率，跟踪提供程序将数据直接写入共享内存段（Zircon [** VMO ** mdash；虚拟内存对象]（/ docs / zircon / objects / vm_object.md））数据不会被复制到任何地方，而是在生成时存储在内存中。

This means that the trace client must somehow find out where that data is stored. This discovery is mediated by the trace manager. 这意味着跟踪客户端必须以某种方式找出该数据的存储位置。此发现由跟踪管理器进行调解。

There's exactly one trace manager in the system, and it serves as a central rendezvous point: a place where trace providers and trace clients meet. 系统中仅存在一个跟踪管理器，它充当中心集合点：跟踪提供者和跟踪客户端相遇的地方。

 
## Walkthrough  演练 

Let's look at this one step at a time.  让我们一次看看这一步。

 
### Trace Provider operation  跟踪提供程序操作 

Your program starts a background async loop (implemented as a thread in C, for example).This allows it to play the role of a trace provider by handling messages fromthe trace manager (like "start tracing" or "stop tracing"). 您的程序启动一个后台异步循环（例如，在C中实现为线程）。通过处理来自跟踪管理器的消息（例如“开始跟踪”或“停止跟踪”），它可以扮演跟踪提供者的角色。

Then, your program registers with the trace manager, telling it that it is ready to take on the role of being a trace provider. 然后，您的程序在跟踪管理器中注册，告知它已准备好充当跟踪提供者的角色。

Finally, your program goes about its business. Note that no tracing is happening yet &mdash; we're waiting for the tracemanager to start tracing in your program. 最后，您的程序开始其业务。请注意，尚未进行任何跟踪-mdash;我们正在等待tracemanager开始在您的程序中进行跟踪。

When tracing starts, the trace manager provides your program with a VMO into which it can write its data. 跟踪开始时，跟踪管理器为您的程序提供一个VMO，可以在其中写入数据。

From the perspective of your program, there's nothing special you need to do to handle the interaction with the async loop (that is, to turn tracing on oroff) &mdash; your program calls the various tracing API functions, and theythemselves determine if data should be written to the VMO or not. 从程序的角度来看，不需要做任何特殊的事情来处理与异步循环的交互（即打开或关闭跟踪）。您的程序调用了各种跟踪API函数，它们自己确定是否应将数据写入VMO。

> Note that tracing can be disabled entirely at compile-time. > In this case, *no* tracing code is present in your program;> and thus there's no way to turn it on.> A program built with tracing *enabled*, however, can respond to commands from> the trace manager to selectively enable or disable tracing. >请注意，可以在编译时完全禁用跟踪。 >在这种情况下，您的程序中没有*跟踪代码；>因此无法打开它。>但是，已启用* trace *跟踪功能的程序可以响应来自跟踪管理器的命令以选择性地进行响应。启用或禁用跟踪。

 
### Trace Client operation  跟踪客户端操作 

When a program wishes to assume the role of a trace client (that is, to get trace data), it contacts the trace manager, requests tracing to start (andsubsequently stop), and then finally saves collected trace data.The trace manager gathers the data and sends it over a socket to the traceclient. 当程序希望承担跟踪客户端的角色（即获取跟踪数据）时，它会与跟踪管理器联系，请求开始跟踪（并随后停止），然后最终保存收集的跟踪数据。数据并通过套接字将其发送到traceclient。

 
### Decoupling  去耦 

Because the trace provider writes to the VMO, the trace manager reads from the VMO, and the trace client reads data from a socket (provided by the tracemanager), there's no way for the trace client to directly affect the operationof the trace provider. 因为跟踪提供程序写入VMO，跟踪管理器从VMO读取，并且跟踪客户端从套接字（由tracemanager提供）读取数据，所以跟踪客户端无法直接影响跟踪提供程序的操作。

 
## On Demand  一经请求 

Tracing is on-demand &mdash; that is, your program normally runs with tracing turned off.When some event occurs (e.g., a system problem, or the user initiates adebugging session), tracing can be turned on for an arbitrary period.Not only can tracing be turned on or off, but specific categories of tracingcan be individually selected (we'll see this shortly). 跟踪是随需应变的；也就是说，您的程序通常在关闭跟踪的情况下运行。当发生某些事件（例如系统问题或用户启动调试会话）时，可以在任意时间打开跟踪。不仅可以打开或关闭跟踪。 ，但是可以单独选择特定的跟踪类别（我们将在不久后看到）。

Some time later, tracing can be turned off again.  一段时间后，可以再次关闭跟踪。

 
## `trace` and `traceutil`  trace和traceutil 

As mentioned above, there is currently just the one trace client. It consists of two utilities: `trace` and `traceutil`.The `trace` utility runs on the target, and `traceutil` runs on the developmenthost. 如上所述，当前只有一个跟踪客户端。它由两个实用程序组成：`trace`和`traceutil`。`trace`实用程序在目标上运行，`traceutil`在developmenthost上运行。

`trace` is used to control tracing &mdash; it sends the commands to the trace manager to start and stop tracing, and it gathers the trace data. trace用于控制跟踪。它将命令发送到跟踪管理器以开始和停止跟踪，并收集跟踪数据。

`traceutil`, on the development host side, communicates with `trace`. Trace data can be streamed from `trace` through `traceutil` right to thedeveloper's desktop. 在开发主机端，`traceutil`与`trace`通信。跟踪数据可以从trace到traceutil流到开发人员的桌面。

 
# Hello World  你好，世界 

Assuming that the background async loop is started and running (see [Fuchsia Tracing System Design](design.md) for details),this is the minimum code you need in order to write a simple string tothe trace buffer: 假设后台异步循环已启动并正在运行（有关详细信息，请参见[Fuchsia跟踪系统设计]（design.md）），这是将简单的字符串写入跟踪缓冲区所需的最少代码：

```c
TRACE_INSTANT("category", "name", TRACE_SCOPE_PROCESS, "message", TA_STRING("Hello, World!"));
```
 

There are 5 arguments to the macro `TRACE_INSTANT()`. In order, they are: 宏`TRACE_INSTANT（）`有5个参数。按顺序，它们是：

 
1. `"category"` &mdash; this is a nul-terminated string representing the category of the trace event. 1.“类别”这是一个以空值结尾的字符串，表示跟踪事件的类别。
2. `"name"` &mdash; a nul-terminated string representing the name of the trace event. 2.`“ name”`mdash;以空值结尾的字符串，表示跟踪事件的名称。
3. `TRACE_SCOPE_PROCESS` &mdash; for the `TRACE_INSTANT` tracing macro, this indicates the scope of the event. 3.`TRACE_SCOPE_PROCESS` mdash;对于“ TRACE_INSTANT”跟踪宏，它指示事件的范围。
4. `"message"` &mdash; this is the "key" part of the data.  4.`“ message”`mdash;这是数据的“关键”部分。
5. `TA_STRING("Hello, World!")` &mdash; this is the "value" part of the data.  5.`TA_STRING（“ Hello，World！”）`mdash;这是数据的“价值”部分。

The result of executing this code is that if tracing is compiled in, and enabled, a trace datum will be logged to the VMO.If tracing is compiled in, but not enabled, this code returns almostimmediately (it checks to see if tracing is enabled, and discovering that it'snot, doesn't do anything else).If tracing isn't compiled in, this code doesn't even make it past the Ccompiler &mdash; no code is generated (it's like the entire `TRACE_INSTANT()`macro was a comment). 执行此代码的结果是，如果在其中编译并启用了跟踪，则将跟踪数据记录到VMO中。如果在其中编译了但未启用跟踪，则该代码几乎立即返回（它检查是否启用了跟踪） ，并发现它不是，则不会执行任何其他操作。）如果未编译跟踪，则此代码甚至无法通过Ccompiler mdash；没有代码生成（就像整个TRACE_INSTANT（）宏是注释一样）。

> The key and value arguments are optional, and can be repeated. > Whenever you specify a key you must specify a value (even if the value> is nul). >键和值参数是可选的，并且可以重复。 >每当您指定键时，都必须指定一个值（即使value>为nul）。

 
## Category  类别 

What is a category?  什么是类别？

A category is something that you define; there's a convention for how categories should look: 类别是您定义的；有一个关于类别外观的约定：

*provider*`:`*category*[`:`*sub-category*[...]]  * provider *`：`* category * [`：`* sub-category * [...]]

For example, "`demo:flow:outline`" which has three colon-delimited elements:  例如，“`demo：flow：outline`”具有三个以冒号分隔的元素：

 
* `demo` is the name of the trace provider; it identifies your program  *`demo`是跟踪提供者的名称；它可以识别您的程序
* `flow` is the name of the category; here, we're using a name that suggests that we are tracing the call-by-call flow of the program *`flow`是类别的名称；在这里，我们使用的名称表明我们正在跟踪程序的逐个调用流程
* `outline` is the name of the sub-category; here, we're using a name that suggests that we are tracing the high-level flow of the program, perhapsjust a few top-level functions. *`outline`是子类别的名称；在这里，我们使用的名称表明我们正在跟踪程序的高层流程，也许只是一些顶层函数。

We might have another category name, `demo:flow:detailed`, for example, which we could use to trace the detailed flow of the program. 例如，我们可能有另一个类别名称“ demo：flow：detailed”，可用于跟踪程序的详细流程。

> The names are at your discretion; whatever has meaning for you. > Beware though, that the category namespace is global to all programs running,> so if there was another program with the "provider" set to `demo` as well,> you would most likely run into naming conflicts (and thus could end up with> unrelated data from some other trace provider). >名称由您自行决定；任何对您有意义的东西。 >但是要注意，类别名称空间对于所有正在运行的程序都是全局的，>因此，如果还有另一个将“ provider”设置为`demo`的程序，>您很可能会遇到命名冲突（因此可能最终会冲突）来自其他跟踪提供程序的不相关数据）。

Categories should be grouped hierarchically. For example, with statistics collection, you might have some sub-categories: 类别应按层次进行分组。例如，对于统计信息收集，您可能有一些子类别：

 
* `demo:statistics:bandwidth` &mdash; to collect bandwidth statistics,  *`demo：statistics：bandwidth` mdash;收集带宽统计信息，
* `demo:statistics:requests` &mdash; to collect user request statistics.  *`demo：statistics：requests` mdash;收集用户请求统计信息。

Categories, therefore, give you control over what's collected. If a category is not requested by the trace client program, then the data isnot collected by the trace provider. 因此，类别使您可以控制所收集的内容。如果跟踪客户端程序未请求类别，则跟踪提供程序不会收集数据。

 
## Name  名称 

The name argument (2nd argument in our `TRACE_INSTANT()`, and in fact most other macros) is a string description of the event data. 名称参数（我们的TRACE_INSTANT（）中的第二个参数，实际上是大多数其他宏）是事件数据的字符串描述。

So, if we had a category of `demo:statistics:bandwidth` we might have two different trace points, one that counted received packets and another thatcounted transmitted packets.We'd use the name to distinguish them: 因此，如果我们有一个类别为``demo：statistics：bandwidth''，我们可能有两个不同的跟踪点，一个跟踪接收数据包，另一个跟踪传输数据包，我们将使用名称来区分它们：

```c
// we just received another packet, log it
status.rx_count++;
TRACE_INSTANT("demo:statistics:bandwidth", "rxpackets", TRACE_SCOPE_PROCESS,
              "count", TA_UINT64(status.rx_count));
```
 

versus  与

```c
// we just transmitted another packet, log it
status.tx_count++;
TRACE_INSTANT("demo:statistics:bandwidth", "txpackets", TRACE_SCOPE_PROCESS,
              "count", TA_UINT64(status.tx_count));
```
 

> Notice that, as mentioned above, we have both a key (the `"count"` argument) > and a value (the `TA_UINT64()` encoded value). >请注意，如上所述，我们既有一个键（“ count”参数）又有一个值（TA_UINT64（）编码值）。

 
## Encoding  编码方式 

In the examples above, we saw `TA_STRING()` and `TA_UINT64()` macros. They're used to properly encode the value for C.For C++, you can still use the macro, but it's notrequired because the value type can be inferred (for all but three, shown inthe table below as "req'd" in the "C++" column). 在上面的示例中，我们看到了TA_STRING（）和TA_UINT64（）宏。它们用于对C的值进行正确编码。对于C ++，您仍然可以使用宏，但这不是必需的，因为可以推断出值的类型（对于除三个以外的所有值，下表中的“ req'd”显示为“ C ++”列）。

Macro             |  C++  | Description ------------------|-------|--------------------------------------------------------------TA_NULL           |       | a null value.TA_BOOL           |       | a boolean value.TA_INT32          |       | a signed 32-bit integer value.TA_UINT32         |       | an unsigned 32-bit integer value.TA_INT64          |       | a signed 64-bit integer value.TA_UINT64         |       | an unsigned 64-bit integer value.TA_DOUBLE         |       | a double-precision floating point value.TA_CHAR_ARRAY     | req'd | a character array with a length (copied rather than cached).TA_STRING         |       | a null-terminated dynamic string (copied rather than cached).TA_STRING_LITERAL | req'd | a null-terminated static string constant (cached).TA_POINTER        |       | a pointer value (records the memory address, not the target).TA_KOID           | req'd | a kernel object id. 宏| C ++ |说明------------------ | ------- | ---------------------- ---------------------------------------- TA_NULL | |一个空值。 |一个布尔值。 |一个有符号的32位整数值。 | TA_INT64 |一个无符号的32位整数值。 |一个有符号的64位整数值。 |一个无符号的64位整数值。 | TA_CHAR_ARRAY |一个双精度浮点值。要求|具有长度（复制而不是缓存）的字符数组。 |一个以空值结尾的动态字符串（已复制而不是缓存）。TA_STRING_LITERAL|要求|一个以空值终止的静态字符串常量（已缓存）。 |一个指针值（记录内存地址，而不是目标）。要求|内核对象ID。

For the most part, the above operate as you'd expect. For example, the `TA_INT32()` macro takes a 32-bit signed integer as anargument. 在大多数情况下，上述操作会按您期望的那样进行。例如，TA_INT32（）宏将32位带符号整数作为自变量。

The notable exceptions are:  值得注意的例外是：

 
* `TA_NULL()` &mdash; does not take an argument, that is, it's written literally as `TA_NULL()` (in C++, you could use `nullptr` instead of the`TA_NULL()` macro). *`TA_NULL（）`mdash;不带参数，也就是说，它的字面写为“ TA_NULL（）”（在C ++中，可以使用“ nullptr”代替“ TA_NULL（）”宏）。
* `TA_CHAR_ARRAY()` &mdash; takes two arguments, the first is a pointer to the character array, and the second is its length. *`TA_CHAR_ARRAY（）`mdash;有两个参数，第一个是指向字符数组的指针，第二个是其长度。

 
### C++ notes  C ++笔记 

Note that in C++, when using a literal constant, type inference needs a hint in order to get the size, signedness, and type right. 请注意，在C ++中，使用文字常量时，类型推断需要提示以获取大小，符号和正确的类型。

For example, is the value `77` a signed 32-bit integer? An unsigned 32-bit integer? Or maybe even a 64-bit integer of some kind? 例如，值“ 77”是否为带符号的32位整数？一个无符号的32位整数？或者甚至是某种64位整数？

Type inference in the tracing macros works according to the standard C++ rules:  跟踪宏中的类型推断根据标准C ++规则进行工作：

 
*   `77` is a signed 32-bit integer, `TA_INT32`  * 77是带符号的32位整数TA_INT32
*   `77U` is an unsigned 32-bit integer, `TA_UINT32`  * 77U是32位无符号整数TA_UINT32
*   `77L` is a signed 64-bit integer, `TA_INT64`  *`77L`是一个有符号的64位整数TA_INT64
*   `77LU` is an unsigned 64-bit integer, `TA_UINT64`  * 77LU是一个无符号的64位整数TA_UINT64

This also means that floating point needs to be explicitly noted if it's an (otherwise) integer value.`77` is, as above, a `TA_INT32`, but `77.` (note the period) is a `TA_DOUBLE`. 这也意味着如果浮点数是一个（否则）整数值，则需要明确指出浮点数。如上所述，`77`是TA_INT32`，但是`77.（请注意句点）是TA_DOUBLE。

For this reason, if you're using constants, you should consider retaining the encoding macros if you're expressing the values directly, or you should usethe appropriate `const` type: 因此，如果使用常量，则在直接表达值时应考虑保留编码宏，或者应使用适当的const类型：

```cpp
TRACE_INSTANT("category", "name", "int", 77);   // discouraged
```
 

is the same as:  是相同的：

```cpp
const int32_t my_id = 77;                       // well defined type
TRACE_INSTANT("category", "name", "int", my_id);
```
 

and:  和：

```cpp
#define MY_ID   (TA_INT32(77))                  // uses the typing macro
TRACE_INSTANT("category", "name", "int", MY_ID);
```
 

 
## Multiple key/value pairs  多个键/值对 

As mentioned above, you can have zero or more key/value pairs. For example: 如上所述，您可以有零个或多个键/值对。例如：

```cpp
TRACE_INSTANT("category", "name", TRACE_SCOPE_PROCESS);
TRACE_INSTANT("category", "name", TRACE_SCOPE_PROCESS, "key1", nullptr);
TRACE_INSTANT("category", "name", TRACE_SCOPE_PROCESS, "key1", "string1");
TRACE_INSTANT("category", "name", TRACE_SCOPE_PROCESS, "key1", "string1", "key2", 77);
```
 

 
## Scope  范围 

For the `TRACE_INSTANT()` macros, there are three values of the "scope" (3rd argument): 对于`TRACE_INSTANT（）`宏，“ scope”（第三个参数）有三个值：

Scope               | Meaning --------------------|---------TRACE_SCOPE_THREAD  | The event is only relevant to the thread it occurred onTRACE_SCOPE_PROCESS | The event is only relevant to the process in which it occurredTRACE_SCOPE_GLOBAL  | The event is globally relevant 范围|含义-------------------- | --------- TRACE_SCOPE_THREAD |该事件仅与发生在TRACE_SCOPE_PROCESS上的线程有关。该事件仅与发生该事件的过程有关。该活动具有全球意义

 
# Conditional compilation for tracing  用于跟踪的条件编译 

There are cases where you might wish to entirely disable tracing (like final release). 在某些情况下，您可能希望完全禁用跟踪（例如最终版本）。

The `NTRACE` macro is what's used to make this happen.  NTRACE宏是用来实现此目的的宏。

This is similar to the `NDEBUG` macro used with **assert()** &mdash; if the macro is present, then the **assert()** calls don't generate any code. 这类似于与** assert（）** mdash一起使用的`NDEBUG`宏；如果存在宏，则assert（）调用不会生成任何代码。

In the case of tracing, if the `NTRACE` macro is present, then the tracing macros don't generate any code. 在跟踪的情况下，如果存在“ NTRACE”宏，则跟踪宏不会生成任何代码。

> In particular, keep in mind the *negative* sense &mdash; if the macro is > **present**, then tracing is **disabled**. >特别要记住*负*符号；如果宏> **存在**，则跟踪被禁用**。

You can explicitly turn on the macro yourself to disable tracing:  您可以自己显式打开宏以禁用跟踪：

```c
#define NTRACE  // disable tracing
#include <trace/event.h>
```
 

Here, the macros contained in the tracing file (like `TRACE_INSTANT()`) are made inactive; they're effectively converted to comments, which are eliminatedby the compiler. 在这里，包含在跟踪文件中的宏（如`TRACE_INSTANT（）`）被禁用；它们被有效地转换为注释，编译器将其消除。

> Notice that we defined the macro *before* the `#include` &mdash; this is > required in order to select the inactive forms of the macro expansions in> the `#include` file. >注意，我们在`include` mdash之前*定义了宏；为了在“ include”文件中选择无效的宏扩展形式，这是必需的。

You can also test the `NTRACE` macro, to see if you need to provide tracing data. 您也可以测试`NTRACE`宏，以查看是否需要提供跟踪数据。

In the example above, where we discussed the `rxpackets` and `txpackets` counters, you might have a general statistics structure: 在上面的示例中，我们讨论了rxpackets和txpackets计数器，您可能具有常规的统计结构：

```c
typedef struct {
#ifndef NTRACE  // reads as "if tracing is not disabled"
    uint64_t    rx_count;
    uint64_t    tx_count;
#endif
    uint64_t    npackets;
} my_statistics_t;
```
 

The `rx_count` and `tx_count` fields are used only with tracing, so if `NTRACE` is asserted (meaning tracing is completely disabled), they don't take up anyroom in your `my_statistics_t` structure. rx_count和tx_count字段仅与跟踪一起使用，因此，如果断言了NTRACE（意味着完全禁用了跟踪），则它们不会占用my_statistics_t结构中的任何空间。

This does mean that you need to conditionally compile the code for managing the recording of those statistics: 这确实意味着您需要有条件地编译用于管理这些统计信息记录的代码：

```c
#ifndef NTRACE
    status.tx_count++;
    TRACE_INSTANT("demo:statistics:bandwidth", "txpackets", TRACE_SCOPE_PROCESS,
                  "count", TA_UINT64(status.tx_count));
#endif  // NTRACE
```
 

 
## Determining if tracing is on or off  确定跟踪是打开还是关闭 

There's one more case to consider.  还有一种情况需要考虑。

Sometimes, you may wish to determine if tracing is on at runtime. There's a handy test macro, `TRACE_ENABLED()`.If tracing is compiled in (`NTRACE` is not defined), then the `TRACE_ENABLED()`macro looks to see if tracing is currently turned on or off in your traceprovider, and returns a true or false value at runtime.Note that if tracing is compiled out, then `TRACE_ENABLED()` always returnsfalse (generally causing the compiler to entirely optimize out the code). 有时，您可能希望确定运行时是否启用了跟踪。有一个方便的测试宏`TRACE_ENABLED（）`如果在（未定义`NTRACE`）中编译跟踪，则`TRACE_ENABLED（）`宏会查看您的traceprovider中当前是打开还是关闭了跟踪，并且在运行时返回一个true或false值。注意，如果跟踪被编译出来，那么TRACE_ENABLED（）总是返回false（通常使编译器完全优化代码）。

For example:  例如：

```c
#ifndef NTRACE
    if (TRACE_ENABLED()) {
        int v = do_something_expensive();
        TRACE_INSTANT(...
    }
#endif  // NTRACE
```
 

Here, if tracing is compiled in, **and** enabled, we call **do_something_expensive()**, perhaps to fetch some data for tracing. 在这里，如果跟踪被编译，启用并启用，我们将调用do_something_expensive（）**，也许是为了获取一些数据进行跟踪。

Notice that we used both the `#ifndef` and the `TRACE_ENABLED()` macro together.That's because the function **do_something_expensive()** might not exist in thetrace-disabled version, and thus you'd get compiler and linker diagnostics. 注意我们同时使用了`ifndef`和`TRACE_ENABLED（）`宏，这是因为禁用跟踪的版本中可能不存在函数** do_something_expensive（）**，因此您将获得编译器和链接器诊断信息。

 
### Category selection  类别选择 

There's a similar macro, `TRACE_CATEGORY_ENABLED()` that simply gives you more refinement; you can test if a particular category is enabled or not.As with `TRACE_ENABLED()`, if tracing is compiled out, this macro reduces to an`if (0)`, which the compiler optimizes out. 有一个类似的宏`TRACE_CATEGORY_ENABLED（）`可以使您更加完善。您可以测试是否启用了特定类别。与`TRACE_ENABLED（）`一样，如果跟踪被编译出来，则该宏将减少为`if（0）`，编译器会对其进行优化。

 
# Timing events  计时事件 

Another common function during tracing is timing things. Often, you'll want to know "how long does this operation take?"or "how long does this procedure run for?" 跟踪过程中的另一个常见功能是计时。通常，您会想知道“此操作需要多长时间？”或“此过程需要运行多长时间？”。

There are three macros that can be used here:  这里可以使用三个宏：

 
* `TRACE_DURATION()` &mdash; monitor the duration of the current scope,  *`TRACE_DURATION（）`mdash;监视当前范围的持续时间，
* `TRACE_DURATION_BEGIN()` and `TRACE_DURATION_END()` &mdash; monitor the duration of a specific, bounded section of code. *`TRACE_DURATION_BEGIN（）`和`TRACE_DURATION_END（）`mdash;监视特定的有界代码段的持续时间。

> These timing macros are often used without any key/value data; we'll > show them both ways below. >这些计时宏通常不使用任何键/值数据；我们将在下面以两种方式显示它们。

For example:  例如：

```c
int my_function(void) {
    TRACE_DURATION("demo:timing:functions", "my_function");
    // your function does stuff here...
}
```
 

This generates a trace event when **my_function()** ends, indicating the length of time spent in the function (and all called functions). 当** my_function（）**结束时，这将生成一个跟踪事件，指示该函数（以及所有调用的函数）所花费的时间长度。

> Yes, this works in C &mdash; a compiler extension is used to add a code hook > at scope end. >是的，这适用于C mdash；编译器扩展用于在作用域末尾添加代码hook>。

 
## Use during constructor  在构造函数中使用 

A fairly common use case for the `TRACE_DURATION()` macro is in C++ constructors (and other member functions), with additional data captured atthe same time. 在C ++构造函数（和其他成员函数）中，TRACE_DURATION（）宏的一个相当普遍的用例是同时捕获其他数据。

This is from one of the `blobfs` vnode constructors (`zircon/system/ulib/blobfs/blobfs.cpp`): 这来自`blobfs` vnode构造函数之一（`zircon / system / ulib / blobfs / blobfs.cpp`）：

 

```cpp
zx_status_t VnodeBlob::InitCompressed() {
    TRACE_DURATION("blobfs", "Blobfs::InitCompressed", "size", inode_.blob_size,
                   "blocks", inode_.num_blocks);
    ...
```
 

Here, the length of time spent in the constructor, along with the size and number of blocks, is captured.By the way, notice how the macros for the types of `inode_.blob_size` and`inode_.num_blocks` are not used in the C++ version &mdash; their type isinferred by the compiler. 在这里，捕获了在构造函数中花费的时间以及块的大小和数量，顺便说一下，注意在inode_.blob_size和inode_.num_blocks类型的宏中是如何不使用的。 C ++版本的mdash;它们的类型由编译器推断。

 
## Use for arbitrary scope  用于任意范围 

`TRACE_DURATION()` can be used for any scope, not just an entire function:  TRACE_DURATION（）可以用于任何范围，而不仅仅是整个功能：

```c
int my_function(void) {
    if (this) {
        TRACE_DURATION("demo:timing:functions", "my_function", "path", TA_STRING ("this"));
        // do stuff that's timed
    } else {
        TRACE_DURATION("demo:timing:functions", "my_function", "path", TA_STRING ("that"));
        // do other stuff that's timed
    }
}
```
 

Here, two different timing durations are captured, depending on which path is taken in the code, with the key/value pair indicating the selected one. 在此，根据代码中采用的路径，捕获了两个不同的计时持续时间，其中键/值对指示选定的一个。

For greater control over the area that's timed, you can use the `TRACE_DURATION_BEGIN()` and `TRACE_DURATION_END()` macros: 为了更好地控制定时区域，可以使用`TRACE_DURATION_BEGIN（）`和`TRACE_DURATION_END（）`宏：

```c
int my_function(void) {
    if (this) {

        // do something that you don't want to time here

        // start timing
        TRACE_DURATION_BEGIN("demo:timing:functions", "my_function:area1");

        // do something that you'd like to time here

        // end timing
        TRACE_DURATION_END("demo:timing:functions", "my_function:area1");

        // do something else that you don't want to time here
    }
}
```
 

In this sample, we added some path information to the name component.  在此示例中，我们向名称组件添加了一些路径信息。

The rule here is that the `TRACE_DURATION_BEGIN()` must have a matching `TRACE_DURATION_END()` macro in the same scope.Matching means that both the category and name must be the same. 这里的规则是，TRACE_DURATION_BEGIN（）必须在相同范围内具有匹配的`TRACE_DURATION_END（）`宏。匹配意味着类别和名称必须相同。

> The macros must can be nested hierarchically.  >宏必须可以分层嵌套。

For example:  例如：

```c
int my_function(void) {
    if (this) {

        // do something that you don't want to time

        TRACE_DURATION_BEGIN("demo:timing:functions", "my_function:area1");
        // NOTE 1

        // do something that you'd like to time

        TRACE_DURATION_BEGIN("demo:timing:functions", "my_function:inner");
        // NOTE 2

        // do something that you'd like timed by "inner"

        // NOTE 3
        TRACE_DURATION_END("demo:timing:functions", "my_function:inner");

        // do something that's still timed by "area1" but not "inner"

        // NOTE 4
        TRACE_DURATION_END("demo:timing:functions", "my_function:area1");

        // do something else that you don't want to time
    }
}
```
 

To be clear about what the above is doing &mdash; there are two parts of the code being timed; an overall "my_function:area1" that spans from "NOTE 1"through to and including "NOTE 4", and a separately timed area"my_function:inner" that spans from "NOTE 2" through to and including "NOTE 3". 要清楚地知道上面在做什么–定时代码有两个部分；整个“ my_function：area1”范围从“ NOTE 1”到“ NOTE 4”，包括一个单独计时的区域“ my_function：inner”，范围从“ NOTE 2”到“ NOTE 3”。

> Tip: prefer the **TRACE_DURATION()** macro over the > **TRACE_DURATION_BEGIN()** and **TRACE_DURATION_END()** macros. The simple> **TRACE_DURATION()** macro automatically handles leaving scope, whereas the> begin/end style macros don't &mdash; you need to manually ensure correct> nesting and termination.>> Also, note that **TRACE_DURATION()** takes roughly *half* the space in the> output buffer as **TRACE_DURATION_BEGIN()** and **TRACE_DURATION_END()** do!> This can have a big impact on size. >提示：优先于** TRACE_DURATION_BEGIN（）**和** TRACE_DURATION_END（）**宏，而不是** TRACE_DURATION（）**宏。简单的** TRACE_DURATION（）**宏会自动处理离开范围，而>开始/结束样式宏不会乱码；您需要手动确保正确的>嵌套和终止。>>另外，请注意** TRACE_DURATION（）**大约*一半*输出缓冲区中的空间，分别为TRACE_DURATION_BEGIN（）**和TRACE_DURATION_END（） **做！>这会对尺寸产生重大影响。

 
## Resolution  解析度 

All trace timing is expressed as an unsigned 64-bit count of 1 nanosecond ticks, giving a 584+ year range (which should be sufficient for all but themost patient of users). 所有跟踪时间都表示为1纳秒刻度的无符号64位计数，给出了584+年的范围（对于大多数用户之外的所有患者，这应该足够了）。

 
# Asynchronous tracing  异步跟踪 

All of the examples so far have been "synchronous" &mdash; that is, occurring in a linear fashion in one thread. 到目前为止，所有示例都是“同步”的。也就是说，在一个线程中以线性方式发生。

There's a set of "asynchronous" tracing functions that are used when the operation spans multiple threads. 当操作跨越多个线程时，将使用一组“异步”跟踪函数。

For example, in a multi-threaded server, a request is handled by one thread, and then put back on a queue while the operation is in progress.Some time later, another thread receives notification that the operation hascompleted, and "picks up" the processing of that request.The goal of asynchronous tracing is to allow the correlation of these disjointtrace events. 例如，在多线程服务器中，请求由一个线程处理，然后在操作进行时放回队列。一段时间后，另一个线程收到操作已完成的通知，并“提起”异步跟踪的目标是允许这些不交织的跟踪事件相关。

Asynchronous tracing takes into consideration that the same code path is used for multiple different flows of processing.In the previous examples, we were interested in seeing how long a particularfunction ran, or what a certain value was at a given point in time.With asynchronous tracing, we're interested in tracking the same data, but fora logical processing flow, rather than a program location based flow. 异步跟踪考虑了将相同的代码路径用于多个不同的处理流。在前面的示例中，我们感兴趣的是查看特定功能运行了多长时间，或者在给定的时间点确定的值是多少。跟踪，我们有兴趣跟踪相同的数据，但要跟踪逻辑处理流程，而不是基于程序位置的流程。

In the queue processing example, the code that receives requests would tag each request with a "nonce" &mdash; a unique value that follows the request around.This nonce can be generated via `TRACE_NONCE()`, which simply increments aglobal counter. 在队列处理示例中，接收请求的代码将为每个请求加上“ nonce”标记。这个随机数可以通过`TRACE_NONCE（）`生成，它只需增加一个全局计数器即可。

Let's see how this works. First, you declare a place to hold the nonce.This is usually in a context structure for the request itself: 让我们看看它是如何工作的。首先，您声明一个存放随机数的地方，通常在请求本身的上下文结构中：

```c
typedef struct {
...
    // add the nonce to your context structure
    trace_async_id_t async_id;
} my_request_context_t;
```
 

When the request arrives, you fetch a nonce and begin the asynchronous tracing flow: 当请求到达时，您获取一个随机数并开始异步跟踪流程：

```c
// a new request; start asynchronous tracing
ctx->async_id = TRACE_NONCE();
TRACE_ASYNC_BEGIN("category", "name", ctx->async_id, "key", TA_STRING("value"));
```
 

You can log trace events periodically using the `TRACE_ASYNC_INSTANT()` macro (similar to what we did with the `TRACE_INSTANT()` macro above): 您可以使用`TRACE_ASYNC_INSTANT（）`宏定期记录跟踪事件（类似于我们上面对`TRACE_INSTANT（）`宏所做的操作）：

```c
TRACE_ASYNC_INSTANT("category", "name", ctx->async_id, "state", TA_STRING("phase2"));
```
 

And clean up via `TRACE_ASYNC_END()`:  并通过`TRACE_ASYNC_END（）`进行清理：

```c
TRACE_ASYNC_END("category", "name", ctx->async_id);
```
 

> Don't confuse this use of "async" with the async loop that's running in your > process; they aren't related. >不要将这种“异步”的使用与您的进程中正在运行的异步循环混淆；他们没有关系。

 
# Flow tracing  流跟踪 

Asynchronous tracing is intended for tracing within the same process, but perhaps by way of different threads. 异步跟踪旨在在同一进程中进行跟踪，但可能通过不同的线程进行。

There's a higher-level tracing mechanism, called "flow" tracing, that's intended for use between processes or abstraction layers. 有一种更高级别的跟踪机制，称为“流”跟踪，旨在在进程或抽象层之间使用。

You call `TRACE_FLOW_BEGIN()` to mark the start of a "flow". Just like `TRACE_ASYNC_BEGIN()`, you pass in a nonce to identify thisparticular flow. The flow ID is an unsigned 64-bit integer. 您调用`TRACE_FLOW_BEGIN（）`来标记“流”的开始。就像`TRACE_ASYNC_BEGIN（）`一样，您传入一个随机数以标识此特定流。流ID是无符号的64位整数。

Then, you (optionally) call `TRACE_FLOW_STEP()` to indicate trace operations within that flow. 然后，您（可选）调用`TRACE_FLOW_STEP（）`以指示该流中的跟踪操作。

When you're done, you end the flow with `TRACE_FLOW_END()`.  完成后，您将以“ TRACE_FLOW_END（）”结束流程。

A flow could be used, for example, between a client and server for tracking a request end-to-end from the client, through the server, and back to the client. 例如，可以在客户端和服务器之间使用流，以跟踪从客户端到服务器端对端的请求，然后再回到客户端。

 
# Provider registration  提供商注册 

Trace providers must register with Trace Manager in order for them to participate in tracing. This registration involves two pieces: 跟踪提供者必须在跟踪管理器中注册才能使他们参与跟踪。此注册涉及两部分：

 
- code to do the registration,  -进行注册的代码，
- an entry in the component manifest to give the component access to Trace Manager. -组件清单中的条目，使组件可以访问跟踪管理器。

 
## Registration  注册 

The simple form of registration in C++ requires an async loop.  C ++中的简单注册形式需要异步循环。

Here's a simple example:  这是一个简单的例子：

```cpp
#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <trace-provider/provider.h>
// further includes

int main(int argc, const char** argv) {
  // process argv

  async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
  trace::TracelinkProviderWithFdio trace_provider(
      loop.dispatcher(), "my_trace_provider");

  // further setup

  loop.Run();
  return 0;
}
```
 

This example uses `fdio` to set up the FIDL channel with Trace Manager.  本示例使用`fdio`通过跟踪管理器设置FIDL通道。

 
## Component access  组件访问 

Like all things in Fuchsia, access to capabilities must be spelled out, there is no ambient authority. Trace providers indicate their need tocommunicate with Trace Manager by saying so in their component manifest,which typically lives in a file with a `.cmx' suffix. 像紫红色中的所有事物一样，必须明确说明获得功能的权限，没有周围的权限。跟踪提供程序通过在其组件清单中这样表示来表明他们需要与跟踪管理器进行通信，该组件清单通常位于后缀为“ .cmx”的文件中。

Here's a simple example:  这是一个简单的例子：

```json
{
    "program": {
        "binary": "bin/app"
    },
    "sandbox": {
        "services": [
            "fuchsia.tracing.provider.Registry"
        ]
    }
}
```
 

For further information on component manifests, see [Component Manifests](/docs/concepts/storage/component_manifest.md). 有关组件清单的更多信息，请参见[Component Manifests]（/ docs / concepts / storage / component_manifest.md）。

 
# Background  背景 

> @@@ Here we'll highlight the differences and similarities amongst logging, > tracing, inspection, and debugging. > @@@在这里，我们将重点介绍日志记录，跟踪，检查和调试之间的区别和相似之处。

 
# References  参考文献 

 
* [Adding Tracing to Device Drivers](/docs/concepts/drivers/tracing.md) gives details on source code additions (e.g., what `#include` files to add)and Makefile additions required by the trace provider in order to addtracing, or disable it completely. * [向设备驱动程序添加跟踪]（/ docs / concepts / drivers / tracing.md）提供了有关源代码添加的详细信息（例如，要添加的“ include”文件）以及跟踪提供程序为添加跟踪所需的Makefile添加的详细信息，或完全禁用它。
* [Fuchsia Tracing System Design](design.md) goes through the design goals of the tracing system. * [紫红色跟踪系统设计]（design.md）遍历了跟踪系统的设计目标。
