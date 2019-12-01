 
# zx_vmar_destroy  zx_vmar_destroy 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Destroy a virtual memory address region.  销毁虚拟内存地址区域。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_destroy(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_vmar_destroy()` unmaps all mappings within the given region, and destroys all sub-regions of the region.  Note that this operation is logically recursive. zx_vmar_destroy（）取消映射给定区域内的所有映射，并销毁该区域的所有子区域。请注意，此操作在逻辑上是递归的。

This operation does not close *handle*.  Any outstanding handles to this VMAR will remain valid handles, but all VMAR operations on them will fail. 此操作不会关闭*句柄*。此VMAR的所有未完成的句柄将保持有效的句柄，但对其进行的所有VMAR操作将失败。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_vmar_destroy()` returns **ZX_OK** on success.  zx_vmar_destroy（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMAR handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMAR句柄。

**ZX_ERR_BAD_STATE**  This region is already destroyed.  ** ZX_ERR_BAD_STATE **该区域已被破坏。

 
## NOTES  笔记 

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_allocate()`]  -[`zx_vmar_allocate（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmar_protect()`]  -[`zx_vmar_protect（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

