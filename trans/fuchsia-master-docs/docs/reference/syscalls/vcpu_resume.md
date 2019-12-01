 
# zx_vcpu_resume  zx_vcpu_resume 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Resume execution of a VCPU.  恢复执行VCPU。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/port.h>

zx_status_t zx_vcpu_resume(zx_handle_t handle, zx_port_packet_t* packet);
```
 

 
## DESCRIPTION  描述 

`zx_vcpu_resume()` begins or resumes execution of *handle*, and blocks until it has paused execution. On pause of execution, *packet* is populated with reason forthe pause. After handling the reason, execution may be resumed by calling`zx_vcpu_resume()` again. zx_vcpu_resume（）开始或恢复* handle *的执行，并阻塞直到它暂停执行为止。在执行暂停时，会在* packet *中填充暂停原因。处理完原因后，可以通过再次调用zx_vcpu_resume（）来恢复执行。

N.B. Execution of a *handle* must be resumed on the same thread it was created on.  N.B.必须在创建该线程的同一线程上继续执行* handle *。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VCPU** and have **ZX_RIGHT_EXECUTE**.  *句柄*必须为** ZX_OBJ_TYPE_VCPU **类型并具有** ZX_RIGHT_EXECUTE **。

 
## RETURN VALUE  返回值 

`zx_vcpu_resume()` returns **ZX_OK** on success. On failure, an error value is returned. zx_vcpu_resume（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *handle* does not have the **ZX_RIGHT_EXECUTE** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_EXECUTE **权限。

**ZX_ERR_BAD_HANDLE** *handle* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *是无效的句柄。

**ZX_ERR_BAD_STATE** *handle* is in a bad state, and can not be executed.  ** ZX_ERR_BAD_STATE ** *句柄*处于错误状态，无法执行。

**ZX_ERR_CANCELED** *handle* execution was canceled while waiting on an event.  ** ZX_ERR_CANCELED ** *句柄*在等待事件时被取消执行。

**ZX_ERR_INTERNAL** There was an error executing *handle*.  ** ZX_ERR_INTERNAL **执行*句柄*时出错。

**ZX_ERR_INVALID_ARGS** *packet* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *数据包*是无效的指针。

**ZX_ERR_NOT_SUPPORTED** An unsupported operation was encountered while executing *handle*. ** ZX_ERR_NOT_SUPPORTED **执行* handle *时遇到了不受支持的操作。

**ZX_ERR_WRONG_TYPE** *handle* is not a handle to a VCPU.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VCPU的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_guest_set_trap()`]  -[`zx_guest_set_trap（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]
 - [`zx_vcpu_interrupt()`]  -[`zx_vcpu_interrupt（）`]
 - [`zx_vcpu_read_state()`]  -[`zx_vcpu_read_state（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

