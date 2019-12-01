 
# zx_channel_write  zx_channel_write 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write a message to a channel.  将消息写到频道。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_write(zx_handle_t handle,
                             uint32_t options,
                             const void* bytes,
                             uint32_t num_bytes,
                             const zx_handle_t* handles,
                             uint32_t num_handles);
```
 

 
## DESCRIPTION  描述 

`zx_channel_write()` attempts to write a message of *num_bytes* bytes and *num_handles* handles to the channel specified by*handle*.  The pointers *handles* and *bytes* may be NULL if theirrespective sizes are zero. zx_channel_write（）尝试将* num_bytes *个字节和* num_handles *个句柄的消息写入到* handle *指定的通道中。如果指针* handles *和* bytes *的大小均为零，则它们可以为NULL。

On success, all *num_handles* of the handles in the *handles* array are attached to the message and will become available to the readerof that message from the opposite end of the channel. 成功后，* handles *数组中的所有* num_handles *个句柄都将附加到消息上，并将从通道的另一端供该消息的读者使用。

All handles are discarded and no longer available to the caller, on success or failure. Use [`zx_channel_write_etc()`] if handles needto be preserved by the sender. 成功或失败时，所有句柄都将被丢弃，并且不再可供调用者使用。如果句柄需要由发送者保留，则使用[`zx_channel_write_etc（）`]。

It is invalid to include *handle* (the handle of the channel being written to) in the *handles* array (the handles being sent in the message). 在* handles *数组（消息中发送的句柄）中包含* handle *（正在写入的通道的句柄）是无效的。

The maximum number of handles which may be sent in a message is **ZX_CHANNEL_MAX_MSG_HANDLES**, which is 64. 一条消息中可以发送的最大句柄数是** ZX_CHANNEL_MAX_MSG_HANDLES **，即64。

The maximum number of bytes which may be sent in a message is **ZX_CHANNEL_MAX_MSG_BYTES**, which is 65536. 一条消息中可以发送的最大字节数是** ZX_CHANNEL_MAX_MSG_BYTES **，即65536。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CHANNEL** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_CHANNEL **类型，并具有** ZX_RIGHT_WRITE **。

Every entry of *handles* must have **ZX_RIGHT_TRANSFER**.  *“句柄” *的每个条目都必须具有“ ZX_RIGHT_TRANSFER **”。

 
## RETURN VALUE  返回值 

`zx_channel_write()` returns **ZX_OK** on success.  zx_channel_write（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle, any element in *handles* is not a valid handle, or there are repeated handles among thehandles in the *handles* array. ** ZX_ERR_BAD_HANDLE ** * handle *不是有效的句柄，* handles *中的任何元素都不是有效的句柄，或者* handles *数组中的句柄之间有重复的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a channel handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是通道句柄。

**ZX_ERR_INVALID_ARGS**  *bytes* is an invalid pointer, *handles* is an invalid pointer, or *options* is nonzero. ** ZX_ERR_INVALID_ARGS ** * bytes *是无效的指针，* handles *是无效的指针，或* options *非零。

**ZX_ERR_NOT_SUPPORTED**  *handle* was found in the *handles* array, or one of the handles in *handles* was *handle* (the handle to thechannel being written to). ** ZX_ERR_NOT_SUPPORTED **在* handles *数组中找到* handle *，或者* handles *中的一个handle是* handle *（正在写入的通道的句柄）。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE** or any element in *handles* does not have **ZX_RIGHT_TRANSFER**. ** ZX_ERR_ACCESS_DENIED ** * handle *没有** ZX_RIGHT_WRITE **或* handles *中的任何元素没有** ZX_RIGHT_TRANSFER **。

**ZX_ERR_PEER_CLOSED**  The other side of the channel is closed.  ** ZX_ERR_PEER_CLOSED **通道的另一侧已关闭。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_OUT_OF_RANGE**  *num_bytes* or *num_handles* are larger than the largest allowable size for channel messages. ** ZX_ERR_OUT_OF_RANGE ** * num_bytes *或* num_handles *大于通道消息的最大允许大小。

 
## NOTES  笔记 

*num_handles* is a count of the number of elements in the *handles* array, not its size in bytes. * num_handles *是对* handles *数组中元素数量的计数，而不是其大小（以字节为单位）。

The byte size limitation on messages is not yet finalized.  消息的字节大小限制尚未最终确定。

 
## SEE ALSO  也可以看看 

 
 - [`zx_channel_call()`]  -[`zx_channel_call（）`]
 - [`zx_channel_create()`]  -[`zx_channel_create（）`]
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]
 - [`zx_channel_read_etc()`]  -[`zx_channel_read_etc（）`]
 - [`zx_channel_write_etc()`]  -[`zx_channel_write_etc（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

