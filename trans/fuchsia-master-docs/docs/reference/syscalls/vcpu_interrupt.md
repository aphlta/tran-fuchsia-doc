 
# zx_vcpu_interrupt  zx_vcpu_interrupt 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Raise an interrupt on a VCPU.  在VCPU上引发中断。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vcpu_interrupt(zx_handle_t handle, uint32_t vector);
```
 

 
## DESCRIPTION  描述 

`zx_vcpu_interrupt()` raises an interrupt of *vector* on *handle*, and may be called from any thread. zx_vcpu_interrupt（）在* handle *上引发* vector *的中断，可以从任何线程调用。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VCPU** and have **ZX_RIGHT_SIGNAL**.  *句柄*的类型必须为** ZX_OBJ_TYPE_VCPU **且具有** ZX_RIGHT_SIGNAL **。

 
## RETURN VALUE  返回值 

`zx_vcpu_interrupt()` returns **ZX_OK** on success. On failure, an error value is returned. zx_vcpu_interrupt（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *handle* does not have the **ZX_RIGHT_SIGNAL** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_SIGNAL **权限。

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_OUT_OF_RANGE** *vector* is outside of the range interrupts supported by the current architecture. ** ZX_ERR_OUT_OF_RANGE ** *向量*超出了当前架构支持的范围中断。

**ZX_ERR_WRONG_TYPE** *handle* is not a handle to a VCPU.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VCPU的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_guest_set_trap()`]  -[`zx_guest_set_trap（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]
 - [`zx_vcpu_read_state()`]  -[`zx_vcpu_read_state（）`]
 - [`zx_vcpu_resume()`]  -[`zx_vcpu_resume（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

