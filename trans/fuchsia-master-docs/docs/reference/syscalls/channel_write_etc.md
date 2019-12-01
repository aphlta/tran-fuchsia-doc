 
# zx_channel_write_etc  zx_channel_write_etc 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write a message to a channel.  将消息写到频道。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_write_etc(zx_handle_t handle,
                                 uint32_t options,
                                 const void* bytes,
                                 uint32_t num_bytes,
                                 zx_handle_disposition_t* handles,
                                 uint32_t num_handles);
```
 

 
## DESCRIPTION  描述 

Like [`zx_channel_write()`] it attempts to write a message of *num_bytes* bytes and *num_handles* handles to the channel specified by *handle*, but inaddition it will perform operations for the handles that are beingtransferred with *handles* being an array of `zx_handle_disposition_t`: 像[`zx_channel_write（）`]一样，它尝试将* num_bytes *个字节和* num_handles *个句柄的消息写入到* handle *指定的通道中，但除此之外，它将对正在被* handles *传递的句柄执行操作。 zx_handle_disposition_t数组：

```
typedef struct zx_handle_disposition {
    zx_handle_op_t operation;
    zx_handle_t handle;
    zx_rights_t rights;
    zx_obj_type_t type;
    zx_status_t result;
} zx_handle_disposition_t;
```
In zx_handle_disposition_t, *handle* is the source handle to be operated on, *rights* is the desired final rights (not a mask) and *result* must be setto **ZX_OK**. All source handles must have **ZX_RIGHT_TRANSFER**, butit it can  be removed in *rights* so that it is not available to the messagereceiver. 在zx_handle_disposition_t中，* handle *是要操作的源句柄，* rights *是所需的最终权限（不是掩码），并且* result *必须设置为** ZX_OK **。所有源句柄都必须具有** ZX_RIGHT_TRANSFER **，但是可以将其删除为* rights *，以便消息接收器无法使用它。

*type* is used to perform validation of the object type that the caller expects *handle* to be. It can be *ZX_OBJ_TYPE_NONE* to skip validationchecks or one of `zx_obj_type_t` defined types. * type *用于执行调用者期望* handle *是的对象类型的验证。它可以是* ZX_OBJ_TYPE_NONE *来跳过验证检查，也可以是zx_obj_type_t定义的类型之一。

The operation applied to *handle* is one of:  应用于* handle *的操作是以下之一：

 
*   **ZX_HANDLE_OP_MOVE** This is equivalent to first issuing [`zx_handle_replace()`] then [`zx_channel_write()`]. The source handle is always closed. * ** ZX_HANDLE_OP_MOVE **这等效于先发布[`zx_handle_replace（）`然后发布[`zx_channel_write（）]。源句柄始终处于关闭状态。

 
*   **ZX_HANDLE_OP_DUPLICATE** This is equivalent to first issuing [`zx_handle_duplicate()`] then [`zx_channel_write()`]. The source handle always remains open and accessible to thecaller. * ** ZX_HANDLE_OP_DUPLICATE **等效于首先发布[`zx_handle_duplicate（）]然后发布[`zx_channel_write（）]。源句柄始终保持打开状态，并且可供调用者访问。

*handle* will be transferred with capability *rights* which can be **ZX_RIGHT_SAME_RIGHTS** or a reduced set of rights, or **ZX_RIGHT_NONE**. In addition, this operation allows removing**ZX_RIGHT_TRANSFER** in *rights* so that capability is not available for the receiver. *句柄*将被转移为具有*权限*功能，可以是** ZX_RIGHT_SAME_RIGHTS **或一组简化的权限，或** ZX_RIGHT_NONE **。另外，此操作允许删除* rights *中的** ZX_RIGHT_TRANSFER **，因此接收器无法使用此功能。

If any operation fails, the error code for that source handle is written to *result*, and the first failure is made available in the return value for `zx_channel_write_etc()`. Alloperations in the *handles* array are attempted, even if one or more operations fail. 如果任何操作失败，则该源句柄的错误代码将写入* result *，并且第一个失败将在`zx_channel_write_etc（）'的返回值中提供。即使一个或多个操作失败，也会尝试* handles *数组中的所有操作。

All operations for each entry must succeed for the message to be written. On success, handles are attached to the message and will become available to the reader of that message from theopposite end of the channel. 每个条目的所有操作都必须成功才能写入消息。成功后，将把句柄附加到该消息上，并将使该消息的读者可以从通道的另一端使用该句柄。

It is invalid to include *handle* (the handle of the channel being written to) in the *handles* array (the handles being sent in the message). 在* handles *数组（消息中发送的句柄）中包含* handle *（正在写入的通道的句柄）是无效的。

The maximum number of handles which may be sent in a message is **ZX_CHANNEL_MAX_MSG_HANDLES**, which is 64. 一条消息中可以发送的最大句柄数是** ZX_CHANNEL_MAX_MSG_HANDLES **，即64。

The maximum number of bytes which may be sent in a message is **ZX_CHANNEL_MAX_MSG_BYTES**, which is 65536. 一条消息中可以发送的最大字节数是** ZX_CHANNEL_MAX_MSG_BYTES **，即65536。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CHANNEL** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_CHANNEL **类型，并具有** ZX_RIGHT_WRITE **。

Every entry of *handles* must have **ZX_RIGHT_TRANSFER**.  *“句柄” *的每个条目都必须具有“ ZX_RIGHT_TRANSFER **”。

 
## RETURN VALUE  返回值 

`zx_channel_write_etc()` returns **ZX_OK** on success.  `zx_channel_write_etc（）`成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle, any source handle in *handles* is not a valid handle, or there are repeated handlesin the *handles* array if **ZX_HANDLE_OP_DUPLICATE** flags is not present. ** ZX_ERR_BAD_HANDLE ** * handle *不是有效的句柄，* handles *中的任何源句柄都不是有效的句柄，或者如果不存在** ZX_HANDLE_OP_DUPLICATE **标志，则* handles *数组中有重复的handles。

**ZX_ERR_WRONG_TYPE**  *handle* is not a channel handle, or any source handle in *handles* did not match the object type *type*. ** ZX_ERR_WRONG_TYPE ** * handle *不是通道句柄，或者* handles *中的任何源句柄与对象类型* type *不匹配。

**ZX_ERR_INVALID_ARGS**  *bytes* is an invalid pointer, *handles* is an invalid pointer, or *options* is nonzero, or *operation* is notone of ZX_HANDLE_OP_MOVE or ZX_HANDLE_OP_DUPLICATE. ** ZX_ERR_INVALID_ARGS ** * bytes *是无效的指针，* handles *是无效的指针，或* options *非零，或* operation *不是ZX_HANDLE_OP_MOVE或ZX_HANDLE_OP_DUPLICATE之一。

**ZX_ERR_NOT_SUPPORTED**  *handle* is included in the *handles* array.  ** ZX_ERR_NOT_SUPPORTED ** * handle *包含在* handles *数组中。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE** or any source handle in *handles* does not have **ZX_RIGHT_TRANSFER**, orany source handle in *handles* does not have **ZX_RIGHT_DUPLICATE** when**ZX_HANDLE_OP_DUPLICATE** operation is specified. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **或*句柄*中的任何源句柄没有** ZX_RIGHT_TRANSFER **，或者*句柄*中的任何源句柄没有** ZX_RIGHT_DUPLICATE ** * ZX_HANDLE_OP_DUPLICATE **操作被指定。

**ZX_ERR_PEER_CLOSED**  The other side of the channel is closed.  ** ZX_ERR_PEER_CLOSED **通道的另一侧已关闭。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_OUT_OF_RANGE**  *num_bytes* or *num_handles* are larger than the largest allowable size for channel messages. ** ZX_ERR_OUT_OF_RANGE ** * num_bytes *或* num_handles *大于通道消息的最大允许大小。

 
## NOTES  笔记 

If the caller removes the **ZX_RIGHT_TRANSFER** to a handle attached to a message, the reader of the message will receive a handle that cannotbe written to any other channel, but still can be using according to itsrights and can be closed if not needed. 如果调用者将** ZX_RIGHT_TRANSFER **删除到附加到消息的句柄上，则消息的阅读器将收到一个不能写入任何其他通道的句柄，但仍可以根据其权限使用，并且可以在不需要时关闭。

 
## SEE ALSO  也可以看看 

 
 - [`zx_channel_call()`]  -[`zx_channel_call（）`]
 - [`zx_channel_create()`]  -[`zx_channel_create（）`]
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]
 - [`zx_channel_read_etc()`]  -[`zx_channel_read_etc（）`]
 - [`zx_channel_write()`]  -[`zx_channel_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

