 
# zx_handle_replace  zx_handle_replace 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Replace a handle.  更换手柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_handle_replace(zx_handle_t handle,
                              zx_rights_t rights,
                              zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_handle_replace()` creates a replacement for *handle*, referring to the same underlying object, with new access rights *rights*. `zx_handle_replace（）`使用相同的访问权限* rights *来创建* handle *的替换，引用同一基础对象。

*handle* is always invalidated.  *句柄*总是无效的。

If *rights* is **ZX_RIGHT_SAME_RIGHTS**, the replacement handle will have the same rights as the original handle. Otherwise, *rights* must bea subset of original handle's rights. 如果* rights *是** ZX_RIGHT_SAME_RIGHTS **，则替换手柄将具有与原始手柄相同的权限。否则，“权利”必须是原始句柄权利的子集。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_handle_replace()` returns **ZX_OK** and the replacement handle (via *out*) on success. zx_handle_replace（）在成功时返回** ZX_OK **和替换句柄（通过* out *）。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* isn't a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_INVALID_ARGS**  The *rights* requested are not a subset of *handle*'s rights or *out* is an invalid pointer. ** ZX_ERR_INVALID_ARGS **所请求的* rights不是* handle *权限的子集，或者* out *是无效的指针。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_close_many()`]  -[`zx_handle_close_many（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

