 
# zx_iommu_create  zx_iommu_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a new IOMMU object in the kernel.  在内核中创建一个新的IOMMU对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_iommu_create(zx_handle_t resource,
                            uint32_t type,
                            const void* desc,
                            size_t desc_size,
                            zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_iommu_create()` creates a new object in the kernel representing an IOMMU device.  zx_iommu_create（）在内核中创建一个代表IOMMU设备的新对象。

The value of *type* determines the interpretation of *desc*.  See below for details about the values of *type*. * type *的值确定* desc *的解释。有关* type *值的详细信息，请参见下文。

Upon success, a handle for the new IOMMU is returned.  This handle will have rights **ZX_RIGHT_DUPLICATE** and **ZX_RIGHT_TRANSFER**. 成功后，将返回新IOMMU的句柄。此句柄将具有权限** ZX_RIGHT_DUPLICATE **和** ZX_RIGHT_TRANSFER **。

 
### *type* = **ZX_IOMMU_TYPE_DUMMY**  *类型* = ** ZX_IOMMU_TYPE_DUMMY ** 

This type represents a no-op IOMMU.  It provides no hardware-level protections against unauthorized access to memory.  It does allow pinning of physical memorypages, to prevent the reuse of a page until the driver using the page says it isdone with it. 此类型表示无操作IOMMU。它没有针对未经授权访问内存的硬件级别保护。它确实允许固定物理内存页面，以防止页面重用，直到使用该页面的驱动程序说它已经完成。

*desc* must be a valid pointer to a value of type `zx_iommu_desc_dummy_t`. *desc_size* must be `sizeof(zx_iommu_desc_dummy_t)`. * desc *必须是指向`zx_iommu_desc_dummy_t`类型的值的有效指针。 * desc_size *必须为`sizeof（zx_iommu_desc_dummy_t）`。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_ROOT**.  * resource *必须具有资源类型** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

`zx_iommu_create()` returns **ZX_OK** and a handle to the new IOMMU (via *out*) on success.  In the event of failure, a negative error valueis returned. zx_iommu_create（）成功返回** ZX_OK **和新IOMMU的句柄（通过* out *）。发生故障时，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *resource* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *资源*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *resource* is not a resource handle.  ** ZX_ERR_WRONG_TYPE ** *资源*不是资源句柄。

**ZX_ERR_ACCESS_DENIED**  *resource* handle does not have sufficient privileges.  ** ZX_ERR_ACCESS_DENIED ** *资源*句柄没有足够的特权。

**ZX_ERR_NOT_SUPPORTED** *type* is not a defined value or is not supported on this system. ** ZX_ERR_NOT_SUPPORTED ** * type *不是定义的值，或者在此系统上不受支持。

**ZX_ERR_INVALID_ARGS**  *desc_size* is larger than **ZX_IOMMU_MAX_DESC_LEN**, *desc* is an invalid pointer, *out* is an invalid pointer, or the contents of*desc* are not valid for the given *type*. ** ZX_ERR_INVALID_ARGS ** * desc_size *大于** ZX_IOMMU_MAX_DESC_LEN **，* desc *是无效的指针，* out *是无效的指针，或者* desc *的内容对于给定的* type *无效。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_bti_create()`]  -[`zx_bti_create（）`]
 - [`zx_bti_pin()`]  -[`zx_bti_pin（）`]
 - [`zx_pmt_unpin()`]  -[`zx_pmt_unpin（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

