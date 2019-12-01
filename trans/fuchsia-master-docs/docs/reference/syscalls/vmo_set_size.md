 
# zx_vmo_set_size  zx_vmo_set_size 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Resize a VMO object.  调整VMO对象的大小。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_set_size(zx_handle_t handle, uint64_t size);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_set_size()` sets the new size of a VMO object.  zx_vmo_set_size（）设置VMO对象的新大小。

The size will be rounded up to the next page size boundary. Subsequent calls to [`zx_vmo_get_size()`] will return the rounded up size. 尺寸将四舍五入到下一页的尺寸边界。随后调用[`zx_vmo_get_size（）]将返回四舍五入的大小。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_VMO **且具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_vmo_set_size()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_set_size（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMO handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMO句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have the **ZX_RIGHT_WRITE** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **权限。

**ZX_ERR_UNAVAILABLE** The VMO was not created with **ZX_VMO_RESIZABLE** or **ZX_VMO_CHILD_RESIZABLE**. ** ZX_ERR_UNAVAILABLE **不是使用** ZX_VMO_RESIZABLE **或** ZX_VMO_CHILD_RESIZABLE **创建的VMO。

**ZX_ERR_OUT_OF_RANGE**  Requested size is too large.  ** ZX_ERR_OUT_OF_RANGE **请求的大小太大。

**ZX_ERR_NO_MEMORY**  Failure due to lack of system memory.  ** ZX_ERR_NO_MEMORY **由于缺少系统内存而失败。

**ZX_ERR_BAD_STATE**  Requested size would discard pinned pages.  ** ZX_ERR_BAD_STATE **请求的大小将丢弃固定的页面。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_create_child()`]  -[`zx_vmo_create_child（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

