 
# zx_interrupt_trigger  zx_interrupt_trigger 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Triggers a virtual interrupt object.  触发虚拟中断对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_trigger(zx_handle_t handle,
                                 uint32_t options,
                                 zx_time_t timestamp);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_trigger()` is used to trigger a virtual interrupt interrupt object, causing an interrupt message packet to arrive on the bound port, if it is boundto a port, or [`zx_interrupt_wait()`] to return if it is waiting on this interrupt. zx_interrupt_trigger（）用于触发虚拟中断中断对象，如果绑定到端口，则导致中断消息包到达绑定的端口；如果正在等待，则[zx_interrupt_wait（）]返回。打断。

*options* must be zero.  * options *必须为零。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_INTERRUPT** and have **ZX_RIGHT_SIGNAL**.  *句柄*的类型必须为** ZX_OBJ_TYPE_INTERRUPT **且具有** ZX_RIGHT_SIGNAL **。

 
## RETURN VALUE  返回值 

`zx_interrupt_trigger()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_interrupt_trigger（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an interrupt object.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是中断对象。

**ZX_ERR_BAD_STATE** *handle* is not a virtual interrupt.  ** ZX_ERR_BAD_STATE ** *句柄*不是虚拟中断。

**ZX_ERR_CANCELED**  [`zx_interrupt_destroy()`] was called on *handle*.  ** ZX_ERR_CANCELED ** [`zx_interrupt_destroy（）`]在*句柄*上被调用。

**ZX_ERR_ACCESS_DENIED** *handle* lacks **ZX_RIGHT_SIGNAL**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_SIGNAL **。

**ZX_ERR_INVALID_ARGS** *options* is non-zero.  ** ZX_ERR_INVALID_ARGS ** *选项*非零。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_ack()`]  -[`zx_interrupt_ack（）`]
 - [`zx_interrupt_bind()`]  -[`zx_interrupt_bind（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_interrupt_destroy()`]  -[`zx_interrupt_destroy（）`]
 - [`zx_interrupt_wait()`]  -[`zx_interrupt_wait（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

