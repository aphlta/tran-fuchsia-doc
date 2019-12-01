 
# zx_handle_close_many  zx_handle_close_many 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Close a number of handles.  关闭许多手柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_handle_close_many(const zx_handle_t* handles,
                                 size_t num_handles);
```
 

 
## DESCRIPTION  描述 

`zx_handle_close_many()` closes a number of handles, causing each underlying object to be reclaimed by the kernel if no other handles toit exist. zx_handle_close_many（）关闭许多句柄，如果不存在其他句柄，则内核将回收每个基础对象。

If a handle was used in a pending [`zx_object_wait_one()`] or a [`zx_object_wait_many()`] call, the wait will be aborted. 如果在待处理的[`zx_object_wait_one（）]或[`zx_object_wait_many（）]调用中使用了句柄，则等待将被中止。

This operation closes all handles presented to it, even if one or more of the handles is duplicate or invalid. 即使一个或多个句柄重复或无效，此操作也会关闭提供给它的所有句柄。

It is not an error to close the special "never a valid handle" **ZX_HANDLE_INVALID**, similar to `free(NULL)` being a valid call. 关闭特殊的“永不有效的句柄” ** ZX_HANDLE_INVALID **并不是错误，类似于`free（NULL）`是有效的调用。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_handle_close_many()` returns **ZX_OK** on success.  zx_handle_close_many（）在成功时返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  One of the *handles* isn't a valid handle, or the same handle is present multiple times. ** ZX_ERR_BAD_HANDLE ** *一个句柄*不是有效的句柄，或者同一句柄多次出现。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

