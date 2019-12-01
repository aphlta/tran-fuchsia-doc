 
# zx_process_create  zx_process_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a new process.  创建一个新的过程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_process_create(zx_handle_t job,
                              const char* name,
                              size_t name_size,
                              uint32_t options,
                              zx_handle_t* proc_handle,
                              zx_handle_t* vmar_handle);
```
 

 
## DESCRIPTION  描述 

`zx_process_create()` creates a new process.  zx_process_create（）创建一个新进程。

Upon success, handles for the new process and the root of its address space are returned.  The thread will not start executing until [`zx_process_start()`] iscalled. 成功后，将返回新进程的句柄及其地址空间的根。直到调用[`zx_process_start（）]，线程才会开始执行。

*name* is silently truncated to a maximum of `ZX_MAX_NAME_LEN-1` characters.  *名称*被无声地截断为最多ZZ_MAX_NAME_LEN-1个字符。

When the last handle to a process is closed, the process is destroyed.  当进程的最后一个句柄关闭时，该进程将被销毁。

Process handles may be waited on and will assert the signal **ZX_PROCESS_TERMINATED** when the process exits. 进程句柄可以等待，并在进程退出时声明信号** ZX_PROCESS_TERMINATED **。

*job* is the controlling [job object](/docs/concepts/objects/job.md) for the new process, which will become a child of that job. * job *是新流程的控制[job object]（/ docs / concepts / objects / job.md），它将成为该作业的子级。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*job* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_MANAGE_PROCESS**.  * job *必须为** ZX_OBJ_TYPE_JOB **类型，并且必须为** ZX_RIGHT_MANAGE_PROCESS **。

 
## RETURN VALUE  返回值 

On success, `zx_process_create()` returns **ZX_OK**, a handle to the new process (via *proc_handle*), and a handle to the root of its address space (via*vmar_handle*).  In the event of failure, a negative error value is returned. 成功后，`zx_process_create（）`返回** ZX_OK **，新进程的句柄（通过* proc_handle *）和其地址空间根的句柄（通过* vmar_handle *）。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *job* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * job *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *job* is not a job handle.  ** ZX_ERR_WRONG_TYPE ** * job *不是作业句柄。

**ZX_ERR_ACCESS_DENIED**  *job* does not have the **ZX_RIGHT_WRITE** right (only when not **ZX_HANDLE_INVALID**). ** ZX_ERR_ACCESS_DENIED ** *工作*没有** ZX_RIGHT_WRITE **权限（仅当没有** ZX_HANDLE_INVALID **时）。

**ZX_ERR_INVALID_ARGS**  *name*, *proc_handle*, or *vmar_handle*  was an invalid pointer, or *options* was non-zero. ** ZX_ERR_INVALID_ARGS ** * name *，* proc_handle *或* vmar_handle *是无效的指针，或* options *非零。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BAD_STATE**  The job object is in the dead state.  ** ZX_ERR_BAD_STATE **作业对象处于失效状态。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_job_create()`]  -[`zx_job_create（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_process_start()`]  -[`zx_process_start（）`]
 - [`zx_task_kill()`]  -[`zx_task_kill（）`]
 - [`zx_thread_create()`]  -[`zx_thread_create（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_thread_start()`]  -[`zx_thread_start（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

