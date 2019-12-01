 
# zx_interrupt_wait  zx_interrupt_wait 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wait for an interrupt.  等待中断。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_wait(zx_handle_t handle, zx_time_t* out_timestamp);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_wait()` is a blocking syscall which causes the caller to wait until an interrupt is triggered.  It can only be used on interruptobjects that have not been bound to a port with [`zx_interrupt_bind()`] zx_interrupt_wait（）是一个阻塞的系统调用，它使调用者等待直到触发中断为止。它只能用于尚未使用[`zx_interrupt_bind（）`绑定到端口的中断对象

It also, before the waiting begins, will acknowledge the interrupt object, as if [`zx_interrupt_ack()`] were called on it. 在等待开始之前，它也将确认中断对象，就像在其上调用了[`zx_interrupt_ack（）`]一样。

The wait may be aborted with [`zx_interrupt_destroy()`] or by closing the handle.  可以通过[`zx_interrupt_destroy（）`]或通过关闭句柄来中止等待。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_INTERRUPT** and have **ZX_RIGHT_WAIT**.  *句柄*必须为** ZX_OBJ_TYPE_INTERRUPT **类型，并具有** ZX_RIGHT_WAIT **。

 
## RETURN VALUE  返回值 

`zx_interrupt_wait()` returns **ZX_OK** on success, and *out_timestamp*, if non-NULL, returns the timestamp of when the interrupt was triggered (relativeto **ZX_CLOCK_MONOTONIC**) zx_interrupt_wait（）成功返回** ZX_OK **，如果非NULL，则* out_timestamp *返回触发中断的时间戳（相对于** ZX_CLOCK_MONOTONIC **）

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not a handle to an interrupt object.  ** ZX_ERR_WRONG_TYPE ** * handle *不是中断对象的句柄。

**ZX_ERR_BAD_STATE** the interrupt object is bound to a port.  ** ZX_ERR_BAD_STATE **中断对象已绑定到端口。

**ZX_ERR_ACCESS_DENIED** *handle* lacks **ZX_RIGHT_WAIT**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_WAIT **。

**ZX_ERR_CANCELED**  *handle* was closed while waiting or [`zx_interrupt_destroy()`] was called on it. ** ZX_ERR_CANCELED ** *句柄*在等待时关闭，或者在其上调用了[`zx_interrupt_destroy（）`]。

**ZX_ERR_INVALID_ARGS** the *out_timestamp* parameter is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** * out_timestamp *参数是无效的指针。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_ack()`]  -[`zx_interrupt_ack（）`]
 - [`zx_interrupt_bind()`]  -[`zx_interrupt_bind（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_interrupt_destroy()`]  -[`zx_interrupt_destroy（）`]
 - [`zx_interrupt_trigger()`]  -[`zx_interrupt_trigger（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

