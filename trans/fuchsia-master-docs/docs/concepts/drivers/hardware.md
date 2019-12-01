 

 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# Hardware Interfacing  硬件接口 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

 
## Overview  总览 

In past chapters, we saw how the protocol stack was organized within a devhost, and some of the work that goes into binding the individual driver protocols intoa device driver. 在过去的章节中，我们了解了如何在devhost中组织协议栈，以及将单个驱动程序协议绑定到设备驱动程序中的一些工作。

In this section, we'll look at practical considerations of dealing with hardware such as determining configuration, binding to interrupts, allocating memory,and performing DMA operations. 在本节中，我们将研究处理硬件的实际注意事项，例如确定配置，绑定到中断，分配内存以及执行DMA操作。

Here, we'll look at the concepts involved, and show snippets of code as required. Complete working code is shown in subsequent chapters (e.g., [Ethernet Devices](ethernet.md)). 在这里，我们将研究涉及的概念，并根据需要显示代码片段。后续章节中将显示完整的工作代码（例如[以太网设备]（ethernet.md））。

For the most part, we'll focus on the PCI bus, and we'll cover the following functions: 在大多数情况下，我们将专注于PCI总线，并且将介绍以下功能：

 
* Access related:  *访问相关：
    *   **pci_map_bar()**  * ** pci_map_bar（）**
* Interrupt related:  *中断相关：
    *   **pci_map_interrupt()**  * ** pci_map_interrupt（）**
    *   **pci_query_irq_mode()**  * ** pci_query_irq_mode（）**
    *   **pci_set_irq_mode()**  * ** pci_set_irq_mode（）**
* DMA related:  *与DMA相关：
    *   **pci_enable_bus_master()**  * ** pci_enable_bus_master（）**
    *   **pci_get_bti()**  * ** pci_get_bti（）**

 
# Configuration  组态 

Hardware peripherals are attached to the CPU via a bus, such as the PCI bus.  硬件外围设备通过总线（例如PCI总线）连接到CPU。

During bootup, the BIOS (or equivalent platform startup software) discovers all of the peripherals attached to the PCI bus.Each peripheral is assigned resources (notably interrupt vectors,and address ranges for configuration registers). 在启动过程中，BIOS（或等效的平台启动软件）会发现连接到PCI总线的所有外围设备。每个外围设备都分配有资源（特别是中断向量和配置寄存器的地址范围）。

The impact of this is that the actual resources assigned to each peripheral may be different across reboots.When the operating system software starts up, it enumeratesthe bus and starts drivers for all supported devices.The drivers then call PCI functions in order to obtain configuration information abouttheir device(s) so that they can map registers and bind to interrupts. 这样做的影响是分配给每个外围设备的实际资源在重新引导后可能会有所不同。当操作系统软件启动时，它将枚举总线并启动所有受支持设备的驱动程序，然后驱动程序调用PCI函数以获取配置信息关于它们的设备，以便它们可以映射寄存器并绑定到中断。

 
## Base address register  基址寄存器 

The Base Address Register (**BAR**) is a configuration register that exists on each PCI device.It's where the BIOS stores information about the device, such as the assigned interrupt vectorand addresses of control registers.Other, device specific information, is stored there as well. 基址寄存器（** BAR **）是每个PCI设备上存在的配置寄存器，BIOS在其中存储有关该设备的信息，例如分配的中断向量和控制寄存器的地址。存储在那里。

Call **pci_map_bar()** to cause the BAR register to be mapped into the devhost's address space: 调用** pci_map_bar（）**使BAR寄存器映射到devhost的地址空间：

```c
zx_status_t pci_map_bar(const pci_protocol_t* pci, uint32_t bar_id,
                        uint32_t cache_policy, void** vaddr, size_t* size,
                        zx_handle_t* out_handle);
```
 

The first parameter, `pci`, is a pointer to the PCI protocol. Typically, you obtain this in your **bind()** function via**device_get_protocol()**. 第一个参数“ pci”是指向PCI协议的指针。通常，您可以通过device_get_protocol（）**在** bind（）**函数中获得此值。

The second parameter, `bar_id`, is the BAR register number, starting with `0`.  第二个参数“ bar_id”是BAR寄存器号，从“ 0”开始。

The third parameter, `cache_policy`, determines the caching policy for access, and can take on the following values: 第三个参数`cache_policy`确定访问的缓存策略，并可以采用以下值：

`cache_policy` value                | Meaning ------------------------------------|---------------------`ZX_CACHE_POLICY_CACHED`            | use hardware caching`ZX_CACHE_POLICY_UNCACHED`          | disable caching`ZX_CACHE_POLICY_UNCACHED_DEVICE`   | disable caching, and treat as device memory`ZX_CACHE_POLICY_WRITE_COMBINING`   | uncached with write combining `cache_policy`值|含义------------------------------------ | ------------ ---------`ZX_CACHE_POLICY_CACHED` |使用硬件缓存`ZX_CACHE_POLICY_UNCACHED` |禁用缓存`ZX_CACHE_POLICY_UNCACHED_DEVICE` |禁用高速缓存，并将其视为设备内存`ZX_CACHE_POLICY_WRITE_COMBINING` |通过写合并取消缓存

Note that `ZX_CACHE_POLICY_UNCACHED_DEVICE` is architecture dependent and may in fact be equivalent to `ZX_CACHE_POLICY_UNCACHED` on some architectures. 注意，“ ZX_CACHE_POLICY_UNCACHED_DEVICE”取决于体系结构，实际上在某些体系结构上可能等效于“ ZX_CACHE_POLICY_UNCACHED”。

The next three arguments are return values. The `vaddr` and `size` return a pointer (and length) of the register region, while`out_handle` stores the created handle to the[VMO](/docs/concepts/objects/vm_object.md). 接下来的三个参数是返回值。 vaddr和size返回寄存器区域的指针（和长度），而out_handle将创建的句柄存储到[VMO]（/ docs / concepts / objects / vm_object.md）。

 
## Reading and writing memory  读写记忆 

Once the **pci_map_bar()** function returns with a valid result, you can access the BAR via simple pointeroperations, for example: 一旦** pci_map_bar（）**函数返回有效结果，您就可以通过简单的指针操作访问BAR，例如：

```c
volatile uint32_t* base;
...
zx_status_t rc;
rc = pci_map_bar(dev->pci, 0, ZX_CACHE_POLICY_UNCACHED_DEVICE, &base, &size, &handle);
if (rc == ZX_OK) {
    base[REGISTER_X] = 0x1234;  // configure register X for deep sleep mode
}
```
 

It's important to declare `base` as `volatile` &mdash; this tells the compiler not to make any assumptions about the contents of the data that `base` points to.For example: 将base声明为volatile是很重要的。这告诉编译器不要对base指向的数据内容做任何假设，例如：

```c
int timeout = 1000;
while (timeout-- > 0 && !(base[REGISTER_READY] & READY_BIT)) ;
```
 

is a typical (bounded) polling loop, intended for short polling sequences. Without the `volatile` keyword in the declaration, the compiler would have no reasonto believe that the value at `base[REGISTER_READY]` would ever change, so it wouldcause it to be read only once. 是典型的（有界）轮询循环，旨在用于较短的轮询序列。如果在声明中没有`volatile`关键字，编译器将没有理由相信`base [REGISTER_READY]`的值将会改变，因此只会被读取一次。

 
# Interrupts  中断 

An interrupt is an asynchronous event, generated by a device when it needs servicing. For example, an interrupt is generated when data is available on a serial port,or an ethernet packet has arrived.Interrupts allow a driver to know about an event as soon as itoccurs, but without the driver spending time polling (actively waiting) for it. 中断是一个异步事件，由设备在需要服务时生成。例如，当串行端口上有可用数据或以太​​网数据包到达时，将产生一个中断，该中断使驱动程序可以在事件发生后立即知道该事件，而无需驱动程序花费时间轮询（主动等待） 。

The general architecture of a driver that uses interrupts is that a background Interrupt Handling Thread (**IHT**) is created during the driver startup / bindingoperation.This thread waits for an interrupt to happen, and, when it does, performs somekind of servicing action. 使用中断的驱动程序的一般体系结构是在驱动程序启动/绑定操作期间创建了一个后台中断处理线程（** IHT **），该线程等待中断发生，并在发生中断时执行某种服务行动。

As an example, consider a serial port driver. It may receive interrupts due to any of the following events happening: 例如，考虑一个串行端口驱动程序。由于发生以下任何事件，它可能会收到中断：

 
*   one or more characters have arrived,  *一个或多个字符已经到来，
*   room is now available to transmit one or more characters,  *房间现在可以传输一个或多个字符，
*   a control line (like `DTR`, for example) has changed state.  *控制线（例如“ DTR”）已更改状态。

The interrupt wakes up the IHT. The IHT determines the cause of the event, usually by reading some status registers.Then, it runs an appropriate service function to handle the event.Once done, the IHT goes back to sleep, waiting for the next interrupt. 中断唤醒IHT。 IHT通常通过读取一些状态寄存器来确定事件的原因，然后运行适当的服务功能来处理事件，完成后IHT返回睡眠状态，等待下一个中断。

For example, if a character arrives, the IHT wakes up, reads a status register that indicates "data is available," and then calls a function that drains all availablecharacters from the serial port FIFO into the driver's buffer. 例如，如果一个字符到达，则IHT唤醒，读取一个指示“数据可用”的状态寄存器，然后调用一个函数，该函数将所有可用字符从串行端口FIFO排入驱动程序的缓冲区。

 
## No kernel-level code required  无需内核级代码 

You may be familiar with other operating systems which use Interrupt Service Routines (**ISR**).These are kernel-level handlers that run in privileged mode and interface withthe interrupt controller hardware. 您可能熟悉使用中断服务例程（** ISR **）的其他操作系统。这些是在特权模式下运行并与中断控制器硬件接口的内核级处理程序。

In Fuchsia, the kernel deals with the privileged part of the interrupt handling, and provides thread-level functions for driver use. 在Fuchsia中，内核处理中断处理的特权部分，并提供线程级函数供驱动程序使用。

The difference is that the IHT runs at thread level, whereas the ISR runs at kernel level in a very restricted (and sometimes fragile) environment.A principal advantage is that if the IHT crashes, it takes out only thedriver, whereas a failing ISR can take out the entire operating system. 区别在于IHT在线程级别运行，而ISR在非常受限（有时甚至是脆弱）的环境中运行在内核级别。其主要优点是，如果IHT崩溃，则仅删除驱动程序，而发生故障的ISR可以取出整个操作系统。

 
## Attaching to an interrupt  附加到中断 

Currently, the only bus that provides interrupts is the PCI bus. It supports two kinds: legacy and Message Signaled Interrupts (**MSI**). 当前，唯一提供中断的总线是PCI总线。它支持两种：传统和消息信号中断（** MSI **）。

Therefore, in order to use interrupts on PCI:  因此，为了在PCI上使用中断：

 
1.  determine which kind your device supports (legacy or MSI),  1.确定您的设备支持哪种类型（旧版或MSI），
2.  set the interrupt mode to match,  2.将中断模式设置为匹配，
3.  get a handle to your device's interrupt vector (usually one, but may be multiple),  3.获取设备中断向量的句柄（通常是一个，但可能是多个），
4.  start IHT background thread,  4.启动IHT后台线程，
5.  arrange for IHT thread to wait for interrupts (on handle(s) from step 3).  5.安排IHT线程等待中断（在步骤3中的句柄上）。

Steps `1` and `2` are usually done closely together, for example:  通常将步骤“ 1”和“ 2”紧密地结合在一起，例如：

```c
// Query whether we have MSI or Legacy interrupts.
uint32_t irq_cnt = 0;
if ((pci_query_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_MSI, &irq_cnt) == ZX_OK) &&
    (pci_set_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_MSI, 1) == ZX_OK)) {
    // using MSI interrupts
} else if ((pci_query_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_LEGACY, &irq_cnt) == ZX_OK) &&
           (pci_set_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_LEGACY, 1) == ZX_OK)) {
    // using legacy interrupts
} else {
    // an error
}
```
 

The **pci_query_irq_mode()** function takes three arguments: ** pci_query_irq_mode（）**函数采用三个参数：

```c
zx_status_t pci_query_irq_mode(const pci_protocol_t* pci,
                               zx_pci_irq_mode_t mode,
                               uint32_t* out_max_irqs);
```
 

The first argument, `pci`, is a pointer to the PCI protocol stack bound to your device just like we saw above, in the BAR documentation. 第一个参数“ pci”是指向BAR设备中绑定到您设备的PCI协议栈的指针。

The second argument, `mode`, is the kind of interrupt that you are interested in; it's one of the two constants shown in the example. 第二个参数“ mode”是您感兴趣的一种中断。它是示例中显示的两个常量之一。

> @@@ there's also a `ZX_PCIE_IRQ_MODE_MSI_X` in the syscalls/pci.h file; should I say anything about that? How would we use it in the above case, just make a third condition?  > @@@ syscalls / pci.h文件中还有一个ZX_PCIE_IRQ_MODE_MSI_X；我该说些什么吗？在上面的情况下，仅作第三个条件，我们将如何使用它？

The third argument is a pointer to integer that returns how many interrupts of the specified type your device supports. 第三个参数是一个指向整数的指针，该整数返回设备支持的指定类型的中断次数。

Having determined the kind of interrupt supported, you then call **pci_set_irq_mode()**to indicate that this is indeed the kind of interrupt that you wish to use. 确定支持的中断类型后，您可以调用** pci_set_irq_mode（）**来表明这确实是您希望使用的中断类型。

Finally, you call **pci_map_interrupt()** to create a handle to the selected interrupt. Note that**pci_map_interrupt()** has the following prototype: 最后，您调用** pci_map_interrupt（）**创建所选中断的句柄。请注意，** pci_map_interrupt（）**具有以下原型：

```c
zx_status_t pci_map_interrupt(const pci_protocol_t* pci,
                              int which_irq,
                              zx_handle_t* out_handle);
```
 

The first argument is the same as in the previous call, the second argument, `which_irq` indicates the device-relative interrupt number you'd like, and the third argumentis a pointer to the created interrupt handle. 第一个参数与上一个调用中的参数相同，第二个参数“ which_irq”指示您想要的设备相对中断号，第三个参数是指向创建的中断句柄的指针。

You now have an interrupt handle.  您现在有了一个中断句柄。

> Note that the vast majority of devices have just one interrupt, so simply passing > `0` for `which_irq` is normal.> If your device does have more than one interrupt, the common practice is to run the> **pci_map_interrupt()** function in a `for` loop> and bind handles to each interrupt. >请注意，绝大多数设备只有一个中断，因此只需为which_irq传递> 0即可。>如果您的设备确实有多个中断，通常的做法是运行** pci_map_interrupt（ ）**在“ for”循环中起作用，并将句柄绑定到每个中断。

 
## Waiting for the interrupt  等待中断 

In your IHT, you call [**zx_interrupt_wait()**](/docs/reference/syscalls/interrupt_wait.md) to wait for the interrupt.The following prototype applies: 在您的IHT中，您调用[** zx_interrupt_wait（）**]（/ docs / reference / syscalls / interrupt_wait.md）等待中断。以下原型适用：

```c
zx_status_t zx_interrupt_wait(zx_handle_t handle,
                              zx_time_t* out_timestamp);
```
 

The first argument is the handle you obtained via the call to **pci_map_interrupt()**,and the second parameter can be `NULL` (typical), or it can be a pointer to a timestamp that indicates when the interrupt was triggered (in nanoseconds,relative to the clock source `ZX_CLOCK_MONOTONIC`). 第一个参数是您通过调用** pci_map_interrupt（）**获得的句柄，第二个参数可以是“ NULL”（典型值），也可以是指向指示中断触发时间的时间戳的指针（相对于时钟源“ ZX_CLOCK_MONOTONIC”（以纳秒为单位）。

Therefore, a typical IHT would have the following shape:  因此，典型的IHT具有以下形状：

```c
static int irq_thread(void* arg) {
    my_device_t* dev = arg;
    for (;;) {
        zx_status_t rc;
        rc = zx_interrupt_wait(dev->irq_handle, NULL);
        // do stuff
    }
}
```
 

The convention is that the argument passed to the IHT is your device context block. The context block has a member (here `irq_handle`) that is the handle you obtained via**pci_map_interrupt()**. 约定是传递给IHT的参数是您的设备上下文块。上下文块具有一个成员（此处为“ irq_handle”），该成员是您通过** pci_map_interrupt（）**获得的句柄。

 
## Edge vs level interrupt mode  边沿电平中断模式 

The interrupt hardware can operate in one of two modes; "edge" or "level".  中断硬件可以在以下两种模式之一中运行： “边缘”或“水平”。

In edge mode, the interrupt is armed on the active-going edge (when the hardware signal goes from inactive to active), and works as a one-shot.That is, the signal must go back to inactive before it can be recognized again. 在边缘模式下，中断被设在活动的上升沿（当硬件信号从非活动状态变为活动状态时），并且是一次触发，也就是说，信号必须回到非活动状态才能再次被识别。

In level mode, the interrupt is active when the hardware signal is in the active state. 在级别模式下，当硬件信号处于活动状态时，中断处于活动状态。

Typically, edge mode is used when the interrupt is dedicated, and level mode is used when the interrupt is shared by multiple devices (because you want theinterrupt to remain active until *all* devices have de-asserted their request line). 通常，在专用于中断时使用边沿模式，而在多个设备共享中断时使用电平模式（因为您希望中断保持活动状态，直到*所有*设备取消声明其请求线为止）。

The Zircon kernel automatically masks and unmasks the interrupt as appropriate. For level-triggered hardware interrupts,[**zx_interrupt_wait()**](/docs/reference/syscalls/interrupt_wait.md)masks the interrupt before returning, and unmasks it when called the next time.For edge-triggered interrupts, the interrupt remains unmasked. Zircon内核会根据需要自动屏蔽和取消屏蔽中断。对于级别触发的硬件中断，[** zx_interrupt_wait（）**]（/ docs / reference / syscalls / interrupt_wait.md）在返回之前屏蔽该中断，并在下次调用时取消屏蔽。对于边沿触发的中断，中断保持未屏蔽状态。

> The IHT should not perform any long-running tasks. > For drivers that perform lengthy tasks, use a worker thread. > IHT不应执行任何长期运行的任务。 >对于执行冗长任务的驱动程序，请使用辅助线程。

 
## Shutting down a driver that uses interrupts  关闭使用中断的驱动程序 

In order to cleanly shut down a driver that uses interrupts, you can use [**zx_interrupt_destroy()**](/docs/reference/syscalls/interrupt_destroy.md)to abort the[**zx_interrupt_wait()**](/docs/reference/syscalls/interrupt_wait.md)call. 为了彻底关闭使用中断的驱动程序，可以使用[** zx_interrupt_destroy（）**]（/ docs / reference / syscalls / interrupt_destroy.md）中止[** zx_interrupt_wait（）**]（/ docs / reference / syscalls / interrupt_wait.md）调用。

The idea is that when the foreground thread determines that the driver should be shut down, it simply destroys the interrupt handle, causing the IHT to shut down: 这个想法是，当前台线程确定应关闭驱动程序时，它只会破坏中断句柄，从而导致IHT关闭：

```c
static void main_thread() {
    ...
    if (shutdown_requested) {
        // destroy the handle, this will cause zx_interrupt_wait() to pop
        zx_interrupt_destroy(dev->irq_handle);

        // wait for the IHT to finish
        thrd_join(dev->iht, NULL);
    }
    ...
}

static int irq_thread(void* arg) {
    ...
    for(;;) {
        zx_status_t rc;
        rc = zx_interrupt_wait(dev->irq_handle, NULL);
        if (rc == ZX_ERR_CANCELED) {
            // we are being shut down, do any cleanups required
            ...
            return;
        }
        ...
    }
}
```
 

The main thread, when requested to shut down, destroys the interrupt handle. This causes the IHT's[**zx_interrupt_wait()**](/docs/reference/syscalls/interrupt_wait.md)call to wake up with an error code.The IHT looks at the error code (in this case, `ZX_ERR_CANCELED`) and makesthe decision to end.Meanwhile, the main thread is waiting to join the IHT via the callto **thrd_join()**.Once the IHT exits, **thrd_join()** returns, and the mainthread can finish its processing. 当请求关闭主线程时，它将破坏中断句柄。这会导致IHT的[** zx_interrupt_wait（）**]（/ docs / reference / syscalls / interrupt_wait.md）调用以错误代码唤醒。IHT会查看错误代码（在本例中为`ZX_ERR_CANCELED`）。同时，主线程正在等待通过调用thrd_join（）**加入IHT。一旦IHT退出，** thrd_join（）**将返回，并且主线程可以完成其处理。

The advanced reader is invited to look at some of the other interrupt related functions available: 欢迎高级阅读者查看其他一些与中断有关的功能：

 
*   [**zx_interrupt_ack()**](/docs/reference/syscalls/interrupt_ack.md)  * [** zx_interrupt_ack（）**]（/ docs / reference / syscalls / interrupt_ack.md）
*   [**zx_interrupt_bind()**](/docs/reference/syscalls/interrupt_bind.md)  * [** zx_interrupt_bind（）**]（/ docs / reference / syscalls / interrupt_bind.md）
*   [**zx_interrupt_create()**](/docs/reference/syscalls/interrupt_create.md)  * [** zx_interrupt_create（）**]（/ docs / reference / syscalls / interrupt_create.md）
*   [**zx_interrupt_trigger()**](/docs/reference/syscalls/interrupt_trigger.md)  * [** zx_interrupt_trigger（）**]（/ docs / reference / syscalls / interrupt_trigger.md）

 
# DMA  DMA 

Direct Memory Access (**DMA**) is a feature that allows hardware to access memory without CPU intervention.At the highest level, the hardware is given the source and destination of thememory region to transfer (along with its size) and told to copy the data.Some hardware peripherals even support the ability to do multiple"scatter / gather" style operations, where several copy operationscan be performed, one after the other, without additional CPU intervention. 直接内存访问（** DMA **）是一项允许硬件访问内存而无需CPU干预的功能。在最高级别上，硬件将获得要传输的主题区域的源和目标（及其大小）并告知复制数据。某些硬件外围设备甚至支持执行多个“分散/收集”样式的操作的能力，在这些操作中，可以一个接一个地执行多个复制操作，而无需其他CPU干预。

 
## DMA considerations  DMA注意事项 

In order to fully appreciate the issues involved, it's important to keep the following in mind: 为了充分理解所涉及的问题，请务必牢记以下几点：

 
*   each process operates in a virtual address space,  *每个进程都在虚拟地址空间中运行，
*   an MMU can map a contiguous virtual address range onto multiple, discontiguous physical address ranges (and vice-versa), * MMU可以将连续的虚拟地址范围映射到多个不连续的物理地址范围（反之亦然），
*   each process has a limited window into physical address space,  *每个进程都有进入物理地址空间的有限窗口，
*   some peripherals support their own virtual addresses via an Input / Output Memory Management Unit (**IOMMU**). *一些外设通过输入/输出内存管理单元（** IOMMU **）支持它们自己的虚拟地址。

Let's discuss each point in turn.  让我们依次讨论每个要点。

 
### Virtual, physical, and device-physical addresses  虚拟，物理和设备物理地址 

The addresses that the process has access to are virtual; that is, they are an illusion created by the CPU's Memory Management Unit (**MMU**).A virtual address is mapped by the MMU into a physical address.The mapping granularity is based on a parameter called "page size," whichis at least 4k bytes, though larger sizes are available on modern processors. 进程可以访问的地址是虚拟的；也就是说，它们是由CPU的内存管理单元（** MMU **）创建的一种幻觉。虚拟地址由MMU映射为物理地址。映射粒度基于称为“页面大小”的参数，即至少4k字节，尽管现代处理器可以使用更大的大小。

![Figure: Relationship between virtual and physical addresses](dma-000-cropped.png)  ！[图：虚拟地址和物理地址之间的关系]（dma-000-cropped.png）

In the diagram above, we show a specific process (process 12) with a number of virtual addresses (in blue).The MMU is responsible for mapping the blue virtual addresses into CPU physicalbus addresses (red).Each process has its own mapping; so even though process 12 has a virtual address`300`, some other process may also have a virtual address `300`.That other process's virtual address `300` (if it exists) would be mappedto a different physical address than the one in process 12. 在上图中，我们显示了一个特定的进程（进程12），其中包含多个虚拟地址（蓝色）。MMU负责将蓝色的虚拟地址映射到CPU物理总线地址（红色）。因此，即使进程12具有虚拟地址“ 300”，其他进程也可能具有虚拟地址“ 300”。该其他进程的虚拟地址“ 300”（如果存在）将被映射到与其中一个不同的物理地址。过程12。

> Note that we've used small decimal numbers as "addresses" to keep the discussion simple. > In reality, each square shown above represents a page of memory (4k or more),> and is identified by a 32 or 64 bit value (depending on the platform). >请注意，我们使用小十进制数字作为“地址”，以使讨论变得简单。 >实际上，上面显示的每个正方形代表一个内存页面（4k或更多），并且由32位或64位值标识（取决于平台）。

The key points shown in the diagram are:  图中显示的关键点是：

 
1.  virtual addresses can be allocated in groups (three are shown, `300`-`303`, `420`-`421`, and `770`-`771`), 1.可以按组分配虚拟地址（显示了三个，即“ 300”-“ 303”，“ 420” -`421和“ 770”-“ 771”），
2.  virtually contiguous (e.g., `300`-`303`) is not necessarily physically contiguous.  2.实际上是连续的（例如，“ 300”-“ 303”）在物理上不一定是连续的。
3.  some virtual addresses are not mapped (for example, there is no virtual address `304`) 3.一些虚拟地址未映射（例如，没有虚拟地址“ 304”）
4.  not all physical addresses are available to each process (for example, process `12` doesn't have access to physical address `120`). 4.并非所有物理地址都可用于每个进程（例如，进程“ 12”无法访问物理地址“ 120”）。

Depending on the hardware available on the platform, a device's address space may or may not follow a similar translation.Without an IOMMU, the addresses that the peripheral uses are the same asthe physical addresses used by the CPU: 取决于平台上可用的硬件，设备的地址空间可能遵循也可能不遵循类似的转换。没有IOMMU，外围设备使用的地址与CPU使用的物理地址相同：

![Figure: A device that doesn't use an IOMMU](dma-002-cropped.png)  ！[图：不使用IOMMU的设备]（dma-002-cropped.png）

In the diagram above, portions of the device's address space (for example, a frame buffer, or control registers), appear directly in the CPU's physicaladdress range.That is to say, the device occupies physical addresses `122` through `125`inclusive. 在上图中，设备地址空间的某些部分（例如帧缓冲区或控制寄存器）直接出现在CPU的物理地址范围内，也就是说，设备占用的物理地址为122至125 。

In order for the process to access the device's memory, it would need to create an MMU mapping from some virtual addresses to the physical addresses `122` through`125`.We'll see how to do that, below. 为了使进程访问设备的内存，需要创建一个从某些虚拟地址到物理地址“ 122”到“ 125”的MMU映射。我们将在下面看到如何做到这一点。

But with an IOMMU, the addresses seen by a peripheral may be different than the CPU's physical addresses: 但是对于IOMMU，外围设备看到的地址可能与CPU的物理地址不同：

![Figure: A device that uses an IOMMU](dma-001-cropped.png)  ！[图：使用IOMMU的设备]（dma-001-cropped.png）

Here, the device has its own "device-physical" addresses that it knows about, that is, addresses `0` through `3` inclusive.It's up to the IOMMU to map the device-physical addresses `0` through `3`into CPU physical addresses `109`, `110`, `101`, and `119`, respectively. 在这里，设备具有自己知道的“设备物理”地址，即地址“ 0”到“ 3”（含）。由IOMMU来映射设备物理地址“ 0”到“ 3”。分别进入CPU物理地址“ 109”，“ 110”，“ 101”和“ 119”。

In this scenario, in order for the process to use the device's memory, it needs to arrange two mappings: 在这种情况下，为了使进程使用设备的内存，它需要安排两个映射：

 
*   one set from the virtual address space (e.g., `300` through `303`) to the CPU physical address space (`109`, `110`, `101`, and `119`, respectively),via the MMU, and *一组通过MMU从虚拟地址空间（例如，“ 300”到“ 303”）到CPU物理地址空间（分别为“ 109”，“ 110”，“ 101”和“ 119”）的集合，和
*   one set from the CPU physical address space (addresses `109`, `110`, `101`, and `119`) to the device-physical addresses (`0` through `3`) via the IOMMU. *一组通过IOMMU从CPU物理地址空间（地址109、110、101和119）到设备物理地址（0到3）。

While this may seem complicated, Zircon provides an abstraction that removes the complexity. 尽管这看起来很复杂，但Zircon提供了消除复杂性的抽象。

Also, as we'll see below, the reason for having an IOMMU, and the benefits provided, are similar to those obtained by having an MMU. 另外，正如我们将在下面看到的，拥有IOMMU的原因以及所提供的好处与拥有MMU所获得的好处相似。

 
### Contiguity of memory  记忆的连续性 

When you allocate a large chunk of memory (e.g. via **calloc()**), your process will, of course, see a large, contiguous virtual address range.The MMU creates the illusion of contiguous memory at the virtual addressinglevel, even though the MMU may choose to back that memory area with physicallydiscontiguous memory at the physical address level. 当您分配大量内存时（例如通过** calloc（）**），您的进程当然会看到较大的连续虚拟地址范围。MMU会在虚拟寻址级别上产生连续内存的错觉，甚至尽管MMU可以选择在物理地址级别使用物理上不连续的内存来支持该内存区域。

Furthermore, as processes allocate and deallocate memory, the mapping of physical memory to virtual address space tends to become morecomplex, encouraging more "swiss cheese" holes to appear (that is,more discontiguities in the mapping). 此外，随着进程分配和取消分配内存，物理内存到虚拟地址空间的映射趋向于变得更加复杂，从而鼓励出现更多的“瑞士奶酪”漏洞（即，映射中的更多不一致性）。

Therefore, it's important to keep in mind that contiguous virtual addresses are not necessarily contiguous physical addresses, and indeed that contiguousphysical memory becomes more precious over time. 因此，重要的是要记住，连续的虚拟地址不一定是连续的物理地址，而且随着时间的推移，连续的物理内存确实变得越来越宝贵。

 
### Access controls  访问控制 

Another benefit of the MMU is that processes are limited in their view of physical memory (for security and reliability reasons).The impact on drivers, though, is that a process has to specifically requesta mapping from virtual address space to physical address space, andhave the requisite privilege in order to do so. MMU的另一个好处是，进程在物理内存方面受到限制（出于安全性和可靠性的考虑）。但是，对驱动程序的影响是，进程必须专门请求从虚拟地址空间到物理地址空间的映射，并且具有这样做所需的特权。

 
### IOMMU  国际货币基金组织 

Contiguous physical memory is generally preferred. It's more efficient to do one transfer (with one source address and onedestination address) than it is to set up and manage multiple individualtransfers (which may require CPU intervention between each transfer inorder to set up the next one). 连续的物理内存通常是首选。进行一次传输（使用一个源地址和目标地址）要比设置和管理多个单独的传输（这可能需要在每次传输之间进行CPU干预才能设置下一个传输）更为有效。

The IOMMU, if available, alleviates this problem by doing the same thing for the peripherals that the CPU's MMU does for the process &mdash; it gives the peripheralthe illusion that it's dealing with a contiguous address space bymapping multiple discontiguous chunks into a virtually contiguous space.By limiting the mapping region, the IOMMU also provides security (in the same way asthe MMU does), by preventing the peripheral from accessing memory that's not "in scope"for the current operation. IOMMU（如果可用）通过对外围设备执行与CPU MMU对进程mdash相同的操作来缓解此问题。通过将多个不连续的块映射到一个实际上连续的空间，它给外围设备带来了一种幻想，即它正在处理连续的地址空间。通过限制映射区域，IOMMU还通过防止外围设备访问而提供了安全性（与MMU相同）。当前操作不在“范围内”的内存。

 
### Tying it all together  绑在一起 

So, it may appear that you need to worry about virtual, physical, and device-physical address spaces when you are writing your driver.But that's not the case. 因此，似乎在编写驱动程序时需要担心虚拟，物理和设备物理地址空间，但事实并非如此。

 
## DMA and your driver  DMA和您的驱动程序 

Zircon provides a set of functions that allow you to cleanly deal with all of the above.The following work together: Zircon提供了一组功能，使您可以轻松地处理上述所有问题。

 
*   a Bus Transaction Initiator (**[BTI](/docs/concepts/objects/bus_transaction_initiator.md)**), and  *公交交易发起人（** [BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）**），以及
*   a Virtual Memory Object (**[VMO](/docs/concepts/objects/vm_object.md)**).  *虚拟内存对象（** [VMO]（/ docs / concepts / objects / vm_object.md）**）。

The [BTI](/docs/concepts/objects/bus_transaction_initiator.md) kernel object provides an abstraction of the model, and an API to deal withphysical (or device-physical) addresses associated with[VMO](/docs/concepts/objects/vm_object.md)s. [BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）内核对象提供了模型的抽象，以及用于处理与[VMO]（/ docs / concepts / objects）相关的物理（或设备物理）地址的API /vm_object.md）。

In your driver's initialization, call **pci_get_bti()**to obtain a [BTI](/docs/concepts/objects/bus_transaction_initiator.md) handle: 在驱动程序的初始化中，调用** pci_get_bti（）**以获取[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）句柄：

```c
zx_status_t pci_get_bti(const pci_protocol_t* pci,
                        uint32_t index,
                        zx_handle_t* bti_handle);
```
 

The **pci_get_bti()** function takes a `pci` protocol pointer (just like all the other **pci_...()** functionsdiscussed above) and an `index` (reserved for future use, use `0`).It returns a [BTI](/docs/concepts/objects/bus_transaction_initiator.md)handle through the `bti_handle` pointer argument. ** pci_get_bti（）**函数使用一个`pci`协议指针（就像上面讨论的所有其他** pci _...（）**函数一样）和一个`index`（保留以供将来使用，请使用`0`）。 ）。它通过`bti_handle`指针参数返回一个[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）处理。

Next, you need a [VMO](/docs/concepts/objects/vm_object.md). Simplistically, you can think of the [VMO](/docs/concepts/objects/vm_object.md)as a pointer to a chunk of memory,but it's more than that &mdash; it's a kernel object that represents a setof virtual pages (that may or may not have physical pages committed to them),which can be mapped into the virtual address space of the driver process.(It's even more than that, but that's a discussion for a different chapter.) 接下来，您需要一个[VMO]（/ docs / concepts / objects / vm_object.md）。简而言之，您可以将[VMO]（/ docs / concepts / objects / vm_object.md）视为指向大块内存的指针，但它不仅仅限于此。它是一个内核对象，代表一组虚拟页面（可能已提交或可能未提交物理页面），这些虚拟页面可映射到驱动程序进程的虚拟地址空间中（甚至更多，但这是针对不同的章节。）

Ultimately, these pages serve as the source or destination of the DMA transfer.  最终，这些页面充当DMA传输的源或目标。

There are two functions, [**zx_vmo_create()**](/docs/reference/syscalls/vmo_create.md)and[**zx_vmo_create_contiguous()**](/docs/reference/syscalls/vmo_create_contiguous.md)that allocate memory and bind it to a [VMO](/docs/concepts/objects/vm_object.md): 有两个函数，[** zx_vmo_create（）**]（/ docs / reference / syscalls / vmo_create.md）和[** zx_vmo_create_contiguous（）**]（/ docs / reference / syscalls / vmo_create_contiguous.md）分配内存并将其绑定到[VMO]（/ docs / concepts / objects / vm_object.md）：

```c
zx_status_t zx_vmo_create(uint64_t size,
                          uint32_t options,
                          zx_handle_t* out);

zx_status_t zx_vmo_create_contiguous(zx_handle_t bti,
                                     size_t size,
                                     uint32_t alignment_log2,
                                     zx_handle_t* out);
```
 

As you can see, they both take a `size` parameter indicating the number of bytes required, and they both return a [VMO](/docs/concepts/objects/vm_object.md) (via `out`).They both allocate virtually contiguous pages, for a given size. 如您所见，它们都使用一个“ size”参数来指示所需的字节数，并且都通过“ out”返回一个[VMO]（/ docs / concepts / objects / vm_object.md）。对于给定的大小，实际上是连续的页面。

> Note that this differs from the standard C library memory allocation functions, > (e.g., **malloc()**), which allocate virtually contiguous memory, but without> regard to page boundaries. Two small **malloc()** calls in a row might allocate> two memory regions from the *same* page, for instance, whereas> the [VMO](/docs/concepts/objects/vm_object.md)> creation functions will always allocate memory starting with a *new* page. >请注意，这与标准C库内存分配函数>（例如** malloc（）**）不同，后者实际上分配了连续的内存，却不考虑页面边界。例如，连续两个小的** malloc（）**调用可能会从* same *页面中分配>两个内存区域，而> [VMO]（/ docs / concepts / objects / vm_object.md）>创建函数将始终从* new *页开始分配内存。

The [**zx_vmo_create_contiguous()**](/docs/reference/syscalls/vmo_create_contiguous.md)function does what[**zx_vmo_create()**](/docs/reference/syscalls/vmo_create.md)does, *and* ensures that the pages are suitablyorganized for use with the specified [BTI](/docs/concepts/objects/bus_transaction_initiator.md)(which is why it needs the [BTI](/docs/concepts/objects/bus_transaction_initiator.md) handle).It also features an `alignment_log2` parameter that can be used to specify a minimumalignment requirement.As the name suggests, it must be an integer power of 2 (with the value `0` indicatingpage aligned). [** zx_vmo_create_contiguous（）**]（/ docs / reference / syscalls / vmo_create_contiguous.md）函数可以执行[** zx_vmo_create（）**]（/ docs / reference / syscalls / vmo_create.md） *确保适当地组织页面以与指定的[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）一起使用（这就是为什么它需要[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）句柄的原因）。它还具有一个`alignment_log2`参数，该参数可用于指定最小对齐要求。顾名思义，它必须是2的整数次幂（值'0'表示页面已对齐）。

At this point, you have two "views" of the allocated memory:  此时，您对分配的内存有两个“视图”：

 
*   one contiguous virtual address space that represents memory from the point of view of the driver, and *一个连续的虚拟地址空间，从驱动程序的角度代表内存；以及
*   a set of (possibly contiguous, possibly committed) physical pages for use by the peripheral. *外围设备使用的一组（可能是连续的，可能是已提交的）物理页面。

Before using these pages, you need to ensure that they are present in memory (that is, "committed" &mdash; the physical pages are accessible to your process), and that theperipheral has access to them (via the IOMMU if present).You will also need the addresses of the pages (from the point of view of the device)so that you can program the DMA controller on your device to access them. 在使用这些页面之前，您需要确保它们存在于内存中（即“已提交”-物理页面可供您的进程访问），并且外围设备可以访问它们（通过IOMMU（如果存在））。 （从设备的角度来看）还需要页面的地址，以便您可以对设备上的DMA控制器进行编程以访问它们。

The [**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md)function is used to do all that: [** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md）函数用于执行所有操作：

```c
#include <zircon/syscalls.h>

zx_status_t zx_bti_pin(zx_handle_t bti, uint32_t options,
                       zx_handle_t vmo, uint64_t offset, uint64_t size,
                       zx_paddr_t* addrs, size_t addrs_count,
                       zx_handle_t* pmt);
```
 

There are 8 parameters to this function:  此功能有8个参数：

Parameter       | Purpose ----------------|------------------------------------`bti`           | the [BTI](/docs/concepts/objects/bus_transaction_initiator.md) for this peripheral`options`       | options (see below)`vmo`           | the [VMO](/docs/concepts/objects/vm_object.md) for this memory region`offset`        | offset from the start of the [VMO](/docs/concepts/objects/vm_object.md)`size`          | total number of bytes in [VMO](/docs/concepts/objects/vm_object.md)`addrs`         | list of return addresses`addrs_count`   | number of elements in `addrs``pmt`           | returned [PMT](/docs/concepts/objects/pinned_memory_token.md) (see below) 参数目的---------------- | -------------------------------- ----`bti` |该外围设备选项的[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）|选项（见下文）此内存区域的偏移量[VMO]（/ docs / concepts / objects / vm_object.md）|从[VMO]（/ docs / concepts / objects / vm_object.md）`大小的开始偏移。 [VMO]（/ docs / concepts / objects / vm_object.md）`addrs`中的字节总数|返回地址列表“ addrs_count” | `addrs``pmt`中元素的数量|返回的[PMT]（/ docs / concepts / objects / pinned_memory_token.md）（请参见下文）

The `addrs` parameter is a pointer to an array of `zx_paddr_t` that you supply. This is where the peripheral addresses for each page are returned into.The array is `addrs_count` elements long, and must match the count ofelements expected from[**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md). 参数addrs是指向您提供的zx_paddr_t数组的指针。这是返回每个页面的外围地址的地方。数组的长度为`addrs_count`个元素，并且必须与[** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md ）。

> The values written into `addrs` are suitable for programming the peripheral's > DMA controller &mdash; that is, they take into account any translations that> may be performed by an IOMMU, if present. >写入“ addrs”的值适用于对外设的DMA控制器进行编程。也就是说，它们考虑了IOMMU可能执行的任何翻译（如果存在）。

On a technical note, the other effect of [**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md)is that the kernel will ensure those pages are not decommitted(i.e., moved or reused) while pinned. 从技术上讲，[** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md）的另一个效果是，内核将确保固定时这些页面不会被撤消（即，移动或重用） 。

The `options` argument is actually a bitmap of options:  `options`参数实际上是选项的位图：

Option                  | Purpose ------------------------|--------------------------------`ZX_BTI_PERM_READ`      | pages can be read by the peripheral (written by the driver)`ZX_BTI_PERM_WRITE`     | pages can be written by the peripheral (read by the driver)`ZX_BTI_COMPRESS`       | (see "Minimum contiguity property," below) 选项|目的------------------------ | ------------------------ --------`ZX_BTI_PERM_READ` | ZX_BTI_PERM_WRITE` |外围设备可以读取页面（由驱动程序写入） ZX_BTI_COMPRESS` |页可以由外围设备写入（由驱动程序读取）。 （请参见下面的“最小连续性”）

For example, refer to the diagrams above showing "Device #3". If an IOMMU is present, `addrs` would contain `0`, `1`, `2`, and `3` (that is,the device-physical addresses).If no IOMMU is present, `addrs` would contain `109`, `110`, `101`, and `119` (that is,the physical addresses). 例如，请参考上面显示“设备3”的图。如果存在IOMMU，则`addrs`将包含`0`，`1，`2`和`3`（即设备物理地址）。如果不存在IOMMU，则`addrs`将包含` 109`，`110`，`101`和`119`（即物理地址）。

 
### Permissions  权限 

Keep in mind that the permissions are from the perspective *of the peripheral*, and not the driver.For example, in a block device **write** operation, the device **reads** from memory pages andtherefore the driver specifies `ZX_BTI_PERM_READ`, and vice versa in the block device read. 请记住，权限是从外围设备的角度*而不是驱动程序的角度来看的。例如，在块设备** write **操作中，设备**从内存页面读取**，因此驱动程序指定` ZX_BTI_PERM_READ`，反之亦然。

 
### Minimum contiguity property  最小连续性 

By default, each address returned through `addrs` is one page long. Larger chunks may be requested by setting the `ZX_BTI_COMPRESS` optionin the `options` argument.In that case, the length of each entry returned corresponds to the "minimum contiguity" property.While you can't set this property, you can read it via[**zx_object_get_info()**](/docs/reference/syscalls/object_get_info.md).Effectively, the minimum contiguity property is a guarantee that[**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md)will always be able to return addresses that are contiguous for at least that many bytes. 默认情况下，通过“ addrs”返回的每个地址都为一页长。可以通过在options参数中设置ZX_BTI_COMPRESS选项来请求更大的块。在这种情况下，返回的每个条目的长度都对应于“最小连续性”属性。虽然您不能设置此属性，但您可以阅读它通过[** zx_object_get_info（）**]（/ docs / reference / syscalls / object_get_info.md）。有效地，最小连续性属性是对[** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md）将始终能够返回至少连续多个字节的连续地址。

For example, if the property had the value 1MB, then a call to [**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md)with a requested size of 2MB would return at most two physically-contiguous runs.If the requested size was 2.5MB, it would return at most three physically-contiguous runs,and so on. 例如，如果属性的值为1MB，则对请求的大小为2MB的[** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md）的调用最多将返回两个物理连续的如果请求的大小为2.5MB，它将最多返回三个物理连续的运行，依此类推。

 
### Pinned Memory Token (**PMT**)  固定内存令牌（** PMT **） 

[**zx_bti_pin()**](/docs/reference/syscalls/bti_pin.md) returns a Pinned Memory Token (**[PMT](/docs/concepts/objects/pinned_memory_token.md)**)upon success in the *pmt* argument.The driver must call [**zx_pmt_unpin()**](/docs/reference/syscalls/pmt_unpin.md) when the device is done withthe memory transaction to unpin and revoke access to the memory pages by the device. [** zx_bti_pin（）**]（/ docs / reference / syscalls / bti_pin.md）成功执行后会返回固定内存令牌（** [PMT]（/ docs / concepts / objects / pinned_memory_token.md）**）。 * pmt *参数。当设备完成内存事务后，驱动程序必须调用[** zx_pmt_unpin（）**]（/ docs / reference / syscalls / pmt_unpin.md），以取消固定并撤消对内存页的访问设备。

 
## Advanced topics  进阶主题 

 
### Cache Coherency  缓存一致性 

On fully DMA-coherent architectures, hardware ensures the data in the CPU cache is the same as the data in main memory without software intervention. Not all architectures areDMA-coherent. On these systems, the driver must ensure the CPU cache is made coherent byinvoking appropriate cache operations on the memory range before performing DMA operations,so that no stale data will be accessed. 在完全DMA一致的体系结构上，硬件可确保CPU缓存中的数据与主存储器中的数据相同，而无需软件干预。并非所有体系结构都是DMA一致的。在这些系统上，驱动程序必须通过在执行DMA操作之前在内存范围内调用适当的缓存操作来确保CPU缓存是连贯的，以便不会访问过时的数据。

To invoke cache operations on the memory represented by [VMO](/docs/concepts/objects/vm_object.md)s, use the [**zx_vmo_op_range()**](/docs/reference/syscalls/vmo_op_range.md)syscall.Prior to a peripheral-read(driver-write) operation, clean the cache using `ZX_VMO_OP_CACHE_CLEAN` to write out dirtydata to main memory. Prior to a peripheral-write (driver-read), mark the cache linesas invalid using `ZX_VMO_OP_CACHE_INVALIDATE` to ensure data is fetched from mainmemory on the next access. 要在[VMO]（/ docs / concepts / objects / vm_object.md）s表示的内存上调用缓存操作，请使用[** zx_vmo_op_range（）**]（/ docs / reference / syscalls / vmo_op_range.md）syscall在执行外围设备读取（驱动程序写入）操作之前，请使用ZX_VMO_OP_CACHE_CLEAN清理高速缓存以将脏数据写出到主存储器中。在进行外设写（驱动程序读）之前，请使用ZX_VMO_OP_CACHE_INVALIDATE将高速缓存行标记为无效，以确保下次访问时从主内存中获取数据。

