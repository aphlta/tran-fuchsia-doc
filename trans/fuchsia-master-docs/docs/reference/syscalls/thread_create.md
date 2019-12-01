 
# zx_thread_create  zx_thread_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a thread.  创建一个线程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_thread_create(zx_handle_t process,
                             const char* name,
                             size_t name_size,
                             uint32_t options,
                             zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_thread_create()` creates a thread within the specified process.  zx_thread_create（）在指定进程内创建一个线程。

Upon success a handle for the new thread is returned.  The thread will not start executing until [`zx_thread_start()`] is called. 成功后，将返回新线程的句柄。直到调用[`zx_thread_start（）]，线程才会开始执行。

*name* is silently truncated to a maximum of `ZX_MAX_NAME_LEN-1` characters.  *名称*被无声地截断为最多ZZ_MAX_NAME_LEN-1个字符。

Thread handles may be waited on and will assert the signal **ZX_THREAD_TERMINATED** when the thread stops executing (due to[`zx_thread_exit()`] being called). 线程句柄可以等待，并在线程停止执行（由于调用[`zx_thread_exit（）]）时断言信号** ZX_THREAD_TERMINATED **。

*process* is the controlling [process object](/docs/concepts/objects/process.md) for the new thread, which will become a child of that process. * process *是新线程的控制[process object]（/ docs / concepts / objects / process.md），它将成为该进程的子级。

For thread lifecycle details see [thread object](/docs/concepts/objects/thread.md).  有关线程生命周期的详细信息，请参见[thread object]（/ docs / concepts / objects / thread.md）。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*process* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_MANAGE_THREAD**.  *处理*必须为** ZX_OBJ_TYPE_PROCESS **类型，并且具有** ZX_RIGHT_MANAGE_THREAD **。

 
## RETURN VALUE  返回值 

On success, `zx_thread_create()` returns **ZX_OK** and a handle (via *out*) to the new thread.  In the event of failure, a negative error value isreturned. 成功时，`zx_thread_create（）`将** ZX_OK **和句柄（通过* out *）返回到新线程。如果发生故障，则返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *process* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *进程*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *process* is not a process handle.  ** ZX_ERR_WRONG_TYPE ** *进程*不是进程句柄。

**ZX_ERR_ACCESS_DENIED**  *process* does not have the **ZX_RIGHT_MANAGE_THREAD** right.  ** ZX_ERR_ACCESS_DENIED ** *进程*没有** ZX_RIGHT_MANAGE_THREAD **权限。

**ZX_ERR_INVALID_ARGS**  *name* or *out* was an invalid pointer, or *options* was non-zero. ** ZX_ERR_INVALID_ARGS ** *名称*或*总分*是一个无效的指针，或者*选择*为非零。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_thread_start()`]  -[`zx_thread_start（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

