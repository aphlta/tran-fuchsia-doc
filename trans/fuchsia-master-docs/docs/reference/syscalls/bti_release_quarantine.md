 
# zx_bti_release_quarantine  zx_bti_release_quarantine 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Releases all quarantined PMTs.  释放所有隔离的PMT。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_bti_release_quarantine(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_bti_release_quarantine()` releases all quarantined PMTs for the given BTI. This will release the PMTs' underlying references to VMOs and physical pagepins.  The underlying physical pages may be eligible to be reallocatedafterwards. zx_bti_release_quarantine（）释放给定BTI的所有隔离的PMT。这将释放PMT对VMO和物理分页图钉的基础引用。基础物理页面可能有资格在以后重新分配。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_BTI** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_BTI **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_bti_release_quarantine()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_bti_release_quarantine（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a BTI handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是BTI句柄。

**ZX_ERR_ACCESS_DENIED** *handle* does not have the **ZX_RIGHT_WRITE** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **权限。

 
## SEE ALSO  也可以看看 

 
 - [`zx_bti_pin()`]  -[`zx_bti_pin（）`]
 - [`zx_pmt_unpin()`]  -[`zx_pmt_unpin（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

