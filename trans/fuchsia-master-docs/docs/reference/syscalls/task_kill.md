 
# zx_task_kill  zx_task_kill 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Kill the provided task (job, process, or thread).  杀死提供的任务（作业，进程或线程）。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_task_kill(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

This asynchronously kills the given process, thread or job and its children recursively, until the entire task tree rooted at *handle* is dead. 这将以异步方式杀死给定的进程，线程或作业及其子级，直到以* handle *为根的整个任务树都消失了。

It is possible to wait for the task to be dead via the **ZX_TASK_TERMINATED** signal. When the procedure completes, as observed by the signal, the task andall its children are considered to be in the dead state and most operationswill no longer succeed. 可以通过** ZX_TASK_TERMINATED **信号等待任务终止。当程序完成时，如信号所示，该任务及其所有子级都被视为处于死状态，大多数操作将不再成功。

If *handle* is a job and the syscall is successful, the job cannot longer be used to create new processes. 如果* handle *是一个作业，并且系统调用成功，则该作业不能再用于创建新进程。

When a process or job is killed via this syscall, the `return_code` is **ZX_TASK_RETCODE_SYSCALL_KILL** as reported by [`zx_object_get_info()`] viathe **ZX_INFO_PROCESS** or **ZX_INFO_JOB** topic. 通过此系统调用杀死进程或作业时，return_code是ZX_TASK_RETCODE_SYSCALL_KILL，如[zx_object_get_info（）]通过** ZX_INFO_PROCESS **或** ZX_INFO_JOB **主题报告的那样。

Processes and Jobs can also be killed by other agents such as the Job policy with **ZX_POL_ACTION_KILL** or when the system is running low on memory [OOM](/docs/development/memory/oom.md). 进程和作业也可以被其他代理杀死，例如带有** ZX_POL_ACTION_KILL **的作业策略，或者当系统内存不足[OOM]（/ docs / development / memory / oom.md）时终止。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_DESTROY**.  *句柄*必须具有** ZX_RIGHT_DESTROY **。

 
## RETURN VALUE  返回值 

On success, `zx_task_kill()` returns **ZX_OK**. If a process or thread uses this syscall to kill itself, this syscall does not return. 成功时，`zx_task_kill（）`返回** ZX_OK **。如果进程或线程使用此syscall杀死自己，则此syscall不会返回。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a task handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是任务句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have the **ZX_RIGHT_DESTROY** right. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_DESTROY **权限。

 
## SEE ALSO  也可以看看 

 
 - [`zx_job_create()`]  -[`zx_job_create（）`]
 - [`zx_process_create()`]  -[`zx_process_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

