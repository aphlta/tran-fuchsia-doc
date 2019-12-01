 
# zx_event_create  zx_event_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create an event.  创建一个事件。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_event_create(uint32_t options, zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_event_create()` creates an event, which is an object that is signalable. That is, its **ZX_USER_SIGNAL_n** (where *n* is 0 through 7) signals can bemanipulated using [`zx_object_signal()`]. zx_event_create（）创建一个事件，该事件是可发信号的对象。也就是说，可以使用[`zx_object_signal（）`来操纵其** ZX_USER_SIGNAL_n **（其中* n *为0到7）信号。

The newly-created handle will have the [basic rights](/docs/concepts/kernel/rights.md#zx_rights_basic) plus **ZX_RIGHT_SIGNAL**. 新创建的句柄将具有[基本权限]（/ docs / concepts / kernel / rights.mdzx_rights_basic）加上** ZX_RIGHT_SIGNAL **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_event_create()` returns **ZX_OK** and a valid event handle (via *out*) on success. On failure, an error value is returned. zx_event_create（）在成功时返回** ZX_OK **和有效的事件句柄（通过* out *）。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer, or *options* is nonzero.  ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针，或* options *非零。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_eventpair_create()`]  -[`zx_eventpair_create（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_signal()`]  -[`zx_object_signal（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

