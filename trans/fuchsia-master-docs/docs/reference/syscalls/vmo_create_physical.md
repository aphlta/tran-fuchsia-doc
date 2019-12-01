 
# zx_vmo_create_physical  zx_vmo_create_physical 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a VM object referring to a specific contiguous range of physical memory.  创建一个VM对象，该对象引用物理内存的特定连续范围。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_create_physical(zx_handle_t resource,
                                   zx_paddr_t paddr,
                                   size_t size,
                                   zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_create_physical()` creates a new virtual memory object (VMO), which represents the *size* bytes of physical memory beginning at physical address *paddr*. zx_vmo_create_physical（）创建一个新的虚拟内存对象（VMO），该对象表示物理内存的* size *字节，起始于物理地址* paddr *。

One handle is returned on success, representing an object with the requested size. 成功返回一个句柄，代表具有请求大小的对象。

The following rights will be set on the handle by default:  默认情况下，将在句柄上设置以下权限：

**ZX_RIGHT_DUPLICATE** - The handle may be duplicated.  ** ZX_RIGHT_DUPLICATE **-手柄可能重复。

**ZX_RIGHT_TRANSFER** - The handle may be transferred to another process.  ** ZX_RIGHT_TRANSFER **-句柄可以转移到另一个进程。

**ZX_RIGHT_READ** - May be read from or mapped with read permissions.  ** ZX_RIGHT_READ **-可以从读取权限中读取或映射为具有读取权限。

**ZX_RIGHT_WRITE** - May be written to or mapped with write permissions.  ** ZX_RIGHT_WRITE **-可以被写入或具有写入权限映射。

**ZX_RIGHT_EXECUTE** - May be mapped with execute permissions.  ** ZX_RIGHT_EXECUTE **-可能具有执行权限映射。

**ZX_RIGHT_MAP** - May be mapped.  ** ZX_RIGHT_MAP **-可能被映射。

**ZX_RIGHT_GET_PROPERTY** - May get its properties using [`zx_object_get_property()`]. ** ZX_RIGHT_GET_PROPERTY **-可以使用[`zx_object_get_property（）]获得其属性。

**ZX_RIGHT_SET_PROPERTY** - May set its properties using [`zx_object_set_property()`]. ** ZX_RIGHT_SET_PROPERTY **-可以使用[`zx_object_set_property（）`设置其属性。

The **ZX_VMO_ZERO_CHILDREN** signal is active on a newly created VMO. It becomes inactive whenever a child of the VMO is created and becomes active again whenall children have been destroyed and no mappings of those children into addressspaces exist. ZX_VMO_ZERO_CHILDREN **信号在新创建的VMO上处于活动状态。每当创建VMO的子代时，它就变得不活动，而当所有子代都被销毁并且不存在那些子代到地址空间的映射时，它将再次变为活动。

 
## NOTES  笔记 

The VMOs created by this syscall are not usable with [`zx_vmo_read()`] and [`zx_vmo_write()`]. 此系统调用创建的VMO不能与[`zx_vmo_read（）`]和[`zx_vmo_write（）`]一起使用。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_MMIO**.  * resource *必须具有资源类型** ZX_RSRC_KIND_MMIO **。

 
## RETURN VALUE  返回值 

`zx_vmo_create_physical()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_create_physical（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZER_ERR_WRONG_TYPE** *resource* is not a handle to a Resource object.  ** ZER_ERR_WRONG_TYPE ** * resource *不是Resource对象的句柄。

**ZER_ERR_ACCESS_DENIED** *resource* does not grant access to the requested range of memory. ** ZER_ERR_ACCESS_DENIED ** *资源*不授予对请求的内存范围的访问权限。

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer or NULL, or *paddr* or *size* are not page-aligned. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针或NULL，或者* paddr *或* size *没有页面对齐。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

