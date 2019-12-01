 
# zx_vmo_replace_as_executable  zx_vmo_replace_as_executable 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Add execute rights to a VMO.  向VMO添加执行权限。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_replace_as_executable(zx_handle_t handle,
                                         zx_handle_t vmex,
                                         zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_replace_as_executable()` creates a replacement for *handle*, referring to the same underlying VM object, adding the right **ZX_RIGHT_EXECUTE**. zx_vmo_replace_as_executable（）创建* handle *的替换，引用相同的基础VM对象，并添加右** ZX_RIGHT_EXECUTE **。

*handle* is always invalidated.  *句柄*总是无效的。

*vmex* may currently be **ZX_HANDLE_INVALID** to ease migration of new code, this is TODO(SEC-42) and will be removed. * vmex *当前可能是** ZX_HANDLE_INVALID **以简化新代码的迁移，这是TODO（SEC-42），将被删除。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMO**.  *句柄*必须为** ZX_OBJ_TYPE_VMO **类型。

*vmex* must have resource kind **ZX_RSRC_KIND_VMEX**.  * vmex *必须具有资源类型** ZX_RSRC_KIND_VMEX **。

 
## RETURN VALUE  返回值 

`zx_vmo_replace_as_executable()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_replace_as_executable（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* isn't a valid VM object handle, or *vmex* isn't a valid **ZX_RSRC_KIND_VMEX** resource handle. ** ZX_ERR_BAD_HANDLE ** * handle *不是有效的VM对象句柄，或者* vmex *不是有效的** ZX_RSRC_KIND_VMEX **资源句柄。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_resource_create()`]  -[`zx_resource_create（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

