 
# zx_vcpu_create  zx_vcpu_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a VCPU.  创建一个VCPU。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vcpu_create(zx_handle_t guest,
                           uint32_t options,
                           zx_vaddr_t entry,
                           zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_vcpu_create()` creates a VCPU within a guest, which allows for execution within the virtual machine. One or more VCPUs may be created per guest, wherethe number of VCPUs does not need to match the number of physical CPUs on themachine. zx_vcpu_create（）在来宾中创建一个VCPU，从而允许在虚拟机中执行。可以为每个来宾创建一个或多个VCPU，其中VCPU的数量不需要与计算机上的物理CPU的数量匹配。

*entry* is the instruction pointer used to indicate where in guest physical memory execution of the VCPU should start. * entry *是指令指针，用于指示应在客户机物理内存中的哪个位置开始执行VCPU。

*out* is bound to the thread that created it, and all syscalls that operate on it must be called from the same thread, with the exception of[`zx_vcpu_interrupt()`]. * out *绑定到创建它的线程，除[`zx_vcpu_interrupt（）]之外，所有在其上进行的系统调用都必须从同一线程中调用。

N.B. VCPU is an abbreviation of virtual CPU.  N.B. VCPU是虚拟CPU的缩写。

The following rights will be set on the handle *out* by default:  默认情况下，将在句柄* out *上设置以下权限：

**ZX_RIGHT_DUPLICATE** &mdash; *out* may be duplicated.  ** ZX_RIGHT_DUPLICATE **- *输出*可能重复。

**ZX_RIGHT_TRANSFER** &mdash; *out* may be transferred over a channel.  ** ZX_RIGHT_TRANSFER **- * out *可以通过通道传输。

**ZX_RIGHT_EXECUTE** &mdash; *out* may have its execution resumed (or begun)  ** ZX_RIGHT_EXECUTE **- * out *可能会恢复执行（或开始执行）

**ZX_RIGHT_SIGNAL** &mdash; *out* may be interrupted  ** ZX_RIGHT_SIGNAL **- *输出*可能会被打断

**ZX_RIGHT_READ** &mdash; *out* may have its state read  ** ZX_RIGHT_READ **- *出*可能会读取其状态

**ZX_RIGHT_WRITE** &mdash; may have its state written  ** ZX_RIGHT_WRITE **-可能写有状态

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*guest* must be of type **ZX_OBJ_TYPE_GUEST** and have **ZX_RIGHT_MANAGE_PROCESS**.  *来宾*必须为** ZX_OBJ_TYPE_GUEST **类型，并且必须为** ZX_RIGHT_MANAGE_PROCESS **。

 
## RETURN VALUE  返回值 

`zx_vcpu_create()` returns **ZX_OK** on success. On failure, an error value is returned. zx_vcpu_create（）成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *guest* does not have the **ZX_RIGHT_MANAGE_PROCESS** right. ** ZX_ERR_ACCESS_DENIED **来宾*没有** ZX_RIGHT_MANAGE_PROCESS **权限。

**ZX_ERR_BAD_HANDLE** *guest* is an invalid handle.  ** ZX_ERR_BAD_HANDLE ** *来宾*是无效的句柄。

**ZX_ERR_INVALID_ARGS** *args* contains an invalid argument, or *out* is an invalid pointer, or *options* is nonzero. ** ZX_ERR_INVALID_ARGS ** * args *包含无效的参数，或者* out *是无效的指针，或者* options *非零。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_WRONG_TYPE** *guest* is not a handle to a guest.  ** ZX_ERR_WRONG_TYPE ** *来宾*不是来宾的句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_guest_set_trap()`]  -[`zx_guest_set_trap（）`]
 - [`zx_vcpu_interrupt()`]  -[`zx_vcpu_interrupt（）`]
 - [`zx_vcpu_read_state()`]  -[`zx_vcpu_read_state（）`]
 - [`zx_vcpu_resume()`]  -[`zx_vcpu_resume（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

