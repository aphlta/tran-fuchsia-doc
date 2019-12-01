 
# zx_pager_detach_vmo  zx_pager_detach_vmo 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Detaches a vmo from a pager.  从寻呼机上卸下vmo。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pager_detach_vmo(zx_handle_t pager, zx_handle_t vmo);
```
 

 
## DESCRIPTION  描述 

Detaching *vmo* from *pager* causes the kernel to stop queuing page requests for the vmo. Subsequent accesses which would have generated page requests will instead fail. 从* pager *分离* vmo *会导致内核停止对vmo的页面请求进行排队。随后会生成页面请求的访问将失败。

No new **ZX_PAGER_VMO_READ** requests will be generated after detaching, but some requests may still be in flight. The pager service is free to ignore these requests, as the kernel will resume andfault the threads which generated these requests. The final request the pager service willreceive is a **ZX_PAGER_VMO_COMPLETE** request. 分离后将不会生成新的** ZX_PAGER_VMO_READ **请求，但某些请求可能仍在执行中。寻呼机服务可以随意忽略这些请求，因为内核将继续执行并修复生成这些请求的线程。寻呼机服务将收到的最终请求是** ZX_PAGER_VMO_COMPLETE **请求。

The kernel is free to evict clean pages from deregistered vmos.  内核可以自由地从注销的vmos中清除干净的页面。

TODO(stevensd): Update once writeback is supported.  TODO（stevensd）：一旦支持写回就更新。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*pager* must be of type **ZX_OBJ_TYPE_PAGER**.  * pager *必须为** ZX_OBJ_TYPE_PAGER **类型。

*vmo* must be of type **ZX_OBJ_TYPE_VMO**.  * vmo *必须为** ZX_OBJ_TYPE_VMO **类型。

 
## RETURN VALUE  返回值 

`zx_pager_detach_vmo()` returns ZX_OK on success, or one of the following error codes on failure.  zx_pager_detach_vmo（）成功返回ZX_OK，失败则返回以下错误代码之一。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *pager* or *vmo* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * pager *或* vmo *不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *pager* is not a pager handle or *vmo* is not a vmo handle.  ** ZX_ERR_WRONG_TYPE ** * pager *不是寻呼机句柄，或者* vmo *不是vmo句柄。

**ZX_ERR_INVALID_ARGS**  *vmo* is not a vmo created from *pager*.  ** ZX_ERR_INVALID_ARGS ** * vmo *不是从* pager *创建的vmo。

 
## SEE ALSO  也可以看看 

 
 - [`zx_pager_create_vmo()`]  -[`zx_pager_create_vmo（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

