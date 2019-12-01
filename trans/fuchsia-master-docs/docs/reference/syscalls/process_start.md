 
# zx_process_start  zx_process_start 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Start execution on a process.  开始在流程上执行。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_process_start(zx_handle_t handle,
                             zx_handle_t thread,
                             zx_vaddr_t entry,
                             zx_vaddr_t stack,
                             zx_handle_t arg1,
                             uintptr_t arg2);
```
 

 
## DESCRIPTION  描述 

`zx_process_start()` is similar to [`zx_thread_start()`], but is used for the purpose of starting the first thread in a process. zx_process_start（）与[`zx_thread_start（）`]类似，但用于启动进程中的第一个线程。

`zx_process_start()` causes a thread to begin execution at the program counter specified by *entry* and with the stack pointer set to *stack*.The arguments *arg1* and *arg2* are arranged to be in the architecturespecific registers used for the first two arguments of a function callbefore the thread is started.  All other registers are zero upon start. zx_process_start（）导致线程在* entry *指定的程序计数器处开始执行，并且堆栈指针设置为* stack *。* arg1 *和* arg2 *被安排在用于特定于体系结构的寄存器中在线程启动之前，函数调用的前两个参数。启动时所有其他寄存器均为零。

The first argument (*arg1*) is a handle, which will be transferred from the process of the caller to the process which is being started, and anappropriate handle value will be placed in arg1 for the newly startedthread. If `zx_process_start()` returns an error, *arg1* is closed ratherthan transferred to the process being started. 第一个参数（* arg1 *）是一个句柄，该句柄将从调用方的进程转移到正在启动的进程，并且将适当的句柄值放置在arg1中以用于新启动的线程。如果zx_process_start（）返回错误，则* arg1 *将关闭而不是转移到正在启动的进程中。

Alternatively, *arg1* can be **ZX_HANDLE_INVALID** instead of a handle. In this case the process starts with **ZX_HANDLE_INVALID** (i.e. zero)in its first argument register instead of a handle.  This means thereare *no* handles in the process and *can never* be any handles to anyobjects shared outside the process.  `zx_process_start()` is the onlyway to transfer a handle into a process that doesn't involve the processmaking some system call using a handle it already has (*arg1* is usuallythe "bootstrap" handle).  A process with no handles can make the fewsystem calls that don't require a handle, such as [`zx_process_exit()`],if it's been provided with a vDSO mapping.  It can create new kernelobjects with system calls that don't require a handle, such as[`zx_vmo_create()`], but there is no way to make use of those objectswithout more handles and no way to transfer them outside the process.Its only means of communication is via the memory mapped into itsaddress space by others. 另外，* arg1 *可以是** ZX_HANDLE_INVALID **而不是句柄。在这种情况下，该过程在其第一个参数寄存器而不是句柄中以** ZX_HANDLE_INVALID **（即零）开始。这意味着流程中没有“句柄”，并且“绝不能”是流程外部共享的任何对象的句柄。 zx_process_start（）是将句柄转移到不涉及使用已经拥有的句柄（* arg1 *通常是“ bootstrap”句柄）进行系统调用的过程的唯一方法。如果没有vDSO映射，则没有句柄的进程可以进行一些不需要句柄的系统调用，例如[`zx_process_exit（）]。它可以使用不需要句柄的系统调用来创建新的内核对象，例如[`zx_vmo_create（）]，但是没有更多的句柄就无法利用这些对象，也无法将它们转移到进程外。唯一的通信方式是通过其他人映射到其地址空间的内存。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_PROCESS **且具有** ZX_RIGHT_WRITE **。

*thread* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_WRITE**.  *线程*必须为** ZX_OBJ_TYPE_THREAD **类型，并具有** ZX_RIGHT_WRITE **。

*arg1* must have **ZX_RIGHT_TRANSFER**.  * arg1 *必须具有** ZX_RIGHT_TRANSFER **。

 
## RETURN VALUE  返回值 

`zx_process_start()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_process_start（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *process* or *thread* or *arg1* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *进程*或*线程*或* arg1 *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *process* is not a process handle or *thread* is not a thread handle. ** ZX_ERR_WRONG_TYPE ** * process *不是进程句柄或* thread *不是线程句柄。

**ZX_ERR_ACCESS_DENIED**  The handle *thread* lacks **ZX_RIGHT_WRITE** or *thread* does not belong to *process*, or the handle *process* lacks **ZX_RIGHT_WRITE** or*arg1* lacks **ZX_RIGHT_TRANSFER**. ** ZX_ERR_ACCESS_DENIED **句柄* thread *缺少** ZX_RIGHT_WRITE **或* thread *不属于* process *，或者句柄* process *缺少** ZX_RIGHT_WRITE **或* arg1 *缺少** ZX_RIGHT_TRANSFER ** 。

**ZX_ERR_BAD_STATE**  *process* is already running or has exited.  ** ZX_ERR_BAD_STATE ** *进程*已在运行或已退出。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_process_create()`]  -[`zx_process_create（）`]
 - [`zx_thread_create()`]  -[`zx_thread_create（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_thread_start()`]  -[`zx_thread_start（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

