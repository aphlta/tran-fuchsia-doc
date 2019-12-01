 
# zx_socket_shutdown  zx_socket_shutdown 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Prevent reading or writing.  防止阅读或写作。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_socket_shutdown(zx_handle_t handle, uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_socket_shutdown()` attempts to prevent future reads or writes on a socket, where options can be a combination of **ZX_SOCKET_SHUTDOWN_READ** and**ZX_SOCKET_SHUTDOWN_WRITE**: zx_socket_shutdown（）试图防止将来在套接字上进行读写，其中选项可以是** ZX_SOCKET_SHUTDOWN_READ **和** ZX_SOCKET_SHUTDOWN_WRITE **的组合：

 
 * If **ZX_SOCKET_SHUTDOWN_READ** is passed to *options*, then reading is disabled for the socket endpoint at *handle*. All data buffered in the socketat the time of the call can be read, but further reads from this endpoint orwrites to the other endpoint of the socket will fail with**ZX_ERR_BAD_STATE**. *如果将** ZX_SOCKET_SHUTDOWN_READ **传递给* options *，则在* handle *处的套接字端点将无法读取。可以读取调用时在套接字中缓冲的所有数据，但是从该端点进行的进一步读取或对套接字的另一个端点的写入将失败，并显示** ZX_ERR_BAD_STATE **。

 
 * If **ZX_SOCKET_SHUTDOWN_WRITE** is passed to *options*, then writing is disabled for the socket endpoint at *handle*. Further writes to this endpointor reads from the other endpoint of the socket will fail with**ZX_ERR_BAD_STATE**. *如果将** ZX_SOCKET_SHUTDOWN_WRITE **传递给* options *，则在* handle *处的套接字端点将禁止写入。对该套接字的进一步写入或从套接字的另一个端点的读取将失败，并显示** ZX_ERR_BAD_STATE **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_SOCKET** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_SOCKET **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_socket_shutdown()` returns **ZX_OK** on success.  `zx_socket_shutdown（）`成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a socket handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是套接字句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_INVALID_ARGS** *options* contains an undefined flag.  ** ZX_ERR_INVALID_ARGS ** *选项*包含未定义的标志。

 
## SEE ALSO  也可以看看 

 
 - [`zx_socket_create()`]  -[`zx_socket_create（）`]
 - [`zx_socket_read()`]  -[`zx_socket_read（）`]
 - [`zx_socket_write()`]  -[`zx_socket_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

