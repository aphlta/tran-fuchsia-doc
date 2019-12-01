 
# zx_resource_create  zx_resource_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a resource object.  创建一个资源对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_resource_create(zx_handle_t parent_rsrc,
                               uint32_t options,
                               uint64_t base,
                               size_t size,
                               const char* name,
                               size_t name_size,
                               zx_handle_t* resource_out);
```
 

 
## DESCRIPTION  描述 

`zx_resource_create()` creates a resource object for use with other DDK syscalls. Resources are typically handed out to bus drivers and rarely need tobe interacted with directly by drivers using driver protocols. Resource objectsgrant access to an address space range starting at *base* up to but notincluding *base* + *size*. Two special values for *kind* exist:**ZX_RSRC_KIND_ROOT** and **ZX_RSRC_KIND_HYPERVISOR**. These resources have norange associated with them and are used as a privilege check. zx_resource_create（）创建一个资源对象以与其他DDK syscall一起使用。通常将资源分发给总线驱动程序，很少需要驱动程序使用驱动程序协议直接与之交互。资源对象允许访问从* base *到不包括* base * + * size *的地址空间范围。存在* kind *的两个特殊值：** ZX_RSRC_KIND_ROOT **和** ZX_RSRC_KIND_HYPERVISOR **。这些资源没有与之关联的范围，并用作特权检查。

*parent_rsrc* must be a handle to a resource of *kind* **ZX_RSRC_KIND_ROOT**, or a resource that matches the requested *kind* and contains [*base*, *base*+size*]in its range. * parent_rsrc *必须是* kind *资源** ZX_RSRC_KIND_ROOT **的句柄，或者是与请求的* kind *匹配并且在其范围内包含[* base *，* base * + size *]的资源的句柄。

*options* must specify which kind of resource to create and may contain optional flags. Valid kinds of resources are **ZX_RSRC_KIND_MMIO**, **ZX_RSRC_KIND_IRQ**,**ZX_RSRC_KIND_IOPORT** (x86 only), **ZX_RSRC_KIND_ROOT**,**ZX_RSRC_KIND_HYPERVISOR**, **ZX_RSRC_KIND_VMEX**, and **ZX_RSRC_KIND_SMC**(ARM only).**ZX_RSRC_KIND_ROOT**, **ZX_RSRC_KIND_HYPERVISOR**, and **ZX_RSRC_KIND_VMEX**must be paired with zero values for *base* and *size*, as they do not usean address space range.At this time the only optional flag is **ZX_RSRC_FLAG_EXCLUSIVE**. If**ZX_RSRC_FLAG_EXCLUSIVE** is provided then the syscall will attempt toexclusively reserve the requested address space region, preventing otherresources creation from overlapping with it as long as it exists. * options *必须指定要创建的资源类型，并且可以包含可选标志。有效种类的资源是** ZX_RSRC_KIND_MMIO **，** ZX_RSRC_KIND_IRQ **，** ZX_RSRC_KIND_IOPORT **（仅x86），** ZX_RSRC_KIND_ROOT **，** ZX_RSRC_KIND_HYPERVISOR **，** ZX_RSRS_KIND_IRQ **，** *（仅ARM）唯一的可选标志是** ZX_RSRC_FLAG_EXCLUSIVE **。如果提供了** ZX_RSRC_FLAG_EXCLUSIVE **，则系统调用将尝试排他地保留所请求的地址空间区域，从而防止其他资源创建与其重叠（只要存在）。

*name* and *name_size* are optional and truncated to **ZX_MAX_NAME_LENGTH** - 1. This name is provided for debugging / tool use only and is not used by thekernel. * name *和* name_size *是可选的，并被截断为** ZX_MAX_NAME_LENGTH **-1。此名称仅供调试/工具使用，内核不使用。

On success, a valid resource handle is returned in *resource_out*.  成功后，将在* resource_out *中返回有效的资源句柄。

 
## RETURN VALUE  返回值 

`zx_resource_create()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_resource_create（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

The returned handle will have **ZX_RIGHT_TRANSFER** (allowing it to be sent to another process via [`zx_channel_write()`]), **ZX_RIGHT_DUPLICATE** (allowingthe handle to be duplicated), **ZX_RIGHT_INSPECT** (to allow inspection of theobject with [`zx_object_get_info()`] and **ZX_RIGHT_WRITE** which is checked by`zx_resource_create()` itself. 返回的句柄将具有** ZX_RIGHT_TRANSFER **（允许通过[`zx_channel_write（）]发送到另一个进程），** ZX_RIGHT_DUPLICATE **（允许复制句柄），** ZX_RIGHT_INSPECT **（允许用[`zx_object_get_info（）`]和** ZX_RIGHT_WRITE **检查对象，由zx_resource_create（）本身检查。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*parent_rsrc* must be of type **ZX_OBJ_TYPE_RESOURCE** and have **ZX_RIGHT_WRITE**.  * parent_rsrc *必须为** ZX_OBJ_TYPE_RESOURCE **类型，且必须为** ZX_RIGHT_WRITE **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** the *parent_rsrc* handle is invalid.  ** ZX_ERR_BAD_HANDLE ** * parent_rsrc *句柄无效。

**ZX_ERR_WRONG_TYPE** the *parent_rsrc* handle is not a resource handle.  ** ZX_ERR_WRONG_TYPE ** * parent_rsrc *句柄不是资源句柄。

**ZX_ERR_ACCESS_DENIED** The *parent_rsrc* handle is not a resource of either *kind* or **ZX_RSRC_KIND_ROOT**. ** ZX_ERR_ACCESS_DENIED ** ** parent_rsrc *句柄不是* Kind *或** ZX_RSRC_KIND_ROOT **的资源。

**ZX_ERR_INVALID_ARGS** *options* contains an invalid kind or flag combination, *name* is an invalid pointer, or the *kind* specified is one of**ZX_RSRC_KIND_ROOT** or **ZX_RSRC_KIND_HYPERVISOR** but *base* and *size* arenot 0. ** ZX_ERR_INVALID_ARGS ** *选项*包含无效的种类或标志组合，*名称*是无效的指针，或者指定的*种类*是** ZX_RSRC_KIND_ROOT **或** ZX_RSRC_KIND_HYPERVISOR **之一，但* base *和*大小*不是0。

**ZX_ERR_NO_MEMORY** Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error. In a future build this error will nolonger occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_ioports_request()`]  -[`zx_ioports_request（）`]
 - [`zx_vmo_create_physical()`]  -[`zx_vmo_create_physical（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

