 
# zx_interrupt_ack  zx_interrupt_ack 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Acknowledge an interrupt and re-arm it.  确认中断并重新布防。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_ack(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_ack()` acknowledges an interrupt object, causing it to be eligible to trigger again (and delivering a packet to the port it is bound to). zx_interrupt_ack（）确认一个中断对象，使其有资格再次触发（并将数据包传递到其绑定的端口）。

If the interrupt object is a physical interrupt, if it is a level interrupt and still asserted, or is an edge interrupt that has been asserted since it lasttriggered, the interrupt will trigger immediately, delivering a packet to theport it is bound to. 如果中断对象是物理中断，或者是级别中断且仍被断言，或者是自上次触发以来已被断言的边沿中断，则该中断将立即触发，将数据包传递到其绑定的端口。

Virtual interrupts behave as edge interrupts.  虚拟中断的行为就像边缘中断。

This syscall only operates on interrupts which are bound to a port.  Interrupts being waited upon with [`zx_interrupt_wait()`] do not need to be re-armed with thiscall -- it happens automatically when [`zx_interrupt_wait()`] is called. 该系统调用仅在绑定到端口的中断上运行。用[`zx_interrupt_wait（）]等待的中断不需要通过此调用重新设防-当调用[`zx_interrupt_wait（）]时，它会自动发生。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_INTERRUPT** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_INTERRUPT **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_interrupt_ack()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_interrupt_ack（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an interrupt object.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是中断对象。

**ZX_ERR_BAD_STATE** *handle* is not bound to a port.  ** ZX_ERR_BAD_STATE ** *句柄*未绑定到端口。

**ZX_ERR_CANCELED**  [`zx_interrupt_destroy()`] was called on *handle*.  ** ZX_ERR_CANCELED ** [`zx_interrupt_destroy（）`]在*句柄*上被调用。

**ZX_ERR_ACCESS_DENIED** *handle* lacks **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_WRITE **。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_bind()`]  -[`zx_interrupt_bind（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_interrupt_destroy()`]  -[`zx_interrupt_destroy（）`]
 - [`zx_interrupt_trigger()`]  -[`zx_interrupt_trigger（）`]
 - [`zx_interrupt_wait()`]  -[`zx_interrupt_wait（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

