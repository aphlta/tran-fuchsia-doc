 
# Futex  Futex 

 
## NAME  名称 

futex - A primitive for creating userspace synchronization tools.  futex-用于创建用户空间同步工具的原语。

 
## SYNOPSIS  概要 

A **futex** is a Fast Userspace muTEX. It is a low level synchronization primitive which is a building block for higher levelAPIs such as `pthread_mutex_t` and `pthread_cond_t`. ** futex **是快速用户空间muTEX。它是一个低级同步原语，是高级API（例如pthread_mutex_t和pthread_cond_t）的构建块。

Futexes are designed to not enter the kernel or allocate kernel resources in the uncontested case. Futex被设计为在无争议的情况下不进入内核或分配内核资源。

 
## DESCRIPTION  描述 

The zircon futex implementation currently supports three operations distributed over 6 syscalls: Zircon futex实现当前支持分布在6个系统调用上的三个操作：

```C
    zx_status_t zx_futex_wait(const zx_futex_t* value_ptr,
                              zx_futex_t current_value,
                              zx_handle_t new_futex_owner,
                              zx_time_t deadline);
    zx_status_t zx_futex_wake(const zx_futex_t* value_ptr, uint32_t wake_count);
    zx_status_t zx_futex_wake_single_owner(const zx_futex_t* value_ptr);
    zx_status_t zx_futex_requeue(const zx_futex_t* value_ptr,
                                 uint32_t wake_count,
                                 zx_futex_t current_value,
                                 const zx_futex_t* requeue_ptr,
                                 uint32_t requeue_count,
                                 zx_handle_t new_requeue_owner);
    zx_status_t zx_futex_requeue_single_owner(const zx_futex_t* value_ptr,
                                              zx_futex_t current_value,
                                              const zx_futex_t* requeue_ptr,
                                              uint32_t requeue_count,
                                              zx_handle_t new_requeue_owner);
    zx_status_t zx_futex_get_owner(const zx_futex_t* value_ptr, uint64_t* koid);
```
 

All of these share a `value_ptr` parameter, which is the virtual address of an aligned userspace integer. This virtual address is theinformation used in kernel to track what futex given threads arewaiting on. The kernel does not currently modify the value of`*value_ptr` (but see below for future operations which might doso). It is up to userspace code to correctly atomically modify thisvalue across threads in order to build mutexes and so on. 所有这些共享一个“ value_ptr”参数，该参数是对齐的用户空间整数的虚拟地址。该虚拟地址是内核中用于跟踪给定线程正在等待的线程的信息。内核当前不修改* value_ptr的值（但请参阅下面的内容，以了解将来的操作）。用户空间代码可以正确地在各个线程之间原子地修改此值，以构建互斥体等。

See the [`zx_futex_wait()`], [`zx_futex_wake()`], [`zx_futex_requeue()`], and [`zx_futex_get_owner()`] man pages for more details. 有关更多详细信息，请参见[`zx_futex_wait（）`]，[`zx_futex_wake（）`]，[`zx_futex_requeue（）`]和[`zx_futex_get_owner（）`）手册页。

 
## RIGHTS  权利 

Futex objects do not have any rights associated with them.  Futex对象没有任何与之关联的权限。

There are only 2 primitive operations which userspace code can perform on a futex: waiting and waking (requeue is a combination of the two).  Becausefutexes are strictly a process local concept, revoking access to either of theseoperations would make the futex functionally worthless. 用户空间代码只能对futex执行两种基本操作：等待和唤醒（重新排队是两者的组合）。由于futex严格来说是过程本地的概念，因此撤销对这两个操作的访问将使futex在功能上一文不值。

Additionally, from the kernel's perspective, futexes are ephemeral objects whose state only exists while the futex has waiters.  Without a more durable statepresent in the kernel, it is more or less impossible to have a persisted conceptof rights for a futex. 另外，从内核的角度来看，futex是短暂的对象，其状态仅在futex具有服务员时才存在。如果在内核中没有更持久的状态，则持久地拥有futex的权利概念几乎是不可能的。

 
### Differences from Linux futexes  与Linux futexes的区别 

Note that all of the zircon futex operations key off of the virtual address of an userspace pointer. This differs from the Linuximplementation, which distinguishes private futex operations (whichcorrespond to our in-process-only ones) from ones shared acrossaddress spaces. 请注意，所有锆石futex操作都将用户空间指针的虚拟地址作为密钥。这与Linux实现不同，后者将私有futex操作（对应于我们仅进程内操作）与跨地址空间共享的操作区分开。

As noted above, all of our futex operations leave the value of the futex unmodified from the kernel. Other potential operations, such asLinux's `FUTEX_WAKE_OP`, requires atomic manipulation of the valuefrom the kernel, which our current implementation does not require. 如上所述，我们所有的futex操作都保留了内核未修改的futex值。其他可能的操作，例如Linux的“ FUTEX_WAKE_OP”，需要对内核中的值进行原子操作，而我们当前的实现并不需要这种操作。

 
### Ownership and Priority Inheritance  所有权和优先级继承 

 
#### Overview  总览 

Some runtimes may need to implement synchronization primitives based on futexes which exhibit priority inheritance behavior.  In order to support these users,zircon futexes have a concept of 'ownership' which can be used to implement suchprimitives.  Use of this feature is optional. 某些运行时可能需要基于展现优先级继承行为的futex实现同步原语。为了支持这些用户，锆石futex具有“所有权”的概念，可用于实现此类原语。此功能的使用是可选的。

At any point in time, a futex may be either unowned, or owned by a single thread.  When a thread owns one or more futexes, its effective priority becomesthe maximum of its base priority, and the priorities of all of the currentwaiters of all of the futexes currently owned by it.  As soon a thread no longerowns a futex, the pressure of the priorities of the futex's waiters disappearsfrom the relationship above.  Once the thread no longer owns any futexes, itspriority will relax back to its base priority. 在任何时间点，futex都可以是无主线程，也可以是由单个线程拥有。当一个线程拥有一个或多个futex时，其有效优先级将变为其基本优先级的最大值，以及该线程当前拥有的所有futex的所有当前等待者的优先级。线程不再拥有futex时，futex服务员的优先级压力就从上述关系中消失了。一旦线程不再拥有任何futex，其优先级将放回到其基本优先级。

Signaling of the owner of a futex is the responsibility of the userspace code, as is applying the ownership concept properly when constructing a specific typeof synchronization object which needs priority inheritance behavior. futex所有者的信号是用户空间代码的责任，在构造需要优先级继承行为的特定类型的同步对象时，正确应用所有权概念也是如此。

Zircon futexes have at most a single owner.  Multiple ownership of futexes for the purpose of priority inheritance is not supported.  The owner of a futex maynever simultaneously be a waiter for the same futex. 锆石futex最多只有一个所有者。不支持出于优先级继承目的对futex进行多重所有权。一个futex的所有者可能永远不会同时是同一futex的服务员。

 
#### Assigning Ownership  分配所有权 

Ownership of a futex is assigned via each 'wait' or 'requeue' operation.  In the case of a requeue operation, the target futex is the requeue futex, not thewake_futex.  Users pass a handle to a thread indicating who the current owner ofthe futex should be, or **ZX_HANDLE_INVALID** if there should be no owner. futex的所有权是通过每个“ wait”或“ requeue”操作分配的。在重新排队操作的情况下，目标futex是重新排队futex，而不是thewake_futex。用户将一个句柄传递给一个线程，该线程指示该futex的当前所有者是谁，如果没有所有者，则为** ZX_HANDLE_INVALID **。

 
+ Passing a valid handle to a thread to indicate the futex owner is the responsibility of the userspace code.  Passing an invalid handle, or a handleto a non-thread object will result in the wait/requeue operation failing. +将有效的句柄传递给线程以指示futex所有者是用户空间代码的责任。传递无效的句柄或传递给非线程对象的句柄将导致等待/重新排队操作失败。
+ If the wait/requeue operation succeeds, the owner of the target futex will _always_ be set to either the thread specified, or nothing if**ZX_HANDLE_INVALID** is passed. +如果等待/排队操作成功，则目标futex的所有者将始终设置为指定的线程，或者如果传递** ZX_HANDLE_INVALID **则不设置任何线程。
+ In particular, if the wait/requeue operation fails because of a mismatch between the expected futex value and the actual futex value, the owner of thefutex will remain unchanged and the status code for the operation will beZX_ERR_BAD_STATE. This error code will be returned regardless of the valuepassed for handle indicating ownership, even if the value passed would haveresulted in a status of ZX_ERR_BAD_HANDLE being returned. +特别是，如果由于预期的futex值和实际的futex值之间不匹配而导致等待/排队操作失败，则thefutex的所有者将保持不变，并且该操作的状态码将为ZX_ERR_BAD_STATE。不管传递的用于指示所有权的句柄值如何，都将返回此错误代码，即使传递的值将导致返回ZX_ERR_BAD_HANDLE状态。

 
#### Transferring Ownership  所有权转移 

Ownership of a futex may be transferred by the kernel on behalf of the user during a wake operation or a requeue operation.  In the case of a requeueoperation, the target of the transfer is the wake_futex, not the requeue_futex.Ownership transfer only takes place when using the[`zx_futex_wake_single_owner()`] or [`zx_futex_requeue_single_owner()`]variants of the wake/requeue operations.  The `single_owner` variants ofthese operations will release exactly one waiter, andassign ownership of the futex to the released thread. 内核可以在唤醒操作或重新排队操作期间代表用户转让futex的所有权。在重新排队操作的情况下，转移的目标是wake_futex，而不是requeue_futex。所有权转移仅在使用唤醒/重新排队操作的[`zx_futex_wake_single_owner（）`]或[`zx_futex_requeue_single_owner（）`]变体时发生。这些操作的“ single_owner”变体将恰好释放一个侍者，并将futex的所有权分配给释放的线程。

 
+ If there are _no_ waiters during the wake operation, then there is already no owner.  This will remain unchanged. +如果在唤醒操作期间有_no_个服务员，则已经没有所有者。这将保持不变。
+ If a requeue operation fails because of a mismatch between the expected futex value and the actual futex value, the owner of the futex will remainunchanged. +如果由于预期futex值与实际futex值之间的不匹配而导致重新排队操作失败，则futex的所有者将保持不变。
+ A successful call to either of the non-single_owner variants of the wake/requeue operation will cause the target futex's owner to be set tonothing. +成功调用唤醒/重新排队操作的non-single_owner变体中的任何一个，将导致目标futex的所有者被设置为空。

 
### Papers about futexes  关于futex的论文 

 
- [Fuss, Futexes and Furwocks: Fast Userlevel Locking in Linux](https://www.kernel.org/doc/ols/2002/ols2002-pages-479-495.pdf), Hubertus Franke and Rusty Russell  -[Fuss，Futexes和Furwocks：Linux中的快速用户级锁定]（https://www.kernel.org/doc/ols/2002/ols2002-pages-479-495.pdf），Hubertus Franke和Rusty Russell

    This is the original white paper describing the Linux futex. It documents the history and design of the original implementation,prior (failed) attempts at creating a fast userspacesynchronization primitive, and performance measurements. 这是描述Linux futex的原始白皮书。它记录了原始实现的历史和设计，先前（失败的）尝试创建快速用户空间同步原语的尝试以及性能评估。

 
- [Futexes Are Tricky](https://www.akkadia.org/drepper/futex.pdf), Ulrich Drepper  -[Futexes是棘手的]（https://www.akkadia.org/drepper/futex.pdf），Ulrich Drepper

    This paper describes some gotchas and implementation details of futexes in Linux. It discusses the kernel implementation, and goesinto more detail about correct and efficient userspaceimplementations of mutexes, condition variables, and so on. 本文介绍了Linux中futex的一些陷阱和实现细节。它讨论了内核实现，并详细介绍了互斥量，条件变量等的正确有效的用户空间实现。

 
- [Mutexes and Condition Variables using Futexes](http://locklessinc.com/articles/mutex_cv_futex/)  -[使用Futex的Mutex和条件变量]（http://locklessinc.com/articles/mutex_cv_futex/）

    Further commentary on "Futexes are tricky", outlining a simple implementation that avoids the need for `FUTEX_CMP_REQUEUE` 有关“ Futexes棘手”的更多评论，概述了避免使用FUTEX_CMP_REQUEUE的简单实现。

 
- [Locking in WebKit](https://webkit.org/blog/6161/locking-in-webkit/), Filip Pizlo  -[锁定WebKit]（https://webkit.org/blog/6161/locking-in-webkit/），Filip Pizlo

    An in-depth tour of the locking primitives in WebKit, complete with benchmarks and analysis. Contains a detailed explanation of the "parkinglot" concept, which allows very compact representation of userspacemutexes. 深入介绍WebKit中的锁定原语，并提供基准测试和分析。包含对“ parkinglot”概念的详细说明，该概念允许非常紧凑地表示用户空间互斥量。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_futex_wait()`]  -[`zx_futex_wait（）`]
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]
 - [`zx_futex_requeue()`]  -[`zx_futex_requeue（）`]
 - [`zx_futex_get_owner()`]  -[`zx_futex_get_owner（）`]

