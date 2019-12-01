 
# Fuchsia Rust Crates  紫红色的锈条板箱 

 
* [fdio/](/garnet/public/rust/fdio/)  * [fdio /]（/石榴石/公共/铁锈/ fdio /）

    Wrapper over zircon-fdio library  Zircon-Fdio库上的包装

 
* [fuchsia-archive/](/garnet/public/rust/fuchsia-archive/)  * [紫红色档案/]（/石榴石/公共/铁锈/紫红色档案/）

    Work with Fuchsia Archives (FARs)  与紫红色档案馆（FAR）合作

 
* [fuchsia-async/](/garnet/public/rust/fuchsia-async/)  * [紫红色异步/]（/石榴石/公共/铁锈/紫红色异步/）

    Fuchsia-specific Futures executor and asynchronous primitives (Channel, Socket, Fifo, etc.)  紫红色特定的期货执行器和异步原语（通道，套接字，Fifo等）

 
* [fuchsia-device/](/garnet/public/rust/fuchsia-device/)  * [紫红色装置/]（/石榴石/公共/铁锈/紫红色装置/）

    Rust bindings to common Fuchsia device libraries  锈绑定到常见的Fuchsia设备库

 
* [fuchsia-framebuffer/](/garnet/public/rust/fuchsia-framebuffer/)  * [紫红色帧缓冲区​​/]（/石榴石/公共/铁锈/紫红色帧缓冲区​​/）

    Configure, create and use FrameBuffers in Fuchsia  在紫红色中配置，创建和使用FrameBuffers

 
* [fuchsia-merkle/](/garnet/public/rust/fuchsia-merkle/)  * [倒挂金钟/]（/石榴石/公共/锈/倒挂金钟/）

    Protect and verify data blobs using [Merkle Trees](/docs/concepts/storage/merkleroot.md)  使用[Merkle树]保护和验证数据Blob（/docs/concepts/storage/merkleroot.md）

 
* [fuchsia-scenic/](/garnet/public/rust/fuchsia-scenic/)  * [紫红色场景/]（/石榴石/公共/锈/紫红色场景/）

    Rust interface to Scenic, the Fuchsia compositor  紫红色合成器Scenic的Rust接口

 
* [fuchsia-syslog-listener/](/garnet/public/rust/fuchsia-syslog-listener/)  * [紫红色syslog-listener /]（/ garnet / public / rust /紫红色syslog-listener /）

    Implement fuchsia syslog listeners in Rust  在Rust中实现紫红色的syslog监听器

 
* [fuchsia-syslog/](/garnet/public/rust/fuchsia-syslog/)  * [fuchsia-syslog /]（/ garnet / public / rust / fuchsia-syslog /）

    Rust interface to the fuchsia syslog  紫红色系统日志的Rust接口

 
* [fuchsia-system-alloc/](/garnet/public/rust/fuchsia-system-alloc/)  * [fuchsia-system-alloc /]（/ garnet / public / rust / fuchsia-system-alloc /）

    A crate that sets the Rust allocator to the system allocator. This is automatically included for projects that use fuchsia-async, and all Fuchsia binaries should ensure that they take a transitive dependency on this crate (and “use” it, as merely setting it as a dependency in GN is not sufficient to ensure that it is linked in).  一个将Rust分配器设置为系统分配器的板条箱。对于使用fuchsia-async的项目，这会自动包括在内，并且所有的Fuchsia二进制文件都应确保对此板条箱具有传递性依赖关系（并“使用”它，因为仅将其设置为GN中的依赖项不足以确保它已链接）。

 
* [fuchsia-trace/](/garnet/public/rust/fuchsia-trace/)  * [紫红色痕迹/]（/石榴石/公共/锈/紫红色痕迹/）

    A safe Rust interface to Fuchsia's tracing interface  安全的Rust界面到Fuchsia的跟踪界面

 
* [fuchsia-vfs/](/garnet/public/rust/fuchsia-vfs/)  * [紫红色vfs /]（/石榴石/公共/铁锈/紫红色vfs /）

    Bindings and protocol for serving filesystems on the Fuchsia platform  在Fuchsia平台上服务文件系统的绑定和协议

 
* [fuchsia-vfs/fuchsia-vfs-watcher/](/garnet/public/rust/fuchsia-vfs/fuchsia-vfs-watcher/)  * [紫红色vfs /紫红色vfs-watcher /]（/石榴石/公共/锈/紫红色vfs /紫红色vfs-watcher /）

    Bindings for watching a directory for changes  监视目录更改的绑定

 
* [fuchsia-zircon/](/garnet/public/rust/fuchsia-zircon/)  * [紫红色锆石/]（/石榴石/公共/锈/紫红色锆石/）

    Rust language bindings for Zircon kernel syscalls  Zircon内核syscall的Rust语言绑定

 
* [mapped-vmo/](/src/lib/mapped-vmo/)  * [mapped-vmo /]（/ src / lib / mapped-vmo /）

    A convenience crate for Zircon VMO objects mapped into memory  Zircon VMO对象映射到内存的便利箱

 
* [mundane/](/garnet/public/rust/mundane/)  * [平凡/]（/石榴石/公共/铁锈/平凡/）

    A Rust crypto library backed by BoringSSL  由BoringSSL支持的Rust加密库

 
* [shared-buffer/](/src/lib/shared-buffer/)  * [共享缓冲区/]（/ src / lib /共享缓冲区/）

    Utilities for safely operating on memory shared between untrusting processes  在不信任进程之间共享的内存上安全运行的实用程序

 
* [zerocopy/](/garnet/public/rust/zerocopy/)  * [zerocopy /]（/ garnet / public / rust / zerocopy /）

