 
# zx_pager_supply_pages  zx_pager_supply_pages 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Supply pages into a pager owned vmo.  将页面供应到寻呼机拥有的vmo中。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pager_supply_pages(zx_handle_t pager,
                                  zx_handle_t pager_vmo,
                                  uint64_t offset,
                                  uint64_t length,
                                  zx_handle_t aux_vmo,
                                  uint64_t aux_offset);
```
 

 
## DESCRIPTION  描述 

Moves the pages of *aux_vmo* in the range [*aux_offset*, *aux_offset* + *length*) to *pager_vmo* in the range [*offset*, *offset* + *length*). Any pages in *pager_vmo* in the specified range will notbe replaced; instead the corresponding pages from *aux_vmo* will be freed. *aux_vmo* must have beencreated by [`zx_vmo_create()`], must have no children or mappings, and must be fully committed withno pinned pages in the specified range. After this operation, the specified region of *aux_vmo* willbe fully decommitted. 将[aux_offset *，* aux_offset * + * length *）范围内的* aux_vmo *页面移动到[* offset *，* offset * + * length *]范围内的* pager_vmo *页面。 * pager_vmo *中指定范围内的任何页面都不会被替换；而是将释放* aux_vmo *中的相应页面。 * aux_vmo *必须由[`zx_vmo_create（）`]创建，必须没有子代或映射，并且必须完全提交且没有指定范围内的固定页面。完成此操作后，* aux_vmo *的指定区域将被完全取消使用。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*pager* must be of type **ZX_OBJ_TYPE_PAGER**.  * pager *必须为** ZX_OBJ_TYPE_PAGER **类型。

*pager_vmo* must be of type **ZX_OBJ_TYPE_VMO**.  * pager_vmo *必须为** ZX_OBJ_TYPE_VMO **类型。

*aux_vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ** and have **ZX_RIGHT_WRITE**.  * aux_vmo *必须为** ZX_OBJ_TYPE_VMO **类型，并且具有** ZX_RIGHT_READ **和** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_pager_supply_pages()` returns ZX_OK on success, or one of the following error codes on failure. On failure the specified range of *aux_vmo* may be either untouched or fully decommitted. If*aux_vmo* is decommitted, then an unspecified number of pages in *pager_vmo* will have beenpopulated. zx_pager_supply_pages（）成功返回ZX_OK，失败则返回以下错误代码之一。失败时，* aux_vmo *的指定范围可能未触及或完全取消使用。如果* aux_vmo *被停用，则* pager_vmo *中的未指定页面数将被填充。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *pager*, *pager_vmo*, or *aux_vmo* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * pager *，* pager_vmo *或* aux_vmo *不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *pager* is not a pager handle, *pager_vmo* is not a vmo handle, or *aux_vmo* is not a vmo handle. ** ZX_ERR_WRONG_TYPE ** * pager *不是寻呼机句柄，* pager_vmo *不是vmo句柄，或者* aux_vmo *不是vmo句柄。

**ZX_ERR_INVALID_ARGS**  *pager_vmo* is not a vmo created from *pager*, or *offset*, *size*, or *aux_offset* is not page aligned. ** ZX_ERR_INVALID_ARGS ** * pager_vmo *不是从* pager *创建的vmo，或者* offset *，* size *或* aux_offset *不是页面对齐的。

**ZX_ERR_ACCESS_DENIED** *aux_vmo* is does not have **ZX_RIGHT_WRITE** or **ZX_RIGHT_READ**.  ** ZX_ERR_ACCESS_DENIED ** * aux_vmo *没有** ZX_RIGHT_WRITE **或** ZX_RIGHT_READ **。

**ZX_ERR_BAD_STATE** *aux_vmo* is not in a state where it can supply the required pages.  ** ZX_ERR_BAD_STATE ** * aux_vmo *处于无法提供所需页面的状态。

**ZX_ERR_NOT_SUPPORTED** *aux_vmo* is a physical vmo.  ** ZX_ERR_NOT_SUPPORTED ** * aux_vmo *是物理vmo。

**ZX_ERR_OUT_OF_RANGE** The specified range in *pager_vmo* or *aux_vmo* is invalid.  ** ZX_ERR_OUT_OF_RANGE **在* pager_vmo *或* aux_vmo *中指定的范围无效。

**ZX_ERR_NO_MEMORY** Failure due to lack of memory.  ** ZX_ERR_NO_MEMORY **由于内存不足而失败。

 
## SEE ALSO  也可以看看 

 
 - [`zx_pager_create_vmo()`]  -[`zx_pager_create_vmo（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

