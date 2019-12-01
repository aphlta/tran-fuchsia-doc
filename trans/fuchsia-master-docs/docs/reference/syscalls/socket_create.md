 
# zx_socket_create  zx_socket_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a socket.  创建一个套接字。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_socket_create(uint32_t options,
                             zx_handle_t* out0,
                             zx_handle_t* out1);
```
 

 
## DESCRIPTION  描述 

`zx_socket_create()` creates a socket, a connected pair of bidirectional stream transports, that can move only data, and thathave a maximum capacity. zx_socket_create（）创建一个套接字，即一对连接的双向流传输，只能移动数据，并具有最大容量。

Data written to one handle may be read from the opposite.  写入一个句柄的数据可以从另一句柄读取。

The *options* must set either the **ZX_SOCKET_STREAM** or **ZX_SOCKET_DATAGRAM** flag. * options *必须设置** ZX_SOCKET_STREAM **或** ZX_SOCKET_DATAGRAM **标志。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_socket_create()` returns **ZX_OK** on success. In the event of failure, one of the following values is returned. zx_socket_create（）成功时返回** ZX_OK **。发生故障时，将返回以下值之一。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out0* or *out1* is an invalid pointer or NULL or *options* is any value other than **ZX_SOCKET_STREAM** or **ZX_SOCKET_DATAGRAM**. ** ZX_ERR_INVALID_ARGS ** * out0 *或* out1 *是无效的指针，或者NULL或* options *是** ZX_SOCKET_STREAM **或** ZX_SOCKET_DATAGRAM **以外的任何值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## LIMITATIONS  局限性 

The maximum capacity is not currently set-able.  当前无法设置最大容量。

 
## SEE ALSO  也可以看看 

 
 - [`zx_socket_read()`]  -[`zx_socket_read（）`]
 - [`zx_socket_shutdown()`]  -[`zx_socket_shutdown（）`]
 - [`zx_socket_write()`]  -[`zx_socket_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

