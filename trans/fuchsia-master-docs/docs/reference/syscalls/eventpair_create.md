 
# zx_eventpair_create  zx_eventpair_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create an event pair.  创建一个事件对。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_eventpair_create(uint32_t options,
                                zx_handle_t* out0,
                                zx_handle_t* out1);
```
 

 
## DESCRIPTION  描述 

`zx_eventpair_create()` creates an event pair, which is a pair of objects that are mutually signalable. zx_eventpair_create（）创建一个事件对，这是一对相互可发信号的对象。

The signals **ZX_EVENTPAIR_SIGNALED** and **ZX_USER_SIGNAL_n** (where *n* is 0 through 7) may be set or cleared using [`zx_object_signal()`], which modifies the signals on theobject itself, or [`zx_object_signal_peer()`], which modifies the signals on itscounterpart. 信号** ZX_EVENTPAIR_SIGNALED **和** ZX_USER_SIGNAL_n **（其中* n *为0到7）可以使用[`zx_object_signal（）`]设置或清除，该信号会修改对象本身的信号，或[`zx_object_signal_peer（ ）`]，修改其对应部分的信号。

When all the handles to one of the objects have been closed, the **ZX_EVENTPAIR_PEER_CLOSED** signal will be asserted on the opposing object. 当所有对象之一的所有句柄都已关闭时，** ZX_EVENTPAIR_PEER_CLOSED **信号将在相对的对象上置位。

The newly-created handles will have the **ZX_RIGHT_TRANSFER**, **ZX_RIGHT_DUPLICATE**, **ZX_RIGHT_READ**, **ZX_RIGHT_WRITE**, **ZX_RIGHT_SIGNAL**,and **ZX_RIGHT_SIGNAL_PEER** rights. 新创建的句柄将具有** ZX_RIGHT_TRANSFER **，** ZX_RIGHT_DUPLICATE **，** ZX_RIGHT_READ **，** ZX_RIGHT_WRITE **，** ZX_RIGHT_SIGNAL **和** ZX_RIGHT_SIGNAL_PEER **权限。

Currently, no options are supported, so *options* must be set to 0.  当前，不支持任何选项，因此* options *必须设置为0。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_eventpair_create()` returns **ZX_OK** on success. On failure, a (negative) error code is returned. zx_eventpair_create（）成功返回** ZX_OK **。失败时，将返回（负）错误代码。

 

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out0* or *out1* is an invalid pointer or NULL.  ** ZX_ERR_INVALID_ARGS ** * out0 *或* out1 *是无效的指针或NULL。

**ZX_ERR_NOT_SUPPORTED**  *options* has an unsupported flag set (i.e., is not 0).  ** ZX_ERR_NOT_SUPPORTED ** *选项*设置了不受支持的标志（即不为0）。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_event_create()`]  -[`zx_event_create（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_signal()`]  -[`zx_object_signal（）`]
 - [`zx_object_signal_peer()`]  -[`zx_object_signal_peer（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

