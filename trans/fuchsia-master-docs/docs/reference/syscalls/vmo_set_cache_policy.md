 
# zx_vmo_set_cache_policy  zx_vmo_set_cache_policy 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Set the caching policy for pages held by a VMO.  为VMO保留的页面设置缓存策略。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_set_cache_policy(zx_handle_t handle, uint32_t cache_policy);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_set_cache_policy()` sets caching policy for a VMO. Generally used on VMOs that point directly at physical memory. Such VMOs are generally only handed touserspace via bus protocol interfaces, so this syscall will typically only beused by drivers dealing with device memory. This call can also be used on aregular memory backed VMO with similar limitations and uses. zx_vmo_set_cache_policy（）设置VMO的缓存策略。通常用于直接指向物理内存的VMO。此类VMO通常仅通过总线协议接口传递给用户空间，因此该系统调用通常仅由处理设备内存的驱动程序使用。此调用也可以在具有类似限制和用途的基于区域内存的VMO上使用。

A handle must have the **ZX_RIGHT_MAP** right for this call to be permitted. Additionally, the VMO must not presently be mapped by any process,have any children, be a child itself, or have any memory committed. 句柄必须具有** ZX_RIGHT_MAP **权限才能允许此调用。此外，VMO当前不得通过任何进程进行映射，具有任何子代，本身是子代或已提交任何内存。

*cache_policy* cache flags to use:  * cache_policy *缓存标志以使用：

**ZX_CACHE_POLICY_CACHED** - Use hardware caching. On Aarch64 this corresponds to the Normal Memory, Outer Write-back non-transient Read and Write allocate, InnerWrite-back non-transient Read and Write allocate memory attributes ** ZX_CACHE_POLICY_CACHED **-使用硬件缓存。在Aarch64上，这对应于“普通内存”，“外部写回非瞬态读写”分配，“内部写回非瞬态读写”分配内存属性

**ZX_CACHE_POLICY_UNCACHED** - Disable caching. On Aarch64 this corresponds to the Device-nGnRnE memory attributes. ** ZX_CACHE_POLICY_UNCACHED **-禁用缓存。在Aarch64上，这对应于Device-nGnRnE内存属性。

**ZX_CACHE_POLICY_UNCACHED_DEVICE** - Disable cache and treat as device memory. This is architecture dependent and may be equivalent to**ZX_CACHE_POLICY_UNCACHED** on some architectures. On Aarch64 this corresponds tothe Device-nGnRE memory attributes. ** ZX_CACHE_POLICY_UNCACHED_DEVICE **-禁用缓存并将其视为设备内存。这取决于体系结构，在某些体系结构上可能等效于** ZX_CACHE_POLICY_UNCACHED **。在Aarch64上，这对应于Device-nGnRE内存属性。

**ZX_CACHE_POLICY_WRITE_COMBINING** - Uncached with write combining. On Aarch64 this corresponds to the Normal memory, uncached memory attributes. ** ZX_CACHE_POLICY_WRITE_COMBINING **-通过写合并未缓存。在Aarch64上，它对应于普通内存，未缓存的内存属性。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_MAP**.  *句柄*必须为** ZX_OBJ_TYPE_VMO **类型，并具有** ZX_RIGHT_MAP **。

 
## RETURN VALUE  返回值 

`zx_vmo_set_cache_policy()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_vmo_set_cache_policy（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** Cache policy has been configured for this VMO already and may not be changed, or *handle* lacks the **ZX_RIGHT_MAP** right. ** ZX_ERR_ACCESS_DENIED **已经为此VMO配置了缓存策略，并且可能无法更改，或者* handle *缺少** ZX_RIGHT_MAP **权限。

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_INVALID_ARGS** *cache_policy* contains flags outside of the ones listed above, or *cache_policy* contains an invalid mix of cache policy flags. ** ZX_ERR_INVALID_ARGS ** * cache_policy *包含上述标记之外的标记，或者* cache_policy *包含无效的缓存策略标记组合。

**ZX_ERR_NOT_SUPPORTED** The VMO *handle* corresponds to is not one holding physical memory. ** ZX_ERR_NOT_SUPPORTED **对应的VMO *句柄*不是一个持有物理内存的内存。

**ZX_ERR_BAD_STATE** Cache policy cannot be changed because the VMO is presently mapped, has children, is a child itself, or have any memory committed. ** ZX_ERR_BAD_STATE **不能更改缓存策略，因为VMO当前已映射，具有子项，本身是子项或已提交任何内存。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

