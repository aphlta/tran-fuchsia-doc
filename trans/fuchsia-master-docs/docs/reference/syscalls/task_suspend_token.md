 
# zx_task_suspend_token  zx_task_suspend_token 

This function replaces [task_suspend](task_suspend.md). When all callers are updated, [`zx_task_suspend()`] will be deleted and this function will be renamed[`zx_task_suspend()`]. 此函数替换[task_suspend]（task_suspend.md）。更新所有调用方后，[`zx_task_suspend（）]将被删除，此函数将被重命名为[`zx_task_suspend（）]。

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Suspend the given task. Currently only thread or process handles may be suspended.  暂停给定的任务。当前，只有线程或进程句柄可以被挂起。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_task_suspend_token(zx_handle_t handle, zx_handle_t* token);
```
 

 
## DESCRIPTION  描述 

`zx_task_suspend_token()` causes the requested task to suspend execution. Task suspension is not synchronous and the task might not be suspended before thecall returns. The task will be suspended soon after `zx_task_suspend_token()` isinvoked, unless it is currently blocked in the kernel, in which case it willsuspend after being unblocked. zx_task_suspend_token（）使请求的任务挂起执行。任务挂起不是同步的，并且在调用返回之前任务可能不会挂起。调用`zx_task_suspend_token（）`之后，该任务将立即挂起，除非它当前已在内核中被阻塞，在这种情况下，它将在被解除阻塞后挂起。

Invoking [`zx_task_kill()`] on a task that is suspended will successfully kill the task. 在被挂起的任务上调用[`zx_task_kill（）`]将成功杀死该任务。

 
## RESUMING  恢复 

The allow the task to resume, close the suspend token handle. The task will remain suspended as long as there are any open suspend tokens. Like suspending,resuming is asynchronous so the thread may not be in a running state when the[`zx_handle_close()`] call returns, even if no other suspend tokensare open. 允许任务恢复，关闭挂起令牌句柄。只要有任何打开的挂起令牌，任务将保持挂起状态。与挂起类似，恢复操作是异步的，因此即使没有打开其他挂起令牌，调用[zx_handle_close（）]返回时线程也可能不会处于运行状态。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** or **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_THREAD **或** ZX_OBJ_TYPE_PROCESS **并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

[`zx_task_suspend()`] returns **ZX_OK** on success. In the event of failure, a negative error value is returned. [`zx_task_suspend（）`]成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not a thread handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是线程句柄。

**ZX_ERR_INVALID_ARGS**  *token*  was an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *令牌*是无效的指针。

**ZX_ERR_BAD_STATE**  The task is not in a state where suspending is possible.  ** ZX_ERR_BAD_STATE **任务未处于可以挂起的状态。

 
## LIMITATIONS  局限性 

Currently only thread handles are supported.  当前仅支持线程句柄。

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

