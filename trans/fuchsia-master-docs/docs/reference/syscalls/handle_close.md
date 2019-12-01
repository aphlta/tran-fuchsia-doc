 
# zx_handle_close  zx_handle_close 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Close a handle.  关闭手柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_handle_close(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_handle_close()` closes a *handle*, causing the underlying object to be reclaimed by the kernel if no other handles to it exist. zx_handle_close（）关闭* handle *，如果不存在基础对象，则内核将回收该基础对象。

If the *handle* was used in a pending [`zx_object_wait_one()`] or a [`zx_object_wait_many()`] call, the wait will be aborted. 如果* handle *在未决的[`zx_object_wait_one（）`]或[`zx_object_wait_many（）`]调用中使用，则等待将被中止。

It is not an error to close the special "never a valid handle" **ZX_HANDLE_INVALID**, similar to `free(NULL)` being a valid call. 关闭特殊的“永不有效的句柄” ** ZX_HANDLE_INVALID **并不是错误，类似于`free（NULL）`是有效的调用。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_handle_close()` returns **ZX_OK** on success.  zx_handle_close（）成功时返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* isn't a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close_many()`]  -[`zx_handle_close_many（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

