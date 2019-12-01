 
# zx_channel_read_etc  zx_channel_read_etc 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read a message from a channel.  阅读来自频道的消息。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_read_etc(zx_handle_t handle,
                                uint32_t options,
                                void* bytes,
                                zx_handle_info_t* handles,
                                uint32_t num_bytes,
                                uint32_t num_handles,
                                uint32_t* actual_bytes,
                                uint32_t* actual_handles);
```
 

 
## DESCRIPTION  描述 

See [`zx_channel_read()`] for a full description.  有关完整说明，请参见[`zx_channel_read（）`]。

Both forms of read behave the same except that [`zx_channel_read()`] returns an array of raw `zx_handle_t` handle values while `zx_channel_read_etc()` returnsan array of `zx_handle_info_t` structures of the form: 两种形式的读取行为相同，除了[zx_channel_read（）]返回原始zx_handle_t处理值的数组，而zx_channel_read_etc（）返回数组zx_handle_info_t结构的数组：

```
typedef struct {
    zx_handle_t handle;     // handle value
    zx_obj_type_t type;     // type of object, see ZX_OBJ_TYPE_
    zx_rights_t rights;     // handle rights
    uint32_t unused;        // set to zero
} zx_handle_info_t;
```
 

When communicating to an untrusted party over a channel, it is recommended that the `zx_channel_read_etc()` form is used and each handle type and rightsare validated against the expected values. 通过通道与不受信任的一方进行通信时，建议使用“ zx_channel_read_etc（）”形式，并根据预期值验证每个句柄类型和权限。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CHANNEL** and have **ZX_RIGHT_READ**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CHANNEL **且具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

Both forms of read return **ZX_OK** on success, if *actual_bytes* and *actual_handles* (if non-NULL), contain the exact number of bytesand count of handles read. 如果* actual_bytes *和* actual_handles *（如果为非NULL），则两种形式的读取都在成功时返回** ZX_OK **，它们包含确切的字节数和读取的句柄数。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a channel handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是通道句柄。

**ZX_ERR_INVALID_ARGS**  If any of *bytes*, *handles*, *actual_bytes*, or *actual_handles* are non-NULL and an invalid pointer. ** ZX_ERR_INVALID_ARGS **如果* bytes *，* handles *，* actual_bytes *或* actual_handles *中的任何一个为非NULL且为无效指针。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_READ**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_READ **。

**ZX_ERR_SHOULD_WAIT**  The channel contained no messages to read.  ** ZX_ERR_SHOULD_WAIT **通道不包含要读取的消息。

**ZX_ERR_PEER_CLOSED**  The other side of the channel is closed.  ** ZX_ERR_PEER_CLOSED **通道的另一侧已关闭。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BUFFER_TOO_SMALL**  The provided *bytes* or *handles* buffers are too small (in which case, the minimum sizes necessary to receivethe message will be written to *actual_bytes* and *actual_handles*,provided they are non-NULL). If *options* has **ZX_CHANNEL_READ_MAY_DISCARD**set, then the message is discarded. ** ZX_ERR_BUFFER_TOO_SMALL **所提供的* bytes *或* handles *缓冲区太小（在这种情况下，接收消息所需的最小大小将被写入* actual_bytes *和* actual_handles *，前提是它们为非NULL）。如果* options *设置了** ZX_CHANNEL_READ_MAY_DISCARD **，则该消息将被丢弃。

 
## NOTES  笔记 

*num_handles* and *actual_handles* are counts of the number of elements in the *handles* array, not its size in bytes. * num_handles *和* actual_handles *是* handles *数组中元素数量的计数，而不是其大小（以字节为单位）。

 
## SEE ALSO  也可以看看 

 
 - [`zx_channel_call()`]  -[`zx_channel_call（）`]
 - [`zx_channel_create()`]  -[`zx_channel_create（）`]
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]
 - [`zx_channel_write()`]  -[`zx_channel_write（）`]
 - [`zx_channel_write_etc()`]  -[`zx_channel_write_etc（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

