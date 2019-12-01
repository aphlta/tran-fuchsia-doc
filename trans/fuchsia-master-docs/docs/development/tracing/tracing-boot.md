 
# Tracing Booting Fuchsia  追踪引导紫红色 

The Zircon kernel's internal tracing system can be active on boot (and in fact is currently the default). This means that one can traceat least the kernel side of booting without extra effort. The datais already there, one just needs to collect it. Zircon内核的内部跟踪系统可以在引导时处于活动状态（实际上是当前的默认设置）。这意味着至少可以毫不费力地跟踪启动的内核方面。数据已经存在，只需收集即可。

 
## Including kernel boot trace data in trace results  在跟踪结果中包括内核引导跟踪数据 

As long as the kernel's internal trace buffer is not rewound the data is available to be included in the trace. This is achieved by passingcategory "kernel:retain" to the `trace` or `traceutil` program.Note that the moment a trace is made without passing `kernel:retain`then the ktrace buffer is rewound and the data is lost. 只要不回绕内核的内部跟踪缓冲区，就可以将数据包含在跟踪中。这是通过将类别“ kernel：retain”传递给`trace`或`traceutil`程序来实现的。请注意，在进行跟踪时没有传递`kernel：retain`的那一刻，则ktrace缓冲区被倒回并且数据丢失。

Example:  例：

```shell
# ... Fuchsia boots ...
host$ fx traceutil record --categories=kernel,kernel:retain \
    --buffer-size=64 --duration=1s --stream
```
 

There are a few important things to note here.  这里有一些重要的事情要注意。

The first thing to note is the categories passed: `kernel` and `kernel:retain`. The `kernel` category tells the kernel to trace everything.In this example the kernel has already been tracing everything: that isthe default on boot. It is specified here as a simple way totell `ktrace_provider`, which is the interface between the Fuchsia tracingsystem and the kernel, that kernel data is being collected.The `kernel:retain` category tells `ktrace_provider` not to rewind thekernel trace buffer at the start of tracing. 首先要注意的是传递的类别：“内核”和“内核：保留”。 ``kernel''类别告诉内核跟踪所有内容。在此示例中，内核已经跟踪了所有内容：这是引导时的默认设置。这里指定了一种简单的方式来告诉kuch_provider，这是紫红色的跟踪系统和内核之间的接口，它正在收集内核数据。kernel：retain类别告诉ktrace_provider不要在以下位置回退内核跟踪缓冲区。跟踪的开始。

The second is the buffer size. The kernel's default trace buffer size is 32MB whereas the Fuchsia trace default buffer size is 4MB.Using a larger Fuchsia trace buffer size means there is enough spaceto hold the contents of the kernel's trace buffer.There are some implementation quirks at play here.The kernel currently has its own trace format called "ktrace". Whentracing stops the `ktrace_provider` program reads the kernel trace bufferand converts it to Fuchsia's trace format. Depending on circumstancesthe ktrace buffer format is a little more compact. That is why theabove example provides a 64MB buffer even though the kernel's buffersize was 32MB. 第二个是缓冲区大小。内核的默认跟踪缓冲区大小为32MB，而Fuchsia跟踪默认缓冲区大小为4MB。使用更大的Fuchsia跟踪缓冲区大小意味着有足够的空间来容纳内核跟踪缓冲区的内容。当前具有自己的跟踪格式，称为“ ktrace”。当跟踪停止时，`ktrace_provider`程序读取内核跟踪缓冲区，并将其转换为紫红色的跟踪格式。根据情况，ktrace缓冲区格式会更紧凑。因此，即使内核的缓冲区大小为32MB，上述示例也提供了64MB的缓冲区。

The third important thing to note is that in this example we just want to grab the current contents of the trace buffer, and aren't interestedin tracing anything more. That is why a duration of one second is used.Ideally we would pass `--duration=0s` but `traceutil` currently interpretsthat as requesting the default which is ten seconds. 要注意的第三点重要是，在此示例中，我们只想获取跟踪缓冲区的当前内容，而对跟踪任何内容都不感兴趣。这就是为什么要使用一秒钟的持续时间的原因。理想情况下，我们会传递`--duration = 0s`，但是`traceutil`当前将其解释为请求默认的十秒。

The `--stream` arg just says to send the results directly to the development host instead of first writing them to disk on the target. --stream参数仅表示将结果直接发送到开发主机，而不是先将它们写到目标磁盘上。

 
# Changing kernel trace parameters at boot  引导时更改内核跟踪参数 

The size of the kernel's trace buffer can be changed at boot time with the `ktrace.bufsize=N` command line option, where `N` is the sizeof the buffer in megabytes. 内核跟踪缓冲区的大小可以在引导时使用dtrace.bufsize = IN命令行选项进行更改，其中“ N”是缓冲区的大小（以兆字节为单位）。

The choice of data to collect is controlled with the `ktrace.grpmask=0xNNN' command line option. The 0xNNN value is a bit mask of *KTRACE\_GRP\_\**values from//zircon/system/ulib/zircon-internal/include/lib/zircon-internal/ktrace.h.The default is 0xfff which enables all trace categories (or groups inktrace parlance). 收集数据的选择是通过ktrace.grpmask = 0xNNN命令行选项控制的。 0xNNN值是来自//zircon/system/ulib/zircon-internal/include/lib/zircon-internal/ktrace.h的* KTRACE \ _GRP \ _ \ **值的位掩码。默认值为0xfff，它将启用所有跟踪类别（或将inktrace术语分组）。

For more information on Zircon command line options see [kernel\_cmdline][kernel_cmdline]. 有关Zircon命令行选项的更多信息，请参见[kernel \ _cmdline] [kernel_cmdline]。

 

