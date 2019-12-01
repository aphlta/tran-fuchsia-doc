 
# zx_vmar_allocate  zx_vmar_allocate 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Allocate a new subregion.  分配一个新的子区域。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_allocate(zx_handle_t parent_vmar,
                             zx_vm_option_t options,
                             uint64_t offset,
                             uint64_t size,
                             zx_handle_t* child_vmar,
                             zx_vaddr_t* child_addr);
```
 

 
## DESCRIPTION  描述 

Creates a new VMAR within the one specified by *parent_vmar*.  在* parent_vmar *指定的范围内创建一个新的VMAR。

*options* is a bit vector that contains one more of the following:  * options *是一个位向量，包含以下一项：

 
- **ZX_VM_COMPACT**  A hint to the kernel that allocations and mappings within the newly created subregion should be kept close together.   See theNOTES section below for discussion. -** ZX_VM_COMPACT **给内核的提示是，新创建的子区域内的分配和映射应保持紧密联系。请参阅下面的“注释”部分进行讨论。
- **ZX_VM_SPECIFIC**  Use the *offset* to place the mapping, invalid if vmar does not have the **ZX_VM_CAN_MAP_SPECIFIC** permission.  *offset*is an offset relative to the base address of the parent region.  It is an errorto specify an address range that overlaps with another VMAR or mapping. -** ZX_VM_SPECIFIC **使用* offset *放置映射，如果vmar没有** ZX_VM_CAN_MAP_SPECIFIC **权限，则无效。 * offset *是相对于父区域的基地址的偏移量。指定与另一个VMAR或映射重叠的地址范围是错误的。
- **ZX_VM_CAN_MAP_SPECIFIC**  The new VMAR can have subregions/mappings created with **ZX_VM_SPECIFIC**.  It is NOT an error if the parent doesnot have **ZX_VM_CAN_MAP_SPECIFIC** permissions. -** ZX_VM_CAN_MAP_SPECIFIC **新的VMAR可以具有使用** ZX_VM_SPECIFIC **创建的子区域/映射。如果父级没有** ZX_VM_CAN_MAP_SPECIFIC **权限，这不是错误。
- **ZX_VM_CAN_MAP_READ**  The new VMAR can contain readable mappings. It is an error if the parent does not have **ZX_VM_CAN_MAP_READ** permissions. -** ZX_VM_CAN_MAP_READ **新的VMAR可以包含可读的映射。如果父级没有** ZX_VM_CAN_MAP_READ **权限，这是一个错误。
- **ZX_VM_CAN_MAP_WRITE**  The new VMAR can contain writable mappings. It is an error if the parent does not have **ZX_VM_CAN_MAP_WRITE** permissions. -** ZX_VM_CAN_MAP_WRITE **新的VMAR可以包含可写映射。如果父级没有** ZX_VM_CAN_MAP_WRITE **权限，则会出现错误。
- **ZX_VM_CAN_MAP_EXECUTE**  The new VMAR can contain executable mappings. It is an error if the parent does not have **ZX_VM_CAN_MAP_EXECUTE** permissions. -** ZX_VM_CAN_MAP_EXECUTE **新的VMAR可以包含可执行映射。如果父级没有** ZX_VM_CAN_MAP_EXECUTE **权限，这是一个错误。

*offset* must be 0 if *options* does not have **ZX_VM_SPECIFIC** set.  如果* options *没有设置** ZX_VM_SPECIFIC **，则* offset *必须为0。

In addition, the following power-of-two alignment flags can added:  此外，可以添加以下两个幂的对齐标志：

 
- **ZX_VM_ALIGN_1KB** aligns *child_addr* to a power-of-2 at least 1K bytes.  -** ZX_VM_ALIGN_1KB **将* child_addr *对齐为2的幂，至少为1K字节。
- **ZX_VM_ALIGN_2KB** aligns *child_addr* to a power-of-2 at least 2K bytes.  -** ZX_VM_ALIGN_2KB **将* child_addr *对齐为2的幂，至少2K字节。
- **ZX_VM_ALIGN_4KB** aligns *child_addr* to a power-of-2 at least 4K bytes.  -** ZX_VM_ALIGN_4KB **将* child_addr *对齐为2的幂，至少4K字节。
- **ZX_VM_ALIGN_8KB** aligns *child_addr* to a power-of-2 at least 8K bytes.  -** ZX_VM_ALIGN_8KB **将* child_addr *对齐为2的幂，至少8K字节。

and continues up to  并持续到

 
- **ZX_VM_ALIGN_4GB** aligns *child_addr* to a power-of-2 at least 4G bytes.  -** ZX_VM_ALIGN_4GB **将* child_addr *对齐为2的幂，至少4G字节。

TODO(ZX-3978): Currently, alignment flags greater than 4KB cannot be used when allocating a new VMAR within a compact VMAR. TODO（ZX-3978）：当前，在紧凑型VMAR中分配新的VMAR时，不能使用大于4KB的对齐标志。

Using **ZX_VM_ALIGN** flags with **ZX_VM_SPECIFIC** will fail if the *parent_vmar* base address + *offset* are not aligned to the requestedvalue. 如果* parent_vmar *基地址+ * offset *未与请求值对齐，则将** ZX_VM_ALIGN **标志与** ZX_VM_SPECIFIC **一起使用将失败。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

If *options* & **ZX_VM_CAN_MAP_READ**, *parent_vmar* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_READ**.  如果* options * ** ZX_VM_CAN_MAP_READ **，则* parent_vmar *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_READ **。

If *options* & **ZX_VM_CAN_MAP_WRITE**, *parent_vmar* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_WRITE**.  如果* options * ** ZX_VM_CAN_MAP_WRITE **，则* parent_vmar *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_WRITE **。

If *options* & **ZX_VM_CAN_MAP_EXECUTE**, *parent_vmar* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_EXECUTE**.  如果* options * ** ZX_VM_CAN_MAP_EXECUTE **，则* parent_vmar *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_EXECUTE **。

 
## RETURN VALUE  返回值 

`zx_vmar_allocate()` returns **ZX_OK**, the absolute base address of the subregion (via *child_addr*), and a handle to the new subregion (via*child_vmar*) on success.  The base address will be page-aligned and non-zero.In the event of failure, a negative error value is returned. zx_vmar_allocate（）返回** ZX_OK **，该子区域的绝对基地址（通过* child_addr *），并在成功时返回新子区域的句柄（通过* child_vmar *）。基址将是页面对齐且非零。如果发生故障，则返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *parent_vmar* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * parent_vmar *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *parent_vmar* is not a VMAR handle.  ** ZX_ERR_WRONG_TYPE ** * parent_vmar *不是VMAR句柄。

**ZX_ERR_BAD_STATE**  *parent_vmar* refers to a destroyed VMAR.  ** ZX_ERR_BAD_STATE ** * parent_vmar *是指已损坏的VMAR。

**ZX_ERR_INVALID_ARGS**  *child_vmar* or *child_addr* are not valid, *offset* is non-zero when **ZX_VM_SPECIFIC** is not given, *offset* and *size* describean unsatisfiable allocation due to exceeding the region bounds, *offset*or *size* is not page-aligned, or *size* is 0. ** ZX_ERR_INVALID_ARGS ** * child_vmar *或* child_addr *无效，当未提供** ZX_VM_SPECIFIC **时，* offset *不为零，* offset *和* size *描述了由于超出区域界限而无法满足的分配， *偏移*或*大小*未页面对齐，或*大小*为0。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_ACCESS_DENIED**  Insufficient privileges to make the requested allocation.  ** ZX_ERR_ACCESS_DENIED **特权不足，无法进行请求的分配。

 
## NOTES  笔记 

 
### Deallocation  解除分配 

The address space occupied by a VMAR will remain allocated (within its parent VMAR) until the VMAR is destroyed by calling [`zx_vmar_destroy()`]. VMAR占用的地址空间将保持分配状态（在其父VMAR内），直到通过调用[`zx_vmar_destroy（）]销毁VMAR。

Note that just closing the VMAR's handle does not deallocate the address space occupied by the VMAR. 请注意，仅关闭VMAR的句柄并不会释放VMAR占用的地址空间。

 
### The COMPACT flag  COMPACT标志 

The kernel interprets this flag as a request to reduce sprawl in allocations. While this does not necessitate reducing the absolute entropy of the allocatedaddresses, there will potentially be a very high correlation between allocations.This is a trade-off that the developer can make to increase locality ofallocations and reduce the number of page tables necessary, if they are willingto have certain addresses be more correlated. 内核将此标志解释为减少分配蔓延的请求。虽然这不必减少分配的地址的绝对熵，但分配之间可能存在很高的相关性。这是开发人员可以做出的权衡取舍，以增加分配的局部性并减少必要的页表数量（如果有的话）愿意让某些地址更相关。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_destroy()`]  -[`zx_vmar_destroy（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmar_protect()`]  -[`zx_vmar_protect（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

