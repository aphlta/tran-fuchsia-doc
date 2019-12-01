 
# Magma: Porting Guide  岩浆：移植指南 

For an overview of Magma including background, hardware requirements, and description of architecture, please see [Magma: Overview](README.md).  有关Magma的概述，包括背景，硬件要求和体系结构描述，请参阅[Magma：概述]（README.md）。

For each component, a short term and long term process is described, where, in the short term, all Fuchsia related development is performed by the Magma team.  对于每个组件，都描述了一个短期和长期的过程，其中，在短期内，所有与紫红色相关的开发都由岩浆团队执行。

 
## Magma system driver  岩浆系统驱动程序 

The magma system driver must be open source but not GPL and hosted on *fuchsia.googlesource.com*.  A magma system driver must provide an implementation of the [msd interface](/garnet/lib/magma/include/msd_abi/msd.h).  岩浆系统驱动程序必须是开源的，而不是GPL，并且必须托管在* fuchsia.googlesource.com *上。岩浆系统驱动程序必须提供[msd接口]（/ garnet / lib / magma / include / msd_abi / msd.h）的实现。

 
### Short term  短期 

The Magma team writes new code, supporting only the latest gpu hardware generations. Some combination of the following resources are required:  Magma团队编写了新代码，仅支持最新的gpu硬件。需要以下资源的某种组合：

 
* Hardware documentation (register spec, theory of operation)  *硬件文档（寄存器规格，操作原理）
* A reference implementation (Linux)  *参考实现（Linux）
* Vendor support  *供应商支持

 
### Long term  长期 

The gpu vendor supplies and maintains the system driver using the Zircon DDK.  gpu供应商使用Zircon DDK提供并维护系统驱动程序。

 
### Tasks  任务 

 
* Initialize hardware: register access, clocks, regulators, interrupts, firmware.  **Note** where the GPU block is agnostic of these concerns, they should be configured in a separate board driver; see Zircon [platform-bus](/docs/concepts/drivers/platform-bus.md).  *初始化硬件：寄存器访问，时钟，调节器，中断，固件。 **注意**如果GPU模块与这些问题无关，则应在单独的板卡驱动程序中进行配置；参见Zircon [platform-b​​us]（/ docs / concepts / drivers / platform-b​​us.md）。
	* *msd_driver_create*  * * msd_driver_create *
	* *msd_driver_configure*  * * msd_driver_configure *
	* *msd_driver_destroy*  * * msd_driver_destroy *
	* *msd_driver_create_device*  * * msd_driver_create_device *
	* *msd_device_destroy*  * * msd_device_destroy *
* Support for parameter querying  *支持参数查询
	* *msd_device_query*  * * msd_device_query *
* Create connections  *创建连接
	* *msd_device_open*  * * msd_device_open *
	* *msd_connection_close*  * * msd_connection_close *
* Create buffers  *创建缓冲区
	* *msd_buffer_import*  * * msd_buffer_import *
	* *msd_buffer_destroy*  * * msd_buffer_destroy *
* Set up memory spaces and buffer mappings  *设置内存空间和缓冲区映射
	* *msd_connection_map_buffer_gpu*  * * msd_connection_map_buffer_gpu *
	* *msd_connection_unmap_buffer_gpu*  * * msd_connection_unmap_buffer_gpu *
	* *msd_connection_commit_buffer*  * * msd_connection_commit_buffer *
	* *msd_connection_release_buffer*  * * msd_connection_release_buffer *
* Set up hardware contexts  *设置硬件上下文
	* *msd_connection_create_context*  * * msd_connection_create_context *
	* *msd_context_destroy*  * * msd_context_destroy *
* Command buffer scheduling  *命令缓冲区调度
	* *msd_context_execute_command_buffer*  * * msd_context_execute_command_buffer *
	* *msd_context_execute_immediate_commands*  * * msd_context_execute_immediate_commands *
	* *msd_connection_set_notification_callback*  * * msd_connection_set_notification_callback *
* Create semaphores  *创建信号量
	* *msd_semaphore_import*  * * msd_semaphore_import *
	* *msd_semaphore_destroy*  * * msd_semaphore_destroy *
* Support for status dump  *支持状态转储
	* *msd_device_dump_status*  * * msd_device_dump_status *
* Fault handling  *故障处理
* Power management  * 能源管理

 
## Client side library  客户端库 

Not required to be open source; for bringup, the repo may be hosted by the Magma team internally and only the binary objects will be distributed.  不需要是开源的；对于启动，该回购可能由Magma团队在内部托管，并且只会分发二进制对象。

The client driver library should provide a conformant implementation of Vulkan 1.0/1.1.  It must also implement several Fuchsia specific variants of common KHR Vulkan extensions for external memory and semaphores. These are currently WIP and subject to change, but can be found in the Fuchsia internal [Vulkan header](https://fuchsia.googlesource.com/third_party/vulkan_loader_and_validation_layers/+/master/include/vulkan/vulkan.h):  客户端驱动程序库应提供Vulkan 1.0 / 1.1的一致实现。它还必须实现一些常见的KHR Vulkan扩展的紫红色特定变体，以用于外部存储器和信号量。这些当前是WIP，并且可能会更改，但是可以在Fuchsia内部的[Vulkan标头]（https://fuchsia.googlesource.com/third_party/vulkan_loader_and_validation_layers/+/master/include/vulkan/vulkan.h）中找到：

 
* VK_FUCHSIA_external_memory  * VK_FUCHSIA_external_memory
* VK_FUCHSIA_external_semaphore  * VK_FUCHSIA_external_semaphore

 
### Short term  短期The Magma team pulls codebase updates from the vendor periodically.  The Fuchsia customization work must be then pushed back upstream to the vendor to ease the burden of future merges.  Magma团队会定期从供应商处获取代码库更新。然后，必须将紫红色的定制工作向上游推回给供应商，以减轻将来合并的负担。

 
### Long term  长期Eventually, the vendor will be able to build and test for Fuchsia, so the Fuchsia port can be handled entirely by the vendor like any other supported operating system.  最终，供应商将能够构建和测试Fuchsia，因此Fuchsia端口可以像其他任何受支持的操作系统一样完全由供应商处理。

 
### Bring-up Tasks  提拔任务 

 
* Build the vendor code  *建立供应商代码
* If closed source, make a static library as a distributable prebuilt that can be linked with dependencies in fuchsia to make a complete shared library that can be loaded into the application’s process space  *如果是封闭源，则将静态库制作为可分发的预构建库，并可以将其与紫红色中的依赖项链接在一起，以创建可以加载到应用程序进程空间中的完整共享库
* Port any os dependencies to Fuchsia (Fuchsia provides a c library with a lot of posix support and a std c++ library)  *将任何os依赖项移植到Fuchsia（Fuchsia提供了一个带有posix支持的c库和一个std c ++库）
* Rework system integration layer to use magma interfaces instead of kernel interfaces  *重做系统集成层以使用岩浆接口而不是内核接口
* Implement Fuchsia Vulkan extensions  *实现紫红色Vulkan扩展

 
### Validation Stages  验证阶段 

 
* A simple Vulkan test passes  *简单的Vulkan测试通过
	* Test: [vkreadback](/src/graphics/tests/vkreadback) (draws a color then reads back the framebuffer values)  *测试：[vkreadback]（/ src / graphics / tests / vkreadback）（先绘制颜色，然后读回帧缓冲区值）
* Add support for fuchsia window system integration extensions using zircon framebuffer library  *使用锆石帧缓冲库添加对紫红色窗口系统集成扩展的支持
    * Test: [vkcube](/src/graphics/examples/vkcube/) (animated, using VK_KHR_swapchain)  *测试：[vkcube]（/ src / graphics / examples / vkcube /）（使用VK_KHR_swapchain进行动画处理）
* Add support for fuchsia external memory and semaphore extensions  *添加对紫红色外部存储器和信号量扩展的支持
	* Test: [vkext](/src/graphics/tests/vkext)  *测试：[vkext]（/ src / graphics / tests / vkext）

