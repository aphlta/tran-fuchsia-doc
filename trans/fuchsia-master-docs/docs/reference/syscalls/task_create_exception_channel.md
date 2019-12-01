 
# zx_task_create_exception_channel  zx_task_create_exception_channel 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create an exception channel for a given job, process, or thread.  为给定的作业，流程或线程创建异常通道。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_task_create_exception_channel(zx_handle_t handle,
                                             uint32_t options,
                                             zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_task_create_exception_channel()` creates a channel which will receive exceptions from the thread, process, or job. zx_task_create_exception_channel（）创建一个通道，该通道将从线程，进程或作业中接收异常。

*handle* is the thread, process, or job handle to receive exceptions from.  * handle *是用于接收异常的线程，进程或作业句柄。

*options* can be 0 or **ZX_EXCEPTION_CHANNEL_DEBUGGER** to register for debug exceptions (process or job only). * options *可以为0或** ZX_EXCEPTION_CHANNEL_DEBUGGER **以注册调试异常（仅适用于进程或作业）。

*out* will be filled with the newly created channel endpoint on success. This channel will be read-only with the following rights: 成功时，* out *将被新创建的通道端点填充。该频道将是只读的，具有以下权限：

 
* **ZX_RIGHT_TRANSFER**  * ** ZX_RIGHT_TRANSFER **
* **ZX_RIGHT_WAIT**  * ** ZX_RIGHT_WAIT **
* **ZX_RIGHT_READ**  * ** ZX_RIGHT_READ **

 
### Exception Messages  异常消息 

When an exception occurs, the channel will receive a message containing one exception handle and one `zx_exception_info_t` data. 发生异常时，通道将收到一条消息，其中包含一个异常句柄和一个`zx_exception_info_t`数据。

The thread will remain blocked in the exception until the received exception handle is closed, at which point it will either resume or exception processingwill continue according to the chosen behavior (see **ZX_PROP_EXCEPTION_STATE**in [`zx_object_get_property()`]). 线程将在异常中保持阻塞状态，直到关闭接收到的异常句柄为止，这时该线程将恢复或根据所选行为继续进行异常处理（请参阅[`zx_object_get_property（）]中的** ZX_PROP_EXCEPTION_STATE **）。

 
### Unbinding  解除绑定 

Closing the created channel handle will unregister the exception handler. If an exception message is waiting in the channel at the time it's closed, exceptionhandling will continue on to the next handler in the search order. 关闭创建的通道句柄将取消注册异常处理程序。如果异常消息在关闭时正在通道中等待，则异常处理将继续搜索顺序中的下一个处理程序。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_INSPECT** and have **ZX_RIGHT_DUPLICATE** and have **ZX_RIGHT_TRANSFER** and have **ZX_RIGHT_MANAGE_THREAD**.  *句柄*必须具有** ZX_RIGHT_INSPECT **且具有** ZX_RIGHT_DUPLICATE **且具有** ZX_RIGHT_TRANSFER **且具有** ZX_RIGHT_MANAGE_THREAD **。

If *handle* is of type **ZX_OBJ_TYPE_JOB** or **ZX_OBJ_TYPE_PROCESS**, it must have **ZX_RIGHT_ENUMERATE**.  如果* handle *类型为** ZX_OBJ_TYPE_JOB **或** ZX_OBJ_TYPE_PROCESS **，则它必须具有** ZX_RIGHT_ENUMERATE **。

 
## RETURN VALUE  返回值 

`zx_task_create_exception_channel()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_task_create_exception_channel（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** The caller has a job policy in place preventing the creation of new channels. ** ZX_ERR_ACCESS_DENIED **呼叫者已制定工作策略，以防止创建新渠道。

**ZX_ERR_ALREADY_BOUND** *handle* is already bound to an exception channel.  ** ZX_ERR_ALREADY_BOUND ** *句柄*已绑定到异常通道。

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_BAD_STATE** *handle* is dying or dead.  ** ZX_ERR_BAD_STATE ** *句柄*垂死或死亡。

**ZX_ERR_INVALID_ARGS** A bad value has been passed in *options*.  ** ZX_ERR_INVALID_ARGS ** *选项*中传递了错误的值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_WRONG_TYPE**  *handle* is not that of a job, process, or thread.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是作业，进程或线程的句柄。

 
## SEE ALSO  也可以看看 

 
 - [exceptions](/docs/concepts/kernel/exceptions.md)  -[例外]（/ docs / concepts / kernel / exceptions.md）
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

