 
# zx_pmt_unpin  zx_pmt_unpin 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Unpin pages and revoke device access to them.  取消固定页面并撤消设备对其的访问权限。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pmt_unpin(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_pmt_unpin()` unpins pages that were previously pinned by [`zx_bti_pin()`], and revokes the access that was granted by the pin call. `zx_pmt_unpin（）`取消固定先前由[`zx_bti_pin（）]固定的页面，并撤消由pin调用授予的访问权限。

Always consumes *handle*. It is invalid to use *handle* afterwards, including to call [`zx_handle_close()`] on it. 总是消耗* handle *。此后再使用* handle *是无效的，包括对其调用[`zx_handle_close（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

On success, `zx_pmt_unpin()` returns **ZX_OK**. In the event of failure, a negative error value is returned. 成功时，`zx_pmt_unpin（）`返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a PMT handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是PMT句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_bti_create()`]  -[`zx_bti_create（）`]
 - [`zx_bti_pin()`]  -[`zx_bti_pin（）`]
 - [`zx_bti_release_quarantine()`]  -[`zx_bti_release_quarantine（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

