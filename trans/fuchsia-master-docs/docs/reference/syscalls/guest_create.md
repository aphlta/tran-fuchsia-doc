 
# zx_guest_create  zx_guest_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a guest.  创建一个访客。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_guest_create(zx_handle_t resource,
                            uint32_t options,
                            zx_handle_t* guest_handle,
                            zx_handle_t* vmar_handle);
```
 

 
## DESCRIPTION  描述 

`zx_guest_create()` creates a guest, which is a virtual machine that can be run within the hypervisor, with *vmar_handle* used to represent the physical addressspace of the guest. zx_guest_create（）创建一个来宾，该来宾是可以在虚拟机管理程序中运行的虚拟机，并使用* vmar_handle *表示来宾的物理地址空间。

To create a guest, a *resource* of **ZX_RSRC_KIND_HYPERVISOR** must be supplied.  要创建访客，必须提供*资源* ** ZX_RSRC_KIND_HYPERVISOR **。

In order to begin execution within the guest, a VMO should be mapped into *vmar_handle* using [`zx_vmar_map()`], and a VCPU must be created using[`zx_vcpu_create()`], and then run using [`zx_vcpu_resume()`]. 为了开始在guest虚拟机中执行，应该使用[`zx_vmar_map（）]将VMO映射到* vmar_handle *，并且必须使用[`zx_vcpu_create（）`]创建VCPU，然后使用[`zx_vcpu_resume（ ）`]。

Additionally, a VMO should be mapped into *vmar_handle* to provide a guest with physical memory. 此外，应将VMO映射到* vmar_handle *，以为访客提供物理内存。

The following rights will be set on the handle *guest_handle* by default:  默认情况下，将在句柄* guest_handle *上设置以下权限：

**ZX_RIGHT_TRANSFER** &mdash; *guest_handle* may be transferred over a channel.  ** ZX_RIGHT_TRANSFER **- * guest_handle *可以通过通道进行传输。

**ZX_RIGHT_DUPLICATE** &mdash; *guest_handle* may be duplicated.  ** ZX_RIGHT_DUPLICATE **- * guest_handle *可能重复。

**ZX_RIGHT_WRITE** &mdash; A trap to be may be set using [`zx_guest_set_trap()`].  ** ZX_RIGHT_WRITE **-可以使用[`zx_guest_set_trap（）`]设置要设置的陷阱。

**ZX_RIGHT_MANAGE_PROCESS** &mdash; A VCPU may be created using [`zx_vcpu_create()`].  ** ZX_RIGHT_MANAGE_PROCESS **-可以使用[`zx_vcpu_create（）`]创建一个VCPU。

See [`zx_vmo_create()`] for the set of rights applied to *vmar_handle*.  有关应用于* vmar_handle *的权限集，请参见[`zx_vmo_create（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_HYPERVISOR**.  * resource *必须具有资源类型** ZX_RSRC_KIND_HYPERVISOR **。

 
## RETURN VALUE  返回值 

`zx_guest_create()` returns **ZX_OK** on success. On failure, an error value is returned. zx_guest_create（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *resource* is not of **ZX_RSRC_KIND_HYPERVISOR**.  ** ZX_ERR_ACCESS_DENIED ** *资源*不是** ZX_RSRC_KIND_HYPERVISOR **。

**ZX_ERR_INVALID_ARGS** *guest_handle* or *vmar_handle* is an invalid pointer, or *options* is nonzero. ** ZX_ERR_INVALID_ARGS ** * guest_handle *或* vmar_handle *是无效的指针，或* options *非零。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_WRONG_TYPE** *resource* is not a handle to a resource.  ** ZX_ERR_WRONG_TYPE ** *资源*不是资源的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_set_trap()`]  -[`zx_guest_set_trap（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]
 - [`zx_vcpu_interrupt()`]  -[`zx_vcpu_interrupt（）`]
 - [`zx_vcpu_read_state()`]  -[`zx_vcpu_read_state（）`]
 - [`zx_vcpu_resume()`]  -[`zx_vcpu_resume（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

