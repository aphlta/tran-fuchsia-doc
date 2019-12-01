 
# zx_exception_get_process  zx_exception_get_process 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a handle for the exception's process.  为异常的过程创建一个句柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_exception_get_process(zx_handle_t handle, zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

The exception process is only available for job and process exception channels, thread exceptions cannot access their parent process handles. 异常流程仅适用于作业和流程异常通道，线程异常无法访问其父流程句柄。

*handle* is the exception handle.  * handle *是异常句柄。

*out* will be filled with a new handle to the exception process. This handle will have the same rights as the task given to[`zx_task_create_exception_channel()`]. * out *将填充异常处理的新句柄。该句柄与赋予[`zx_task_create_exception_channel（）`]的任务具有相同的权限。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_EXCEPTION**.  **句柄*必须为** ZX_OBJ_TYPE_EXCEPTION **类型。

 
## RETURN VALUE  返回值 

`zx_exception_get_process()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_exception_get_process（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *handle* was received via a thread exception channel.  ** ZX_ERR_ACCESS_DENIED ** *句柄*是通过线程异常通道接收的。

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_NO_MEMORY**  Failed to allocate memory for a new handle.  ** ZX_ERR_NO_MEMORY **无法为新句柄分配内存。

**ZX_ERR_WRONG_TYPE**  *handle* is not an exception.  ** ZX_ERR_WRONG_TYPE ** *句柄*也不例外。

 
## SEE ALSO  也可以看看 

 
 - [exceptions](/docs/concepts/kernel/exceptions.md)  -[例外]（/ docs / concepts / kernel / exceptions.md）
 - [`zx_exception_get_thread()`]  -[`zx_exception_get_thread（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

