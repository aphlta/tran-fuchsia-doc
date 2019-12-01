 
# Zircon Kernel objects  锆石内核对象 

[TOC]  [目录]

Zircon is an object-based kernel. User mode code almost exclusively interacts with OS resources via object handles. A handle can be thought of as an activesession with a specific OS subsystem scoped to a particular resource. Zircon是基于对象的内核。用户模式代码几乎完全通过对象句柄与OS资源交互。可以将句柄视为具有特定OS子系统的活动会话，该OS子系统的作用域是特定资源。

Zircon actively manages the following resources:  Zircon积极管理以下资源：

 
+ processor time  +处理器时间
+ memory and address spaces  +内存和地址空间
+ device-io memory  + device-io内存
+ interrupts  +中断
+ signaling and waiting  +信号和等待

 
## Kernel objects for applications  应用程序的内核对象 

 
### IPC  IPC 
+ [Channel](/docs/concepts/objects/channel.md)  + [频道]（/ docs / concepts / objects / channel.md）
+ [Socket](/docs/concepts/objects/socket.md)  + [套接字]（/ docs / concepts / objects / socket.md）
+ [FIFO](/docs/concepts/objects/fifo.md)  + [FIFO]（/ docs / concepts / objects / fifo.md）

 
### Tasks  任务 
+ [Process](/docs/concepts/objects/process.md)  + [流程]（/ docs / concepts / objects / process.md）
+ [Thread](/docs/concepts/objects/thread.md)  + [线程]（/ docs / concepts / objects / thread.md）
+ [Job](/docs/concepts/objects/job.md)  + [工作]（/ docs / concepts / objects / job.md）
+ [Task](/docs/concepts/objects/task.md)  + [任务]（/ docs / concepts / objects / task.md）

 
### Scheduling  排程 
+ [Profile](/docs/concepts/objects/profile.md)  + [个人资料]（/ docs / concepts / objects / profile.md）

 
### Signaling  发信号 
+ [Event](/docs/concepts/objects/event.md)  + [事件]（/ docs / concepts / objects / event.md）
+ [Event Pair](/docs/concepts/objects/eventpair.md)  + [事件对]（/ docs / concepts / objects / eventpair.md）
+ [Futex](/docs/concepts/objects/futex.md)  + [Futex]（/ docs / concepts / objects / futex.md）

 
### Memory and address space  内存和地址空间 
+ [Virtual Memory Object](/docs/concepts/objects/vm_object.md)  + [虚拟内存对象]（/ docs / concepts / objects / vm_object.md）
+ [Virtual Memory Address Region](/docs/concepts/objects/vm_address_region.md)  + [虚拟内存地址区域]（/ docs / concepts / objects / vm_address_region.md）
+ [bus_transaction_initiator](/docs/concepts/objects/bus_transaction_initiator.md)  + [bus_transaction_initiator]（/ docs / concepts / objects / bus_transaction_initiator.md）
+ [Pager](/docs/concepts/objects/pager.md)  + [Pager]（/ docs / concepts / objects / pager.md）

 
### Waiting  等候 
+ [Port](/docs/concepts/objects/port.md)  + [端口]（/ docs / concepts / objects / port.md）
+ [Timer](/docs/concepts/objects/timer.md)  + [计时器]（/ docs / concepts / objects / timer.md）

 
## Kernel objects for drivers  驱动程序的内核对象 

 
+ [Interrupts](/docs/concepts/objects/interrupts.md)  + [中断]（/ docs / concepts / objects / interrupts.md）
+ [Resource](/docs/concepts/objects/resource.md)  + [资源]（/ docs / concepts / objects / resource.md）
+ [Debuglog](/docs/concepts/objects/debuglog.md)  + [Debuglog]（/ docs / concepts / objects / debuglog.md）

 
## Kernel Object and LK  内核对象和LKSome kernel objects wrap one or more LK-level constructs. For example the Thread object wraps one `thread_t`. However the Channel does not wrapany LK-level objects. 一些内核对象包装一个或多个LK级别的构造。例如，Thread对象包装了一个`thread_t`。但是，通道不会包装任何LK级别的对象。

 
## Kernel object lifetime  内核对象生存期Kernel objects are ref-counted. Most kernel objects are born during a syscall and are held alive at refcount = 1 by the handle which binds the handle valuegiven as the output of the syscall. The handle object is held alive as long itis attached to a handle table. Handles are detached from the handle tableclosing them (for example via `sys_close()`) which decrements the refcount ofthe kernel object. Usually, when the last handle is closed the kernel objectrefcount will reach 0 which causes the destructor to be run. 内核对象被引用计数。大多数内核对象是在系统调用期间生成的，并由句柄以refcount = 1保持活动状态，该句柄将给定的句柄值绑定为系统调用的输出。只要将其附着在手柄台上，就可以使手柄物体保持活动状态。从句柄表分离句柄，将它们关闭（例如通过sys_close（）），这会减少内核对象的引用计数。通常，当最后一个句柄关闭时，内核objectrefcount将达到0，这将导致析构函数运行。

The refcount increases both when new handles (referring to the object) are created and when a direct pointer reference (by some kernel code) is acquired;therefore a kernel object lifetime might be longer than the lifetime of theprocess that created it. 创建新的句柄（引用对象）和获取直接指针引用（通过某些内核代码）时，refcount都会增加；因此，内核对象的生存期可能比创建它的进程的生存期更长。

 
## Dispatchers  调度员A kernel object is implemented as a C++ class that derives from `Dispatcher` and that overrides the methods it implements. Thus, for example, the codeof the Thread object is found in `ThreadDispatcher`. There is plenty ofcode that only cares about kernel objects in the generic sense, in that casethe name you'll see is `fbl::RefPtr<Dispatcher>`. 内核对象被实现为C ++类，该类派生自Dispatcher并覆盖其实现的方法。因此，例如，在“ ThreadDispatcher”中可以找到Thread对象的代码。有很多代码只关心一般意义上的内核对象，在这种情况下，您将看到的名称是`fbl :: RefPtr <Dispatcher>。

 
## Kernel Object security  内核对象安全In principle, kernel objects do not have an intrinsic notion of security and do not do authorization checks; security rights are held by each handle. Asingle process can have two different handles to the same object withdifferent rights. 原则上，内核对象没有固有的安全性概念，也不进行授权检查。担保权由每个句柄持有。单个进程可以对具有不同权限的同一对象具有两个不同的句柄。

 
## See Also  也可以看看