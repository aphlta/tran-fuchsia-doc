 
# zx_socket_read  zx_socket_read 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read data from a socket.  从套接字读取数据。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_socket_read(zx_handle_t handle,
                           uint32_t options,
                           void* buffer,
                           size_t buffer_size,
                           size_t* actual);
```
 

 
## DESCRIPTION  描述 

`zx_socket_read()` attempts to read *buffer_size* bytes into *buffer*. If successful, the number of bytes actually read are return via*actual*. zx_socket_read（）尝试将* buffer_size *个字节读取到* buffer *中。如果成功，则通过* actual *返回实际读取的字节数。

If a NULL *actual* is passed in, it will be ignored.  如果传入NULL * actual *，那么它将被忽略。

If the socket was created with **ZX_SOCKET_DATAGRAM**, this syscall reads only the first available datagram in the socket (if one is present).If *buffer* is too small for the datagram, then the read will betruncated, and any remaining bytes in the datagram will be discarded. 如果套接字是使用** ZX_SOCKET_DATAGRAM **创建的，则此系统调用仅读取套接字中的第一个可用数据报（如果存在）;如果* buffer *对于数据报而言太小，则读取将被截断，而其余的将被截断数据报中的字节将被丢弃。

Supported *options* are:  支持的*选项*是：

 
* **ZX_SOCKET_PEEK** to leave the message in the socket.  * ** ZX_SOCKET_PEEK **将消息保留在套接字中。

To determine how many bytes are available to read, use the **rx_buf_available** field of the resulting `zx_info_socket_t`, which you can obtain using the**ZX_INFO_SOCKET** topic for [`zx_object_get_info()`]. 要确定有多少字节可供读取，请使用生成的`zx_info_socket_t`的** rx_buf_available **字段，您可以使用[`zx_object_get_info（）]的** ZX_INFO_SOCKET **主题获取该字段。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_SOCKET** and have **ZX_RIGHT_READ**.  *句柄*必须为** ZX_OBJ_TYPE_SOCKET **类型，并具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_socket_read()` returns **ZX_OK** on success, and writes into *actual* (if non-NULL) the exact number of bytes read. zx_socket_read（）成功时返回** ZX_OK **，并将读取的确切字节数写入* actual *（如果非NULL）。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_BAD_STATE**  reading has been disabled for this socket endpoint via [`zx_socket_shutdown()`].  通过[`zx_socket_shutdown（）`）已禁用此套接字端点的** ZX_ERR_BAD_STATE **读取。

**ZX_ERR_WRONG_TYPE**  *handle* is not a socket handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是套接字句柄。

**ZX_ERR_INVALID_ARGS** If any of *buffer* or *actual* are non-NULL but invalid pointers, or if *buffer* is NULL, or if *options* is zero. ** ZX_ERR_INVALID_ARGS **如果* buffer *或* actual *中的任何一个为非NULL但指针无效，或者* buffer *为NULL，或者* options *为零。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_READ**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_READ **。

**ZX_ERR_SHOULD_WAIT**  The socket contained no data to read.  ** ZX_ERR_SHOULD_WAIT **套接字中没有要读取的数据。

**ZX_ERR_PEER_CLOSED**  The other side of the socket is closed and no data is readable. ** ZX_ERR_PEER_CLOSED **套接字的另一侧已关闭，并且无法读取任何数据。

 
## SEE ALSO  也可以看看 

 
 - [`zx_socket_create()`]  -[`zx_socket_create（）`]
 - [`zx_socket_shutdown()`]  -[`zx_socket_shutdown（）`]
 - [`zx_socket_write()`]  -[`zx_socket_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

