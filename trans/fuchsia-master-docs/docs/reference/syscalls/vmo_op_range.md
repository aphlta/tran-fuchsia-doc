 
# zx_vmo_op_range  zx_vmo_op_range 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Perform an operation on a range of a VMO.  在一定范围的VMO上执行操作。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_op_range(zx_handle_t handle,
                            uint32_t op,
                            uint64_t offset,
                            uint64_t size,
                            void* buffer,
                            size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_op_range()` performs cache and memory operations against pages held by the VMO.  zx_vmo_op_range（）对VMO拥有的页面执行缓存和内存操作。

*offset* byte offset specifying the starting location for *op* in the VMO's held memory.  * offset *字节偏移量，用于指定VMO保留内存中* op *的起始位置。

*size* length, in bytes, to perform the operation on.  * size *长度，以字节为单位执行操作。

*op* the operation to perform:  * op *执行的操作：

*buffer* and *buffer_size* are currently unused.  * buffer *和* buffer_size *当前未使用。

**ZX_VMO_OP_COMMIT** - Commit *size* bytes worth of pages starting at byte *offset* for the VMO. More information can be found in the [vm object documentation](/docs/concepts/objects/vm_object.md).Requires the **ZX_RIGHT_WRITE** right. ** ZX_VMO_OP_COMMIT **-提交* size *个字节的页面，起始于VMO的字节* offset *。可以在[vm对象文档]（/ docs / concepts / objects / vm_object.md）中找到更多信息。需要** ZX_RIGHT_WRITE **权限。

**ZX_VMO_OP_DECOMMIT** - Release a range of pages previously committed to the VMO from *offset* to *offset*+*size*, which resets that range's bytes to 0. Requires the **ZX_RIGHT_WRITE** right.This is only supported for vmos created from [`zx_vmo_create()`] which do not have non-slicechildren, and for slice children of such vmos. Provided range must be page aligned. ** ZX_VMO_OP_DECOMMIT **-释放先前提交给VMO的页面范围，从* offset *到* offset * + * size *，该范围的字节重置为0。需要** ZX_RIGHT_WRITE **权限。仅受支持用于从[`zx_vmo_create（）`]创建的vmos，该vmos没有非切片子对象，并且用于此类vmos的切片子对象。提供的范围必须页面对齐。

**ZX_VMO_OP_ZERO_RANGE** - Resets the range of bytes in the VMO from *offset* to *offset*+*size* to  ** ZX_VMO_OP_ZERO_RANGE **-将VMO中的字节范围从* offset *重置为* offset * + * size *
0. This is semantically equivalent to writing 0's with [`zx_vmo_write()`](/docs/reference/syscalls/vmo_write.md), except that it is able to be done moreefficiently and save memory by de-duping to shared zero pages. Requires the **ZX_RIGHT_WRITE** right. 0。从语义上讲，它等效于使用[`zx_vmo_write（）`]（/ docs / reference / syscalls / vmo_write.md）写入0，除了可以更高效地完成操作并通过将重复数据删除到共享的零页来节省内存。需要** ZX_RIGHT_WRITE **权限。

**ZX_VMO_OP_LOCK** - Presently unsupported.  ** ZX_VMO_OP_LOCK **-目前不受支持。

**ZX_VMO_OP_UNLOCK** - Presently unsupported.  ** ZX_VMO_OP_UNLOCK **-目前不受支持。

**ZX_VMO_OP_CACHE_SYNC** - Performs a cache sync operation. Requires the **ZX_RIGHT_READ** right. ** ZX_VMO_OP_CACHE_SYNC **-执行缓存同步操作。需要** ZX_RIGHT_READ **权限。

**ZX_VMO_OP_CACHE_INVALIDATE** - Performs a cache invalidation operation. Requires the **ZX_RIGHT_WRITE** right. ** ZX_VMO_OP_CACHE_INVALIDATE **-执行缓存失效操作。需要** ZX_RIGHT_WRITE **权限。

**ZX_VMO_OP_CACHE_CLEAN** - Performs a cache clean operation. Requires the **ZX_RIGHT_READ** right. ** ZX_VMO_OP_CACHE_CLEAN **-执行缓存清除操作。需要** ZX_RIGHT_READ **权限。

**ZX_VMO_OP_CACHE_CLEAN_INVALIDATE** - Performs cache clean and invalidate operations together. Requires the **ZX_RIGHT_READ** right. ** ZX_VMO_OP_CACHE_CLEAN_INVALIDATE **-一起执行缓存清除和无效操作。需要** ZX_RIGHT_READ **权限。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

If *op* is **ZX_VMO_OP_COMMIT**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  如果* op *为** ZX_VMO_OP_COMMIT **，则* handle *必须为** ZX_OBJ_TYPE_VMO **类型并具有** ZX_RIGHT_WRITE **。

If *op* is **ZX_VMO_OP_DECOMMIT**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  如果* op *为** ZX_VMO_OP_DECOMMIT **，则* handle *必须为** ZX_OBJ_TYPE_VMO **类型并具有** ZX_RIGHT_WRITE **。

If *op* is **ZX_VMO_OP_CACHE_SYNC**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  如果* op *是** ZX_VMO_OP_CACHE_SYNC **，则* handle *的类型必须为** ZX_OBJ_TYPE_VMO **且具有** ZX_RIGHT_READ **。

If *op* is **ZX_VMO_OP_CACHE_INVALIDATE**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  如果* op *是** ZX_VMO_OP_CACHE_INVALIDATE **，则* handle *的类型必须为** ZX_OBJ_TYPE_VMO **并具有** ZX_RIGHT_WRITE **。

If *op* is **ZX_VMO_OP_CACHE_CLEAN**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  如果* op *为** ZX_VMO_OP_CACHE_CLEAN **，则* handle *必须为** ZX_OBJ_TYPE_VMO **类型，并且必须为** ZX_RIGHT_READ **。

If *op* is **ZX_VMO_OP_CACHE_CLEAN_INVALIDATE**, *handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  如果* op *为** ZX_VMO_OP_CACHE_CLEAN_INVALIDATE **，则* handle *必须为** ZX_OBJ_TYPE_VMO **类型，并且必须为** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_vmo_op_range()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. `zx_vmo_op_range（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_OUT_OF_RANGE**  An invalid memory range specified by *offset* and *size*.  ** ZX_ERR_OUT_OF_RANGE **由* offset *和* size *指定的无效内存范围。

**ZX_ERR_NO_MEMORY**  Allocations to commit pages for **ZX_VMO_OP_COMMIT** or **ZX_VMO_OP_ZERO_RANGE** failed. ** ZX_ERR_NO_MEMORY **为** ZX_VMO_OP_COMMIT **或** ZX_VMO_OP_ZERO_RANGE **提交页面的分配失败。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMO handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMO句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have sufficient rights to perform the operation.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有足够的权限执行该操作。

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer, *op* is not a valid operation, *size* is zero and *op* is a cache operation, or *op* was **ZX_VMO_OP_DECOMMIT** andrange was not page aligned. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针，* op *不是有效的操作，* size *是零并且* op *是缓存操作，或* op *是** ZX_VMO_OP_DECOMMIT **并且range不是页面对齐。

**ZX_ERR_NOT_SUPPORTED**  *op* was **ZX_VMO_OP_LOCK** or **ZX_VMO_OP_UNLOCK**, or *op* was **ZX_VMO_OP_DECOMMIT** and the underlying VMO does not allow decommiting. ** ZX_ERR_NOT_SUPPORTED ** * op *为** ZX_VMO_OP_LOCK **或** ZX_VMO_OP_UNLOCK **，或* op *为** ZX_VMO_OP_DECOMMIT **，并且基础VMO不允许取消授权。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_create_child()`]  -[`zx_vmo_create_child（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

