 
# CPU Performance Monitor  CPU性能监控器 

 
## Introduction  介绍 

The CPU Performance Monitor Trace Provider gives the user access to the performance counters built into the CPU using the[tracing system provided by Fuchsia](usage-guide.md). CPU性能监视器跟踪提供程序使用户可以使用Fuchsia提供的跟踪系统（usage-guide.md）访问内置于CPU的性能计数器。

At present this is only supported for Intel chipsets.  目前仅英特尔芯片组支持。

On Intel the Performance Monitor provides the user with statistics regarding many aspects the CPU.For a complete list of the performance events available for, e.g.,Skylake chips see Intel Volume 3 Chapter 19.2,Performance Monitoring Events For 6th And 7th Generation Processors.Not all events (or "counters") are currently available, there's a lot(!),but hopefully a number of useful events are currently present. 在Intel上，性能监视器向用户提供有关CPU各个方面的统计信息。有关可用于例如Skylake芯片的性能事件的完整列表，请参阅英特尔第3卷第19.2节“第六代和第七代处理器的性能监视事件”。事件（或“计数器”）当前可用，有很多（！），但希望当前存在许多有用的事件。

Here are a few examples:  这里有一些例子：

 
- cache hits/misses, for each of L1, L2, L3  -缓存命中/未命中，分别针对L1，L2，L3
- cycles stalled due to cache misses  -由于缓存未命中而使周期停止
- branch mispredicts  -分支预测错误
- instructions retired  -退休指令

The tracing system uses "categories" to let one specify what trace data to collect. Cpuperf uses these categories to simplify the specificationof what h/w events to enable. The full set of categories can be foundin the `.inc` files in this directory. A representative set of categoriesis described below. 跟踪系统使用“类别”来指定要收集的跟踪数据。 Cpuperf使用这些类别来简化要启用的硬件事件的规范。完整的类别集可以在此目录中的.inc文件中找到。一组代表性的类别如下所述。

To collect trace data, run `trace record` on your Fuchsia system, or indirectly via the `traceutil` host tool. The latter is recommendedas it automates the download of the collected "trace.json" file to yourdesktop. 要收集跟踪数据，请在您的紫红色系统上运行“跟踪记录”，或通过“ traceutil”宿主工具间接运行。建议使用后者，因为它可以自动将收集到的“ trace.json”文件下载到您的桌面。

Example:  例：

```shell
host$ categories="gfx"
host$ categories="$categories,cpu:fixed:unhalted_reference_cycles"
host$ categories="$categories,cpu:fixed:instructions_retired"
host$ categories="$categories,cpu:l2_lines,cpu:sample:10000"
host$ fx traceutil record --buffer-size=64 --duration=2s \
  --categories=$categories
Starting trace; will stop in 2 seconds...
Stopping trace...
Trace file written to /data/trace.json
Downloading trace... done
Converting trace-2017-11-12T17:55:45.json to trace-2017-11-12T17:55:45.html... done.
```
 

After you have the `.json` file on your desktop you can load it into `chrome://tracing`. If you are using `traceutil` an easier way to viewthe trace is by loading the corresponding `.html` file that `traceutil`generates. The author finds it easiest to run `traceutil` from the top levelFuchsia directory, view that directory in Chrome (e.g.,`file:///home/dje/fnl/ipt/fuchsia`), hit Refresh after each new traceand then view the trace file in a separate tab. 在桌面上拥有.json文件之后，您可以将其加载到chrome：// tracing中。如果您使用的是traceutil，查看跟踪的一种更简便的方法是加载由traceutil生成的相应的.html文件。作者发现最容易从顶层紫红色目录运行`traceutil`，在Chrome中查看该目录（例如，file：/// home / dje / fnl / ipt / fuchsia`），在每次新建跟踪后点击刷新，然后查看跟踪文件在单独的选项卡中。

 
## Basic Operation  基本操作 

The basic operation of performance data collection is to allocate a buffer for trace records for each CPU, and then set a counter (on each CPU)to trigger an interrupt after a pre-specified number of events occurs.This interrupt is called the PMI interrupt (Performance Monitor Interrupt).On Intel the interrupt triggers when the counter overflows, at which pointthe interrupt service routine will write various information (for exampletimestamp and program counter) to the trace buffer, reset the counterto re-trigger another interrupt after the pre-specified number of events,and return. 性能数据收集的基本操作是为每个CPU的跟踪记录分配一个缓冲区，然后设置计数器（在每个CPU上）以在发生预定数量的事件后触发中断。此中断称为PMI中断（性能监视器中断）。在Intel上，当计数器溢出时会触发中断，这时中断服务程序会将各种信息（例如时间戳和程序计数器）写入跟踪缓冲区，重置计数器以在预执行后重新触发另一个中断指定数量的事件，然后返回。

When tracing stops the buffer is read by the Cpuperf Trace Provider and converted to the trace format used by the Trace Manager. 跟踪停止时，缓冲区将由Cpuperf跟踪提供程序读取，并转换为跟踪管理器使用的跟踪格式。

Tracing also stops when the buffer fills. Note that an internal buffer is used, and thus circular and streaming modes are not (currently) supported.How much trace data can be collected depends on several factors: 当缓冲区填满时，跟踪也会停止。请注意，由于使用了内部缓冲区，因此（当前）不支持循环和流模式。可以收集多少跟踪数据取决于以下几个因素：

 
- duration of the trace  -跟踪的持续时间
- size of the buffer  -缓冲区的大小
- frequency of sampling  -采样频率
- how frequently the counter overflows  -计数器溢出的频率
- whether program counter information is written to the buffer  -是否将程序计数器信息写入缓冲区

 
## Data Collection Categories  数据收集类别 

As stated earlier, the Fuchsia tracing system uses "categories" to let one specify what data to collect. For CPU tracing, there are categoriesto specify what counters to enable, whether to trace the os, userspace,or both, as well as specify the sampling frequency. 如前所述，紫红色的跟踪系统使用“类别”来指定要收集的数据。对于CPU跟踪，有一些类别可以指定要启用哪些计数器，是否要跟踪os，用户空间或同时跟踪这两者以及指定采样频率。

For each performance counter see the Intel documentation for further information. This document does not attempt to provide detailed informationon each counter. 有关每个性能计数器，请参阅英特尔文档以获取更多信息。本文档未尝试在每个计数器上提供详细信息。

 
### Sample Rate  采样率 

Data for each counter is collected at a rate specified by the user. Eventually specifying a random rate will be possible. In the meantimethe following set of rates are supported: 每个计数器的数据以用户指定的速率收集。最终可以指定一个随机速率。同时，支持以下一组费率：

 
- cpu:sample:100  -cpu：sample：100
- cpu:sample:500  -cpu：sample：500
- cpu:sample:1000  -cpu：sample：1000
- cpu:sample:5000  -cpu：sample：5000
- cpu:sample:10000  -cpu：sample：10000
- cpu:sample:50000  -cpu：sample：50000
- cpu:sample:100000  -cpu：sample：100000
- cpu:sample:500000  -cpu：sample：500000
- cpu:sample:1000000  -cpu：sample：1000000

 
#### Independent sampling  独立抽样 

By default each counter is sampled independently. For example, if one requests "cpu:fixed:instructions_retired"and "arch:llc" (Last Level Cache - L3) with a sampling rate of 10000,then retired instructions will be sampled every 10000 "instruction retired"events and LLC operations will be sampled every 10000 "LLC" events,with the former happening far more frequently than the latter.Timestamps are collected with each sample so one can know how long it tookto, for example, retire 10000 instructions. 默认情况下，每个计数器都是独立采样的。例如，如果一个请求以10000的采样率请求“ cpu：fixed：instructions_retired”和“ arch：llc”（最后一级缓存-L3），则每10000个“ instruction retired”事件将对已退休的指令进行采样，LLC操作将每10000个“ LLC”事件采样一次，前者的发生频率要远高于后者。时间戳与每个采样一起收集，因此人们可以知道花费了多长时间，例如，退出10000条指令。

 
#### Timebased sampling  基于时间的采样 

A few counters are available to be used as "timebases". In timebase mode one counter is used to drive data collection of all counters,as opposed to each counter being collected at their own rate.This can provide a more consistent view of what's happening. On the other hand,doing so means we forego collecting statistical pc data for each event(since the only pc values we will have are those for the timebase event).A sample rate must be provided in addition to the timebase counter. 一些计数器可用作“时基”。在时基模式下，一个计数器用于驱动所有计数器的数据收集，而不是每个计数器都以自己的速率收集数据。这样可以更清楚地了解正在发生的事情。另一方面，这样做意味着我们放弃为每个事件收集统计pc数据（因为唯一的pc值是时基事件的pc值）。除了时基计数器外，还必须提供采样率。

See below for the set of timebase counters as of this writing, and `garnet/bin/cpuperf_provider/intel-timebase-categories.inc`in the source tree for the current set. 截至本文撰写之时，请参阅下面的时基计数器集，以及当前集的源树中的“ garnet / bin / cpuperf_provider / intel-timebase-categories.inc”。

 
### Tally Mode  提示模式 

Tally mode is a simpler alternative to sampling mode where counts of each event are collected over the entire trace run and then reported. 提示模式是采样模式的一种更简单的替代方法，在采样模式下，在整个跟踪运行中收集每个事件的计数，然后进行报告。

Tally mode is enabled via a category of "cpu:tally" instead of one of the "cpu:sample:* categories. 通过“ cpu：tally”类别而不是“ cpu：sample：*”类别之一可以启用Tally模式。

Example:  例：

```shell
host$ categories="cpu:l2_summary"
host$ categories="$categories,cpu:fixed:unhalted_reference_cycles"
host$ categories="$categories,cpu:fixed:instructions_retired"
host$ categories="$categories,cpu:mem:bytes,cpu:mem:requests"
host$ categories="$categories,cpu:tally"
host$ fx traceutil record --buffer-size=64 --duration=2s \
  --categories=$categories --report-type=tally --stdout
```
 

 
### Options  选件 

 
- cpu:os - collect data for code running in kernelspace.  -cpu：os-收集在内核空间中运行的代码的数据。

 
- cpu:user - collect data for code running in userspace.  -cpu：user-收集在用户空间中运行的代码的数据。

 
- cpu:profile_pc - collect pc data associated with each event  -cpu：profile_pc-收集与每个事件关联的pc数据

This is useful when wanting to know where, for example, cache misses are generally occurring (statistically speaking, depending upon thesample rate). The address space and program counter of each sampleis included in the trace output. Doing so doubles the size of eachtrace record though, so there are tradeoffs. 当想知道一般在哪里发生高速缓存未命中时（从统计上来说，取决于采样率），这很有用。跟踪输出中包含每个样本的地址空间和程序计数器。这样做会使每个跟踪记录的大小增加一倍，因此需要进行权衡。

 
### Fixed Counters  固定柜台 

The Intel Architecture provides three "fixed" counters:  英特尔架构提供三个“固定”计数器：

 
- cpu:fixed:instructions_retired  -cpu：fixed：instructions_retired

 
- cpu:fixed:unhalted_core_cycles  -cpu：fixed：unhalted_core_cycles

 
- cpu:fixed:unhalted_reference_cycles  -cpu：fixed：unhalted_reference_cycles

These counters are "fixed" in the sense that they don't use the programmable counters. There are three of them and each of them has a fixed use.The advantage of them is that they don't use up a programmable counter:There are dozens of counters but, depending on the model, typically onlyat most four are usable at a time. 这些计数器在不使用可编程计数器的意义上是“固定的”。它们共有三个，每个都有固定用途。它们的优点是它们不会用完可编程计数器：有几十个计数器，但根据型号的不同，通常最多只能使用四个时间。

 
### Programmable Counters  可编程计数器 

There are dozens of programmable counters on Skylake (and Kaby Lake) chips. For a complete list see Intel Volume 3 Chapter 19.2,Performance Monitoring Events For 6th And 7th Generation Processors.For a list of the ones that are currently supported see`zircon/system/ulib/zircon-internal/include/lib/zircon-internal/device/cpu-trace/intel-pm-events.inc`and`zircon/system/ulib/zircon-internal/include/lib/zircon-internal/device/cpu-trace/skylake-pm-events.inc`in the source tree. Skylake（和Kaby Lake）芯片上有数十个可编程计数器。有关完整列表，请参阅“英特尔第3卷第19.2节，第六代和第七代处理器的性能监视事件”。有关当前受支持的列表，请参见`zircon / system / ulib / zircon-internal / include / lib / zircon-internal /device/cpu-trace/intel-pm-events.inc和zircon / system / ulib / zircon-internal / include / lib / zircon-internal / device / cpu-trace / skylake-pm-events.inc源树。

To simplify specifying the programmable counters they have been grouped into categories defined in`garnet/bin/cpuperf_provider/intel-pm-categories.inc`and`garnet/bin/cpuperf_provider/skylake-pm-categories.inc`in the source tree. See these files for a full list. 为了简化对可编程计数器的指定，它们已在源树中分为garnet / bin / cpuperf_provider / intel-pm-categories.inc和garnet / bin / cpuperf_provider / skylake-pm-categories.inc中定义的类别。请参阅这些文件以获取完整列表。

Only one of these categories may be specified at a time. [Later we'll provide more control over what data to collect.] 一次只能指定其中一个类别。 [稍后，我们将对收集哪些数据提供更多控制。]

A small selection of useful categories:  一小部分有用的类别：

 
- cpu:arch:llc  -cpu：arch：llc
  - Last Level Cache (L3) references  -最后一级缓存（L3）参考
  - Last Level Cache (L3) misses  -末级缓存（L3）未命中

 
- cpu:arch:branch  -cpu：arch：branch
  - Branch instructions retired  -分支机构的指示已退役
  - Branch instructions mispredicted  -分支指令错误

 
- cpu:skl:l1_summary  -cpu：skl：l1_summary
  - Number of outstanding L1D misses every cycle  -每个周期未完成的L1D错过次数
  - Number of outstanding L1D misses for any logical thread on this processor core  -此处理器内核上任何逻辑线程的未完成L1D丢失次数
  - Number of lines brought into L1 data cache  -进入L1数据缓存的行数

 
- cpu:skl:l2_summary  -cpu：skl：l2_summary
  - Demand requests that missed L2  -缺少L2的需求请求
  - All requests that missed L2  -所有错过L2的请求
  - All Demand Data Read requests to L2  -所有对L2的需求数据读取请求
  - All requests to L2  -所有对L2的请求

 
- cpu:skl:l3_summary  -cpu：skl：l3_summary
  - Requests originating from core that reference cache line in L3  -来自核心的请求引用了L3中的缓存行
  - Cache miss condition for references to L3  -缓存未命中情况，用于引用L3

 
- cpu:skl:offcore_demand_code  -cpu：skl：offcore_demand_code
  - Incremented each cycle of the number of offcore outstanding Demand Code Read transactions in SQ to uncore  -在SQ中将未完成的脱机未完成需求代码读取事务的数量的每个周期增加，以取消核
  - Cycles with at least 1 offcore outstanding Demand Code Read transactions in SQ to uncore  -以SQ中至少有1个离岸未完成的按需代码读取事务进行循环以取消核

 
- cpu:skl:offcore_demand_data  -cpu：skl：offcore_demand_data
  - Incremented each cycle of the number of offcore outstanding Demand Data Read transactions in SQ to uncore  -将SQ中的脱机未完成需求数据读取事务数的每个周期增加以取消核
  - Cycles with at least 1 offcore outstanding Demand Data Read transactions in SQ to uncore  -用SQ中至少有1个离岸未完成的需求数据读取事务进行循环以解除核
  - Cycles with at least 6 offcore outstanding Demand Data Read transactions in SQ to uncore  -至少用SQ中的6个脱机未完成需求数据读取事务进行循环以取消核

 
- cpu:skl:l1_miss_cycles  -cpu：skl：l1_miss_cycles
  - Cycles while L1 data miss demand load is outstanding  -当L1数据未满足需求负载时循环运行
  - Execution stalls while L1 data miss demand load is outstanding  -当L1数据未满足需求负载时，执行停止

 
- cpu:skl:l2_miss_cycles  -cpu：skl：l2_miss_cycles
  - Cycles while L2 miss demand load is outstanding  -L2未满足需求负载时循环运行
  - Execution stalls while L2 miss demand load is outstanding  -执行失速而L2的未命中需求负载突出

 
- cpu:skl:l3_miss_cycles  -cpu：skl：l3_miss_cycles
  - Cycles while L3 miss demand load is outstanding  -L3未满足需求负荷时循环运行
  - Execution stalls while L3 miss demand load is outstanding  -执行失速而L3的未命中需求负载突出

 
- cpu:skl:mem_cycles  -cpu：skl：mem_cycles
  - Cycles while memory subsystem has an outstanding load  -在内存子系统负载突出时循环
  - Execution stalls while memory subsystem has an outstanding load  -当内存子系统的负载很大时，执行将停止

Note: The wording of some of these events may seem odd. The author has tried to preserve the wording foundin the Intel manuals, though improvements are welcome. 注意：其中某些事件的措词可能看起来很奇怪。作者尝试保留Intel手册中的措词，但欢迎进行改进。

Note: This is just a first pass! They'll be reworked as the need arises. Please see the category `.inc` filesin your source tree for an up to date list. 注意：这只是第一步！如有需要，将对其进行重新加工。请查看源代码树中的目录.inc文件以获取最新列表。

 
### Timebase Counters  时基计数器 

These counters may be used as timebases. More will be added in time. 这些计数器可以用作时基。更多信息将及时添加。

 
- cpu:timebase:fixed:instructions_retired  -cpu：timebase：fixed：instructions_retired
  - same counter as cpu:fixed:instructions_retired  -与cpu：fixed：instructions_retired相同的计数器

 
- cpu:timebase:fixed:unhalted_reference_cycles  -cpu：timebase：fixed：unhalted_reference_cycles
