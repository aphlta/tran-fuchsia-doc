 
# zx_vmo_create  zx_vmo_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a VM object.  创建一个VM对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_create(uint64_t size, uint32_t options, zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_create()` creates a new virtual memory object (VMO), which represents a container of zero to *size* bytes of memory managed by the operatingsystem. zx_vmo_create（）创建一个新的虚拟内存对象（VMO），该对象表示一个由操作系统管理的零至* size *字节内存的容器。

The size of the VMO will be rounded up to the next page size boundary. Use [`zx_vmo_get_size()`] to return the current size of the VMO. VMO的大小将四舍五入到下一页的大小边界。使用[`zx_vmo_get_size（）`]返回VMO的当前大小。

One handle is returned on success, representing an object with the requested size. 成功返回一个句柄，代表具有请求大小的对象。

The following rights will be set on the handle by default:  默认情况下，将在句柄上设置以下权限：

**ZX_RIGHT_DUPLICATE** - The handle may be duplicated.  ** ZX_RIGHT_DUPLICATE **-手柄可能重复。

**ZX_RIGHT_TRANSFER** - The handle may be transferred to another process.  ** ZX_RIGHT_TRANSFER **-句柄可以转移到另一个进程。

**ZX_RIGHT_READ** - May be read from or mapped with read permissions.  ** ZX_RIGHT_READ **-可以从读取权限中读取或映射为具有读取权限。

**ZX_RIGHT_WRITE** - May be written to or mapped with write permissions.  ** ZX_RIGHT_WRITE **-可以被写入或具有写入权限映射。

**ZX_RIGHT_MAP** - May be mapped.  ** ZX_RIGHT_MAP **-可能被映射。

**ZX_RIGHT_GET_PROPERTY** - May get its properties using [`zx_object_get_property()`]. ** ZX_RIGHT_GET_PROPERTY **-可以使用[`zx_object_get_property（）]获得其属性。

**ZX_RIGHT_SET_PROPERTY** - May set its properties using [`zx_object_set_property()`]. ** ZX_RIGHT_SET_PROPERTY **-可以使用[`zx_object_set_property（）`设置其属性。

The *options* field can be 0 or **ZX_VMO_RESIZABLE** to create a VMO that can change size. Children of a non-resizable VMO can be resized. * options *字段可以为0或** ZX_VMO_RESIZABLE **以创建可以更改大小的VMO。不可调整大小的VMO的子项可以调整大小。

The **ZX_VMO_ZERO_CHILDREN** signal is active on a newly created VMO. It becomes inactive whenever a child of the VMO is created and becomes active again whenall children have been destroyed and no mappings of those children into addressspaces exist. ZX_VMO_ZERO_CHILDREN **信号在新创建的VMO上处于活动状态。每当创建VMO的子代时，它就变得不活动，而当所有子代都被销毁并且不存在那些子代到地址空间的映射时，它将再次变为活动。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_vmo_create()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_create（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer or NULL or *options* is any value other than 0. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针，或者NULL或* options *是除0以外的任何值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmo_create_child()`]  -[`zx_vmo_create_child（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_replace_as_executable()`]  -[`zx_vmo_replace_as_executable（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

