 
# Fuchsia is not Linux  紫红色不是Linux_A modular, capability-based operating system_  _基于功能的模块化操作系统_

This document is a collection of articles describing the Fuchsia operating system, organized around particular subsystems. Sections will be populated over time. 该文档是围绕特定子系统组织的描述Fuchsia操作系统的文章的集合。随着时间的推移，将填充各个部分。

[TOC]  [目录]

 
## Zircon Kernel  锆石内核 

Zircon is the microkernel underlying the rest of Fuchsia. Zircon also provides core drivers and Fuchsia's libc implementation. 锆石是紫红色其余部分的微内核。 Zircon还提供了核心驱动程序和Fuchsia的libc实现。

 
 - [Concepts][zircon-concepts]  -[概念] [锆石概念]
 - [System Calls][zircon-syscalls]  -[系统调用] [zircon-syscalls]
 - [vDSO (libzircon)][zircon-vdso]  -[vDSO（libzircon）] [zircon-vdso]

 
## Zircon Core  锆石核心 

 
 - Device Manager & Device Hosts  -设备管理器设备主机
 - [Device Driver Model (DDK)][zircon-ddk]  -[设备驱动程序模型（DDK）] [zircon-ddk]
 - [C Library (libc)](/docs/concepts/system/libc.md)  -[C库（libc）]（/ docs / concepts / system / libc.md）
 - [POSIX I/O (libfdio)](/docs/concepts/system/life_of_an_open.md)  -[POSIX I / O（libfdio）]（/ docs / concepts / system / life_of_an_open.md）
 - [Process Creation](/docs/concepts/booting/process_creation.md)  -[流程创建]（/ docs / concepts / booting / process_creation.md）

 
## Framework  构架 

 
 - [Overview][framework-overview]  -[概述] [框架概述]
 - [Core Libraries](/docs/concepts/framework/core_libraries.md)  -[核心库]（/ docs / concepts / framework / core_libraries.md）
 - Application model  -应用模式
   - [Interface definition language (FIDL)][FIDL]  -[接口定义语言（FIDL）] [FIDL]
   - Services  - 服务
   - Environments  -环境
 - [Boot sequence](/docs/concepts/framework/boot_sequence.md)  -[启动顺序]（/ docs / concepts / framework / boot_sequence.md）
 - Device, user, and story runners  -设备，用户和故事执行者
 - Components  - 组件
 - [Namespaces](/docs/concepts/framework/namespaces.md)  -[命名空间]（/ docs / concepts / framework / namespaces.md）
 - [Sandboxing](/docs/concepts/framework/sandboxing.md)  -[沙箱]（/ docs / concepts / framework / sandboxing.md）
 - [Story][framework-story]  -[故事] [框架故事]
 - [Module][framework-module]  -[模块] [框架模块]
 - [Agent][framework-agent]  -[代理商] [框架代理]

 
## Storage  存储 

 
 - [Block devices](/docs/concepts/storage/block_devices.md)  -[阻止设备]（/ docs / concepts / storage / block_devices.md）
 - [File systems](/docs/concepts/storage/filesystems.md)  -[文件系统]（/ docs / concepts / storage / filesystems.md）
 - Directory hierarchy  -目录层次
 - [Ledger][ledger]  -[分类帐] [分类帐]
 - Document store  -文件存储
 - Application cache  -应用程序缓存

 
## Networking  联网 

 
 - Ethernet  -以太网
 - [Wireless](/docs/concepts/networking/wireless_networking.md)  -[无线]（/ docs / concepts / networking / wireless_networking.md）
 - [Bluetooth](/docs/concepts/networking/bluetooth_architecture.md)  -[蓝牙]（/ docs / concepts / networking / bluetooth_architecture.md）
 - [Telephony][telephony]  -[电话] [电话]
 - Sockets  -插座
 - HTTP  -HTTP

 
## Graphics  图形 

 
 - [UI Overview][ui-overview]  -[UI概述] [ui-overview]
 - [Magma (vulkan driver)][magma]  -[岩浆（vulkan驱动程序）] [岩浆]
 - [Escher (physically-based renderer)][escher]  -[Escher（基于物理的渲染器）] [escher]
 - [Scenic (compositor)][scenic]  -[风景（合成器）] [风景]
 - [Input manager][input-manager]  -[输入管理器] [输入管理器]
 - [Flutter (UI toolkit)][flutter]  -[Flutter（UI工具包）] [flutter]

 
## Components  组件 

 
 - [Component framework](/docs/concepts/components/README.md)  -[组件框架]（/ docs / concepts / components / README.md）

 
## Media  媒体 

 
 - Audio  -音讯
 - Video  - 视频
 - DRM  -DRM

 
## Intelligence  情报 

 
 - Context  -上下文
 - Agent Framework  -代理框架
 - Suggestions  -建议

 
## User interface  用户界面 

 
 - Device, user, and story shells  -设备，用户和故事外壳
 - Stories and modules  -故事和模块

 
## Backwards compatibility  向后兼容 

 
 - POSIX lite (what subset of POSIX we support and why)  -POSIX lite（我们支持POSIX的哪些子集以及原因）
 - Web runtime  -Web运行时

 
## Update and recovery  更新和恢复 

 
 - [Software Update System][software-update-system]  -[软件更新系统] [软件更新系统]
 - Verified boot  -验证启动
 - Updater  -更新器

