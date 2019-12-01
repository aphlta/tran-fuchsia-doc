 
# zx_interrupt_bind_vcpu  zx_interrupt_bind_vcpu 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Bind an interrupt object to a VCPU.  将中断对象绑定到VCPU。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_interrupt_bind_vcpu(zx_handle_t handle,
                                   zx_handle_t vcpu,
                                   uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_interrupt_bind_vcpu()` binds an interrupt object to a VCPU. When the interrupt object is triggered, the interrupt is redirected to the VCPU, in orderto be processed by a guest with no host intervention. zx_interrupt_bind_vcpu（）将中断对象绑定到VCPU。触发中断对象时，中断将重定向到VCPU，以便由来宾在没有主机干预的情况下进行处理。

An interrupt object may be bound to multiple VCPUs, in order to distribute the interrupt. Simply invoke `zx_interrupt_bind_vcpu()` with the same *handle*, butdifferent *vcpu*s. However, all VCPUs must belong to a single guest. 中断对象可以绑定到多个VCPU，以便分配中断。只需使用相同的* handle *，但不同的* vcpu * s调用`zx_interrupt_bind_vcpu（）`。但是，所有VCPU必须属于一个来宾。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_INTERRUPT** and have **ZX_RIGHT_READ**.  *句柄*必须为** ZX_OBJ_TYPE_INTERRUPT **类型，并具有** ZX_RIGHT_READ **。

*vcpu* must be of type **ZX_OBJ_TYPE_VCPU** and have **ZX_RIGHT_WRITE**.  * vcpu *必须为** ZX_OBJ_TYPE_VCPU **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_interrupt_bind_vcpu()` returns **ZX_OK** on success. On failure, an error value is returned. zx_interrupt_bind_vcpu（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* or *vcpu* are not valid handles.  ** ZX_ERR_BAD_HANDLE ** * handle *或* vcpu *不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an interrupt object or *vcpu* is not a VCPU. ** ZX_ERR_WRONG_TYPE ** * handle *不是中断对象，或者* vcpu *不是VCPU。

**ZX_ERR_CANCELED** [`zx_interrupt_destroy()`] was called on *handle*.  ** ZX_ERR_CANCELED ** [`zx_interrupt_destroy（）`]在*句柄*上被调用。

**ZX_ERR_BAD_STATE**  a thread is waiting on the interrupt using [`zx_interrupt_wait()`]. ** ZX_ERR_BAD_STATE **线程正在使用[`zx_interrupt_wait（）`]等待中断。

**ZX_ERR_ACCESS_DENIED** *handle* lacks **ZX_RIGHT_READ** or *vcpu* lacks **ZX_RIGHT_WRITE**. ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_READ **或* vcpu *缺少** ZX_RIGHT_WRITE **。

**ZX_ERR_ALREADY_BOUND** *handle* is already bound to another guest or to a port. ** ZX_ERR_ALREADY_BOUND ** *句柄*已绑定到另一个来宾或端口。

**ZX_ERR_INVALID_ARGS** *vcpu* is bound to a different guest than previously bound VCPUs, or *options* is non-zero. ** ZX_ERR_INVALID_ARGS ** * vcpu *与先前绑定的VCPU绑定到不同的guest虚拟机，或者* options *非零。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

