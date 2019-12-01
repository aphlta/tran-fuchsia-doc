 
# Zircon  锆石 

Zircon is the core platform that powers the Fuchsia OS.  Zircon is composed of a microkernel (source in [/zircon/kernel](/zircon/kernel)as well as a small set of userspace services, drivers, and libraries(source in [/zircon/system/](/zircon/system) necessary for the systemto boot, talk to hardware, load userspace processes and run them, etc.Fuchsia builds a much larger OS on top of this foundation. Zircon是支持Fuchsia OS的核心平台。 Zircon由一个微内核（位于[/ zircon / kernel]（/ zircon / kernel）中的源代码以及一小组用户空间服务，驱动程序和库（位于[/ zircon / system /]（/ zircon / system中的源代码）组成），这对于系统启动，与硬件对话，加载用户空间进程并运行它们等是必需的.Fuchsia在此基础上构建了一个更大的OS。

The canonical Zircon repository part of the Fuchsia project at: [https://fuchsia.googlesource.com/fuchsia/+/refs/heads/master/zircon/](/zircon/) 紫红色项目的规范Zircon储存库部分，位于：[https://fuchsia.googlesource.com/fuchsia/+/refs/heads/master/zircon/](/zircon/）

The Zircon Kernel provides syscalls to manage processes, threads, virtual memory, inter-process communication, waiting on object statechanges, and locking (via futexes). Zircon内核提供系统调用来管理进程，线程，虚拟内存，进程间通信，等待对象状态更改和锁定（通过futex）。

Currently there are some temporary syscalls that have been used for early bringup work, which will be going away in the future as the long termsyscall API/ABI surface is finalized.  The expectation is that there willbe about 100 syscalls. 当前，有一些临时syscall用于早期启动工作，随着长期syscall API / ABI表面的最终确定，这些临时调用将在将来消失。预期将有大约100个syscall。

Zircon syscalls are generally non-blocking.  The wait_one, wait_many port_wait and thread sleep being the notable exceptions. Zircon系统调用通常是非阻塞的。其中，wait_one，wait_many port_wait和线程sleep是值得注意的例外。

This page is a non-comprehensive index of the zircon documentation.  此页面是Zircon文档的非全面索引。

 
+ [Getting Started](/docs/development/kernel/getting_started.md)  + [入门]（/ docs / development / kernel / getting_started.md）
+ [Contributing Patches to Zircon](/docs/development/source_code/contribute_changes.md#contributing-patches-to-zircon) + [为Zircon贡献补丁]（/ docs / development / source_code / contribute_changes.mdcontributing-patches-to-zircon）
+ [GN in Zircon](/docs/development/build/zircon_gn.md)  + [Zircon中的GN]（/ docs / development / build / zircon_gn.md）

 
+ [Concepts Overview](/docs/concepts/kernel/concepts.md)  + [概念概述]（/ docs / concepts / kernel / concepts.md）
+ [Kernel Objects](/docs/concepts/objects/objects.md)  + [内核对象]（/ docs / concepts / objects / objects.md）
+ [Kernel Invariants](kernel_invariants.md)  + [内核不变式]（kernel_invariants.md）
+ [Kernel Scheduling](kernel_scheduling.md)  + [内核调度]（kernel_scheduling.md）
+ [Fair Scheduler](fair_scheduler.md)  + [Fair Scheduler]（fair_scheduler.md）
+ [Errors](errors.md)  + [错误]（errors.md）
+ [Time](/docs/concepts/objects/time.md)  + [时间]（/ docs / concepts / objects / time.md）

 
+ [Process Objects](/docs/concepts/objects/process.md)  + [过程对象]（/ docs / concepts / objects / process.md）
+ [Thread Objects](/docs/concepts/objects/thread.md)  + [线程对象]（/ docs / concepts / objects / thread.md）
+ [Thread local storage](/docs/development/threads/tls.md)  + [线程本地存储]（/ docs / development / threads / tls.md）
+ [Thread annotations](/docs/development/threads/thread_annotations.md)  + [线程注释]（/ docs / development / threads / thread_annotations.md）
+ [Handles](/docs/concepts/objects/handles.md)  + [句柄]（/ docs / concepts / objects / handles.md）
+ [Lock validation](lockdep.md)  + [锁定验证]（lockdep.md）
+ [System Calls](/docs/reference/syscalls/README.md)  + [系统调用]（/ docs / reference / syscalls / README.md）
+ [zxcrypt](/docs/concepts/filesystems/zxcrypt.md)  + [zxcrypt]（/ docs / concepts / filesystems / zxcrypt.md）

 
+ [Driver Development Kit](/docs/concepts/drivers/overview.md)  + [驱动程序开发套件]（/ docs / concepts / drivers / overview.md）
+ [Driver interfaces - audio overview](/docs/concepts/drivers/driver_interfaces/audio_overview.md)  + [驱动程序接口-音频概述]（/ docs / concepts / drivers / driver_interfaces / audio_overview.md）

 
+ [libc](/docs/development/languages/c-cpp/libc.md)  + [libc]（/ docs / development / languages / c-cpp / libc.md）
+ [C++ fit::promise<> guide](/docs/development/languages/c-cpp/fit_promise_guide.md)  + [C ++ fit :: promise <>指南]（/ docs / development / languages / c-cpp / fit_promise_guide.md）

 
+ [Testing](/docs/development/testing/testing.md)  + [测试]（/ docs / development / testing / testing.md）
+ [Kernel tracing](/docs/development/tracing/ktrace.md)  + [内核跟踪]（/ docs / development / tracing / ktrace.md）
+ [Block device testing](/docs/development/testing/block_device_testing.md)  + [块设备测试]（/ docs / development / testing / block_device_testing.md）
+ [nand Testing](/docs/development/testing/nand_testing.md)  + [nand测试]（/ docs / development / testing / nand_testing.md）

 
+ [Compile-time object collections](/docs/development/languages/c-cpp/compile_time_object_collections.md)  + [编译时对象集合]（/ docs / development / languages / c-cpp / compile_time_object_collections.md）
+ [ACPI debugging](/docs/development/debugging/acpi.md)  + [ACPI调试]（/ docs / development / debugging / acpi.md）
+ [Fuzzing the FIDL host tools](/docs/development/testing/fuzzing/fuzzing_fidl.md)  + [模糊FIDL主机工具]（/ docs / development / testing / fuzzing / fuzzing_fidl.md）
+ [Entropy collection TODOs](/docs/concepts/system/jitterentropy/entropy_collection_todos.md)  + [熵收集待办事项]（/ docs / concepts / system / jitterentropy / entropy_collection_todos.md）
+ [Memory usage analysis tools](/docs/development/memory/memory.md)  + [内存使用情况分析工具]（/ docs / development / memory / memory.md）
+ [Symbolizer](/docs/reference/kernel/symbolizer_markup.md)  + [Symbolizer]（/ docs / reference / kernel / symbolizer_markup.md）
+ [Relationship with LK](zx_and_lk.md)  + [与LK的关系]（zx_and_lk.md）
+ [Micro-benchmarks](/docs/development/benchmarking/microbenchmarks.md)  + [微型基准]（/ docs / development / benchmarking / microbenchmarks.md）
