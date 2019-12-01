Magma Test Strategy =================== 岩浆测试策略===================

 
## Architecture Diagram  架构图 

 
* [Magma Block Diagram](block_diagram.svg)  * [岩浆方块图]（block_diagram.svg）

Four major interfaces  四个主要界面

 
* [Vulkan](https://www.khronos.org/vulkan)  * [Vulkan]（https://www.khronos.org/vulkan）
* [magma](/garnet/lib/magma/include/magma_abi/magma.h)  * [岩浆]（/ garnet / lib / magma / include / magma_abi / magma.h）
* [magma system](/garnet/lib/magma/src/magma_util/platform/platform_connection.h)  * [岩浆系统]（/ garnet / lib / magma / src / magma_util / platform / platform_connection.h）
* [msd](/garnet/lib/magma/include/msd_abi/msd.h)  * [msd]（/ garnet / lib / magma / include / msd_abi / msd.h）

Four major components  四个主要组成部分

 
* libvulkan  * libvulkan
* libmagma  * libmagma
* magma_system  *岩浆系统
* vendor msd (magma service driver)  *供应商MSD（岩浆服务驱动程序）

 
## Challenges  挑战性 

 
* Vulkan drivers require hardware for complete testing  * Vulkan驱动程序需要硬件才能进行完整的测试
    * Each supported gpu requires testing of a different hardware platform  *每个受支持的GPU需要测试不同的硬件平台
* GPUs are complex pieces of hardware with flaws that may trigger misbehavior infrequently  * GPU是复杂的硬件，其缺陷可能很少触发错误行为
    * There may be tests that flake rarely  *可能有很少剥落的测试
* Vulkan CTS (conformance) takes several hours to run  * Vulkan CTS（符合性）需要几个小时才能运行
    * Should be run on a daily build, not part of normal CQ  *应该每天运行，而不是常规CQ的一部分
* Upstreaming libvulkan changes to the vendor  *将libvulkan更改上传到供应商
    * Vendor must be provided a build and test environment with which they can validate Vulkan CTS on Fuchsia  *必须为供应商提供构建和测试环境，以便他们可以在紫红色上验证Vulkan CTS
* Source access to gfxbench is restricted  *限制对gfxbench的源访问
    * Should we test a binary package?  *我们应该测试二进制包吗？

 
## Unit Tests  单元测试 

Some of these require hardware; those that don't are included in pre-submit checks for CQ.  其中一些需要硬件。提交前的CQ检查中未包含的内容。

 
* magma_util_tests  * magma_util_tests
    * Coverage 100% of magma_util (not including platform)  *覆盖magma_util的100％（不包括平台）
* magma_platform_tests:  * magma_platform_tests：
    * Coverage 100% of magma_util/platform  *覆盖magma_util / platform的100％
* magma_system_tests  * magma_system_tests
    * Coverage 100% of magma system  *岩浆系统覆盖率100％
    * Uses mock msd  *使用模拟MSD
* vendor msd  *供应商MSD
    * Coverage 80-100% (may not be worth mocking out some portions of the hardware interacting code)  *覆盖率80-100％（可能不值得模拟出硬件交互代码的某些部分）
    * Several mocks used in place of hardware  *数个模拟代替硬件
        * platform mmio  *平台mmio
        * platform bus mapper  *平台总线映射器
        * address space  *地址空间
        * mapped batch  *映射的批次
* libvulkan  * libvulkan
    * Supplied by vendor  *由供应商提供
    * Uses mock magma system (if not sufficient, becomes a hardware interaction test)  *使用模拟岩浆系统（如果不够，将成为硬件交互测试）

 
## Hardware Interaction Tests  硬件交互测试 

The interaction between app, libvulkan, msd, and gpu is complex.  Generally speaking the app generates Vulkan command buffers and shader programs which are created in a gpu specific binary format by libvulkan. Those command buffers as well as other resources are shared with the magma system driver, which maps resources into the gpu's address space and schedules command buffers on the gpu's execution units. 应用程序，libvulkan，msd和gpu之间的交互非常复杂。一般来说，应用程序会生成Vulkan命令缓冲区和着色器程序，这些程序是由libvulkan以gpu特定的二进制格式创建的。这些命令缓冲区以及其他资源与岩浆系统驱动程序共享，后者将资源映射到gpu的地址空间，并在gpu的执行单元上调度命令缓冲区。

 
* magma_abi_conformance_tests  * magma_abi_conformance_tests
    * Does not execute command buffers; rely on Vulkan CTS for command buffer coverage  *不执行命令缓冲区；依靠Vulkan CTS来覆盖命令缓冲区
* msd_abi_conformance_tests  * msd_abi_conformance_tests
    * Validates a vendor's msd implementation  *验证供应商的msd实施
    * Coverage goal 100%, currently ~50% (MA-451 for implementing vendor specifics)  *覆盖率目标为100％，目前约为50％（MA-451用于实施特定于供应商的内容）
* vendor specific  *特定于供应商
    * Shutdown  * 关掉
    * Hang/fault recovery  *挂起/故障恢复
* vkreadback  * vkreadback
    * Validates Vulkan end-to-end as simply as possible  *尽可能简单地验证Vulkan端到端
* vkloop  * vkloop
    * Validates hang detection and recovery  *验证挂起检测和恢复
* vkext  * vkext
    * Validates Fuchsia Vulkan extensions  *验证紫红色Vulkan扩展名
* [Vulkan CTS](https://github.com/KhronosGroup/VK-GL-CTS)  * [Vulkan CTS]（https://github.com/KhronosGroup/VK-GL-CTS）
    * Takes several hours to run  *需要几个小时才能运行
    * Should be run at least once a day  *应该每天至少运行一次
    * Vendor must be provided a build and test environment with which they can validate Vulkan CTS on Fuchsia  *必须为供应商提供构建和测试环境，以便他们可以在紫红色上验证Vulkan CTS

 
### Hardware required  所需硬件 

Fuchsia supports devices with the following gpus:  紫红色支持具有以下GPU的设备：

 
* Intel Gen 9 - Intel HD Graphics  * Intel Gen 9-英特尔高清显卡
* ARM Mali - Bifrost  * ARM马里-Bifrost
* Verisilicon GC7000  * Verisilicon GC7000

GPUs are complex pieces of hardware with flaws that may trigger misbehavior infrequently. There may be tests that flake rarely.  If detected these should be treated as driver bugs.  GPU是具有缺陷的复杂硬件，这些缺陷可能很少触发错误行为。可能有很少剥落的测试。如果检测到这些，应将其视为驱动程序错误。

 
## Performance Tests  性能测试 

 
* [Gfxbench](https://gfxbench.com)  * [Gfxbench]（https://gfxbench.com）
    * A large and complex performance benchmark.  *大型而复杂的性能基准。
    * Fuchsia details, forthcoming.  *紫红色细节，即将推出。

 
## See Also  也可以看看 
* [Contributing](contributing.md)  * [贡献]（contributing.md）

