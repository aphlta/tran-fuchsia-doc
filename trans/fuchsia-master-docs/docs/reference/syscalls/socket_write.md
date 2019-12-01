 
# zx_socket_write  zx_socket_write 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write data to a socket.  将数据写入套接字。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_socket_write(zx_handle_t handle,
                            uint32_t options,
                            const void* buffer,
                            size_t buffer_size,
                            size_t* actual);
```
 

 
## DESCRIPTION  描述 

`zx_socket_write()` attempts to write *buffer_size* bytes to the socket specified by *handle*. The pointer to *bytes* may be NULL if *buffer_size* is zero. zx_socket_write（）尝试将* buffer_size *字节写入* handle *指定的套接字。如果* buffer_size *为零，则指向* bytes *的指针可能为NULL。

If a NULL *actual* is passed in, it will be ignored.  如果传入NULL * actual *，那么它将被忽略。

A **ZX_SOCKET_STREAM** socket write can be short if the socket does not have enough space for all of *buffer*. If a non-zero amount of data was written tothe socket, the amount written is returned via *actual* and the call succeeds.Otherwise, if the socket was already full, the call returns**ZX_ERR_SHOULD_WAIT** and the client should wait (e.g., with[`zx_object_wait_one()`] or [`zx_object_wait_async()`]). 如果套接字没有足够的空间可用于所有* buffer *，则** ZX_SOCKET_STREAM **套接字写操作可能很短。如果向套接字写入了非零数量的数据，则通过* actual *返回写入的数量，并且调用成功;否则，如果套接字已满，则调用返回** ZX_ERR_SHOULD_WAIT **，客户端应等待（例如，带有[`zx_object_wait_one（）`或[`zx_object_wait_async（）`））。

 

A **ZX_SOCKET_DATAGRAM** socket write is never short. If the socket has insufficient space for *buffer*, it writes nothing and returns**ZX_ERR_SHOULD_WAIT**. If the write succeeds, *buffer_size* is returned via*actual*. Attempting to write a packet larger than the datagram socket'scapacity will fail with **ZX_ERR_OUT_OF_RANGE**. ZX_SOCKET_DATAGRAM **套接字写操作永远不会短。如果套接字没有足够的空间用于* buffer *，则不写任何内容并返回** ZX_ERR_SHOULD_WAIT **。如果写入成功，则通过* actual *返回* buffer_size *。尝试写入大于数据报套接字容量的数据包将失败，并显示** ZX_ERR_OUT_OF_RANGE **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_SOCKET** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_SOCKET **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_socket_write()` returns **ZX_OK** on success.  zx_socket_write（）成功时返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_BAD_STATE**  writing has been disabled for this socket endpoint via [`zx_socket_shutdown()`].  ** ZX_ERR_BAD_STATE **已通过[`zx_socket_shutdown（）]禁止对此套接字端点进行写入。

**ZX_ERR_WRONG_TYPE**  *handle* is not a socket handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是套接字句柄。

**ZX_ERR_INVALID_ARGS**  *buffer* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *缓冲区*是无效的指针。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_SHOULD_WAIT**  The buffer underlying the socket is full.  ** ZX_ERR_SHOULD_WAIT **套接字底层的缓冲区已满。

**ZX_ERR_OUT_OF_RANGE**  The socket was created with **ZX_SOCKET_DATAGRAM** and *buffer* is larger than the remaining space in the socket. ** ZX_ERR_OUT_OF_RANGE **套接字是用** ZX_SOCKET_DATAGRAM **创建的，并且* buffer *大于套接字中的剩余空间。

**ZX_ERR_PEER_CLOSED**  The other side of the socket is closed.  ** ZX_ERR_PEER_CLOSED **插座的另一侧已关闭。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_socket_create()`]  -[`zx_socket_create（）`]
 - [`zx_socket_read()`]  -[`zx_socket_read（）`]
 - [`zx_socket_shutdown()`]  -[`zx_socket_shutdown（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

