 
# Adding tracing to device drivers  向设备驱动程序添加跟踪 

This document describes how to add tracing to device drivers.  本文档介绍了如何向设备驱动程序添加跟踪。

 
## Overview  总览 

Please read [Fuchsia Tracing System Design](/docs/development/tracing/design.md) for an overview of tracing. 请阅读[紫红色跟踪系统设计]（/ docs / development / tracing / design.md），以获取跟踪概述。

 
## Trace Provider  跟踪提供者 

Drivers don't have to specify a Trace Provider, the devhost process via `libdriver.so` provides it. It is mentioned here in case the topiccomes up. 驱动程序不必指定跟踪提供程序，通过`libdriver.so`的devhost进程可以提供它。如果主题出现，这里会提到它。

 
## Adding trace records  添加跟踪记录 

 
### Source additions  来源增加 

Trace records are easiest to add by invoking the `TRACE_*()` macros from `ddk/trace/event.h`. 通过从ddk / trace / event.h中调用`TRACE _ *（）`宏，最容易添加跟踪记录。

There are various kinds of trace records that can be emitted. Please see `trace/internal/event_common.h` for a descriptionof the various macros. 可以发出各种跟踪记录。请参阅`trace / internal / event_common.h`了解各种宏。

Looking up macro documentation from internal implementation files is a temporary situation. Ultimately such documentation will livein a more appropriate place. 从内部实现文件中查找宏文档是一种临时情况。最终，此类文档将放在一个更合适的位置。

Example:  例：

```c++
#include <ddk/trace/event.h>

void DoSomething(int a, std::string b) {
  TRACE_DURATION("example:example1", "DoSomething", "a", a, "b", b);

  // Do something
}
```
 

The first two arguments to most macros are the "category" and the event name. Here they are "example:example1" and "DoSomething" respectively. 大多数宏的前两个参数是“类别”和事件名称。它们分别是“ example：example1”和“ DoSomething”。

Trace categories are how the tracing system lets the user specify what data to collect. If a category is not requested by the userthen the data is not collected. 跟踪类别是跟踪系统允许用户指定要收集哪些数据的方式。如果用户未请求类别，则不会收集数据。

Categories don't need to be unique across the driver. One typically groups several events under the same category.By convention categories have the format"<provider-name>:<category-name>[:<subcategory1-name>...]"."<provider-name>" for drivers should generally by the driver name.This is done to avoid collisions in category names across theentire system. A potential augmentation to this convention is to prefixall driver categories with "driver:". E.g., "driver:ethernet:packets".Avoiding naming collisions with other trace providers is important,otherwise the user may ask for a particular category and get completelyunrelated data from a different trace provider. 类别不必在驱动程序中唯一。通常，一个事件将多个事件归为同一类别。按约定类别，驱动程序的格式为“ <提供者名称>：<类别名称> [：<子类别1-名称> ...]”。驱动程序的“ <提供者名称>”通常应使用驱动程序名称。这样做是为了避免整个系统的类别名称冲突。对该约定的潜在增强是在所有驱动程序类别之前添加“ driver：”。例如，“ driver：ethernet：packets”。避免与其他跟踪提供程序的命名冲突很重要，否则用户可能会要求特定的类别并从其他跟踪提供程序获取完全不相关的数据。

The event name is included in the trace to describe what the event is about. It is typically unique for each event. 事件名称包含在跟踪中，以描述事件的含义。对于每个事件，它通常都是唯一的。

 
### BUILD.gn additions  BUILD.gn添加 

The following addition to your driver's `BUILD.gn` target is needed to pick up tracing support: 需要对驱动程序的`BUILD.gn`目标进行以下补充才能获得跟踪支持：

```gn
driver("my_driver") {
  deps = [
    ...
    "$zx/system/ulib/trace:headers"
    "$zx/system/ulib/trace:trace-driver",
  ]
}
```
 

 
## Building with tracing  跟踪构建 

The following needs to be passed to fx set in order to trace drivers that are loaded during boot: `--with-base=//garnet/packages/prod:tracing`. 为了跟踪引导过程中加载的驱动程序，需要将以下内容传递给fx set：--with-base = // garnet / packages / prod：tracing。

```sh
$ fx set ${PRODUCT}.${BOARD} --with-base=//garnet/packages/prod:tracing
$ fx build
```
 

The issue is that without this option then TraceManager won't be present when the driver starts and thus the driver won't be able to participatein tracing when TraceManager is started later. 问题在于，如果没有此选项，则驱动程序启动时TraceManager将不存在，因此，稍后启动TraceManager时，驱动程序将无法参与跟踪。

See the documentation for (fx)[../../../docs/development/workflows/fx.md] or even just the output of `fx help` and especially `fx help set` for furtherdocumentation of running `fx` in general and `fx set` specifically. 请参阅（fx）[../../../ docs / development / workflows / fx.md]的文档，甚至仅查看fx help的输出，尤其是fx help set的输出，以获取运行fx的进一步文档通常是“ fx set”。

 
## Booting with tracing  跟踪启动 

To be conservative, tracing uses a kernel command line flag to enable it: `driver.tracing.enable=1`.`driver.tracing.enable=1` is the default. To disable partipationof drivers in Fuchsia tracing, boot the kernel with `driver.tracing.enable=0`. 保守起见，跟踪使用内核命令行标志来启用它：默认为driver.tracing.enable = 1`.driver.tracing.enable = 1`。要禁用紫红色跟踪中的驱动程序参与，请使用driver.tracing.enable = 0引导内核。

Then boot. See the documentation for your hardware or qemu for instructions for booting the device. Tracing doesn't require anything special during boot. 然后启动。请参阅硬件或qemu的文档以获取有关引导设备的说明。引导过程中不需要任何特殊的跟踪。

 
## Using tracing  使用追踪 

Once the system is booted you can collect traces on the target and then manually copy them to your development host.These examples use the category from the source additions described above. 系统启动后，您可以在目标上收集跟踪，然后将其手动复制到您的开发主机。这些示例使用上述源添加中的类别。

Example:  例：

```sh
fuchsia$ trace record --categories=example:example1,kernel:sched,kernel:meta
host$ fx cp --to-host /data/trace.json trace.json
```
 

However, it's easier to invoke the `traceutil` program on your development host and it will copy the files directly to your host and prepare them forviewing with the Chrome trace viewer. 但是，在开发主机上调用`traceutil`程序会更容易，它将把文件直接复制到您的主机上，并准备好使用Chrome跟踪查看器进行查看。

```sh
host$ fx traceutil record \
  --categories=example:example1,kernel:sched,kernel:meta
```
 

The categories `kernel:sched,kernel:meta` should always be present if you want to visualize the results. The visualizer wants to associate trace datawith threads and processes, and thus it needs the data provided by the kernelvia these categories. 如果您想可视化结果，则应该始终显示类别“ kernel：sched，kernel：meta”。可视化程序希望将跟踪数据与线程和进程相关联，因此它需要内核通过这些类别提供的数据。

 
## Further Reading  进一步阅读 

