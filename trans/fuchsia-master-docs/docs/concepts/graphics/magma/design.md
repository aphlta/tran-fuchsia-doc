Magma: Design ============= 岩浆：设计==============

For an overview of Magma including background, hardware requirements, and description of architecture, please see [Magma: Overview](README.md).  有关Magma的概述，包括背景，硬件要求和体系结构描述，请参阅[Magma：概述]（README.md）。

 
## Goals  目标 

 
### Extensible core  可扩展核心 

Magma aims to pragmatically minimize the architectural differences in the way that client drivers communicate with their respective system drivers across different gpu and client driver designs.  Where necessary, Magma adds gpu-specific queries, command structures, and interfaces to accommodate specific requirements.  These differences are clarified in driver-specific documentation.  Magma的目标是在不同gpu和客户端驱动程序设计之间，通过客户端驱动程序与其各自的系统驱动程序进行通信的方式，务实地最小化体系结构差异。必要时，Magma添加了特定于GPU的查询，命令结构和接口，以适应特定要求。这些差异已在特定于驱动程序的文档中阐明。

 
### Feed forward  前馈 

Wherever possible, the main IPC channel is used in a feed-forward manner to prevent blocking client threads.  For notifications from the system driver back to the client, driver-defined messages are sent asynchronously.  尽可能以前馈方式使用主IPC通道，以防止阻塞客户端线程。对于从系统驱动程序返回到客户端的通知，驱动程序定义的消息是异步发送的。

 
### Avoid gpu faults  避免GPU错误 

Clients can cause the gpu to hang or fault, and when this happens it will affect system critical gpu clients like the compositor, resulting in a noticeable hiccup in user experience.  Consequently Magma attempts to minimize the opportunities for clients to induce gpu faults.  客户端可能导致gpu挂起或发生故障，当这种情况发生时，它将影响系统关键的gpu客户端（例如合成器），从而导致用户体验明显下降。因此，岩浆公司试图最大程度地减少客户诱发GPU故障的机会。

 
## Architecture  建筑 

As mentioned in the overview, the Magma architecture involves two driver components: a client library, and a privileged system driver process.  Both are gpu-specific; the client library must compile software from IR (intermediate representation, for example SPIR-V) into machine code, and format command buffers correctly for consumption by the hardware.  These are fed to the Magma system driver, which performs that actual programming of the hardware.  如概述中所述，Magma体系结构包含两个驱动程序组件：客户端库和特权系统驱动程序进程。两者都是特定于GPU的；客户端库必须将IR（中间表示，例如SPIR-V）中的软件编译为机器代码，并正确格式化命令缓冲区以供硬件使用。这些被馈送到Magma系统驱动程序，该程序执行硬件的实际编程。

![](block_diagram.png)  ！[]（block_diagram.png）

Magma defines two interfaces to gpu-specific code:  岩浆为gpu特定代码定义了两个接口：
* The **magma** interface provides the foundation for the client driver, typically libvulkan  * ** magma **接口为客户端驱动程序（通常为libvulkan）提供了基础
* The **msd** (magma system driver) interface dictates the entry points for an implementation of a magma service driver  * ** msd **（岩浆系统驱动程序）接口规定了岩浆服务驱动程序实现的入口点

libmagma is a convenience layer that implements the magma interface and forwards calls appropriately to magma_system, which is a gpu-agnostic layer handling driver initialization and teardown, transport of IPC commands, and some validation.  libmagma是一个便利层，它实现了magma接口并将调用适当地转发到magma_system，这是一个与gpu无关的层，用于处理驱动程序的初始化和拆卸，IPC命令的传输以及某些验证。

The creation of a magma driver is thus simplified at a high level into two steps:  因此，将岩浆驱动器的创建从高层次简化为两个步骤：

 
1. Produce a client driver by leveraging the magma interface (described below)  1.利用岩浆接口（如下所述）生成客户端驱动程序
2. Implement the msd interface to produce a magma system driver.  2.实施msd接口以生成岩浆系统驱动程序。

For details on the process of building these two components, see the [porting](porting.md) guide.  有关构建这两个组件的过程的详细信息，请参见[porting]（porting.md）指南。

 
## The Magma interface  岩浆接口 

The Magma interface is a service interface provided by the Magma system driver. The interface is designed to be useful for implementing an accelerated graphics api.  It consists of [magma.h](/garnet/lib/magma/include/magma_abi/magma.h) plus gpu specific headers (example: [intel](/garnet/drivers/gpu/msd-intel-gen/include/msd_intel_gen_query.h)). Magma接口是Magma系统驱动程序提供的服务接口。该接口旨在用于实现加速的图形API。它由[magma.h]（/ garnet / lib / magma / include / magma_abi / magma.h）加上gpu特定的标头组成（例如：[intel]（/ garnet / drivers / gpu / msd-intel-gen / include / msd_intel_gen_query.h）。

 
### Physical devices  物理设备During the Fuchsia boot sequence, a Magma system driver is instantiated for each physical device capable of accelerated graphics.  The instantiation creates a device binding in the class gpu; for example, in a single gpu system the device is bound to /dev/class/gpu/000. With appropriate application privilege, client drivers may scan for the presence of one or more gpu class devices, and open them.Synchronous queries may be performed on the device file descriptor to return various parameters, some of which may be useful for helping the application decide which physical devices, under which configuration, to work with. 在紫红色启动过程中，将为每个能够加速图形的物理设备实例化Magma系统驱动程序。实例化在类gpu中创建设备绑定。例如，在单个gpu系统中，设备绑定到/ dev / class / gpu / 000。拥有适当的应用程序特权，客户端驱动程序可以扫描一个或多个gpu类设备的存在，然后将其打开。可以在设备文件描述符上执行同步查询以返回各种参数，其中一些参数可用于帮助应用程序确定使用哪种物理设备，采用哪种配置。

 
### Connections  连接数When the application declares its intent to work with a particular physical device, a connection is established to the Magma system driver. This connection forms the basis for all further communication between the client driver and system driver. A connection allows the client driver to allocate buffers and map them into the gpu address space.  The connection defines a memory isolation boundary; Magma guarantees that buffers mapped into one connection’s address space are by default not accessible to another connection.  Buffer sharing between connections is possible with explicit export/import. 当应用程序声明要使用特定物理设备的意图时，将与Magma系统驱动程序建立连接。此连接构成了客户端驱动程序和系统驱动程序之间所有进一步通信的基础。连接允许客户端驱动程序分配缓冲区并将其映射到gpu地址空间。该连接定义了一个内存隔离边界； Magma保证默认情况下，映射到一个连接的地址空间的缓冲区是另一连接无法访问的。通过显式导出/导入，可以在连接之间共享缓冲区。

 
### Contexts  语境To execute work on the gpu, a context is needed.  Contexts are scheduled for execution on the gpu by the Magma system driver.  Contexts should contain all gpu state required to allow for multiple contexts to be switched onto the hardware.  Command buffers are used to set the state of the gpu, so command buffers are submitted to a particular context. Magma supports multiple contexts per connection; this is to allow for more than one context to share a single address space. 要在gpu上执行工作，需要一个上下文。上下文计划由Magma系统驱动程序在gpu上执行。上下文应包含允许将多个上下文切换到硬件所需的所有gpu状态。命令缓冲区用于设置gpu的状态，因此命令缓冲区被提交到特定的上下文。岩浆每个连接支持多个上下文。这是为了允许多个上下文共享一个地址空间。

When a client connection is closed, to avoid gpu fault the address space must remain alive while gpu is executing work using that address space; therefore, context takes a shared reference on the address space.  当关闭客户端连接时，为避免gpu故障，在gpu使用该地址空间执行工作时，地址空间必须保持活动状态；因此，上下文在地址空间上采用了共享引用。

 
### Buffers and Mappings  缓冲区和映射Currently Magma requires a unified memory architecture, as is the case with most mobile hardware, where cpu and gpu access the same physical memory.   Magma buffers are just zircon virtual memory objects ([VMOs](/docs/concepts/objects/vm_object.md)). Client drivers allocate buffers and register those buffers with the system driver.  目前，与大多数移动硬件一样，Magma需要统一的内存体系结构，其中cpu和gpu访问相同的物理内存。岩浆缓冲区只是锆石虚拟内存对象（[VMOs]（/ docs / concepts / objects / vm_object.md））。客户端驱动程序分配缓冲区，并向系统驱动程序注册这些缓冲区。

Gpu address space management may be performed by the client or by the system driver. The client driver design may dictate the model.  Gpu地址空间管理可以由客户端或系统驱动程序执行。客户驱动程序设计可以决定模型。

If the system driver manages buffer mapping lifetime, the system driver ensures mappings, and their underlying buffers, are alive while command buffers referencing them are outstanding on the gpu.  Since mapping is slow (because it requires ensuring that buffer pages are committed, and modifying page tables to reference the correct bus address for each page), buffers mappings must either persist for the lifetime of the buffer, or a gpu mapping cache could be used to limit the amount of memory used by cached mappings.  如果系统驱动程序管理缓冲区映射生存期，则系统驱动程序可确保映射及其基础缓冲区处于活动状态，而引用它们的命令缓冲区在gpu上仍处于未完成状态。由于映射速度很慢（因为它需要确保已提交缓冲区页面，并修改页面表以为每个页面引用正确的总线地址），因此缓冲区映射必须在缓冲区的生存期内一直存在，或者可以使用gpu映射缓存限制缓存映射使用的内存量。

The disadvantage of system driver managed buffer mappings is when building command lists, the client needs to know the gpu address of mapped buffers; so command buffers must be patched by the Magma service driver prior to execution.  For this reason, it is preferred to have the client driver explicitly manage gpu mapping lifetime.  The disadvantage with the explicit approach is that a client may unmap or release a buffer while a mapping is in flight on the gpu; if this occurs, the page table entries will be invalidated while in use by the gpu, likely causing a gpu fault.  系统驱动程序管理的缓冲区映射的缺点是，在构建命令列表时，客户端需要知道所映射缓冲区的gpu地址。因此，命令缓冲区必须在执行前由Magma服务驱动程序修补。因此，最好让客户端驱动程序显式管理gpu映射生存期。显式方法的缺点是，客户端可能会在gpu上进行映射时取消映射或释放缓冲区。如果发生这种情况，页面表条目将在由gpu使用时失效，可能会导致gpu故障。

A mitigation for this disadvantage is possible if each command buffer is accompanied by a list of dependent buffer mappings; then, the command buffer can share ownership of the gpu mappings; and if an unmap or release is received while a resource is inflight, this is treated as a fatal error to the client without disrupting the gpu.  如果每个命令缓冲区都带有一系列相关的缓冲区映射，则可以缓解此缺点。然后，命令缓冲区可以共享gpu映射的所有权；并且，如果在资源运行过程中收到取消映射或释放，则这将被视为对客户端的致命错误，而不会中断gpu。

 
### Command submission  命令提交 

Commands consist of vendor-specific data that modify the state of the gpu and trigger code execution on the gpu compute cores. The system driver is responsible for queueing and scheduling submitted commands onto the gpu for execution.Various scheduling algorithms are possible: FIFO (default), priority, time slicing.Pre-emption of inflight command buffers, if supported by hardware, can be used to implement context prioritization. 命令由特定于供应商的数据组成，这些数据会修改gpu的状态并触发gpu计算核心上的代码执行。系统驱动程序负责将提交的命令排队并安排到gpu上执行，可以使用各种调度算法：FIFO（默认），优先级，时间分片。如果有硬件支持，则可以使用机上命令缓冲区的抢占。实现上下文优先级。

 
### Semaphores  信号量 

Magma provides semaphores as a general signalling mechanism that can be used to implement Vulkan fences and semaphores.  Magma semaphores are built on zircon [events](/docs/concepts/objects/event.md).  岩浆提供信号量作为一种通用的信号机制，可用于实现Vulkan围墙和信号量。岩浆信号量基于锆石[事件]（/ docs / concepts / objects / event.md）。

 
### Summary of object ownership  对象所有权摘要 
* Client: owns connections; shared ownership of buffers, mappings, contexts  *客户：拥有连接；缓冲区，映射，上下文的共享所有权
* Connection: shared ownership of address space  *连接：地址空间的共享所有权
* Context: shared ownership of address space  *上下文：地址空间的共享所有权
* Address space: shared ownership of mappings  *地址空间：映射的共享所有权
* Mappings: shared ownership of buffers  *映射：缓冲区的共享所有权
* Command buffer: shared ownership of context; may have shared ownership of mappings  *命令缓冲区：上下文的共享所有权；可能拥有映射的共享所有权

 
## Thread Model  螺纹型号 

The thread model used for each installed GPU device and driver is as follows:  用于每个已安装的GPU设备和驱动程序的线程模型如下：

The msd is typically loaded by the [platform bus driver](/docs/concepts/drivers/platform-bus.md) and a msd main devhost thread is created.  The msd main thread in turn creates a device thread to talk to the GPU and a driver-dependent number of interrupt threads to service GPU interrupts.  msd通常由[平台总线驱动程序]（/ docs / concepts / drivers / platform-b​​us.md）加载，并创建一个msd主要devhost线程。 msd主线程又创建了一个设备线程以与GPU进行通信，并创建了与驱动程序有关的多个中断线程来服务GPU中断。

A client driver library that implements the Vulkan api is referred to as a **vcd** (Vulkan Client Driver).  When a Vulkan application starts and makes a new VkDevice, the vcd makes a request to the msd to establish a connection for the device over which all Vulkan commands will be communicated.  The msd main thread responds to this call by creating a new connection thread to service all client commands. The connection thread in turn creates two zircon communication channels: the primary channel and the notification channel.  实现Vulkan api的客户端驱动程序库称为vcd（Vulkan客户端驱动程序）。当Vulkan应用程序启动并制作新的VkDevice时，vcd向msd发出请求，要求为将通过其传达所有Vulkan命令的设备建立连接。 msd主线程通过创建一个新的连接线程来服务所有客户端命令来响应此调用。连接线程又创建了两个锆石通信通道：主要通道和通知通道。

Vulkan state configuration, resource creation and drawing command buffers are sent from the vcd to the msd over the primary channel.  The notification channel is used to convey asynchronous status messages back to the vcd.  A good example of a notification the vcd may be interested in is the completion of a command buffer.  The exact messages sent over the device and notification channels along with how those messages are handled varies by GPU driver.  Vulkan状态配置，资源创建和绘图命令缓冲区通过主通道从vcd发送到msd。通知通道用于将异步状态消息传送回VCD。 vcd可能感兴趣的通知的一个很好的例子是命令缓冲区的完成。通过设备和通知通道发送的确切消息以及如何处理这些消息，具体取决于GPU驱动程序。

![](vulkan_driver_thread_model.png)  ！[]（vulkan_driver_thread_model.png）

Note that the process boundary enclosing the msd is the Fuchsia devhost process boundary for the msd.  This devhost process may include threads from other drivers as well but only msd-specific threads are shown here.  请注意，包围msd的进程边界是msd的Fuchsia devhost进程边界。这个devhost进程可能还包括来自其他驱动程序的线程，但此处仅显示特定于msd的线程。

 
## Error Handling  错误处理 

When an error occurs in the magma service driver, the corresponding connection is killed.  When the client driver attempts to access the closed connection it typically will pass up a "device lost" Vulkan api error.  在岩浆服务驱动程序中发生错误时，将终止相应的连接。当客户端驱动程序尝试访问关闭的连接时，它通常会传递“设备丢失” Vulkan api错误。

 
## Power Management  能源管理 

Power management involves adjustment of the gpu execution frequency based on a measurement of gpu load, and potential power or thermal limitations.  Power management will be detailed in further documentation.  电源管理包括根据gpu负载的测量值以及潜在的功率或热量限制来调整gpu执行频率。电源管理将在进一步的文档中详细介绍。

 
## Testing Strategy  测试策略 

