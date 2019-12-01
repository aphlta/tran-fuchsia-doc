 
# Kernel Tracing  内核跟踪 

The kernel traces various actions by writing records to an internal buffer, which can later be retrieved and printed. 内核通过将记录写入内部缓冲区来跟踪各种动作，以后可以将其检索和打印。

 
## Kernel trace format  内核跟踪格式 

The kernel trace format is pretty simple. See files `ktrace.h` and `ktrace-def.h` in`system/ulib/zircon-internal/include/lib/zircon-internal`for a description. 内核跟踪格式非常简单。有关说明，请参见system / ulib / zircon-internal / include / lib / zircon-internal中的文件ktrace.h和ktrace-def.h。

 
## Controlling what to trace  控制要追踪的内容 

Control of what to trace is provided by a kernel command-line parameter `ktrace.grpmask`. The value is specified as 0xNNN and is a bitmaskof tracing groups to enable. See the *KTRACE\_GRP\_\** values in`system/ulib/zircon-internal/include/lib/zircon-internal/ktrace.h`.The default is 0xfff which traces everything. 内核命令行参数“ ktrace.grpmask”提供了对跟踪内容的控制。该值指定为0xNNN，并且是要启用的跟踪组的位掩码。请参阅system / ulib / zircon-internal / include / lib / zircon-internal / ktrace.h中的* KTRACE \ _GRP \ _ \ **值。默认值为0xfff，它跟踪所有内容。

What to trace can also be controlled by the `ktrace` command-line utility, described below. 跟踪的内容也可以通过ktrace命令行实用程序进行控制，如下所述。

 
## Trace buffer size  跟踪缓冲区大小 

The size of the trace buffer is fixed at boot time and is controlled by the `ktrace.bufsize` kernel command-line parameter. Its value is thebuffer size in megabytes. The default is 32MB. 跟踪缓冲区的大小在引导时是固定的，并由ktrace.bufsize内核命令行参数控制。它的值是缓冲区大小（以兆字节为单位）。默认值为32MB。

 
## ktrace command-line utility  ktrace命令行实用程序 

Kernel tracing may be controlled with the `ktrace` command-line utility.  内核跟踪可以通过ktrace命令行实用程序来控制。

```
$ ktrace --help
Usage: ktrace [options] <control>
Where <control> is one of:
  start <group_mask>  - start tracing
  stop                - stop tracing
  rewind              - rewind trace buffer
  written             - print bytes written to trace buffer
    Note: This value doesn't reset on "rewind". Instead, the rewind
    takes effect on the next "start".
  save <path>         - save contents of trace buffer to <path>

Options:
  --help  - Duh.
```
 

 
## Pretty-printing a kernel trace  漂亮地打印内核跟踪 

The host tool `ktrace-dump` can be used to pretty-print a kernel trace.  宿主工具“ ktrace-dump”可用于漂亮地打印内核跟踪。

Example:  例：

First collect the trace on the target:  首先收集目标上的跟踪：

```
$ ktrace start 0xfff
... do something ...
$ ktrace stop
$ ktrace save /tmp/save.ktrace
```
 

Then copy the file to the development host, and dump it:  然后将文件复制到开发主机，并转储它：

```
host$ ./out/build-zircon/tools/netcp :/tmp/save.ktrace save.ktrace
host$ ./out/build-zircon/tools/ktrace-dump save.ktrace > save.dump
```
 

The pretty-printed output can be quite voluminous, thus it's recommended to send it to a file and then view it in your editor or whatever. 打印精美的输出可能非常庞大，因此建议将其发送到文件中，然后在编辑器或其他任何方式中查看。

 
## Use with Fuchsia Tracing  与紫红色追踪配合使用 

