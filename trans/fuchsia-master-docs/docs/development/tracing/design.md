 
# Fuchsia Tracing System Design  紫红色追踪系统设计 

This document describes a mechanism for collecting diagnostic trace information from running applications on the Fuchsia operating system. 本文档介绍了一种从紫红色操作系统上运行的应用程序收集诊断跟踪信息的机制。

 
## Overview  总览 

The purpose of Fuchsia tracing is to provide a means to collect, aggregate, and visualize diagnostic tracing information from Fuchsia user spaceprocesses and from the Zircon kernel. 紫红色跟踪的目的是提供一种收集，聚合和可视化来自紫红色用户空间过程和Zircon内核的诊断跟踪信息的方法。

 
## Design Goals  设计目标 

 
- Lightweight Instrumentation  -轻巧的仪器
  - Enabling tracing should not significantly affect the performance of running applications.  Trace providers should not need to acquire locks, makesyscalls, or perform dynamic memory allocation required between the timewhen tracing is activated and when it is disabled. -启用跟踪不应显着影响正在运行的应用程序的性能。跟踪提供者在激活跟踪和禁用跟踪之间不需要获取锁，makesyscall或执行所需的动态内存分配。
- Compact Memory Footprint  -紧凑的内存占用
  - Trace records are stored compactly in memory so that buffers can remain small but hold many events. -跟踪记录紧凑地存储在内存中，因此缓冲区可以很小，但可以容纳许多事件。
- Crash-proof  -防撞
  - It is possible to collect partial traces even if trace providers terminate (normally or abnormally) during trace collection. -即使在跟踪收集过程中跟踪提供者终止（正常或异常），也可以收集部分跟踪。
- Flexible and Universal  -灵活通用
  - Can trace code written in any language given a suitable implementation of the tracing library. -在跟踪库的适当实现下，可以跟踪以任何语言编写的代码。
  - Trace points can be manually inserted by the developer or generated dynamically by tools. -跟踪点可以由开发人员手动插入或由工具动态生成。
- General  - 一般
  - The trace format defines general purpose record types which support a wide range of data collection needs. -跟踪格式定义了通用记录类型，可支持各种数据收集需求。
  - Trace data can be transformed into other formats for visualization using tools such as Catapult or TraceViz. -可以使用Catapult或TraceViz等工具将跟踪数据转换为其他格式以进行可视化。
- Extensible  -可扩展
  - New record types can be added in the future without breaking existing tools.  -将来可以添加新的记录类型，而不会破坏现有的工具。
- Robust  - 强大的
  - Enabling tracing does not compromise the integrity of running components or expose them to manipulation by tracing clients. -启用跟踪不会损害正在运行的组件的完整性，也不会通过跟踪客户端而使其暴露于操纵之下。

 
## Moving Parts  移动部件 

 
### Trace Manager  跟踪管理器 

The trace manager is a system service which coordinates registration of trace providers.  It ensures that tracing proceeds in an orderly mannerand isolates components which offer trace providers from trace clients. 跟踪管理器是一项系统服务，可协调跟踪提供者的注册。它确保跟踪有序进行，并将提供跟踪提供程序的组件与跟踪客户端隔离开。

The trace manager implements two FIDL protocols:  跟踪管理器实现两种FIDL协议：

 
- `Controller`: Provides trace clients with the ability to enumerate trace providers and collect trace data. -`Controller`：为跟踪客户端提供枚举跟踪提供者和收集跟踪数据的能力。
- `TraceRegistry`: Provides trace providers with the ability to register themselves at runtime so that they can be discovered by the tracing system. -`TraceRegistry`：使跟踪提供者能够在运行时注册自己，以便跟踪系统可以发现它们。

TODO: The `TraceRegistry` should be replaced by a `Namespace` based approach to publish trace providers from components. 待办事项：应该将“ TraceRegistry”替换为“基于命名空间”的方法，以从组件发布跟踪提供程序。

 
### Trace Providers  跟踪提供者 

Components which can be traced or offer tracing information to the system implement the `TraceProvider` FIDL protocol and register it with the`TraceRegistry`.  Once registered, they will receive messages whenevertracing is started or stopped and will have the opportunity to providetrace data encoded in the [Fuchsia Trace Format](trace-format/README.md). 可以跟踪的组件或向系统提供跟踪信息的组件将实现“ TraceProvider” FIDL协议，并向“ TraceRegistry”注册。一旦注册，他们将在跟踪开始或停止时接收消息，并有机会提供以[紫红色跟踪格式]（trace-format / README.md）编码的跟踪数据。

 
#### Kernel Trace Provider  内核跟踪提供程序 

The `ktrace_provider` program ingests kernel trace events and publishes trace records.  This allows kernel trace data to be captured and visualizedtogether with userspace trace data. ktrace_provider程序提取内核跟踪事件并发布跟踪记录。这允许内核跟踪数据与用户空间跟踪数据一起被捕获和可视化。

 
### Trace Client  跟踪客户端 

The `trace` program offers command-line access to tracing functionality for developers.  It also supports converting Fuchsia trace archives intoother formats, such as Catapult JSON records which can be visualizedusing Catapult (aka. Chrome Trace-Viewer, available at chrome://tracing). trace程序为开发人员提供了对跟踪功能的命令行访问。它还支持将紫红色的跟踪存档转换为其他格式，例如可以使用Catapult（又称为Chrome Trace-Viewer，可从chrome：// tracing获取）可视化的Catapult JSON记录。

Trace information can also be collected programmatically by using the `Controller` FIDL protocol directly. 跟踪信息也可以直接使用Controller FIDL协议以编程方式收集。

 
## Libraries  图书馆 

 
### libtrace: The C and C++ Trace Event Library  libtrace：C和C ++跟踪事件库 

Provides macros and inline functions for instrumenting C and C++ programs with trace points for capturing trace data during trace execution. 提供宏和内联函数，以使用跟踪点对C和C ++程序进行检测，以在跟踪执行期间捕获跟踪数据。

See `<trace/event.h>`.  参见`<trace / event.h>`。

 
#### C++ Example  C ++示例 

This example records trace events marking the beginning and end of the execution of the "DoSomething" function together with its parameters. 本示例记录了跟踪事件，这些事件标记了“ DoSomething”功能及其参数的执行开始和结束。

```c++
#include <trace/event.h>

void DoSomething(int a, std::string b) {
  TRACE_DURATION("example", "DoSomething", "a", a, "b", b);

  // Do something
}
```
 

 
#### C Example  C范例 

This example records trace events marking the beginning and end of the execution of the "DoSomething" function together with its parameters. 本示例记录了跟踪事件，这些事件标记了“ DoSomething”功能及其参数的执行开始和结束。

Unlike in C++, it is necessary to specify the type of each trace argument. In C++ such annotations are supported but are optional since the compilercan infer the type itself. 与C ++不同，有必要指定每个跟踪参数的类型。在C ++中，此类注释受支持，但是可选的，因为编译器可以推断类型本身。

```c
#include <trace/event.h>

void DoSomething(int a, const char* b) {
  TRACE_DURATION("example", "DoSomething", "a", TA_INT32(a), "b", TA_STRING(b));

  // Do something
}
```
 

 
#### Suppressing Tracing Within a Compilation Unit  抑制编译单元中的跟踪 

To completely suppress tracing within a compilation unit, define the NTRACE macro prior to including the trace headers.  This causes the macros tobehave as if tracing is always disabled so they will not produce tracerecords and they will have zero runtime overhead. 若要完全禁止在编译单元中进行跟踪，请在包含跟踪头之前定义NTRACE宏。这将导致宏的行为好像始终禁用跟踪，因此它们将不生成跟踪记录，并且运行时开销为零。

```c
#define NTRACE
#include <trace/event.h>

void DoSomething(void) {
  // This will never produce trace records because the NTRACE macro was
  // defined above.
  TRACE_DURATION("example", "DoSomething");
}
```
 

 
### libtrace-provider: Trace Provider Library  libtrace-provider：跟踪提供程序库 

This library provides C and C++ functions to register a process's trace engine with the Fuchsia tracing system.  For tracing to work in your process,you must initialize the trace provider at some point during its execution(or implement your own trace handler to register the trace engine someother way). 该库提供C和C ++函数，以在Fuchsia跟踪系统中注册进程的跟踪引擎。为了在过程中进行跟踪，必须在执行过程中的某个时刻初始化跟踪提供程序（或实现自己的跟踪处理程序以其他方式注册跟踪引擎）。

The trace provider requires an asynchronous dispatcher to operate.  跟踪提供程序需要异步调度程序才能运行。

 
#### C++ Example  C ++示例 

```c++
#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <trace-provider/provider.h>

int main(int argc, char** argv) {
  // Create a message loop.
   async::Loop loop(&kAsyncLoopConfigNoAttachToCurrentThread);

  // Start a thread for the loop to run on.
  // We could instead use async_loop_run() to run on the current thread.
  zx_status_t status = loop.StartThread();
  if (status != ZX_OK) exit(1);

  // Create the trace provider.
  trace::TraceProviderWithFdio trace_provider(loop.dispatcher());

  // Do something...

  // The loop and trace provider will shut down once the scope exits.
  return 0;
}
```
 

 
#### C Example  C范例 

```c
#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <trace-provider/provider.h>

int main(int argc, char** argv) {
  zx_status_t status;
  async_loop_t* loop;
  trace_provider_t* trace_provider;

  // Create a message loop.
  status = async_loop_create(&kAsyncLoopConfigNoAttachToCurrentThread, &loop);
  if (status != ZX_OK) exit(1);

  // Start a thread for the loop to run on.
  // We could instead use async_loop_run() to run on the current thread.
  status = async_loop_start_thread(loop, "loop", NULL);
  if (status != ZX_OK) exit(1);

  // Create the trace provider.
  async_dispatcher_t* dispatcher = async_loop_get_dispatcher(loop);
  trace_provider = trace_provider_create(dispatcher);
  if (!trace_provider) exit(1);

  // Do something...

  // Tear down.
  trace_provider_destroy(trace_provider);
  async_loop_shutdown(loop);
  return 0;
}
```
 

 
### libtrace-reader: Trace Reader Library  libtrace-reader：跟踪读取器库 

Provides C++ types and functions for reading trace archives.  提供用于读取跟踪存档的C ++类型和功能。

See `<trace-reader/reader.h>`.  参见`<trace-reader / reader.h>`。

 
## Transport Protocol  运输协议 

When the developer initiates tracing, the trace manager asks all relevant trace providers to start tracing and provides each one with a trace bufferVMO into which they should write their trace records. 当开发人员启动跟踪时，跟踪管理器会要求所有相关的跟踪提供者开始跟踪，并为每个跟踪提供者提供一个跟踪缓冲区VMO，他们应该在其中写入跟踪记录。

While a trace is running, the trace manager continues watching for newly registered trace providers and activates them if needed. 在运行跟踪时，跟踪管理器将继续监视新注册的跟踪提供程序，并在需要时激活它们。

What happens when a trace provider's trace buffer becomes full while a trace is running depends on the buffering mode.See [Buffering Modes](#Buffering-Modes) below. 跟踪运行时，跟踪提供程序的跟踪缓冲区已满时会发生什么，取决于缓冲模式。请参见下面的[缓冲模式]（缓冲模式）。

When tracing finishes, the trace manager asks all of the active trace providers to stop tracing then waits a short time for them to acknowledge that theyhave finished writing out their trace events. 跟踪完成后，跟踪管理器会要求所有活动的跟踪提供程序停止跟踪，然后等待一小段时间以使它们确认已完成写出跟踪事件。

The trace manager then reads and validates trace data written into the trace buffer VMOs by trace providers and creates a trace archive.  The trace managercan often recover partial data even when trace providers terminate abnormallyas long as they managed to store some data into their trace buffers.Note that in streaming mode the trace manager only needs to save thecurrently active rolling buffer.See [Buffering Modes](#Buffering-Modes) below. 然后，跟踪管理器读取并验证由跟踪提供者写入跟踪缓冲区VMO中的跟踪数据，并创建跟踪存档。只要跟踪提供程序设法将一些数据存储到其跟踪缓冲区中，即使跟踪提供程序异常终止，跟踪管理器仍可以恢复部分数据。请注意，在流模式下，跟踪管理器仅需要保存当前活动的滚动缓冲区。请参见[缓冲模式]（缓冲-模式）。

The trace manager delivers the resulting trace archive to its client through a socket.  This data is guaranteed to be well-formed according to theFuchsia trace format (but it may be nonsensical if trace providersdeliberately emit garbage data). 跟踪管理器通过套接字将结果跟踪归档传递给其客户端。根据紫红色的跟踪格式，可以保证此数据的格式正确（但是，如果跟踪提供者故意发出垃圾数据，则可能是毫无意义的）。

These are some important invariants of the transport protocol:  这些是传输协议的一些重要不变式：

 
- There are no synchronization points between the trace manager and trace providers other than starting or stopping collection. -除了开始或停止收集之外，跟踪管理器和跟踪提供程序之间没有同步点。
- Trace providers (components being traced) only ever write to trace buffers; they never read from them. -跟踪提供程序（被跟踪的组件）仅写入跟踪缓冲区；他们从不从他们那里读。
- The trace manager only ever reads from trace buffers; it never writes to them.  -跟踪管理器仅从跟踪缓冲区读取；它从不写信给他们。
- Trace clients never see the original trace buffers; they receive trace archives over a socket from the trace manager.  This protects trace providersfrom manipulation by trace clients. -跟踪客户端永远看不到原始跟踪缓冲区；他们通过套接字从跟踪管理器接收跟踪存档。这样可以防止跟踪提供程序受到跟踪客户端的操纵。

 
## Buffering Modes  缓冲模式 

There are three buffering modes: oneshot, circular, and streaming. They specify different behaviors when the trace buffer fills. 共有三种缓冲模式：单发，循环和流式。当跟踪缓冲区填充时，它们指定不同的行为。

Note that in all cases trace provider behavior is independent of each other. Other trace providers can continue to record trace events into their ownbuffers as usual until the trace stops, even as one provider's buffer fills.This may result in a partially incomplete trace. 请注意，在所有情况下，跟踪提供程序的行为都是相互独立的。其他跟踪提供程序可以像往常一样继续将跟踪事件记录到自己的缓冲区中，直到跟踪停止为止，即使一个提供程序的缓冲区已满，这也可能导致部分跟踪不完整。

 
### Oneshot  单发 

If the buffer becomes full then that trace provider will stop recording events.  如果缓冲区已满，则该跟踪提供程序将停止记录事件。

 
### Circular  圆 

The trace buffer is effectively divided into three pieces: the "durable" buffer and two "rolling" buffers. The durable buffer is for records important enoughthat we don't want to risk dropping them. These include records for thread andstring references. 跟踪缓冲区实际上分为三部分：“耐用”缓冲区和两个“滚动”缓冲区。持久缓冲区用于保存足够重要的记录，我们不希望冒险删除它们。这些包括线程和字符串引用的记录。

Tracing begins by writing to the first rolling buffer. Once one rolling buffer fills tracing continues by writing to the other one. 通过写入第一个滚动缓冲区开始跟踪。一旦一个滚动缓冲区填充满，就通过写入另一滚动缓冲区继续跟踪。

If the durable buffer fills then tracing for the provider stops. Tracing in other providers continues as usual. 如果持久缓冲区已满，则将停止对提供程序的跟踪。照常继续在其他提供程序中进行跟踪。

 
### Streaming  流媒体 

The trace buffer is effectively divided into three pieces: the "durable" buffer and two "rolling" buffers. The durable buffer is for records important enoughthat we don't want to risk dropping them. These include records for thread andstring references. 跟踪缓冲区实际上分为三部分：“耐用”缓冲区和两个“滚动”缓冲区。持久缓冲区用于保存足够重要的记录，我们不希望冒险删除它们。这些包括线程和字符串引用的记录。

Tracing begins by writing to the first rolling buffer. Once one rolling buffer fills tracing continues by writing to the other one, if it is available, andnotifying the trace manager that the buffer is full. If the other rollingbuffer is not available, then records are dropped until it becomes available.The other rolling buffer is unavailable between the point when it filled andwhen the manager reports back that the buffer's contents have been saved. 通过写入第一个滚动缓冲区开始跟踪。一旦一个滚动缓冲区已满，就继续写入另一滚动缓冲区（如果有），并继续向跟踪管理器通知缓冲区已满，从而继续进行跟踪。如果另一个滚动缓冲区不可用，则记录将被删除，直到它可用为止。另一个滚动缓冲区在其填充的时间点与管理器报告该缓冲区的内容已保存之间不可用。

Whether records get dropped depends on the rate at which records are created vs the rate at which the trace manager can save the buffers. This can resultin a partially incomplete trace, but is less important than perturbing programperformance by waiting for a buffer to be saved. 记录是否被删除取决于记录的创建速率以及跟踪管理器可以保存缓冲区的速率。这可能会导致部分不完整的跟踪，但是比通过等待缓冲区保存来影响程序性能的重要性要小。

If the durable buffer fills then tracing for the provider stops. Tracing in other providers continues as usual. 如果持久缓冲区已满，则将停止对提供程序的跟踪。照常继续在其他提供程序中进行跟踪。

 
## Trace Manager/Provider FIFO Protocol  跟踪管理器/提供程序FIFO协议 

Notification of trace provider startup and shutdown is done via a FIFO, the handle of which is passed from the trace manager to each trace provideras part of the initial "start tracing" request. The form of each message isdefined in `<trace-provider/provider.h>`. Packets are fixed size with thefollowing format: 跟踪提供者启动和关闭的通知是通过FIFO完成的，FIFO的句柄从跟踪管理器传递到初始“启动跟踪”请求的每个跟踪提供者部分。每个消息的形式在`<trace-provider / provider.h>`中定义。报文固定大小，格式如下：

```cpp
typedef struct trace_provider_packet {
    // One of TRACE_PROVIDER_*.
    uint16_t request;

    // For alignment and future concerns, must be zero.
    uint16_t reserved;

    // Optional data for the request.
    // The contents depend on the request.
    // If unused they must be passed as zero.
    uint32_t data32;
    uint64_t data64;
} trace_provider_packet_t;
```
 

 
### FIFO Packets  FIFO数据包 

The following packets are defined:  定义了以下数据包：

**TRACE_PROVIDER_STARTED**  ** TRACE_PROVIDER_STARTED **

Sent from trace providers to the trace manager. Notify the trace manager that the provider has received the "start tracing"request and is starting to collect trace data.The `data32` field of the packet contains the version number of the FIFOprotocol that the provider is using. The value is specified by**TRACE_PROVIDER_FIFO_PROTOCOL_VERSION** in `<trace-provider/provider.h>`.If the trace manager sees a protocol it doesn't understand it will closeits side of the FIFO and ignore all trace data from the provider. 从跟踪提供者发送到跟踪管理器。通知跟踪管理器提供者已收到“开始跟踪”请求并开始收集跟踪数据。数据包的“ data32”字段包含提供者正在使用的FIFO协议的版本号。该值由<trace-provider / provider.h>中的TRACE_PROVIDER_FIFO_PROTOCOL_VERSION **指定。 。

**TRACE_PROVIDER_SAVE_BUFFER**  ** TRACE_PROVIDER_SAVE_BUFFER **

Sent from trace providers to the trace manager in streaming mode. Notify the trace manager that a buffer is full and needs saving.This request is only used in streaming mode.The `data32` field contains the "wrap count" which is the number of timeswriting has switched from one buffer to the next. The buffer that needs savingis `(data32 & 1)`.The `data64` field contains the offset of the end of data written to the"durable" buffer. 从跟踪提供者以流模式发送到跟踪管理器。通知跟踪管理器缓冲区已满，需要保存。此请求仅在流模式下使用。data32字段包含“换行计数”，即写入从一个缓冲区切换到另一个缓冲区的次数。需要保存的缓冲区是（data32 1）。data64字段包含写入“持久”缓冲区的数据结尾的偏移量。

Only one buffer save request may be sent at a time. The next one cannot be sent until **TRACE_PROVIDER_BUFFER_SAVED** is received acknowledging theprevious request. 一次只能发送一个缓冲区保存请求。在接收到** TRACE_PROVIDER_BUFFER_SAVED **确认先前的请求之前，不能发送下一个。

**TRACE_PROVIDER_BUFFER_SAVED**  ** TRACE_PROVIDER_BUFFER_SAVED **

