Magma: Overview =============== 岩浆：概述===============

 
## Background  背景 

Fuchsia is a new open source, micro-kernel-like operating system from Google.  Drivers do not execute inside the Zircon kernel, instead they are privileged user-space processes.  Drivers are built using a stable [DDK](/docs/concepts/drivers/overview.md).  Fuchsia是Google提供的一种新的开源，类似于微内核的操作系统。驱动程序不在Zircon内核中执行，而是具有特权的用户空间进程。使用稳定的[DDK]（/ docs / concepts / drivers / overview.md）构建驱动程序。

Magma is the gpu driver architecture for Fuchsia. There are two driver components: a gpu-specific library loaded into each application’s address space; and the magma system driver that manages the hardware.  岩浆是紫红色的gpu驱动程序体系结构。有两个驱动程序组件：一个gpu特定的库加载到每个应用程序的地址空间中；以及管理硬件的岩浆系统驱动程序。

 
## Hardware requirements  硬件要求 

 
### Vulkan conformant gpu  符合Vulkan规范的GPUMagma is designed to support [Vulkan](vulkan.md), though it could be used to implement OpenGL or other graphics api.  For legacy codebases Fuchsia intends to support OpenGL via translation to Vulkan using ANGLE.  岩浆被设计为支持[Vulkan]（vulkan.md），尽管它可用于实现OpenGL或其他图形api。对于旧的代码库，Fuchsia打算通过使用ANGLE转换为Vulkan来支持OpenGL。

 
### MMU  MMUA memory management unit that allows arbitrary mapping of system memory pages into the GPU address space is needed for DMA to/from non-contiguous buffers.  DMA需要使用内存管理单元将系统内存页任意映射到GPU地址空间中，以实现DMA与非连续缓冲区之间的往返。

 
### Per-client independent address space  每个客户端独立的地址空间For system security it’s important to maintain address space isolation in the gpu domain as well as in the cpu domain.  为了系统安全，必须在gpu域和cpu域中都保持地址空间隔离。

 
### Unified memory architecture  统一内存架构This may be relaxed in the future.  将来可能会放宽。

 
## Architecture  建筑 

Similar to the direct rendering model on Linux, there are two driver components: a gpu-specific library loaded into each application’s address space; and the magma system driver that manages the hardware.  与Linux上的直接渲染模型类似，有两个驱动程序组件：一个gpu特定的库加载到每个应用程序的地址空间中；以及管理硬件的岩浆系统驱动程序。

 
### Magma system driver  岩浆系统驱动程序 

Responsibilities:  职责：
* Initializing hardware  *初始化硬件
* Setting up memory spaces  *设置存储空间
* Setting up hardware contexts  *设置硬件上下文
* Mapping buffers  *映射缓冲区
* Scheduling command buffers  *调度命令缓冲区
* Handling faults  *处理故障
* Managing power  *管理力量

 
### Client library driver  客户端库驱动 

Responsibilities:  职责：
* Implementing Vulkan 1.0/1.1 entry points  *实现Vulkan 1.0 / 1.1入口点
* Implementing Fuchsia extensions for import and export of external memory and semaphores  *实现紫红色扩展以导入和导出外部存储器和信号量
* Implementing VK_KHR_display and/or VK_KHR_swapchain for direct display access  *实现VK_KHR_display和/或VK_KHR_swapchain用于直接显示访问

Whereas a traditional client driver makes ioctl syscalls to communicate with a kernel driver; magma provides an interface for client drivers to communicate over IPC with the Magma system driver.  传统的客户端驱动程序进行ioctl系统调用以与内核驱动程序进行通信； magma为客户端驱动程序提供接口，以通过IPC与Magma系统驱动程序进行通信。

Details on the Magma interface are given in [Magma: Design](design.md).  在[Magma：Design]（design.md）中提供了有关Magma界面的详细信息。

