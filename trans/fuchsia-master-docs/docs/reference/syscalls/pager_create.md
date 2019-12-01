 
# zx_pager_create  zx_pager_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a new pager object.  创建一个新的寻呼机对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pager_create(uint32_t options, zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_pager_create()` creates a new pager object.  zx_pager_create（）创建一个新的寻呼机对象。

When a pager object is destroyed, any accesses to its vmos that would have required communicating with the pager will fail as if [`zx_pager_detach_vmo()`] had been called. Furthermore, the kernelwill make an effort to ensure that the faults happen as quickly as possible (e.g. by evictingpresent pages), but the precise behavior is implementation dependent. 销毁寻呼机对象后，需要与寻呼机通信的对其vmos的任何访问都将失败，就好像调用了[`zx_pager_detach_vmo（）]一样。此外，内核将努力确保故障尽快发生（例如通过驱逐当前页面），但是确切的行为取决于实现。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_pager_create()` returns ZX_OK on success, or one of the following error codes on failure.  zx_pager_create（）成功时返回ZX_OK，失败则返回以下错误代码之一。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS** *out* is an invalid pointer or NULL or *options* is any value other than 0. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针，或者NULL或* options *是除0以外的任何值。

**ZX_ERR_NO_MEMORY** Failure due to lack of memory.  ** ZX_ERR_NO_MEMORY **由于内存不足而失败。

 
## SEE ALSO  也可以看看 

 
 - [`zx_pager_create_vmo()`]  -[`zx_pager_create_vmo（）`]
 - [`zx_pager_detach_vmo()`]  -[`zx_pager_detach_vmo（）`]
 - [`zx_pager_supply_pages()`]  -[`zx_pager_supply_pages（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

