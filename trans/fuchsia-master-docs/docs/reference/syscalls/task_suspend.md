 
# zx_task_suspend  zx_task_suspend 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Suspend the given task. Currently only thread or process handles may be suspended.  暂停给定的任务。当前，只有线程或进程句柄可以被挂起。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_task_suspend(zx_handle_t handle, zx_handle_t* token);
```
 

 
## DESCRIPTION  描述 

`zx_task_suspend()` causes the requested task to suspend execution. Task suspension is not synchronous and the task might notbe suspended before the call returns. The task will be suspended soonafter `zx_task_suspend()` is invoked, unless it is currently blocked inthe kernel, in which case it will suspend after being unblocked. zx_task_suspend（）使请求的任务暂停执行。任务挂起不是同步的，并且在调用返回之前任务可能不会挂起。该任务将在调用zx_task_suspend（）之后立即挂起，除非它当前在内核中被阻塞，在这种情况下它将在被解除阻塞后挂起。

Tasks can be suspended and/or resumed before they are started. If a task is started while suspended, it will enter suspension before executing any code.Similarly, starting a new thread on a suspended process will suspend the threadbefore it executes any code. 任务可以在开始之前被挂起和/或恢复。如果任务在挂起状态下启动，它将在执行任何代码之前进入挂起状态。类似地，在挂起的进程上启动新线程将在执行任何代码之前挂起该线程。

Invoking [`zx_task_kill()`] on a task that is suspended will successfully kill the task. 在被挂起的任务上调用[`zx_task_kill（）`]将成功杀死该任务。

A task cannot suspend itself or any of its parent tasks because it would never receive the suspend token and would be unable to resume execution. 任务无法挂起自身或其任何父任务，因为它永远不会收到挂起令牌并且将无法恢复执行。

 
## RESUMING  恢复 

The allow the task to resume, close the suspend token handle. The task will remain suspended as long as there are any open suspend tokens. Like suspending,resuming is asynchronous so the thread may not be in a running state when the[`zx_handle_close()`] call returns, even if no other suspend tokensare open. 允许任务恢复，关闭挂起令牌句柄。只要有任何打开的挂起令牌，任务将保持挂起状态。与挂起类似，恢复操作是异步的，因此即使没有打开其他挂起令牌，调用[zx_handle_close（）]返回时线程也可能不会处于运行状态。

 
## SIGNALS AND EXCEPTIONS  信号和例外 

There are two relevant signals that a thread can assert:  线程可以断言两个相关信号：

 
- **ZX_THREAD_RUNNING**  -** ZX_THREAD_RUNNING **
- **ZX_THREAD_SUSPENDED**  -** ZX_THREAD_SUSPENDED **

Neither of these will be asserted until the thread is started via [`zx_process_start()`] or [`zx_thread_start()`]. Whena thread starts, it will assert **ZX_THREAD_RUNNING** whether it is suspendedor not, but if it is suspended will then switch to **ZX_THREAD_SUSPENDED**before executing any code. 在通过[`zx_process_start（）]或[`zx_thread_start（）]启动线程之前，不会声明任何一个。当线程启动时，它将断言** ZX_THREAD_RUNNING **是否已挂起，但是如果被挂起，则将在执行任何代码之前切换到** ZX_THREAD_SUSPENDED **。

The **ZX_EXCP_PROCESS_STARTING** and **ZX_EXCP_THREAD_STARTING** debug exceptions will also be sent on start whether the task is suspended or not. 无论任务是否挂起，都将在启动时发送** ZX_EXCP_PROCESS_STARTING **和** ZX_EXCP_THREAD_STARTING **调试异常。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** or **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_THREAD **或** ZX_OBJ_TYPE_PROCESS **并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_task_suspend()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_task_suspend（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not a thread or process handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是线程或进程句柄。

**ZX_ERR_INVALID_ARGS**  *token*  was an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *令牌*是无效的指针。

**ZX_ERR_BAD_STATE**  The task is already dying or dead and cannot be suspended.  ** ZX_ERR_BAD_STATE **任务已经死亡或死亡，无法暂停。

**ZX_ERR_NO_MEMORY**  Failed to allocate memory.  ** ZX_ERR_NO_MEMORY **分配内存失败。

**ZX_ERR_NOT_SUPPORTED**  The calling thread is attempting to suspend itself or one of its parent tasks. ** ZX_ERR_NOT_SUPPORTED **调用线程正在尝试挂起自身或其父任务之一。

 
## LIMITATIONS  局限性 

Currently only thread and process handles are supported.  当前仅支持线程和进程句柄。

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

