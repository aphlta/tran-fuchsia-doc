 
# zx_channel_read  zx_channel_read 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read a message from a channel.  阅读来自频道的消息。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_read(zx_handle_t handle,
                            uint32_t options,
                            void* bytes,
                            zx_handle_t* handles,
                            uint32_t num_bytes,
                            uint32_t num_handles,
                            uint32_t* actual_bytes,
                            uint32_t* actual_handles);
```
 

 
## DESCRIPTION  描述 

`zx_channel_read()` attempts to read the first message from the channel specified by *handle* into the provided *bytes* and/or *handles* buffers. zx_channel_read（）试图从* handle *指定的通道中读取第一条消息到提供的* bytes *和/或* handles *缓冲区中。

The parameters *num_bytes* and *num_handles* are used to specify the size of the respective read buffers. *num_bytes* is a count of bytes, and*num_handles* is a count of elements of type `zx_handle_t`. 参数* num_bytes *和* num_handles *用于指定各个读取缓冲区的大小。 * num_bytes *是字节计数，* num_handles *是zx_handle_t类型元素的计数。

The length of *bytes*, in bytes, is stored in the location pointed to by *actual_bytes*.  The number of handles is stored in the location pointed to by*actual_handles*.  Either *actual_bytes* or *actual_handles* may be NULL, inwhich case they will be ignored. * bytes *的长度（以字节为单位）存储在* actual_bytes *指向的位置。句柄数存储在* actual_handles *指向的位置。 * actual_bytes *或* actual_handles *都可以为NULL，在这种情况下，它们将被忽略。

Channel messages may contain both byte data and handle payloads and may only be read in their entirety.  Partial reads are not possible. 通道消息可能同时包含字节数据和句柄有效载荷，并且只能完整读取。无法部分读取。

The *bytes* buffer is written before the *handles* buffer. In the event of overlap between these two buffers, the contents written to *handles*will overwrite the portion of *bytes* it overlaps. * bytes *缓冲区写在* handles *缓冲区之前。如果这两个缓冲区发生重叠，则写入* handles *的内容将覆盖* bytes *重叠的部分。

When communicating to an untrusted party over a channel, it is recommended that the [`zx_channel_read_etc()`] form is used and each handle typeand rights are validated against the expected values. 通过通道与不受信任的一方进行通信时，建议使用[`zx_channel_read_etc（）]格式，并根据预期值验证每个句柄的类型和权限。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CHANNEL** and have **ZX_RIGHT_READ**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CHANNEL **且具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

Returns **ZX_OK** on success. If non-NULL, the locations pointed to by *actual_bytes* and *actual_handles* contain the exact number of bytes and countof handles read. 成功返回** ZX_OK **。如果为非NULL，则* actual_bytes *和* actual_handles *所指向的位置将包含字节的确切数目和读取的countof句柄。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a channel handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是通道句柄。

**ZX_ERR_INVALID_ARGS**  If any of *bytes*, *handles*, *actual_bytes*, or *actual_handles* are non-NULL and an invalid pointer. ** ZX_ERR_INVALID_ARGS **如果* bytes *，* handles *，* actual_bytes *或* actual_handles *中的任何一个为非NULL且为无效指针。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_READ**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_READ **。

**ZX_ERR_SHOULD_WAIT**  The channel contained no messages to read.  ** ZX_ERR_SHOULD_WAIT **通道不包含要读取的消息。

**ZX_ERR_PEER_CLOSED**  The other side of the channel is closed.  ** ZX_ERR_PEER_CLOSED **通道的另一侧已关闭。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BUFFER_TOO_SMALL**  The provided *bytes* or *handles* buffers are too small (in which case, the minimum sizes necessary to receivethe message will be written to *actual_bytes* and *actual_handles*,provided they are non-NULL). If *options* has **ZX_CHANNEL_READ_MAY_DISCARD**set, then the message is discarded. ** ZX_ERR_BUFFER_TOO_SMALL **所提供的* bytes *或* handles *缓冲区太小（在这种情况下，接收消息所需的最小大小将被写入* actual_bytes *和* actual_handles *，前提是它们为非NULL）。如果* options *设置了** ZX_CHANNEL_READ_MAY_DISCARD **，则该消息将被丢弃。

 
## SEE ALSO  也可以看看 

 
 - [`zx_channel_call()`]  -[`zx_channel_call（）`]
 - [`zx_channel_create()`]  -[`zx_channel_create（）`]
 - [`zx_channel_read_etc()`]  -[`zx_channel_read_etc（）`]
 - [`zx_channel_write()`]  -[`zx_channel_write（）`]
 - [`zx_channel_write_etc()`]  -[`zx_channel_write_etc（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

