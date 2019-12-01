 
# zx_port_create  zx_port_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create an IO port.  创建一个IO端口。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_port_create(uint32_t options, zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_port_create()` creates a port: a waitable object that can be used to read packets queued by kernel or by user-mode. zx_port_create（）创建一个端口：一个可等待的对象，可用于读取内核或用户模式排队的数据包。

If you need this port to be bound to an interrupt, pass **ZX_PORT_BIND_TO_INTERRUPT** to *options*, otherwise it should be **0**. 如果您需要将此端口绑定到中断，则将** ZX_PORT_BIND_TO_INTERRUPT **传递给* options *，否则应为** 0 **。

In the case where a port is bound to an interrupt, the interrupt packets are delivered via a dedicated queue on ports and are higher priority than other non-interrupt packets. 在端口绑定到中断的情况下，中断数据包通过端口上的专用队列传递，并且比其他非中断数据包具有更高的优先级。

The returned handle will have:  返回的句柄将具有：

 
  * `ZX_RIGHT_TRANSFER`: allowing them to be sent to another process through [`zx_channel_write()`].  *`ZX_RIGHT_TRANSFER`：允许它们通过[`zx_channel_write（）`）发送到另一个进程。
  * `ZX_RIGHT_WRITE`: allowing packets to be *queued*.  ZX_RIGHT_WRITE：允许对数据包进行排队。
  * `ZX_RIGHT_READ`: allowing packets to be *read*.  *`ZX_RIGHT_READ`：允许*读取*数据包。
  * `ZX_RIGHT_DUPLICATE`: allowing them to be *duplicated*.  *`ZX_RIGHT_DUPLICATE`：允许它们*被复制*。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_port_create()` returns **ZX_OK** and a valid IO port handle via *out* on success. In the event of failure, an error value is returned. zx_port_create（）在成功时通过* out *返回** ZX_OK **和有效的IO端口句柄。如果发生故障，将返回一个错误值。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS** *options* has an invalid value, or *out* is an invalid pointer or NULL. ** ZX_ERR_INVALID_ARGS ** * options *具有无效值，或者* out *是无效指针或NULL。

**ZX_ERR_NO_MEMORY** Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future builds this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_port_queue()`]  -[`zx_port_queue（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

