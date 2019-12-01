 
# zx_vmar_map  zx_vmar_map 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Add a memory mapping.  添加内存映射。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_map(zx_handle_t handle,
                        zx_vm_option_t options,
                        uint64_t vmar_offset,
                        zx_handle_t vmo,
                        uint64_t vmo_offset,
                        uint64_t len,
                        zx_vaddr_t* mapped_addr);
```
 

 
## DESCRIPTION  描述 

Maps the given VMO into the given virtual memory address region.  The mapping retains a reference to the underlying virtual memory object, which meansclosing the VMO handle does not remove the mapping added by this function. 将给定的VMO映射到给定的虚拟内存地址区域。映射保留对基础虚拟内存对象的引用，这意味着关闭VMO句柄不会删除此函数添加的映射。

*options* is a bit vector of the following:  * options *是以下内容的位向量：

 
- **ZX_VM_SPECIFIC**  Use the *vmar_offset* to place the mapping, invalid if *handle* does not have the **ZX_VM_CAN_MAP_SPECIFIC** permission.*vmar_offset* is an offset relative to the base address of the given VMAR.It is an error to specify a range that overlaps with another VMAR or mapping. -** ZX_VM_SPECIFIC **使用* vmar_offset *放置映射，如果* handle *没有** ZX_VM_CAN_MAP_SPECIFIC **权限则无效。* vmar_offset *是相对于给定VMAR基址的偏移量。指定与另一个VMAR或映射重叠的范围时出错。
- **ZX_VM_SPECIFIC_OVERWRITE**  Same as **ZX_VM_SPECIFIC**, but can overlap another mapping.  It is still an error to partially-overlap another VMAR.If the range meets these requirements, it will atomically (with respect to allother map/unmap/protect operations) replace existing mappings in the rangespecified by *vmar_offset* and *len*. If that range partially overlaps anymappings, then the portions of those mappings outside the range will remain mapped. -** ZX_VM_SPECIFIC_OVERWRITE **与** ZX_VM_SPECIFIC **相同​​，但可以与另一个映射重叠。将另一个VMAR部分重叠仍然是一个错误，如果范围满足这些要求，它将以原子方式（相对于所有其他map / unmap / protect操作）替换* vmar_offset *和* len *指定的范围中的现有映射。如果该范围与任何映射部分重叠，则那些映射超出范围的部分将保持映射状态。
- **ZX_VM_PERM_READ**  Map *vmo* as readable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_READ** permissions, the *handle* doesnot have the **ZX_RIGHT_READ** right, or the *vmo* handle does not have the**ZX_RIGHT_READ** right. -** ZX_VM_PERM_READ **将* vmo *映射为可读。如果* handle *不具有** ZX_VM_CAN_MAP_READ **权限，* handle *不具有** ZX_RIGHT_READ **权限或* vmo *句柄不具有** ZX_RIGHT_READ **权限，则将发生错误。
- **ZX_VM_PERM_WRITE**  Map *vmo* as writable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_WRITE** permissions, the *handle* doesnot have the **ZX_RIGHT_WRITE** right, or the *vmo* handle does not have the**ZX_RIGHT_WRITE** right. -** ZX_VM_PERM_WRITE **将* vmo *映射为可写。如果* handle *不具有** ZX_VM_CAN_MAP_WRITE **权限，* handle *不具有** ZX_RIGHT_WRITE **权限或* vmo *句柄不具有** ZX_RIGHT_WRITE **权限，则是错误的。
- **ZX_VM_PERM_EXECUTE**  Map *vmo* as executable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_EXECUTE** permissions, the *handle* handle doesnot have the **ZX_RIGHT_EXECUTE** right, or the *vmo* handle does not have the**ZX_RIGHT_EXECUTE** right. -** ZX_VM_PERM_EXECUTE **将* vmo *映射为可执行文件。如果* handle *不具有** ZX_VM_CAN_MAP_EXECUTE **权限，* handle *句柄没有** ZX_RIGHT_EXECUTE **权限或* vmo *句柄没有** ZX_RIGHT_EXECUTE **权限，则是错误的。
- **ZX_VM_MAP_RANGE**  Immediately page into the new mapping all backed regions of the VMO.  This cannot be specified if**ZX_VM_SPECIFIC_OVERWRITE** is used. -** ZX_VM_MAP_RANGE **立即进入VMO所有支持区域的新映射。如果使用** ZX_VM_SPECIFIC_OVERWRITE **，则无法指定。
- **ZX_VM_ALLOW_FAULTS** Required if it would be possible for the created mapping to generate faults. In particular, it is required if *vmo* is resizable,if *vmo* is non-resizable but the mapping extends past the end of *vmo*, or if*vmo* was created from [`zx_pager_create_vmo()`]. -** ZX_VM_ALLOW_FAULTS **如果创建的映射有可能产生故障，则为必需。特别地，如果* vmo *是可调整大小的，* vmo *是不可调整大小的，但是映射超出* vmo *的结尾，或者* vmo *是从[`zx_pager_create_vmo（）`创建的），则是必需的。

*vmar_offset* must be 0 if *options* does not have **ZX_VM_SPECIFIC** or **ZX_VM_SPECIFIC_OVERWRITE** set.  If neither of those are set, thenthe mapping will be assigned an offset at random by the kernel (with anallocator determined by policy set on the target VMAR). 如果* options *没有设置** ZX_VM_SPECIFIC **或** ZX_VM_SPECIFIC_OVERWRITE **，则vmar_offset *必须为0。如果两者均未设置，则内核将为映射随机分配一个偏移量（分配器由目标VMAR上的策略确定）。

*len* must be page-aligned.  * len *必须页面对齐。

In addition one of the following power-of-two alignment flags can added:  此外，可以添加以下两个幂的对齐标记之一：

 
- **ZX_VM_ALIGN_1KB** aligns *child_addr* to a power-of-2 at least 1K bytes.  -** ZX_VM_ALIGN_1KB **将* child_addr *对齐为2的幂，至少为1K字节。
- **ZX_VM_ALIGN_2KB** aligns *child_addr* to a power-of-2 at least 2K bytes.  -** ZX_VM_ALIGN_2KB **将* child_addr *对齐为2的幂，至少2K字节。
- **ZX_VM_ALIGN_4KB** aligns *child_addr* to a power-of-2 at least 4K bytes.  -** ZX_VM_ALIGN_4KB **将* child_addr *对齐为2的幂，至少4K字节。
- **ZX_VM_ALIGN_8KB** aligns *child_addr* to a power-of-2 at least 8K bytes. and continues up to -** ZX_VM_ALIGN_8KB **将* child_addr *对齐为2的幂，至少8K字节。并持续到
- **ZX_VM_ALIGN_4GB** aligns *child_addr* to a power-of-2 at least 4G bytes.  -** ZX_VM_ALIGN_4GB **将* child_addr *对齐为2的幂，至少4G字节。

TODO(ZX-3978): Currently, alignment flags greater than 4KB cannot be used when mapping a VMO into a compact VMAR. TODO（ZX-3978）：当前，将VMO映射到紧凑型VMAR时，不能使用大于4KB的对齐标志。

Using **ZX_VM_ALIGN** flags with **ZX_VM_SPECIFIC** will fail if the vmar base address + *vmo_offset* are not aligned to the requested value. 如果vmar基址+ * vmo_offset *未与请求的值对齐，则将** ZX_VM_ALIGN **标志与** ZX_VM_SPECIFIC **一起使用将失败。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMAR**.  *句柄*必须为** ZX_OBJ_TYPE_VMAR **类型。

*vmo* must be of type **ZX_OBJ_TYPE_VMO**.  * vmo *必须为** ZX_OBJ_TYPE_VMO **类型。

 
## RETURN VALUE  返回值 

`zx_vmar_map()` returns **ZX_OK** and the absolute base address of the mapping (via *mapped_addr*) on success.  The base address will be page-alignedand non-zero.  In the event of failure, a negative error value is returned. zx_vmar_map（）成功返回** ZX_OK **和映射的绝对基址（通过* mapped_addr *）。基址将为页面对齐且非零。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* or *vmo* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *或* vmo *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* or *vmo* is not a VMAR or VMO handle, respectively.  ** ZX_ERR_WRONG_TYPE ** * handle *或* vmo *分别不是VMAR或VMO句柄。

**ZX_ERR_BAD_STATE**  *handle* refers to a destroyed VMAR.  ** ZX_ERR_BAD_STATE ** *句柄*是指已损坏的VMAR。

**ZX_ERR_INVALID_ARGS** *mapped_addr* or *options* are not valid, *vmar_offset* is non-zero when neither **ZX_VM_SPECIFIC** nor**ZX_VM_SPECIFIC_OVERWRITE** are given,**ZX_VM_SPECIFIC_OVERWRITE** and **ZX_VM_MAP_RANGE** are both given,*vmar_offset* and *len* describe an unsatisfiable allocation due to exceeding the region bounds,*vmar_offset* or *vmo_offset* or *len* are not page-aligned,`vmo_offset + ROUNDUP(len, PAGE_SIZE)` overflows. ** ZX_ERR_INVALID_ARGS ** * mapped_addr *或* options *无效，当既未给出** ZX_VM_SPECIFIC **也不** ZX_VM_SPECIFIC_OVERWRITE **，** ZX_VM_SPECIFIC_OVERWRITE **和** ZX_VM_MAP时，* vmar_offset *不为零都给出了，* vmar_offset *和* len *描述了由于超出区域边界而无法满足的分配，* vmar_offset *或* vmo_offset *或* len *没有页面对齐，`vmo_offset + ROUNDUP（len，PAGE_SIZE）`溢出。

**ZX_ERR_ACCESS_DENIED**  Insufficient privileges to make the requested mapping.  ** ZX_ERR_ACCESS_DENIED **权限不足，无法进行请求的映射。

**ZX_ERR_NOT_SUPPORTED** If the vmo is resizable or backed by a pager but **ZX_VM_ALLOW_FAULTS** is not set. ** ZX_ERR_NOT_SUPPORTED **如果vmo可调整大小或由寻呼机支持，但未设置** ZX_VM_ALLOW_FAULTS **。

**ZX_ERR_BUFFER_TOO_SMALL** The VMO is not resizable and the mapping extends past the end of the VMO but **ZX_VM_ALLOW_FAULTS** is not set. ** ZX_ERR_BUFFER_TOO_SMALL ** VMO不可调整大小，并且映射扩展到VMO的末尾，但未设置** ZX_VM_ALLOW_FAULTS **。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## NOTES  笔记 

The VMO that backs a memory mapping can be resized to a smaller size. This can cause the thread is reading or writing to the VMAR region to fault. To avoid this hazard, servicesthat receive VMOs from clients should use **ZX_VM_REQUIRE_NON_RESIZABLE** when mappingthe VMO. 支持内存映射的VMO可以调整为较小的大小。这可能导致线程在读取或写入VMAR区域时出错。为了避免这种危险，在映射VMO时，从客户端接收VMO的服务应使用** ZX_VM_REQUIRE_NON_RESIZABLE **。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_allocate()`]  -[`zx_vmar_allocate（）`]
 - [`zx_vmar_destroy()`]  -[`zx_vmar_destroy（）`]
 - [`zx_vmar_protect()`]  -[`zx_vmar_protect（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

