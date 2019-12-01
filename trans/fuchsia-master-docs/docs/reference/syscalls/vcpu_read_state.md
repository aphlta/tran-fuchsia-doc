 
# zx_vcpu_read_state  zx_vcpu_read_state 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read the state of a VCPU.  读取VCPU的状态。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vcpu_read_state(zx_handle_t handle,
                               uint32_t kind,
                               void* buffer,
                               size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_vcpu_read_state()` reads the state of *handle* as specified by *kind* into *buffer*. It is only valid to read the state of *handle* when execution has beenpaused. zx_vcpu_read_state（）将* kind *指定的* handle *状态读入* buffer *。仅在暂停执行后读取* handle *的状态才有效。

*kind* must be **ZX_VCPU_STATE**.  *类型*必须为** ZX_VCPU_STATE **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VCPU** and have **ZX_RIGHT_READ**.  *句柄*必须为** ZX_OBJ_TYPE_VCPU **类型并具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_vcpu_read_state()` returns **ZX_OK** on success. On failure, an error value is returned. zx_vcpu_read_state（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *handle* does not have the **ZX_RIGHT_READ** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_READ **权限。

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_BAD_STATE** *handle* is in a bad state, and state can not be read.  ** ZX_ERR_BAD_STATE ** *句柄*处于错误状态，无法读取状态。

**ZX_ERR_INVALID_ARGS** *kind* does not name a known VCPU state, *buffer* is an invalid pointer, or *buffer_size* does not match the expected size of *kind*. ** ZX_ERR_INVALID_ARGS ** * kind *不命名已知的VCPU状态，* buffer *是无效的指针，或者* buffer_size *与* kind *的预期大小不匹配。

**ZX_ERR_WRONG_TYPE** *handle* is not a handle to a VCPU.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VCPU的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_guest_set_trap()`]  -[`zx_guest_set_trap（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]
 - [`zx_vcpu_interrupt()`]  -[`zx_vcpu_interrupt（）`]
 - [`zx_vcpu_resume()`]  -[`zx_vcpu_resume（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

