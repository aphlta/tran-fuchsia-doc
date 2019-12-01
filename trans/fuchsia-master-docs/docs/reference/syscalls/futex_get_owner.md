 
# zx_futex_get_owner  zx_futex_get_owner 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Fetch the koid current owner of a futex, if any.  提取futex的koid当前所有者（如果有）。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_get_owner(const zx_futex_t* value_ptr, zx_koid_t* koid);
```
 

 
## DESCRIPTION  描述 

Fetch the koid of the current owner of the futex identified by *value_ptr*, or **ZX_KOID_INVALID** if there is no current owner.  Knowledge of the ownership ofa futex typically serves no purpose when building synchronization primitivesfrom futexes.  This syscall is used primarily for testing. 获取由* value_ptr *标识的futex的当前所有者的类别，如果没有当前所有者，则获取** ZX_KOID_INVALID **。当从futex建立同步基元时，了解fufu的所有权通常没有用。该系统调用主要用于测试。

See *Ownership and Priority Inheritance* in [futex](/docs/concepts/objects/futex.md) for details. 有关详细信息，请参见[futex]（/ docs / concepts / objects / futex.md）中的*所有权和优先级继承*。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_get_owner()` returns **ZX_OK** on success, and koids hold the owner of the futex at the time of the syscall, or **ZX_KOID_INVALID** if there was noowner. zx_futex_get_owner（）成功时返回** ZX_OK **，并且在调用系统时，类机器人保持futex的所有者；如果没有所有者，则** ZX_KOID_INVALID **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  One of the following is true:  ** ZX_ERR_INVALID_ARGS **以下条件之一为真：
+ *value_ptr* is not a valid userspace pointer.  + * value_ptr *不是有效的用户空间指针。
+ *value_ptr* is not aligned to a `sizeof(zx_futex_t)` boundary.  + * value_ptr *未与`sizeof（zx_futex_t）`边界对齐。
+ *koid* is not a valid userspace pointer.  + * koid *不是有效的用户空间指针。

 
## SEE ALSO  也可以看看 

 

