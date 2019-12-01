 
# zx_channel_create  zx_channel_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a channel.  创建一个频道。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_create(uint32_t options,
                              zx_handle_t* out0,
                              zx_handle_t* out1);
```
 

 
## DESCRIPTION  描述 

`zx_channel_create()` creates a channel, a bi-directional datagram-style message transport capable of sending raw data bytesas well as handles from one side to the other. zx_channel_create（）创建一个通道，这是一种双向的数据报样式的消息传输，能够发送原始数据字节以及从一侧到另一侧的句柄。

Two handles are returned on success, providing access to both sides of the channel.  Messages written to one handle may be read fromthe opposite. 成功返回两个句柄，从而可以访问通道的两侧。写入一个句柄的消息可以从相反的方向读取。

The handles will have **ZX_RIGHT_TRANSFER** (allowing them to be sent to another process via [`zx_channel_write()`]), **ZX_RIGHT_WRITE** (allowingmessages to be written to them), and **ZX_RIGHT_READ** (allowing messagesto be read from them). 这些句柄将具有** ZX_RIGHT_TRANSFER **（允许它们通过[`zx_channel_write（）]发送到另一个进程），** ZX_RIGHT_WRITE **（允许将消息写入它们）和** ZX_RIGHT_READ **（允许从他们那里读取消息）。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_channel_create()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_channel_create（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out0* or *out1* is an invalid pointer or NULL or *options* is any value other than 0. ** ZX_ERR_INVALID_ARGS ** * out0 *或* out1 *是无效的指针，或者NULL或* options *是除0以外的任何值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_channel_call()`]  -[`zx_channel_call（）`]
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]
 - [`zx_channel_write()`]  -[`zx_channel_write（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

