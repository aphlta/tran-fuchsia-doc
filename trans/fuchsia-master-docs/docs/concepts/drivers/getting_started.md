 

 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# Getting Started  入门 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

Writing a device driver is often viewed as a daunting task, fraught with complexities and requiring arcane knowledge of little-known kernel secrets. 编写设备驱动程序通常被认为是一项艰巨的任务，充满了复杂性，并且需要对鲜为人知的内核机密的神秘知识。

The goal of this section is to demystify the process; you'll learn everything you need to know about how to write device drivers, starting with what they do, howthey work, and how they fit into the overall system. 本节的目的是使过程神秘化；您将学到所有有关如何编写设备驱动程序的知识，从它们的功能，工作原理以及它们如何适合整个系统开始。

 
## Overview  总览 

At the highest level, a device driver's job is to provide a uniform interface to a particular device, while hiding details specific to the device's implementation. 在最高级别，设备驱动程序的工作是为特定设备提供统一的接口，同时隐藏特定于设备实现的细节。

Two different ethernet drivers, for example, both allow a client to send packets out an interface, using the exact same C language function.Each driver is responsible for managing its own hardware in a way that makes theclient interfaces identical, even though the hardware is different. 例如，两个不同的以太网驱动程序都允许客户端使用完全相同的C语言功能将数据包发送出接口。每个驱动程序负责以一种使客户端接口相同的方式管理自己的硬件，即使硬件是不同。

Note that the interfaces that are provided by the driver may be "intermediate" &mdash; that is, they might not necessarily represent the "final" device in the chain. 注意，驱动程序提供的接口可以是“中间”的。也就是说，它们不一定代表链中的“最终”设备。

Consider a PCI-based ethernet device. First, a base PCI driver is required that understands how to talk to the PCI bus itself.This driver doesn't know anything about ethernet, but it does knowhow to deal with the specific PCI chipset present on the machine. 考虑一个基于PCI的以太网设备。首先，需要一个基本的PCI驱动程序，该驱动程序了解如何与PCI总线本身进行通信;该驱动程序对以太网一无所知，但确实知道如何处理计算机上存在的特定PCI芯片组。

It enumerates the devices on that bus, collects information from the various registers on each device, and provides functions that allowits clients (such as the PCI-based ethernet driver) to perform PCI operationslike allocating an interrupt or a DMA channel. 它枚举该总线上的设备，从每个设备上的各个寄存器中收集信息，并提供允许其客户端（例如基于PCI的以太网驱动程序）执行PCI操作（如分配中断或DMA通道）的功能。

Thus, this base PCI driver provides services to the ethernet driver, allowing the ethernet driver to manage its associated hardware. 因此，此基本PCI驱动程序为以太网驱动程序提供服务，从而允许以太网驱动程序管理其关联的硬件。

At the same time, other devices (such as a video card) could also use the base PCI driver in a similar manner to manage their hardware. 同时，其他设备（例如视频卡）也可以类似的方式使用基本PCI驱动程序来管理其硬件。

 
## The Zircon model  锆石模型 

In order to provide maximum flexibility, drivers in the Zircon world are allowed to bind to matching "parent" devices, and publish "children" of their own.This hierarchy extends as required: one driver might publish a child, only to haveanother driver consider that child their parent, with the second driver publishingits own children, and so on. 为了提供最大的灵活性，Zircon世界中的驱动程序被允许绑定到匹配的“父”设备，并发布其自己的“子级”。此层次结构按要求扩展：一个驱动程序可以发布一个子级，只是为了让另一个驱动程序考虑那个孩子是他们的父母，第二个司机发布自己的孩子，依此类推。

In order to understand how this works, let's follow the PCI-based ethernet example.  为了理解它是如何工作的，我们来看一个基于PCI的以太网示例。

The system starts by providing a special "PCI root" parent. Effectively, it's saying "I know that there's a PCI bus on this system, when youfind it, bind it *here*." 系统通过提供一个特殊的“ PCI root”父节点开始。实际上，这是在说：“我知道该系统上有PCI总线，当您找到它时，请在此处*绑定它。”

> The "Advanced Topics" section below has more details about this process.  >下面的“高级主题”部分提供了有关此过程的更多详细信息。

Drivers are evaluated by the system (a directory is searched), and drivers that match are automatically bound. 系统将评估驱动程序（搜索目录），并自动绑定匹配的驱动程序。

In this case, a driver that binds to a "PCI root" parent is found, and bound.  在这种情况下，找到并绑定了绑定到“ PCI root”父代的驱动程序。

This is the base PCI driver. It's job is to configure the PCI bus, and enumerate the peripherals on the bus. 这是基本的PCI驱动程序。它的工作是配置PCI总线，并枚举总线上的外围设备。

The PCI bus has specific conventions for how peripherals are identified: a combination of a Vendor ID (**VID**) and Device ID (**DID**) uniquely identifiesall possible PCI devices.During enumeration, these values are read from the peripheral, and new parentnodes are published containing the detected VID and DID (and a host of otherinformation). PCI总线具有有关如何识别外围设备的特定约定：供应商ID（** VID **）和设备ID（** DID **）的组合唯一地标识所有可能的PCI设备。在枚举期间，这些值是从外围设备，并发布包含检测到的VID和DID（以及许多其他信息）的新父节点。

Every time a new device is published, the same process as described above (for the initial PCI root device publication) repeats;that is, drivers are evaluated by the system, searching for drivers that matchup with the new parents' characteristics. 每次发布新设备时，都会重复上述步骤（用于初始PCI根设备发布）相同的过程；也就是说，驱动程序由系统评估，搜索与新父母特征匹配的驱动程序。

Whereas with the PCI root device we were searching for a driver that matched a certain kind of functionality (called a "protocol," we'll see this shortly), inthis case, however, we're searching for drivers that match a differentprotocol, namely one that satisfies the requirements of "is a PCI device andhas a given VID and DID." 鉴于使用PCI根设备，我们正在寻找与某种功能匹配的驱动程序（称为“协议”，我们很快会看到这种情况），但是在这种情况下，我们正在寻找与另一种协议匹配的驱动程序，也就是说，满足“是一个PCI设备并具有给定的VID和DID”的要求。

If a suitable driver is found (one that matches the required protocol, VID and DID), it's bound to the parent. 如果找到合适的驱动程序（与所需协议，VID和DID匹配的驱动程序），则将其绑定到父驱动程序。

As part of binding, we initialize the driver &mdash; this involves such operations as setting up the card for operation, bringing up the interface(s), andpublishing a child or children of this device.In the case of the PCI ethernet driver, it publishes the "ethernet" interface,which conforms to yet another protocol, called the "ethernet implementation" protocol.This protocol represents a common protocol that's close to the functions thatclients use (but is one step removed; we'll come back to this). 作为绑定的一部分，我们初始化驱动程序mdash；这涉及诸如操作卡的设置，调出接口以及发布该设备的一个或多个子代之类的操作。对于PCI以太网驱动程序，它将发布“ ethernet”接口，该接口符合另一种协议称为“以太网实现”协议。此协议表示一种通用协议，该协议与客户端使用的功能非常接近（但已删除了一个步骤；我们将回到此步骤）。

 
### Protocols  通讯协定 

We mentioned three protocols above:  我们在上面提到了三种协议：

 
*   the PCI root protocol (`ZX_PROTOCOL_PCIROOT`),  * PCI根协议（`ZX_PROTOCOL_PCIROOT`），
*   the PCI device protocol (`ZX_PROTOCOL_PCI`), and  * PCI设备协议（`ZX_PROTOCOL_PCI`），以及
*   the ethernet implementation protocol (`ZX_PROTOCOL_ETHERNET_IMPL`).  *以太网实现协议（`ZX_PROTOCOL_ETHERNET_IMPL`）。

The names in brackets are the C language constants corresponding to the protocols, for reference.  括号中的名称是与协议相对应的C语言常量，以供参考。

So what is a protocol?  那么什么是协议？

A protocol is a strict interface definition.  协议是严格的接口定义。

The ethernet driver published an interface that conforms to `ZX_PROTOCOL_ETHERNET_IMPL`. This means that it must provide a set of functions defined in a data structure(in this case, `ethernet_impl_protocol_ops_t`). 以太网驱动程序发布了一个符合`ZX_PROTOCOL_ETHERNET_IMPL`的接口。这意味着它必须提供在数据结构中定义的一组功能（在这种情况下，为“ ethernet_impl_protocol_ops_t”）。

These functions are common to all devices implementing the protocol &mdash; for example, all ethernet devices must provide a function that queries the MAC address of theinterface. 这些功能对于实现协议的所有设备都是通用的。例如，所有以太网设备都必须提供查询接口MAC地址的功能。

Other protocols will of course have different requirements for the functions they must provide.For example a block device will publish an interface that conforms to the"block implementation protocol" (`ZX_PROTOCOL_BLOCK_IMPL`) andprovide functions defined by `block_protocol_ops_t`.This protocol includes a function that returns the size of the device in blocks,for example. 当然其他协议对它们必须提供的功能也有不同的要求。例如，一个块设备将发布一个符合“块实现协议”（“ ZX_PROTOCOL_BLOCK_IMPL”）的接口，并提供由“ block_protocol_ops_t”定义的功能。该协议包括一个例如，以块为单位返回设备大小的函数。

We'll examine these protocols in the following chapters.  我们将在接下来的章节中研究这些协议。

 
# Advanced Topics  进阶主题 

The above has presented a big picture view of Zircon drivers, with a focus on protocols.  上面展示了Zircon驱动程序的概况，重点是协议。

In this section, we'll examine some advanced topics, such as platform dependent and platform independent code decoupling,the "miscellaneous" protocol, and how protocols and processes are mapped. 在本节中，我们将研究一些高级主题，例如与平台有关和与平台无关的代码去耦，“杂项”协议以及如何映射协议和过程。

 
## Platform dependent vs platform independent  与平台有关vs与平台无关 

Above, we mentioned that `ZX_PROTOCOL_ETHERNET_IMPL` was "close to" the functions used by the client, but one step removed.That's because there's one more protocol, `ZX_PROTOCOL_ETHERNET`, that sits betweenthe client and the driver.This additional protocol is in place to handle functionality common to all ethernetdrivers (in order to avoid code duplication).Such functionality includes buffer management, status reporting, and administrativefunctions. 上面我们提到，“ ZX_PROTOCOL_ETHERNET_IMPL”与客户端使用的功能“接近”，但是删除了一个步骤，这是因为在客户端和驱动程序之间还有一个协议“ ZX_PROTOCOL_ETHERNET”。处理所有以太网驱动程序共有的功能（以避免代码重复）。此类功能包括缓冲区管理，状态报告和管理功能。

This is effectively a "platform dependent" vs "platform independent" decoupling; common code exists in the platform independent part (once), and driver-specific codeis implemented in the platform dependent part. 这实际上是“与平台无关”与“与平台无关”的解耦。平台独立部分（一次）中存在通用代码，而平台独立部分中实现了特定于驱动程序的代码。

This architecture is repeated in multiple places. With block devices, for example, the hardware driver binds to the bus (e.g., PCI)and provides a `ZX_PROTOCOL_BLOCK_IMPL` protocol.The platform independent driver binds to `ZX_PROTOCOL_BLOCK_IMPL`, and publishes theclient-facing protocol, `ZX_PROTOCOL_BLOCK`. 此架构在多个地方重复。例如，对于块设备，硬件驱动程序绑定到总线（例如PCI）并提供`ZX_PROTOCOL_BLOCK_IMPL`协议。平台无关的驱动程序绑定到`ZX_PROTOCOL_BLOCK_IMPL`，并发布面向客户端的协议`ZX_PROTOCOL_BLOCK`。

You'll also see this with the display controllers, I<sup>2</sup>C bus, and serial drivers.  您还将在显示控制器，I <sup> 2 </ sup> C总线和串行驱动程序中看到这一点。

 
## Miscellaneous protocol  杂项协议 

In [simple drivers](simple.md), we show the code for several drivers that illustrate basic functionality, but don't provide services related to a specific protocol(i.e., they are not "ethernet" or "block" devices).These drivers are bound to `ZX_PROTOCOL_MISC_PARENT`. 在[简单驱动程序]（simple.md）中，我们显示了几个驱动程序的代码，这些代码说明了基本功能，但是不提供与特定协议相关的服务（即，它们不是“以太网”或“块”设备）。这些驱动程序绑定到“ ZX_PROTOCOL_MISC_PARENT”。

> @@@ More content?  > @@@更多内容？

 
## Process / protocol mapping  流程/协议映射 

In order to keep the discussions above simple, we didn't talk about process separation as it relates to the drivers.To understand the issues, let's see how other operating systems deal with them,and compare that to the Zircon approach. 为了使上面的讨论保持简单，我们没有讨论与驱动程序相关的进程分离。要了解这些问题，让我们看看其他操作系统如何处理它们，并将其与Zircon方法进行比较。

In a monolithic kernel, such as Linux, many drivers are implemented within the kernel. This means that they share the same address space, and effectively live in the same"process." 在单片内核（例如Linux）中，许多驱动程序是在内核中实现的。这意味着它们共享相同的地址空间，并有效地存在于相同的“进程”中。

The major problem with this approach is fault isolation / exploitation. A bad driver can take out the entire kernel, because it lives in the same addressspace and thus has privileged access to all kernel memory and resources.A compromised driver can present a security threat for the same reason. 这种方法的主要问题是故障隔离/利用。错误的驱动程序会占用整个内核，因为它位于相同的地址空间中，因此具有对所有内核内存和资源的特权访问。受到破坏的驱动程序可能出于相同的原因而构成安全威胁。

The other extreme, that is, putting each and every driver service into its own process, is used by some microkernel operating systems.Its major drawback is that if one driver relies on the services of another driver,the kernel must effect at least a context switch operation (if not a data transferas well) between the two driver processes.While microkernel operating systems are usually designed to be fast at thesekinds of operations, performing them at high frequency is undesirable. 另一个极端，就是将每个驱动程序服务放入自己的进程中，已由某些微内核操作系统使用。其主要缺点是，如果一个驱动程序依赖于另一个驱动程序的服务，则内核必须至少影响上下文在两个驱动程序进程之间切换操作（如果不能很好地进行数据传输）。尽管通常将微内核操作系统设计为在这类操作中速度较快，但不希望以很高的频率执行它们。

The approach taken by Zircon is based on the concept of a device host (**devhost**). A devhost is a process that contains a protocol stack &mdash; that is, one ormore protocols that work together.The devhost loads drivers from ELF shared libraries (called Dynamic Shared Objects,or **DSO**s).In the [simple drivers](simple.md) section, we'll see the meta informationthat's contained in the DSO to facilitate the discovery process. Zircon采取的方法基于设备主机（** devhost **）的概念。 devhost是一个包含协议堆栈mdash的进程。也就是说，一种或多种协议可以协同工作。devhost从ELF共享库（称为动态共享对象，或** DSO **）加载驱动程序。在[简单驱动程序]（simple.md）部分，我们将看到DSO中包含的元信息以促进发现过程。

The protocol stack effectively allows the creation of a complete "driver" for a device, consisting of platform dependent and platform independent components,in a self-contained process container. 协议栈有效地允许在独立的过程容器中为设备创建一个完整的“驱动程序”，该驱动程序包括与平台有关和与平台无关的组件。

For the advanced reader, take a look at the `dm dump` command available from the Zircon command line.It displays a tree of devices, and shows you the process ID, DSO name, andother useful information. 对于高级阅读器，请查看Zircon命令行中提供的``dm dump''命令，该命令显示一棵设备树，并向您显示进程ID，DSO名称和其他有用信息。

Here's a highly-edited version showing just the PCI ethernet driver parts:  这是一个高度编辑的版本，仅显示PCI以太网驱动程序部分：

```
1. [root]
2.    [sys]
3.       <sys> pid=1416 /boot/driver/bus-acpi.so
4.          [acpi] pid=1416 /boot/driver/bus-acpi.so
5.          [pci] pid=1416 /boot/driver/bus-acpi.so
            ...
6.             [00:02:00] pid=1416 /boot/driver/bus-pci.so
7.                <00:02:00> pid=2052 /boot/driver/bus-pci.proxy.so
8.                   [intel-ethernet] pid=2052 /boot/driver/intel-ethernet.so
9.                      [ethernet] pid=2052 /boot/driver/ethernet.so
```
 

From the above, you can see that process ID `1416` (lines 3 through 6) is the Advanced Configuration and Power Interface (**ACPI**) driver, implementedby the DSO `bus-acpi.so`. 从上面可以看到，进程ID“ 1416”（第3行到第6行）是高级配置和电源接口（** ACPI **）驱动程序，由DSO`bus-acpi.so`实现。

During primary enumeration, the ACPI DSO detected a PCI bus. This caused the publication of a parent with `ZX_PROTOCOL_PCI_ROOT` (line 5,causing the appearance of the `[pci]` entry),which then caused the devhost to load the `bus-pci.so` DSO and bind to it.That DSO is the "base PCI driver" to which we've been referring throughout thediscussions above. 在主要枚举期间，ACPI DSO检测到PCI总线。这导致发布带有ZX_PROTOCOL_PCI_ROOT的父对象（第5行，导致[pci]条目的出现），然后导致devhost加载“ bus-pci.so” DSO并绑定到它。在上面的整个讨论中，DSO是“基本PCI驱动程序”。

During its binding, the base PCI driver enumerated the PCI bus, and found an ethernet card (line 6 detects bus 0, device 2, function 0, shown as `[00:02:00]`).(Of course, many other devices were found as well, but we've removed them fromthe above listing for simplicity). 在绑定期间，基本PCI驱动程序枚举了PCI总线，并找到了一个以太网卡（第6行检测到总线0，设备2，功能0，显示为“ [00:02:00]”）。（当然，还有许多其他还找到了设备，但为简单起见，我们将它们从上面的清单中删除了）。

The detection of this device then caused the base PCI driver to publish a new parent with `ZX_PROTOCOL_PCI` and the device's VID and DID.Additionally, a new devhost (process ID `2052`) was created and loaded with the`bus-pci.proxy.so` DSO (line 7).This proxy serves as the interface from the new devhost (pid `2052`) to the base PCIdriver (pid `1416`). 然后对该设备的检测导致基本PCI驱动程序使用`ZX_PROTOCOL_PCI`和该设备的VID和DID发布了一个新的父对象。此外，还创建了一个新的devhost（进程ID为`2052`）并加载了`bus-pci'。 DSO（第7行）。此代理用作从新devhost（pid“ 2052`”）到基本PCIdriver（pid“ 1416`）的接口。

> This is where the decision was made to "sever" the device driver into its own > process &mdash; the new devhost and the base PCI driver now live in two> different processes. >此处决定将设备驱动程序“分离”到自己的进程中。现在，新的devhost和基础PCI驱动程序位于两个不同的进程中。

The new devhost `2052` then finds a matching child (the `intel-ethernet.so` DSO on line 8; it's considered a match because it has `ZX_PROTOCOL_PCI` and the correctVID and DID).That DSO publishes a `ZX_PROTOCOL_ETHERNET_IMPL`, which binds to a matchingchild (the `ethernet.so` DSO on line 9; it's considered a match because it has a`ZX_PROTOCOL_ETHERNET_IMPL` protocol). 然后，新的devhost`2052`找到一个匹配的子对象（第8行上的`intel-ethernet.so` DSO;由于具有`ZX_PROTOCOL_PCI`和正确的VID和DID，因此被认为是匹配的）.DSO发布了`ZX_PROTOCOL_ETHERNET_IMPL'，绑定到matchingchild（第9行的“ ethernet.so” DSO；被视为匹配项，因为它具有“ ZX_PROTOCOL_ETHERNET_IMPL”协议）。

What's not shown by this chain is that the final DSO (`ethernet.so`) publishes a `ZX_PROTOCOL_ETHERNET` &mdash; that's the piece that clients can use, so ofcourse there's no further "device" binding involved. 该链未显示的是最终DSO（`ethernet.so`）发布了“ ZX_PROTOCOL_ETHERNET” mdash；这是客户可以使用的部分，因此当然不涉及其他“设备”绑定。

 

