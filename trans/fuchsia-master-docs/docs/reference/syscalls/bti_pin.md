 
# zx_bti_pin  zx_bti_pin 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Pin pages and grant devices access to them.  固定页面并授予设备访问权限。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_bti_pin(zx_handle_t handle,
                       uint32_t options,
                       zx_handle_t vmo,
                       uint64_t offset,
                       uint64_t size,
                       zx_paddr_t* addrs,
                       size_t num_addrs,
                       zx_handle_t* pmt);
```
 

 
## DESCRIPTION  描述 

`zx_bti_pin()` pins pages of a VMO (i.e. prevents them from being decommitted with [`zx_vmo_op_range()`]) and grants the hardwaretransaction ID represented by the BTI the ability to access these pages,with the permissions specified in *options*. `zx_bti_pin（）`固定VMO的页面（即防止它们通过[`zx_vmo_op_range（）]取消提交），并授予BTI代表的硬件交易ID能够访问这些页面，并具有* options *中指定的权限。

*offset* must be aligned to page boundaries.  *偏移*必须与页面边界对齐。

*options* is a bitfield that may contain one or more of **ZX_BTI_PERM_READ**, **ZX_BTI_PERM_WRITE**, **ZX_BTI_PERM_EXECUTE**, **ZX_BTI_COMPRESS**, and**ZX_BTI_CONTIGUOUS**.  In order for the call to succeed, *vmo* must have theREAD/WRITE rights corresponding to the permissions flags set in *options*.(Note: **ZX_BTI_PERM_EXECUTE** requires **ZX_RIGHT_READ**, not **ZX_RIGHT_EXECUTE**.)**ZX_BTI_CONTIGUOUS** is only allowed if *vmo* was allocated via[`zx_vmo_create_contiguous()`] or [`zx_vmo_create_physical()`].**ZX_BTI_COMPRESS** and **ZX_BTI_CONTIGUOUS** are mutually exclusive. * options *是一个位字段，可以包含** ZX_BTI_PERM_READ **，** ZX_BTI_PERM_WRITE **，** ZX_BTI_PERM_EXECUTE **，** ZX_BTI_COMPRESS **和** ZX_BTI_CONTIGUOUS **中的一个或多个。为了使调用成功，* vmo *必须具有与* options *中设置的权限标志相对应的READ / WRITE权限。（注意：** ZX_BTI_PERM_EXECUTE **需要** ZX_RIGHT_READ **，而不是** ZX_RIGHT_EXECUTE **。 ）**仅当通过[`zx_vmo_create_contiguous（）]或[`zx_vmo_create_physical（）]分配* vmo *时才允许ZX_BTI_CONTIGUOUS **。** ZX_BTI_COMPRESS **和** ZX_BTI_CONTIGUOUS **是互斥的。

If the range in *vmo* specified by *offset* and *size* contains non-committed pages, a successful invocation of this function will result in those pageshaving been committed.  On failure, it is undefined whether they have beencommitted. 如果由* offset *和* size *指定的* vmo *中的范围包含未提交的页面，则此函数的成功调用将导致那些页面已被提交。如果失败，则不确定是否已提交它们。

*addrs* will be populated with the device-physical addresses of the requested VMO pages.  These addresses may be given to devices that issue memorytransactions with the hardware transaction ID associated with the BTI.  Thenumber of addresses returned depends on whether the **ZX_BTI_COMPRESS** or**ZX_BTI_CONTIGUOUS** options were given.  It number of addresses will be either * addrs *将使用请求的VMO页面的设备物理地址填充。可以将这些地址提供给使用与BTI相关的硬件事务ID发出存储事务的设备。返回的地址数取决于是否给出了** ZX_BTI_COMPRESS **或** ZX_BTI_CONTIGUOUS **选项。地址数将是
1) If neither is set, one per page (`size*/*PAGE_SIZE`)  1）如果两者均未设置，则每页一页（`size * / * PAGE_SIZE`）
2) If **ZX_BTI_COMPRESS** is set, `size/minimum-contiguity`, rounded up (each address representing a run of *minimum-contiguity* run of bytes,with the last one being potentially short if *size* is not a multiple of*minimum-contiguity*).  It is guaranteed that all returned addresses will be*minimum-contiguity*-aligned.  Note that *minimum-contiguity* is discoverablevia [`zx_object_get_info()`]. 2）如果设置了** ZX_BTI_COMPRESS **，则将“ size / minimum-contiguity”向上舍入（每个地址代表一串“ minimum-contiguity”字节，如果没有* size *，则最后一个可能很短。 *最小连续度*的倍数）。保证所有返回的地址都是*最小连续性*对齐的。注意* minimum-contiguity *是可通过[`zx_object_get_info（）`]发现的。
3) If **ZX_BTI_CONTIGUOUS** is set, the single address of the start of the memory.  3）如果设置了** ZX_BTI_CONTIGUOUS **，则为存储器开始的单个地址。

*addrs_count* is the number of entries in the *addrs* array.  It is an error for *addrs_count* to not match the value calculated above. * addrs_count *是* addrs *数组中的条目数。 * addrs_count *与上面计算的值不匹配是一个错误。

The pmt retains a reference to the associated vmo, so the underlying vmo won't be destroyed until the pmt is unpinned. pmt保留对关联vmo的引用，因此在取消固定pmt之前，不会破坏基础vmo。

Resizable vmos can be pinned. If a call to [`zx_set_size()`] would discard pinned pages, that call will fail. 可调整大小的vmos可以固定。如果对[`zx_set_size（）]的调用将丢弃固定的页面，则该调用将失败。

 
## OPTIONS  选件 

 
- **ZX_BTI_PERM_READ**, **ZX_BTI_PERM_WRITE**, and **ZX_BTI_PERM_EXECUTE** define the access types that the hardware bus transaction initiator will be allowedto use. -** ZX_BTI_PERM_READ **，** ZX_BTI_PERM_WRITE **和** ZX_BTI_PERM_EXECUTE **定义了允许硬件总线事务启动器使用的访问类型。
- **ZX_BTI_COMPRESS** causes the returned address list to contain one entry per block of *minimum-contiguity* bytes, rather than one per *PAGE_SIZE*. -** ZX_BTI_COMPRESS **使返回的地址列表在每个块的*最小连续性*字节中包含一个条目，而不是每个* PAGE_SIZE *字节。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_BTI** and have **ZX_RIGHT_MAP**.  *句柄*必须为** ZX_OBJ_TYPE_BTI **类型并具有** ZX_RIGHT_MAP **。

*vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_MAP**.  * vmo *必须为** ZX_OBJ_TYPE_VMO **类型，并具有** ZX_RIGHT_MAP **。

If *options* & **ZX_BTI_PERM_READ**, *vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  如果* options * ** ZX_BTI_PERM_READ **，则* vmo *必须为** ZX_OBJ_TYPE_VMO **类型并具有** ZX_RIGHT_READ **。

If *options* & **ZX_BTI_PERM_WRITE**, *vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  如果* options * ** ZX_BTI_PERM_WRITE **，则* vmo *必须为** ZX_OBJ_TYPE_VMO **类型并具有** ZX_RIGHT_WRITE **。

If *options* & **ZX_BTI_PERM_EXECUTE**, *vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  如果* options * ** ZX_BTI_PERM_EXECUTE **，则* vmo *必须为** ZX_OBJ_TYPE_VMO **类型并具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

On success, `zx_bti_pin()` returns **ZX_OK**.  The device-physical addresses of the requested VMO pages will be written in *addrs*.  A handle to the created PinnedMemory Token is returned via *pmt*.  When the PMT is no longer needed,[`zx_pmt_unpin()`] should be invoked. 成功时，`zx_bti_pin（）`返回** ZX_OK **。请求的VMO页面的设备物理地址将写在* addrs *中。通过* pmt *返回创建的PinnedMemory令牌的句柄。当不再需要PMT时，应调用[`zx_pmt_unpin（）`]。

In the event of failure, a negative error value is returned.  如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* or *vmo* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *或* vmo *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a BTI handle or *vmo* is not a VMO handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是BTI句柄，或者* vmo *不是VMO句柄。

**ZX_ERR_ACCESS_DENIED** *handle* or *vmo* does not have the **ZX_RIGHT_MAP**, or *options* contained a permissions flag corresponding to a right that *vmo* does not have. ** ZX_ERR_ACCESS_DENIED ** *句柄*或* vmo *不具有** ZX_RIGHT_MAP **，或* options *包含与* vmo *不具有的权限相对应的权限标志。

**ZX_ERR_INVALID_ARGS** *options* is 0 or contains an undefined flag, either *addrs* or *pmt* is not a valid pointer, *addrs_count* is not the same as the number of entries that would bereturned, or *offset* or *size* is not page-aligned. ** ZX_ERR_INVALID_ARGS ** * options *为0或包含未定义的标志，* addrs *或* pmt *不是有效的指针，* addrs_count *与要返回的条目数不同，或* offset *或* size *没有页面对齐。

**ZX_ERR_OUT_OF_RANGE** *offset* + *size* is out of the bounds of *vmo*.  ** ZX_ERR_OUT_OF_RANGE ** *偏移量* + *大小*超出* vmo *的范围。

**ZX_ERR_UNAVAILABLE** (Temporary) At least one page in the requested range could not be pinned at this time. ** ZX_ERR_UNAVAILABLE **（临时）目前无法固定在请求范围内的至少一页。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_bti_create()`]  -[`zx_bti_create（）`]
 - [`zx_object_get_info()`]  -[`zx_object_get_info（）`]
 - [`zx_pmt_unpin()`]  -[`zx_pmt_unpin（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

