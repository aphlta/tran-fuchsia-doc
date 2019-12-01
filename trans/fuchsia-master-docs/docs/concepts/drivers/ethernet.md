 

 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# Ethernet Devices  以太网设备 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

 
## Overview  总览 

This chapter looks into the details of ethernet drivers, using the Intel driver code for specific examples. 本章使用特定示例的英特尔驱动程序代码来研究以太网驱动程序的详细信息。

In order to handle ethernet devices, two distinct parts are involved. A "top half" driver handles the generic ethernet protocol, and is located in`//zircon/system/dev/ethernet/ethernet/ethernet.c` (yes, three "ethernets" in a row),and one or more "bottom half" drivers handle the actual devices, located onedirectory higher in `//zircon/system/dev/ethernet/`**_devicename_**`/`. 为了处理以太网设备，涉及两个不同的部分。 “上半部分”驱动程序处理通用以太网协议，位于//zircon/system/dev/ethernet/ethernet/ethernet.c（是的，连续三个“以太网”），并且一个或多个“下半部分”驱动程序处理实际设备，位于“ // zircon / system / dev / ethernet /`** _ devicename _ **`/”中的较高目录中。

Multiple Zircon IPC protocols are used for communication between modules.  多个Zircon IPC协议用于模块之间的通信。

> We'll just use the term "protocol" to refer to these. > Granted, we *are* discussing an Ethernet driver, but since we won't be> discussing any of the on-wire communications protocols supported by the driver,> this usage shouldn't result in any confusion.>> @@@ I hope. >我们仅使用术语“协议”来指代这些。 >当然，我们正在*在讨论以太网驱动程序，但是由于我们不会>在讨论该驱动程序支持的任何在线通信协议，所以这种用法不会造成任何混乱。>> @@@我希望。

 

The top half provides a protocol interface that conforms to `ZX_PROTOCOL_ETHERNET_IMPL`. The bottom half provides a protocol interface that conforms to whatever thehardware is connected to (for example, this might be `ZX_PROTOCOL_PCI`, forPCI-based ethernet cards, or `ZX_PROTOCOL_USB` for USB-based ethernet devices,and so on).We'll focus on the PCI version here. 上半部分提供符合`ZX_PROTOCOL_ETHERNET_IMPL`的协议接口。下半部分提供了一个协议接口，该接口符合所连接的任何硬件（例如，对于基于PCI的以太网卡来说可能是ZX_PROTOCOL_PCI，对于基于USB的以太网设备来说可能是ZX_PROTOCOL_USB，等等）。这里将重点介绍PCI版本。

The bottom half drivers all expose a `ZX_PROTOCOL_ETHERNET_IMPL` binding, which is how the top half finds the bottom halves. 下半部分的驱动程序都公开了ZX_PROTOCOL_ETHERNET_IMPL绑定，这是上半部分找到下半部分的方式。

Effectively, the bottom half ethernet driver is responsible for managing the hardware associated with the ethernet device, and presenting a consistent abstraction of thathardware for use by the top half.The top half manages the ethernet interface to the system. 实际上，下半部分的以太网驱动程序负责管理与以太网设备相关联的硬件，并提​​供该硬件的一致抽象，以供上半部分使用。上半部分管理系统的以太网接口。

![Figure: Relationship amongst layers in ethernet driver stack](ethernet-000-cropped.png)  ！[图：以太网驱动程序堆栈中各层之间的关系]（ethernet-000-cropped.png）

> @@@ this diagram: helpful? too busy? font too small?  > @@@此图：有用吗？太忙了？字体太小？

 
# Intel PCI-based ethernet  基于Intel PCI的以太网 

The Intel ethernet driver can be found in `//zircon/system/dev/ethernet/intel-ethernet`, and consists of the following files: 可以在`// zircon / system / dev / ethernet / intel-ethernet`中找到英特尔以太网驱动程序，它包含以下文件：

<dl> <dt>`ethernet.c`<dd>The device driver part of the code; handles interface to protocols.<dt>`ie.c`<dd>The Intel specific part of the code; knows about the hardware registers on the card.<dt>`ie-hw.h`<dd>Contains the manifest constants for all of the control registers.<dt>`ie.h`<dd>Common definitions (such as the device context block)</dl> <dl> <dt>`ethernet.c` <dd>代码的设备驱动程序部分； <dt>`ie.c` <dd>代码的英特尔特定部分；知道卡上的硬件寄存器。<dt>`ie-hw.h` <dd>包含所有控制寄存器的清单清单常量。<dt>`ie.h` <dd>通用定义（例如设备上下文块）</ dl>

This driver not only handles the `ethmac` protocol, but also:  这个驱动程序不仅处理`ethmac`协议，而且：

 
*   finds its device on the PCI bus,  *在PCI总线上找到其设备，
*   attaches to legacy or Message Signaled Interrupts (**MSI**),  *附加到旧版或消息信号中断（** MSI **），
*   maps I/O memory, and  *映射I / O内存，并且
*   creates a background IRQ handling thread.  *创建一个后台IRQ处理线程。

 
## Binding  捆绑 

The file `ethernet.c` contains the binding information, implemented by the standard binding macros introduced in the [Simple Drivers](simple.md) chapter: 文件ethernet.c包含绑定信息，该信息由[简单驱动程序]（simple.md）一章中介绍的标准绑定宏实现：

```c
ZIRCON_DRIVER_BEGIN(intel_ethernet, intel_ethernet_driver_ops, "zircon", "0.1", 11)
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_PCI),
    BI_ABORT_IF(NE, BIND_PCI_VID, 0x8086),
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x100E), // Qemu
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15A3), // Broadwell
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x1570), // Skylake
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x1533), // I210 standalone
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x1539), // I211-AT
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x156f), // I219-LM (Dawson Canyon NUC)
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15b7), // Skull Canyon NUC
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15b8), // I219-V
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15d8), // Kaby Lake NUC
ZIRCON_DRIVER_END(intel_ethernet)
```
 

This ends up binding to ethernet cards that are identified by vendor ID `0x8086` (Intel), and have any of the listed device IDs (the `BIND_PCI_DID` lines indicate the allowedhexadecimal device IDs).It also requires the `ZX_PROTOCOL_PCI` protocol. 这最终绑定到由供应商ID'0x8086'（Intel）标识的以太网卡，并具有列出的任何设备ID（'BIND_PCI_DID'行表示允许的十六进制设备ID），并且还需要`ZX_PROTOCOL_PCI`协议。

Note the sense of the logic here &mdash; the vendor ID is tested with a "`BI_ABORT_IF(NE`" construct (meaning, "**ABORT IF** the values are **N**ot **E**qual"),whereas the device IDs are tested with "`BI_MATCH_IF(EQ`" constructs (meaning "**MATCHIF** the values are **EQ**ual"). 注意这里的逻辑意义。使用“`BI_ABORT_IF（NE`””结构（即，“ ** ABORT IF **值是** N ** ot ** E ** qual”）测试供应商ID，而设备ID则使用“`BI_MATCH_IF（EQ`””构造（意味着“ ** MATCHIF **值是** EQ ** ual”）。

Intuitively, you might think that the vendor ID could be tested with a "`BI_MATCH_IF(EQ`" as well, (looking for vendor `0x8086`), but this would have two major problems.First, evaluation stops as soon as a condition is true, so that means that **any** devicethat had the Intel vendor ID would be considered a "match."Second, even if the device wasn't an Intel vendor ID, it would open the possibilityof allowing matches to other vendors' devices that had the same device ID as listed. 凭直觉，您可能会认为也可以使用“ BI_MATCH_IF（EQ`）”来测试供应商ID（寻找供应商“ 0x8086”），但这将有两个主要问题。首先，评估一旦条件终止是正确的，因此这意味着具有英特尔供应商ID的任何设备都将被视为“匹配项”。其次，即使该设备不是英特尔供应商ID，也可能允许与其他供应商进行匹配具有与所列相同设备ID的设备。

> The individual tests are evaluated in sequence. > The first one that's true terminates evaluation, and performs> the given action (i.e., `ABORT` or `MATCH`). >依次评估各个测试。 >第一个为真的终止评估，并执行给定的动作（即“ ABORT”或“ MATCH”）。

 
## More about binding  有关绑定的更多信息 

From the command line, `dm drivers` will display this information. Here's the relevant portion for the Intel ethernet driver: 从命令行，“ dm drivers”将显示此信息。这是英特尔以太网驱动程序的相关部分：

```sh
$ dm drivers
<snip>
    Name    : intel_ethernet
    Driver  : /boot/driver/intel-ethernet.so
    Flags   : 0x00000000
    Binding : 11 instructions (88 bytes)
    [1/11]: if (Protocol != 0x70504349) return no-match;
    [2/11]: if (PCI.VID != 0x00008086) return no-match;
    [3/11]: if (PCI.DID == 0x0000100e) return match;
    [4/11]: if (PCI.DID == 0x000015a3) return match;
    [5/11]: if (PCI.DID == 0x00001570) return match;
    [6/11]: if (PCI.DID == 0x00001533) return match;
    [7/11]: if (PCI.DID == 0x00001539) return match;
    [8/11]: if (PCI.DID == 0x0000156f) return match;
    [9/11]: if (PCI.DID == 0x000015b7) return match;
    [10/11]: if (PCI.DID == 0x000015b8) return match;
    [11/11]: if (PCI.DID == 0x000015d8) return match;
```
 

The `Name` field indicates the name of the driver, given as the first argument to the `ZIRCON_DRIVER_BEGIN` and `ZIRCON_DRIVER_END` macros.The `Driver` field indicates the location of the shared object that contains the driver code. Name字段表示驱动程序的名称，它是ZIRCON_DRIVER_BEGIN和ZIRCON_DRIVER_END宏的第一个参数。Driver字段表示包含驱动程序代码的共享库的位置。

> The `Flags` field is not used @@@ correct?  > @ @ @ @ @ @ @ @ @ @是否正确？

The last section, the binding instructions, corresponds with the `BI_ABORT_IF` and `BI_MATCH_IF` macro directives.Note that the first binding instruction compares the field `Protocol` against the hexadecimalnumber `0x70504349` &mdash; that "number" is simply the ASCII encoding of the string "`pPCI`",indicating the PCI protocol (you can see all of the encodings in`//zircon/system/ulib/ddk/include/ddk/protodefs.h`) 最后一部分，绑定指令，对应于BI_ABORT_IF和BI_MATCH_IF宏指令。该“数字”只是字符串“`pPCI`”的ASCII编码，表示PCI协议（您可以在`// zircon / system / ulib / ddk / include / ddk / protodefs.h`中查看所有编码。 ）

From the `ZIRCON_DRIVER_BEGIN` macro, the `intel_ethernet_driver_ops` structure contains the driver operations, in this case just the binding function**eth_bind()**. 在“ ZIRCON_DRIVER_BEGIN”宏中，“ intel_ethernet_driver_ops”结构包含驱动程序操作，在这种情况下，仅包含绑定功能** eth_bind（）**。

Let's turn our attention to the binding function itself.  让我们将注意力转向绑定函数本身。

 
## PCI interface  PCI接口 

The first part of the binding function deals with the PCI interface.  绑定功能的第一部分处理PCI接口。

The Intel ethernet driver is a PCI bus peripheral. As such, it needs to first query the PCI configuration registers in order to discoverwhere the BIOS (or other startup program) has located the device in memoryaddress space, and what interrupt it was assigned.Second, it needs to initialize the device for use (such as mapping the configurationregisters and attaching to the device's interrupt).We broadly discussed this in the [Hardware Interfacing](hardware.md) chapter. 英特尔以太网驱动程序是PCI总线外围设备。因此，它需要首先查询PCI配置寄存器，以发现BIOS（或其他启动程序）将设备放置在内存地址空间中的位置以及分配给它的中断是什么;其次，需要初始化设备以使用（例如映射配置寄存器并附加到设备的中断）。我们在[硬件接口]（hardware.md）一章中对此进行了广泛的讨论。

As usual, the binding function allocates and initializes a context block:  与往常一样，绑定函数分配并初始化上下文块：

```c
static zx_status_t eth_bind(void* ctx, zx_device_t* dev) {
    ethernet_device_t* edev;
    if ((edev = calloc(1, sizeof(ethernet_device_t))) == NULL) {
        return ZX_ERR_NO_MEMORY;
    }
    mtx_init(&edev->lock, mtx_plain);
    mtx_init(&edev->eth.send_lock, mtx_plain);
```
 

This allocates a zeroed ethernet context block (`ethernet_device_t`). Then we initialize two mutexes (one for locking the device itself (`edev->lock`), and onefor locking the ethernet send buffers (`edev->eth.send_lock`)). 这分配了一个归零的以太网上下文块（“ ethernet_device_t”）。然后我们初始化两个互斥锁（一个用于锁定设备本身（edev-> lock），另一个用于锁定以太网发送缓冲区（edev-> eth.send_lock））。

We'll examine the context block in more detail below.  我们将在下面更详细地检查上下文块。

 
### PCI protocol operations  PCI协议操作 

The next step fetches the PCI protocol operations pointer (or fails if it can't):  下一步获取PCI协议操作指针（如果不能，则失败）：

```c
    if (device_get_protocol(dev, ZX_PROTOCOL_PCI, &edev->pci)) {
        printf("no pci protocol\n");
        goto fail;
    }
```
 

This populates `edev->pci` (of type `pci_protocol_t`) with pointers to functions that provide PCI protocol services.Of the many functions available, we use the following subset (listed in order ofuse in the binding function): 这将使用指向提供PCI协议服务的函数的指针填充edev-> pci（类型为pci_protocol_t），在可用的许多函数中，我们使用以下子集（在绑定函数中按使用顺序列出）：

Function            | Description --------------------|------------------------------------------------------------------------------`get_bti`           | Used to get the Bus Transaction Initiator (**[BTI](/docs/concepts/objects/bus_transaction_initiator.md)**) for the device`query_irq_mode`    | Returns the number of the specific type of IRQ available (MSI or legacy)`set_irq_mode`      | Requests the specified IRQ mode to be used for the device`map_interrupt`     | Creates an IRQ handle associated with the device's interrupt`map_bar`           | Returns a pointer to the Base Address Register (**BAR**) of the PCI device`enable_bus_master` | Enables / disables bus mastering for the device 功能介绍说明-------------------- | ---------------------------- -------------------------------------------------- `get_bti` |用于获取设备`query_irq_mode` |的公交交易启动器（** [BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）**）。返回特定类型的可用IRQ的数量（MSI或旧版）。请求指定的IRQ模式用于设备“ map_interrupt” |创建一个与设备的中断map_bar相关的IRQ句柄。返回指向PCI设备enable_bus_master的基址寄存器（** BAR **）的指针。启用/禁用设备的总线主控

> Note that the function names given in the table above are the member names within > the `pci_protocol_t` structure; throughout the code we'll use the **pci_...()** accessor> functions to call the protocol ops. >注意，上表中给出的函数名称是`pci_protocol_t`结构中的成员名称；在整个代码中，我们将使用** pci _...（）** accessor>函数来调用协议操作。

 
### Fetch the BTI  取得BTI 

The first PCI function we call is **pci_get_bti()**: 我们调用的第一个PCI函数是** pci_get_bti（）**：

```c
    zx_status_t status = pci_get_bti(&edev->pci, 0, &edev->btih);
    if (status != ZX_OK) {
        goto fail;
    }
```
 

A [BTI](/docs/concepts/objects/bus_transaction_initiator.md) is used to represent the bus mastering / DMA capability of a device.It can be used for granting memory access to a device.The [BTI](/docs/concepts/objects/bus_transaction_initiator.md)handle is stored in `edev->btih` and is used later to initialize transfer buffers.The [Hardware Interfacing](hardware.md) chapter talks more about this, in the DMA section. [BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）用于表示设备的总线主控/ DMA功能。它可用于授予对设备的内存访问权限。[BTI]（/ docs / concept / objects / bus_transaction_initiator.md）句柄存储在`edev-> btih`中，以后用于初始化传输缓冲区。[Hardware Interface]（hardware.md）一章在DMA部分中对此进行了更多讨论。

 
### Discover and map interrupts  发现和映射中断 

The interrupt is discovered and mapped next:  发现中断，然后映射：

```c
    // Query whether we have MSI or Legacy interrupts.
    uint32_t irq_cnt = 0;
    if ((pci_query_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_MSI, &irq_cnt) == ZX_OK) &&
        (pci_set_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_MSI, 1) == ZX_OK)) {
        printf("eth: using MSI mode\n");
    } else if ((pci_query_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_LEGACY, &irq_cnt) == ZX_OK) &&
               (pci_set_irq_mode(&edev->pci, ZX_PCIE_IRQ_MODE_LEGACY, 1) == ZX_OK)) {
        printf("eth: using legacy irq mode\n");
    } else {
        printf("eth: failed to configure irqs\n");
        goto fail;
    }

    zx_status_t r = pci_map_interrupt(&edev->pci, 0, &edev->irqh);
    if (r != ZX_OK) {
        printf("eth: failed to map irq\n");
        goto fail;
    }
```
 

The **pci_query_irq_mode()** function determines if the device supports any `MSI` or `LEGACY`style interrupts, and returns the count (in `irq_cnt`).We're expecting one interrupt, so we ignore the count and examine just the return status.If the return status indicates one or more interrupts of that type exist, we set the device touse that mode. ** pci_query_irq_mode（）**函数确定设备是否支持任何MSI或LEGACY样式的中断，并返回计数（在irq_cnt中）。我们期望一个中断，因此我们忽略该计数并检查如果返回状态表明存在一个或多个该类型的中断，则将设备设置为使用该模式。

The **pci_map_interrupt()** function is then used to bind the hardware interrupt to a handle, stored in `edev->irqh`. 然后使用** pci_map_interrupt（）**函数将硬件中断绑定到存储在`edev-> irqh`中的句柄。

We'll see this handle later, when we look at the interrupt service thread.  稍后我们将在查看中断服务线程时看到该句柄。

 
### Map PCI BAR  映射PCI BAR 

Next up, we map the PCI BAR:  接下来，我们映射PCI BAR：

```c
    // map iomem
    uint64_t sz;
    zx_handle_t h;
    void* io;
    r = pci_map_bar(&edev->pci, 0u, ZX_CACHE_POLICY_UNCACHED_DEVICE, &io, &sz, &h);
    if (r != ZX_OK) {
        printf("eth: cannot map io %d\n", h);
        goto fail;
    }
    edev->eth.iobase = (uintptr_t)io;
    edev->ioh = h;

    if ((r = pci_enable_bus_master(&edev->pci, true)) < 0) {
        printf("eth: cannot enable bus master %d\n", r);
        goto fail;
    }
```
 

The call to **pci_map_bar()** creates a handle to the first BAR (the `0u` as the second argumentspecifies the BAR ID number), which we store into the context block's `ioh` member.(We also capture the virtual address into `edev->eth.iobase`.) 对** pci_map_bar（）**的调用会创建第一个BAR的句柄（第二个参数指定BAR ID号为“ 0u”，我们将其存储在上下文块的ioh成员中）（我们还将捕获虚拟地址到edev-> eth.iobase中。）

 
### Ethernet setup and configuration  以太网设置和配置 

At this point, we have access to enough of the device that we can go and set it up:  至此，我们可以使用足够的设备进行设置：

```c
    if (eth_enable_phy(&edev->eth) != ZX_OK) {
        goto fail;
    }

    if (eth_reset_hw(&edev->eth)) {
        goto fail;
    }
```
 

The implementation of **eth_enable_phy()** and **eth_reset_hw()** is in the `ie.c` file. eth_enable_phy（）**和eth_reset_hw（）**的实现位于ie.c文件中。

 
### DMA buffer setup and hardware configuration  DMA缓冲区设置和硬件配置 

With the device configured, we can now set up the DMA buffers. Here we see the [BTI](/docs/concepts/objects/bus_transaction_initiator.md)handle, `edev->btih`, that we set up above, as the 2nd argument to**io_buffer_init()**: 配置完设备后，我们现在可以设置DMA缓冲区。在这里，我们看到上面设置的[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）句柄edev-> btih作为io_buffer_init（）**的第二个参数：

```c

    r = io_buffer_init(&edev->buffer, edev->btih, ETH_ALLOC, IO_BUFFER_RW | IO_BUFFER_CONTIG);
    if (r < 0) {
        printf("eth: cannot alloc io-buffer %d\n", r);
        goto fail;
    }

    eth_setup_buffers(&edev->eth, io_buffer_virt(&edev->buffer), io_buffer_phys(&edev->buffer));
    eth_init_hw(&edev->eth);
```
 

The **io_buffer_init()** function zeroes the buffer, and creates a [VMO](/docs/concepts/objects/vm_object.md)handle to the [BTI](/docs/concepts/objects/bus_transaction_initiator.md).The **eth_setup_buffers()** and **eth_init_hw()** functions are defined in the `ie.c` module. io_buffer_init（）函数将缓冲区清零，并为[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）创建一个[VMO]（/ docs / concepts / objects / vm_object.md）句柄。 eth_setup_buffers（）**和eth_init_hw（）**函数在ie.c模块中定义。

 
### Final driver binding  最终驱动程序绑定 

The next part binds the device name ("`intel-ethernet`"), context block (`edev`, allocated above), device operations (`device_ops`, which supports suspend, resume, and release),and the additional optional protocol ops for ethernet (identified as `ZX_PROTOCOL_ETHERNET_IMPL`and contained in `ethernet_impl_ops`): 下一部分绑定设备名称（“ intel-ethernet”），上下文块（“ edev”，上面已分配），设备操作（“ device_ops”，它支持挂起，恢复和释放）以及附加的可选协议以太网的操作（标识为“ ZX_PROTOCOL_ETHERNET_IMPL”，包含在“ ethernet_impl_ops”中）：

```c
    device_add_args_t args = {
        .version = DEVICE_ADD_ARGS_VERSION,
        .name = "intel-ethernet",
        .ctx = edev,
        .ops = &device_ops,
        .proto_id = ZX_PROTOCOL_ETHERNET_IMPL,
        .proto_ops = &ethernet_impl_ops,
    };

    if (device_add(dev, &args, &edev->zxdev)) {
        goto fail;
    }
```
 

 
### Interrupt thread creation  中断线程创建 

Finally, the background Interrupt Handling Thread (**IHT**), **irq_thread()** is created:  最后，创建了后台中断处理线程（** IHT **），** irq_thread（）**：

```c
    thrd_create_with_name(&edev->thread, irq_thread, edev, "eth-irq-thread");
    thrd_detach(edev->thread);

    printf("eth: intel-ethernet online\n");

    return ZX_OK;
```
 

As discussed in the [Hardware Interfacing](hardware.md) chapter, the IHT handles asynchronous hardware events.We'll look at the thread itself below. 如[硬件接口]（hardware.md）一章中所述，IHT处理异步硬件事件。我们将在下面查看线程本身。

 
### Failure handling  故障处理 

In case of failure, the `fail` label is the target of various `goto`s within the code, and is responsible for cleanup of allocated resources as well as returning a failure code to the caller: 万一失败，`fail`标签是代码中各种`goto`的目标，并负责清除分配的资源以及将失败代码返回给调用者：

```c
fail:
    io_buffer_release(&edev->buffer);
    if (edev->btih) {
        zx_handle_close(edev->btih);
    }
    if (edev->ioh) {
        pci_enable_bus_master(&edev->pci, false);
        zx_handle_close(edev->irqh);
        zx_handle_close(edev->ioh);
    }
    free(edev);
    return ZX_ERR_NOT_SUPPORTED;
}
```
 

That concludes the discussion of the binding function.  到此结束了对绑定功能的讨论。

 
## The context structure  上下文结构 

At this point, we can circle back and take a look at the context structure:  在这一点上，我们可以回头看看上下文结构：

```c
typedef struct ethernet_device {
    ethdev_t        eth;
    mtx_t           lock;
    eth_state       state;
    zx_device_t*    zxdev;
    pci_protocol_t  pci;
    zx_handle_t     ioh;
    zx_handle_t     irqh;
    thrd_t          thread;
    zx_handle_t     btih;
    io_buffer_t     buffer;
    bool            online;

    // callback interface to attached ethernet layer
    ethernet_ifc_t*   ifc;
    void*           cookie;
} ethernet_device_t;
```
 

It holds all of the context for the ethernet devices.  它保存了以太网设备的所有上下文。

> @@@ How much discussion do we want of the context block members?  > @@@我们希望对上下文块成员进行多少讨论？

 
## Ethernet protocol operations  以太网协议操作 

Recall from the discussion around the binding function **eth_bind()**that we bound an `ethernet_impl_protocol_ops_t` structure called`ethernet_impl_ops` to the driver.This structure provides the following "bottom-half" ethernet driver protocol operationsfor the Intel driver: 回想一下关于绑定函数eth_bind（）的讨论，我们将名为ethernet_impl_ops的ethernet_impl_protocol_ops_t结构绑定到了驱动程序。该结构为Intel驱动程序提供了以下“下半”以太网驱动程序协议操作：

```c
static ethernet_impl_protocol_ops_t ethernet_impl_ops = {
    .query = eth_query,
    .stop = eth_stop,
    .start = eth_start,
    .queue_tx = eth_queue_tx,
    .set_param = eth_set_param,
//  .get_bti not supported
};
```
 

We examine each in turn below.  我们下面依次检查每个。

 
### Ethernet protocol: **query()**  以太网协议：** query（）** 

The **query()** function takes three parameters: a context block, an options specifier, and a pointer toan `ethernet_info_t` where the information should be stored. query（）函数具有三个参数：上下文块，选项说明符和指向应在其中存储信息的“ ethernet_info_t”的指针。

> Note that at the present time, there are no options defined; therefore, the driver > should return `ZX_ERR_INVALID_ARGS` in case of a non-zero value. >请注意，目前尚未定义任何选项。因此，在非零值的情况下，驱动程序>应该返回ZX_ERR_INVALID_ARGS。

The `ethernet_info_t` structure is defined as follows (reserved fields omitted for clarity):  “ ethernet_info_t”结构的定义如下（为清楚起见，省略了保留字段）：

```c
typedef struct ethernet_info {
    uint32_t    features;
    uint32_t    mtu;
    uint8_t     mac[ETH_MAC_SIZE];
} ethernet_info_t;
```
 

The `mtu` field contains the Maximum Transmission Unit (**MTU**) size that the driver can support.A common value is `1500`. mtu字段包含驱动程序可以支持的最大传输单位（** MTU **）大小。常见值为1500。

The `mac` field contains `ETH_MAC_SIZE` (6 bytes) worth of Media Access Control (**MAC**) address in big-endian order (that is, for a MAC of `01:23:45:67:89:ab`, the value of`mac[0]` is `0x01`). “ mac”字段包含按大端顺序排列的“ ETH_MAC_SIZE”（6个字节）价值的媒体访问控制（** MAC **）地址（即，对于01：23：45：67：89的MAC： ab`，mac [0]的值为0x01。

Finally, the `features` field contains a bitmap of available features:  最后，features字段包含可用功能的位图：

Feature                 | Meaning ------------------------|--------------------------------------------`ETHERNET_FEATURE_WLAN`   | Device is a wireless network device`ETHERNET_FEATURE_SYNTH`  | Device is a synthetic network device`ETHERNET_FEATURE_DMA`    | Driver will be doing DMA to/from the VMO 功能|含义------------------------ | ------------------------ --------------------`ETHERNET_FEATURE_WLAN` |设备是无线网络设备`ETHERNET_FEATURE_SYNTH` |设备是综合网络设备`ETHERNET_FEATURE_DMA` |驱动程序将与VMO之间进行DMA

The Intel driver's **eth_query()** is representative:  英特尔驱动程序的eth_query（）**具有代表性：

```c
static zx_status_t eth_query(void* ctx, uint32_t options, ethernet_info_t* info) {
    ethernet_device_t* edev = ctx;

    if (options) {
        return ZX_ERR_INVALID_ARGS;
    }

    memset(info, 0, sizeof(*info));
    ZX_DEBUG_ASSERT(ETH_TXBUF_SIZE >= ETH_MTU);
    info->mtu = ETH_MTU;
    memcpy(info->mac, edev->eth.mac, sizeof(edev->eth.mac));

    return ZX_OK;
}
```
 

In that it returns `ZX_ERR_INVALID_ARGS` in case the `options` parameter is non zero, and otherwise fills the `mtu` and `mac` members. 在这种情况下，如果options参数不为零，则返回ZX_ERR_INVALID_ARGS，否则将填充mtu和mac成员。

 
### Ethernet protocol: **queue_tx()**  以太网协议：** queue_tx（）** 

The **queue_tx()** function is responsible for taking the `ethernet_netbuf_t` network buffer and transmitting it. queue_tx（）函数负责获取“ ethernet_netbuf_t”网络缓冲区并进行传输。

```c
static zx_status_t eth_queue_tx(void* ctx, uint32_t options, ethernet_netbuf_t* netbuf) {
    ethernet_device_t* edev = ctx;
    if (edev->state != ETH_RUNNING) {
        return ZX_ERR_BAD_STATE;
    }
    return eth_tx(&edev->eth, netbuf->data, netbuf->len);
}
```
 

The real work for the Intel ethernet driver is done in `ie.c`:  英特尔以太网驱动程序的实际工作是在`ie.c`中完成的：

```c
status_t eth_tx(ethdev_t* eth, const void* data, size_t len) {
    if (len > ETH_TXBUF_DSIZE) {
        printf("intel-eth: unsupported packet length %zu\n", len);
        return ZX_ERR_INVALID_ARGS;
    }

    zx_status_t status = ZX_OK;

    mtx_lock(&eth->send_lock);

    reap_tx_buffers(eth);

    // obtain buffer, copy into it, setup descriptor
    framebuf_t *frame = list_remove_head_type(&eth->free_frames, framebuf_t, node);
    if (frame == NULL) {
        status = ZX_ERR_NO_RESOURCES;
        goto out;
    }

    uint32_t n = eth->tx_wr_ptr;
    memcpy(frame->data, data, len);
    // Pad out short packets.
    if (len < 60) {
      memset(frame->data + len, 0, 60 - len);
      len = 60;
    }
    eth->txd[n].addr = frame->phys;
    eth->txd[n].info = IE_TXD_LEN(len) | IE_TXD_EOP | IE_TXD_IFCS | IE_TXD_RS;
    list_add_tail(&eth->busy_frames, &frame->node);

    // inform hw of buffer availability
    n = (n + 1) & (ETH_TXBUF_COUNT - 1);
    eth->tx_wr_ptr = n;
    writel(n, IE_TDT);

out:
    mtx_unlock(&eth->send_lock);
    return status;
}
```
 

This function performs buffer management and talks to the hardware. It first locks the mutex, and then finds an available buffer.This is done by calling **reap_tx_buffers()** to find available buffers,and then calling the macro **list_remove_head_type()** to try and fetcha buffer from the head of the list.If no buffer is available, an error status (`ZX_ERR_NO_RESOURCES`) is setand the function returns. 此功能执行缓冲区管理并与硬件对话。它首先锁定互斥锁，然后找到可用的缓冲区。方法是调用** reap_tx_buffers（）**以查找可用的缓冲区，然后调用宏** list_remove_head_type（）**尝试从头部获取缓冲区如果没有可用的缓冲区，则会设置错误状态（`ZX_ERR_NO_RESOURCES`），然后函数返回。

Otherwise, the frame data is copied (short frames, less than 60 bytes, are padded with zeros). 否则，将复制帧数据（小于60字节的短帧用零填充）。

The hardware is kicked via the macro **writel()**, which writes to the `IE_TDT` register telling it which buffer is available to be written to the ethernet. 硬件通过宏** writel（）**被踢，该宏写入IE_TDT寄存器，告诉它哪个缓冲区可用于写入以太网。

At this point, the frame is queued at the chip level, and will be sent shortly. (The timing depends on if there are other frames queued before this one.) 此时，帧在芯片级别排队，并将很快发送。 （时间取决于在此之前是否还有其他帧排队。）

 
### Ethernet protocol: **set_param()**  以太网协议：** set_param（）** 

Sets a parameter based on the passed `param` argument and `value` argument. The Intel driver supports enabling or disabling promiscuous mode, and nothing else: 根据传递的`param`参数和`value`参数设置参数。英特尔驱动程序支持启用或禁用混杂模式，仅此而已：

```c
static zx_status_t eth_set_param(void *ctx, uint32_t param, int32_t value, void* data) {
    ethernet_device_t* edev = ctx;
    zx_status_t status = ZX_OK;

    mtx_lock(&edev->lock);

    switch (param) {
    case ETHERNET_SETPARAM_PROMISC:
        if ((bool)value) {
            eth_start_promisc(&edev->eth);
        } else {
            eth_stop_promisc(&edev->eth);
        }
        status = ZX_OK;
        break;
    default:
        status = ZX_ERR_NOT_SUPPORTED;
    }
    mtx_unlock(&edev->lock);

    return status;
}
```
 

The following parameters are available:  可以使用以下参数：

Parameter                           | Meaning (additional data) ------------------------------------|-------------------------------------------------------------`ETHERNET_SETPARAM_PROMISC`           | Controls promiscuous mode (bool)`ETHERNET_SETPARAM_MULTICAST_PROMISC` | Controls multicast promiscuous mode (bool)`ETHERNET_SETPARAM_MULTICAST_FILTER`  | Sets multicast filtering addresses (count + array)`ETHERNET_SETPARAM_DUMP_REGS`         | Used for debug, dumps the registers (no additional data) 参数含义（其他数据）------------------------------------ | -------- -------------------------------------------------- ---`ETHERNET_SETPARAM_PROMISC` |控制混杂模式（布尔）`ETHERNET_SETPARAM_MULTICAST_PROMISC`控制多播混杂模式（布尔）`ETHERNET_SETPARAM_MULTICAST_FILTER` |设置多播过滤地址（计数+数组）。ETHERNET_SETPARAM_DUMP_REGS用于调试，转储寄存器（无其他数据）

For multicast filtering, the `value` argument indicates the count of MAC addresses sequentially presented via the `data` argument. For example, if `value` was `2`, then `data`would point to two back-to-back MAC addresses (2 x 6 = 12 bytes total). 对于多播过滤，“值”参数指示通过“数据”参数顺序显示的MAC地址数量。例如，如果“值”为“ 2”，则“数据”将指向两个背对背的MAC地址（总共2 x 6 = 12个字节）。

Note that if a parameter is not supported, the value `ZX_ERR_NOT_SUPPORTED` is returned.  请注意，如果不支持参数，则返回值ZX_ERR_NOT_SUPPORTED。

 
### Ethernet protocol: **start()** and **stop()**  以太网协议：** start（）**和** stop（）** 

The two functions, **eth_start()** and **eth_stop()** are used to start and stop the ethernet device: eth_start（）**和eth_stop（）**这两个函数用于启动和停止以太网设备：

```c
static void eth_stop(void* ctx) {
    ethernet_device_t* edev = ctx;
    mtx_lock(&edev->lock);
    edev->ifc = NULL;
    mtx_unlock(&edev->lock);
}

static zx_status_t eth_start(void* ctx, ethernet_ifc_t* ifc, void* cookie) {
    ethernet_device_t* edev = ctx;
    zx_status_t status = ZX_OK;

    mtx_lock(&edev->lock);
    if (edev->ifc) {
        status = ZX_ERR_BAD_STATE;
    } else {
        edev->ifc = ifc;
        edev->cookie = cookie;
        edev->ifc->status(edev->cookie, edev->online ? ETHERNET_STATUS_ONLINE : 0);
    }
    mtx_unlock(&edev->lock);

    return status;
}
```
 

The Intel ethernet driver code shown above is typical; the `ifc` member of the context block is used as both an indication of status (`NULL` if stopped) and, when running,it points to a valid interface block. 上面显示的英特尔以太网驱动程序代码是典型的代码。上下文块的ifc成员既用作状态指示（如果停止则为NULL），并且在运行时它指向有效的接口块。

 
### Ethernet protocol: **get_bti()**  以太网协议：** get_bti（）** 

The Intel ethernet driver doesn't support the optional **get_bti()** callout.  英特尔以太网驱动程序不支持可选的** get_bti（）**标注。

This callout is used to return a handle to the [BTI](/docs/concepts/objects/bus_transaction_initiator.md). In case the device doesn't support it, it can either leave it out of the `ethernet_impl_protocol_ops_t`structure (like the Intel ethernet driver does), or it can return `ZX_HANDLE_INVALID`. 此标注用于将句柄返回到[BTI]（/ docs / concepts / objects / bus_transaction_initiator.md）。如果设备不支持它，则可以将其保留在“ ethernet_impl_protocol_ops_t”结构之外（如Intel以太网驱动程序那样），也可以返回“ ZX_HANDLE_INVALID”。

If supported, the handle is returned from the function. Note that the ownership of the handle is *not* transferred; the ethernet driver stillowns the handle.In particular, the caller must not close the handle. 如果支持，则从函数返回句柄。注意，句柄的所有权是“不转让”的；以太网驱动程序仍然拥有该句柄。特别是，调用者不得关闭该句柄。

 
## Receiving data  接收资料 

The IHT thread created by the binding function waits for data from the ethernet hardware. When data arrives, it calls **eth_handle_irq()** to process the data. 绑定函数创建的IHT线程等待来自以太网硬件的数据。数据到达时，它将调用eth_handle_irq（）**以处理数据。

The portion of the thread in `ethernet.c` is as follows:  ethernet.c中的线程部分如下：

```c
static int irq_thread(void* arg) {
    ethernet_device_t* edev = arg;
    for (;;) {
        zx_status_t r;
        r = zx_interrupt_wait(edev->irqh, NULL);
        if (r != ZX_OK) {
            printf("eth: irq wait failed? %d\n", r);
            break;
        }
        mtx_lock(&edev->lock);
        unsigned irq = eth_handle_irq(&edev->eth);
        if (irq & ETH_IRQ_RX) {
            void* data;
            size_t len;

            while (eth_rx(&edev->eth, &data, &len) == ZX_OK) {
                if (edev->ifc && (edev->state == ETH_RUNNING)) {
                    edev->ifc->recv(edev->cookie, data, len, 0);
                }
                eth_rx_ack(&edev->eth);
            }
        }
        if (irq & ETH_IRQ_LSC) {
            bool was_online = edev->online;
            bool online = eth_status_online(&edev->eth);
            zxlogf(TRACE, "intel-eth: ETH_IRQ_LSC fired: %d->%d\n", was_online, online);
            if (online != was_online) {
                edev->online = online;
                if (edev->ifc) {
                    edev->ifc->status(edev->cookie, online ? ETHERNET_STATUS_ONLINE : 0);
                }
            }
        }
        mtx_unlock(&edev->lock);
    }
    return 0;
}
```
 

The thread waits on an interrupt, and, when one occurs, calls **eth_handle_irq()** to read the interrupt reason register (which also clears the interruptindication on the card). 线程等待一个中断，并在发生中断时调用eth_handle_irq（）**以读取中断原因寄存器（这还将清除卡上的中断指示）。

Based on the value read from **eth_handle_irq()**, there are two major flows in the thread: 根据从** eth_handle_irq（）**中读取的值，线程中有两个主要流程：

 
1.  the bit `ETH_IRQ_RX` is present &mdash; this indicates data has been received by the card, 1.位“ ETH_IRQ_RX”存在–这表示卡已接收到数据，
2.  the bit `ETH_IRQ_LSC` is present &mdash; this indicates a Line Status Change (LSC) event has been detected by the card. 2.存在“ ETH_IRQ_LSC”位-这表示卡已检测到线路状态更改（LSC）事件。

If data has been received, the following functions are called:  如果已接收到数据，则调用以下功能：

 
*   **eth_rx()** &mdash; obtains a pointer to the receive buffer containing the data  * ** eth_rx（）** mdash;获取指向包含数据的接收缓冲区的指针
*   **eth_rx_ack()** &mdash; acknowledges receipt of the packet by writing to registers on the card  * ** eth_rx_ack（）** mdash;通过写入卡上的寄存器来确认已收到数据包

 

Note that further processing is done by the ethernet device protocol (available via `edev->ifc`):  注意，进一步的处理由以太网设备协议（可通过`edev-> ifc`获得）完成：

 
*   **edev->ifc->recv()** &mdash; processes the received data  * ** edev-> ifc-> recv（）** mdash;处理收到的数据
*   **edev->ifc->status()** &mdash; processes the status change  * ** edev-> ifc-> status（）**-处理状态更改

In the case of a line status change, **eth_status_online()** is called to handle the event.  在线路状态更改的情况下，将调用eth_status_online（）**处理事件。

```c
status_t eth_rx(ethdev_t* eth, void** data, size_t* len) {
    uint32_t n = eth->rx_rd_ptr;
    uint64_t info = eth->rxd[n].info;

    if (!(info & IE_RXD_DONE)) {
        return ZX_ERR_SHOULD_WAIT;
    }

    // copy out packet
    zx_status_t r = IE_RXD_LEN(info);

    *data = eth->rxb + ETH_RXBUF_SIZE * n;
    *len = r;

    return ZX_OK;
}
```
 

