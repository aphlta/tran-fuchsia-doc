 
# zx_vmo_create_child  zx_vmo_create_child 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a child of a VM Object.  创建VM对象的子级。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_create_child(zx_handle_t handle,
                                uint32_t options,
                                uint64_t offset,
                                uint64_t size,
                                zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_create_child()` creates a new virtual memory object (VMO) a child of an existing vmo. The behavior of the semantics depends on the type of the child. zx_vmo_create_child（）创建一个新的虚拟内存对象（VMO），它是现有vmo的子对象。语义的行为取决于孩子的类型。

One handle is returned on success, representing an object with the requested size. 成功返回一个句柄，代表具有请求大小的对象。

*options* must contain exactly one of the following flags to specify the child type: * options *必须完全包含以下标志之一才能指定子类型：

 
- **ZX_VMO_CHILD_COPY_ON_WRITE** - Create a copy-on-write clone. The cloned vmo will behave the same way the parent does, except that any write operation on the clonewill bring in a copy of the page at the offset the write occurred. The new page inthe cloned vmo is now a copy and may diverge from the parent. Any reads fromranges outside of the parent vmo's size will contain zeros, and writes willallocate new zero filled pages. A vmo which has pinned regions cannot be cloned. Seethe NOTES section below for details on VMO syscall interactions with clones. This flagmay not be used for vmos created with [`zx_vmo_create_physical()`] or descendants ofsuch a vmo. -** ZX_VMO_CHILD_COPY_ON_WRITE **-创建写时复制副本。克隆的vmo的行为与父代相同，只是对克隆的任何写操作都将在发生写偏移的位置引入页面的副本。现在，克隆的vmo中的新页面是一个副本，可能与父页面有所不同。从父vmo大小之外的范围进行的任何读取都将包含零，而写入将分配新的零填充页面。具有固定区域的vmo无法克隆。有关与克隆的VMO syscall交互的详细信息，请参见下面的“注意”部分。该标志不得用于使用[`zx_vmo_create_physical（）`]创建的vmos或此类vmo的后代。

 
- **ZX_VMO_CHILD_SLICE** - Create a slice that has direct read/write access into a section of the parent. All operations on the slice vmo behave as if they weredone on the parent. A slice differs from a duplicate handle to the parent by allowingaccess to only a subrange of the parent vmo, and allowing for the**ZX_VMO_ZERO_CHILDREN** signal to be used. This flag may be used with vmos created with[`zx_vmo_create_physical()`] and their descendants. -** ZX_VMO_CHILD_SLICE **-创建对父级部分具有直接读/写访问权限的片。切片vmo上的所有操作的行为就像在父级上所做的一样。切片不同于对父代的重复句柄，它只允许访问父代vmo的子范围，并允许使用** ZX_VMO_ZERO_CHILDREN **信号。该标志可与通过[`zx_vmo_create_physical（）`]创建的vmos及其后代一起使用。

 
- **ZX_VMO_CHILD_PRIVATE_PAGER_COPY** - Create a private copy of a pager vmo. The child vmo will behave the same way the parent does, except that any write operation on thechild will bring in a copy of the page at the offset the write occurred into the childvmo. The new page in the child vmo is now a copy and may diverge from the parent. Anyreads from ranges outside of the parent vmo's size will contain zeros, and writes willallocate new zero filled pages.  See the NOTES section below for details on VMO syscallinteractions with child. This flag is only supported for vmos created with[`zx_pager_create_vmo()`] or descendants of such a vmo. -** ZX_VMO_CHILD_PRIVATE_PAGER_COPY **--创建寻呼机vmo的私有副本。子级vmo的行为与父级vmo相同，不同之处在于，对子级vmo的任何写操作都将在该子级vmo中发生写入偏移的位置引入页面的副本。子vmo中的新页面现在是一个副本，可能与父页面有所不同。父vmo大小范围之外的任何读取都将包含零，并且写入操作将分配新的零填充页面。有关与child的VMO syscall交互的详细信息，请参见下面的NOTES部分。仅使用[`zx_pager_create_vmo（）`]创建的vmos或此类vmo的后代支持此标志。

In addition, *options* can contain zero or more of the following flags to further specify the child's behavior: 此外，* options *可以包含零个或多个以下标志，以进一步指定孩子的行为：

 
- **ZX_VMO_CHILD_RESIZEABLE** - Create a resizeable child VMO.  -** ZX_VMO_CHILD_RESIZEABLE **-创建可调整大小的子VMO。

 
- **ZX_VMO_CHILD_NO_WRITE** - Create a child that cannot be written to.  -** ZX_VMO_CHILD_NO_WRITE **-创建无法写入的子代。

*offset* must be page aligned.  *偏移量*必须页面对齐。

*offset* + *size* may not exceed the range of a 64bit unsigned value.  * offset * + * size *不得超过64位无符号值的范围。

Both offset and size may start or extend beyond the original VMO's size.  偏移量和大小可能会开始或超出原始VMO的大小。

The size of the VMO will be rounded up to the next page size boundary.  VMO的大小将四舍五入到下一页的大小边界。

By default the rights of the child handled will be the same as the original with a few exceptions. See [`zx_vmo_create()`] for adiscussion of the details of each right. 默认情况下，处理的子级的权限与原始权限相同，但有一些例外。有关每个权利的详细信息，请参见[`zx_vmo_create（）`]。

In all cases if **ZX_VMO_NO_WRITE** is set then **ZX_RIGHT_WRITE** will be removed.  在所有情况下，如果设置了** ZX_VMO_NO_WRITE **，那么** ZX_RIGHT_WRITE **将被删除。

If *options* is **ZX_VMO_CHILD_COPY_ON_WRITE** or **ZX_VMO_CHILD_PRIVATE_PAGER_COPY** and **ZX_VMO_CHILD_NO_WRITE** is not set then **ZX_RIGHT_WRITE** will be added and **ZX_RIGHT_EXECUTE**will be removed. 如果* options *是** ZX_VMO_CHILD_COPY_ON_WRITE **或** ZX_VMO_CHILD_PRIVATE_PAGER_COPY **且未设置** ZX_VMO_CHILD_NO_WRITE **，则将添加** ZX_RIGHT_WRITE **并删除** ZX_RIGHT_EXECUTE **。

 
## NOTES  笔记 

Creating a child VMO causes the existing (source) VMO **ZX_VMO_ZERO_CHILDREN** signal to become inactive. Only when the last child is destroyed and no mappingsof those child into address spaces exist, will **ZX_VMO_ZERO_CHILDREN** becomeactive again. 创建子VMO会使现有（源）VMO ** ZX_VMO_ZERO_CHILDREN **信号变为无效。仅当最后一个子项被销毁并且这些子项到地址空间的映射不存在时，** ZX_VMO_ZERO_CHILDREN **才会再次变为活动状态。

Non-slice child vmos will interact with the VMO syscalls in the following ways:  非切片子vmos将通过以下方式与VMO syscall进行交互：

 
- The COMMIT mode of [`zx_vmo_op_range()`] on a child will commit pages into the child that have the same content as its parent's corresponding pages. If those pages are supplied by apager, this operation will also commit those pages in the parent. Otherwise, if those pagesare not comitted in the parent, zero-filled pages will be comitted directly intochild, without affecting the parent. -子项上的[`zx_vmo_op_range（）`]的COMMIT模式会将页面提交给该子项，这些页面的内容与其父项的相应页面相同。如果这些页面是由apager提供的，则此操作还将在父页面中提交这些页面。否则，如果未在父级中合并这些页面，则零填充页面将直接合并到子级中，而不会影响父级。
- The DECOMMIT mode of [`zx_vmo_op_range()`] is not supported.  -不支持[`zx_vmo_op_range（）`]的DECOMMIT模式。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_DUPLICATE** and have **ZX_RIGHT_READ**.  *句柄*的类型必须为** ZX_OBJ_TYPE_VMO **，并且具有** ZX_RIGHT_DUPLICATE **和** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_vmo_create_child()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_create_child（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ERR_BAD_TYPE**  Input handle is not a VMO.  ** ERR_BAD_TYPE **输入句柄不是VMO。

**ZX_ERR_ACCESS_DENIED**  Input handle does not have sufficient rights.  ** ZX_ERR_ACCESS_DENIED **输入句柄没有足够的权限。

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer or NULL or the offset is not page aligned. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针或NULL，或者偏移量不是页面对齐的。

**ZX_ERR_OUT_OF_RANGE**  *offset* + *size* is too large.  ** ZX_ERR_OUT_OF_RANGE ** *偏移量* + *大小*太大。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ERR_BAD_STATE**  A COW child could not be created because the vmo has some pinned pages. ** ERR_BAD_STATE **由于vmo具有一些固定页面，因此无法创建COW子级。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

