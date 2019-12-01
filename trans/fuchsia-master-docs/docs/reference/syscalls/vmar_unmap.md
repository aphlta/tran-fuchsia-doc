 
# zx_vmar_unmap  zx_vmar_unmap 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Unmap virtual memory pages.  取消映射虚拟内存页面。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_unmap(zx_handle_t handle, zx_vaddr_t addr, uint64_t len);
```
 

 
## DESCRIPTION  描述 

`zx_vmar_unmap()` unmaps all VMO mappings and destroys (as if [`zx_vmar_destroy()`] were called) all sub-regions within the absolute range including *addr* and endingbefore exclusively at `addr + len`.  Any sub-region that is in the range mustbe fully in the range (i.e. partial overlaps are an error).  If a mapping isonly partially in the range, the mapping is split and the requested portion isunmapped. “ zx_vmar_unmap（）”取消映射所有VMO映射并销毁（好像调用了“`[zx_vmar_destroy（）”）一样）绝对范围内的所有子区域，包括* addr *并在“ addr + len”之前结束。该范围内的任何子区域都必须完全在该范围内（即部分重叠是错误的）。如果映射仅部分在该范围内，则将拆分映射，并取消映射所请求的部分。

*len* must be page-aligned.  * len *必须页面对齐。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_vmar_unmap()` returns **ZX_OK** on success.  zx_vmar_unmap（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMAR handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMAR句柄。

**ZX_ERR_INVALID_ARGS**  *addr* is not page-aligned, *len* is 0 or not page-aligned, or the requested range partially overlaps a sub-region. ** ZX_ERR_INVALID_ARGS ** * addr *没有页面对齐，* len *是0或页面没有对齐，或者请求的范围部分重叠了子区域。

**ZX_ERR_BAD_STATE**  *handle* refers to a destroyed handle.  ** ZX_ERR_BAD_STATE ** * handle *表示已销毁的句柄。

**ZX_ERR_NOT_FOUND**  Could not find the requested mapping.  ** ZX_ERR_NOT_FOUND **找不到请求的映射。

 
## NOTES  笔记 

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_allocate()`]  -[`zx_vmar_allocate（）`]
 - [`zx_vmar_destroy()`]  -[`zx_vmar_destroy（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmar_protect()`]  -[`zx_vmar_protect（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

