 
# zx_interrupt_destroy  zx_interrupt_destroy 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Destroys an interrupt object.  销毁一个中断对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_destroy(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_destroy()` "destroys" an interrupt object, putting it in a state where any [`zx_interrupt_wait()`] operations on it will return **ZX_ERR_CANCELED**,and it is unbound from any ports it was bound to. `zx_interrupt_destroy（）`“销毁”一个中断对象，使其处于一种状态，在该状态下，对它的任何[`zx_interrupt_wait（）`）操作都将返回** ZX_ERR_CANCELED **，并且它不受绑定到的任何端口的约束。

This provides a clean shut down mechanism.  Closing the last handle to the interrupt object results in similar cancellation but could result in use-after-closeof the handle. 这提供了干净的关闭机制。关闭中断对象的最后一个句柄会导致类似的取消，但可能导致句柄的使用后关闭。

If the interrupt object is bound to a port when cancellation happens, if it has not yet triggered, or it has triggered but the packet has not yet beenreceived by a caller of [`zx_port_wait()`], success is returned and any packetsin flight are removed.  Otherwise, **ZX_ERR_NOT_FOUND** is returned, indicatingthat the packet has been read but the interrupt has not been re-armed by calling[`zx_interrupt_ack()`]. 如果在取消发生时中断对象绑定到端口，如果尚未触发，或者触发了触发对象，但是调用方[`zx_port_wait（）]尚未接收到数据包，则返回成功，并且所有数据包都在传输中被删除。否则，返回** ZX_ERR_NOT_FOUND **，表示已读取数据包，但尚未通过调用[`zx_interrupt_ack（）]重新设防该中断。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_interrupt_destroy()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_interrupt_destroy（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an interrupt object.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是中断对象。

**ZX_ERR_NOT_FOUND**  *handle* was bound (and now no longer is) but was not being waited for. ** ZX_ERR_NOT_FOUND ** *句柄*已绑定（现在不再绑定），但未等待。

**ZX_ERR_ACCESS_DENIED** *handle* lacks **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_WRITE **。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_ack()`]  -[`zx_interrupt_ack（）`]
 - [`zx_interrupt_bind()`]  -[`zx_interrupt_bind（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_interrupt_trigger()`]  -[`zx_interrupt_trigger（）`]
 - [`zx_interrupt_wait()`]  -[`zx_interrupt_wait（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

