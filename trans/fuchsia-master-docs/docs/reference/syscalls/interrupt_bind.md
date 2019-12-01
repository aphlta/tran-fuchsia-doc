 
# zx_interrupt_bind  zx_interrupt_bind 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Bind an interrupt object to a port.  将中断对象绑定到端口。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_bind(zx_handle_t handle,
                              zx_handle_t port_handle,
                              uint64_t key,
                              uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_bind()` binds or unbinds an interrupt object to a port.  zx_interrupt_bind（）将中断对象绑定或取消绑定到端口。

An interrupt object may only be bound to a single port and may only be bound once. The interrupt can only bind to a port which is created with **ZX_PORT_BIND_TO_INTERRUPT**option. 中断对象只能绑定到单个端口，并且只能绑定一次。中断只能绑定到使用** ZX_PORT_BIND_TO_INTERRUPT **选项创建的端口。

When a bound interrupt object is triggered, a **ZX_PKT_TYPE_INTERRUPT** packet will be delivered to the port it is bound to, with the timestamp (relative to **ZX_CLOCK_MONOTONIC**)of when the interrupt was triggered in the `zx_packet_interrupt_t`.  The *key* usedwhen binding the interrupt will be present in the `key` field of the `zx_port_packet_t`. 当绑定的中断对象被触发时，** ZX_PKT_TYPE_INTERRUPT **数据包将被发送到与之绑定的端口，并带有zx_packet_interrupt_t中触发中断的时间戳（相对于** ZX_CLOCK_MONOTONIC **）。绑定中断时使用的“密钥”将出现在“ zx_port_packet_t”的“密钥”字段中。

To bind to a port pass **ZX_INTERRUPT_BIND** in *options*.  要绑定到端口，请在* options *中传递** ZX_INTERRUPT_BIND **。

To unbind a previously bound port pass **ZX_INTERRUPT_UNBIND** in *options*. For unbind the *port_handle* is required but the *key* is ignored. Unbinding the port removes previouslyqueued packets to the port. 要取消绑定先前绑定的端口，请在* options *中传递** ZX_INTERRUPT_UNBIND **。要取消绑定，需要* port_handle *，但忽略* key *。取消绑定端口将先前排队的数据包删除到该端口。

Before another packet may be delivered, the bound interrupt must be re-armed using the [`zx_interrupt_ack()`] syscall.  This is (in almost all cases) best done after the interruptpacket has been fully processed.  Especially in the case of multiple threads readingpackets from a port, if the processing thread re-arms the interrupt and it has triggered,a packet will immediately be delivered to a waiting thread. 在传送另一个数据包之前，必须使用[`zx_interrupt_ack（）]系统调用重新设置绑定的中断。 （在几乎所有情况下）最好在完全处理完中断数据包之后完成此操作。特别是在有多个线程从端口读取数据包的情况下，如果处理线程重新设置了中断并触发了中断，则数据包将立即传递到等待的线程。

Interrupt packets are delivered via a dedicated queue on ports and are higher priority than non-interrupt packets. 中断数据包通过端口上的专用队列传递，并且比非中断数据包具有更高的优先级。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_INTERRUPT** and have **ZX_RIGHT_READ**.  *句柄*必须为** ZX_OBJ_TYPE_INTERRUPT **类型，并具有** ZX_RIGHT_READ **。

*port_handle* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  * port_handle *必须为** ZX_OBJ_TYPE_PORT **类型，且必须为** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_interrupt_bind()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_interrupt_bind（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* or *port_handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *或* port_handle *不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an interrupt object or *port_handle* is not a port object.  ** ZX_ERR_WRONG_TYPE ** * handle *不是中断对象，或者* port_handle *不是端口对象。

**ZX_ERR_CANCELED**  [`zx_interrupt_destroy()`] was called on *handle*.  ** ZX_ERR_CANCELED ** [`zx_interrupt_destroy（）`]在*句柄*上被调用。

**ZX_ERR_BAD_STATE**  A thread is waiting on the interrupt using [`zx_interrupt_wait()`]  ** ZX_ERR_BAD_STATE **线程正在使用[`zx_interrupt_wait（）`]等待中断

**ZX_ERR_ACCESS_DENIED** the *handle* handle lacks **ZX_RIGHT_READ** or the *port_handle* handle lacks **ZX_RIGHT_WRITE** ** ZX_ERR_ACCESS_DENIED ** * handle *句柄缺少** ZX_RIGHT_READ **或* port_handle *句柄缺少** ZX_RIGHT_WRITE **

**ZX_ERR_ALREADY_BOUND** this interrupt object is already bound.  ** ZX_ERR_ALREADY_BOUND **该中断对象已被绑定。

**ZX_ERR_INVALID_ARGS** *options* is not **ZX_INTERRUPT_BIND** or **ZX_INTERRUPT_UNBIND**.  ** ZX_ERR_INVALID_ARGS ** *选项*不是** ZX_INTERRUPT_BIND **或** ZX_INTERRUPT_UNBIND **。

**ZX_ERR_NOT_FOUND** the *port* does not match the bound port.  ** ZX_ERR_NOT_FOUND ** *端口*与绑定的端口不匹配。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_ack()`]  -[`zx_interrupt_ack（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_interrupt_destroy()`]  -[`zx_interrupt_destroy（）`]
 - [`zx_interrupt_trigger()`]  -[`zx_interrupt_trigger（）`]
 - [`zx_interrupt_wait()`]  -[`zx_interrupt_wait（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

