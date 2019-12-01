 
# zx_handle_duplicate  zx_handle_duplicate 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Duplicate a handle.  复制一个句柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_handle_duplicate(zx_handle_t handle,
                                zx_rights_t rights,
                                zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_handle_duplicate()` creates a duplicate of *handle*, referring to the same underlying object, with new access rights *rights*. `zx_handle_duplicate（）`创建* handle *的副本，引用相同的基础对象，并具有新的访问权限* rights *。

To duplicate the handle with the same rights use **ZX_RIGHT_SAME_RIGHTS**. If different rights are desired they must be strictly lesser than of the source handle. It is possibleto specify no rights by using **ZX_RIGHT_NONE**. To remove **ZX_RIGHT_DUPLICATE** right whentransferring through a channel, use [`zx_channel_write_etc()`]. 要复制具有相同权限的句柄，请使用** ZX_RIGHT_SAME_RIGHTS **。如果需要不同的权限，则这些权限必须严格小于源句柄的权限。可以使用** ZX_RIGHT_NONE **指定无权限。要在通过频道传输时删除** ZX_RIGHT_DUPLICATE **，请使用[`zx_channel_write_etc（）]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_DUPLICATE**.  *句柄*必须具有** ZX_RIGHT_DUPLICATE **。

 
## RETURN VALUE  返回值 

`zx_handle_duplicate()` returns **ZX_OK** and the duplicate handle via *out* on success.  zx_handle_duplicate（）在成功时通过** out *返回** ZX_OK **和重复句柄。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* isn't a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_INVALID_ARGS**  The *rights* requested are not a subset of *handle* rights or *out* is an invalid pointer. ** ZX_ERR_INVALID_ARGS **所请求的* rights不是* handle *权限的子集，或者* out *是无效的指针。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_DUPLICATE** and may not be duplicated.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_DUPLICATE **，并且可能不会重复。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [rights](/docs/concepts/kernel/rights.md)  -[权限]（/ docs / concepts / kernel / rights.md）
 - [`zx_channel_write_etc()`]  -[`zx_channel_write_etc（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_close_many()`]  -[`zx_handle_close_many（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

