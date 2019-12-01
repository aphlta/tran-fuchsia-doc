 
# zx_interrupt_create  zx_interrupt_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create an interrupt object.  创建一个中断对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_create(zx_handle_t src_obj,
                                uint32_t src_num,
                                uint32_t options,
                                zx_handle_t* out_handle);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_create()` creates an interrupt object which represents a physical or virtual interrupt. zx_interrupt_create（）创建一个代表物理或虚拟中断的中断对象。

If *options* is **ZX_INTERRUPT_VIRTUAL**, *src_obj* and *src_num* are ignored and a virtual interrupt is returned. 如果* options *为** ZX_INTERRUPT_VIRTUAL **，则* src_obj *和* src_num *被忽略，并返回虚拟中断。

Otherwise *src_obj* must be a suitable resource for creating platform interrupts or a PCI object, and *src_num* is the associated interrupt number.  This restrictsthe creation of interrupts to the internals of the DDK (driver development kit).Physical interrupts are obtained by drivers through various DDK APIs. 否则，* src_obj *必须是用于创建平台中断或PCI对象的合适资源，并且* src_num *是关联的中断号。这将中断的创建限制在DDK（驱动程序开发套件）的内部。物理中断是由驱动程序通过各种DDK API获取的。

Physical interrupts honor the options **ZX_INTERRUPT_EDGE_LOW**, **ZX_INTERRUPT_EDGE_HIGH**, **ZX_INTERRUPT_LEVEL_LOW**, **ZX_INTERRUPT_LEVEL_HIGH**, and **ZX_INTERRUPT_REMAP_IRQ**. 物理中断支持以下选项：ZX_INTERRUPT_EDGE_LOW **，** ZX_INTERRUPT_EDGE_HIGH **，** ZX_INTERRUPT_LEVEL_LOW **，** ZX_INTERRUPT_LEVEL_HIGH **和** ZX_INTERRUPT_REMAP_IRQ **。

The handles will have **ZX_RIGHT_INSPECT**, **ZX_RIGHT_DUPLICATE**, **ZX_RIGHT_TRANSFER** (allowing them to be sent to another process via [`zx_channel_write()`]), **ZX_RIGHT_READ**,**ZX_RIGHT_WRITE** (required for [`zx_interrupt_ack()`]), **ZX_RIGHT_WAIT** (required for[`zx_interrupt_wait()`], and **ZX_RIGHT_SIGNAL** (required for [`zx_interrupt_trigger()`]). 这些句柄将具有** ZX_RIGHT_INSPECT **，** ZX_RIGHT_DUPLICATE **，** ZX_RIGHT_TRANSFER **（允许它们通过[`zx_channel_write（）]发送到另一个进程），** ZX_RIGHT_READ **，** ZX_RIGHT_WRITE * *（对于[`zx_interrupt_ack（）`]是必需的），** ZX_RIGHT_WAIT **（对于[`zx_interrupt_wait（）`]是必需的，以及** ZX_RIGHT_SIGNAL **（对于[`zx_interrupt_trigger（）`是必需的））。

Interrupts are said to be "triggered" when the underlying physical interrupt occurs or when [`zx_interrupt_trigger()`] is called on a virtual interrupt.  A triggered interrupt,when bound to a port with [`zx_interrupt_bind()`], causes a packet to be delivered to the port. 当发生底层物​​理中断或在虚拟中断上调用[`zx_interrupt_trigger（）`]时，中断被称为“触发”。当使用[`zx_interrupt_bind（）]绑定到端口时，触发的中断会导致将数据包传递到该端口。

If not bound to a port, an interrupt object may be waited on with [`zx_interrupt_wait()`].  如果未绑定到端口，则可以使用[`zx_interrupt_wait（）`]等待中断对象。

Interrupts cannot be waited on with the `zx_object_wait_` family of calls.  zx_object_wait_`系列调用无法等待中断。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*src_obj* must have resource kind **ZX_RSRC_KIND_IRQ**.  * src_obj *必须具有资源类型** ZX_RSRC_KIND_IRQ **。

 
## RETURN VALUE  返回值 

`zx_interrupt_create()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_interrupt_create（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** the *src_obj* handle is invalid (if this is not a virtual interrupt)  ** ZX_ERR_BAD_HANDLE ** * src_obj *句柄无效（如果这不是虚拟中断）

**ZX_ERR_WRONG_TYPE** the *src_obj* handle is not of an appropriate type to create an interrupt.  ** ZX_ERR_WRONG_TYPE ** src_obj *句柄不是创建中断的适当类型。

**ZX_ERR_ACCESS_DENIED** the *src_obj* handle does not allow this operation.  ** ZX_ERR_ACCESS_DENIED ** * src_obj *句柄不允许此操作。

**ZX_ERR_INVALID_ARGS** *options* contains invalid flags or the *out_handle* parameter is an invalid pointer. ** ZX_ERR_INVALID_ARGS ** *选项*包含无效的标志，或者* out_handle *参数是无效的指针。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_ack()`]  -[`zx_interrupt_ack（）`]
 - [`zx_interrupt_bind()`]  -[`zx_interrupt_bind（）`]
 - [`zx_interrupt_destroy()`]  -[`zx_interrupt_destroy（）`]
 - [`zx_interrupt_wait()`]  -[`zx_interrupt_wait（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

