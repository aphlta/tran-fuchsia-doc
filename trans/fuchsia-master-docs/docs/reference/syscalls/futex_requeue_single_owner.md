 
# zx_futex_requeue_single_owner  zx_futex_requeue_single_owner 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wake some number of threads waiting on a futex, and move more waiters to another wait queue.  唤醒一些在futex上等待的线程，然后将更多的服务员移到另一个等待队列。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_requeue_single_owner(const zx_futex_t* value_ptr,
                                          zx_futex_t current_value,
                                          const zx_futex_t* requeue_ptr,
                                          uint32_t requeue_count,
                                          zx_handle_t new_requeue_owner);
```
 

 
## DESCRIPTION  描述 

See [`zx_futex_requeue()`] for a full description.  有关完整说明，请参见[`zx_futex_requeue（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_requeue_single_owner()` returns **ZX_OK** on success.  `zx_futex_requeue_single_owner（）`成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  One of the following is true:  ** ZX_ERR_INVALID_ARGS **以下条件之一为真：
+ Either *value_ptr* or *requeue_ptr* is not a valid userspace pointer  + * value_ptr *或* requeue_ptr *不是有效的用户空间指针
+ Either *value_ptr* or *requeue_ptr* is not aligned to a `sizeof(zx_futex_t)` boundary.  + * value_ptr *或* requeue_ptr *均未与`sizeof（zx_futex_t）`边界对齐。
+ *value_ptr* is the same futex as *requeue_ptr*  + * value_ptr *与* requeue_ptr *是同一个futex
+ *new_requeue_owner* is currently a member of the waiters for either *value_ptr* or *requeue_ptr*  + * new_requeue_owner *当前是* value_ptr *或* requeue_ptr *的服务员成员

**ZX_ERR_BAD_HANDLE**  *new_requeue_owner* is not **ZX_HANDLE_INVALID**, and not a valid handle. **ZX_ERR_WRONG_TYPE**  *new_requeue_owner* is a valid handle, but is not a handle to a thread.**ZX_ERR_BAD_STATE**  *current_value* does not match the value at *value_ptr*. ** ZX_ERR_BAD_HANDLE ** * new_requeue_owner *不是** ZX_HANDLE_INVALID **，并且不是有效的句柄。 ** ZX_ERR_WRONG_TYPE ** * new_requeue_owner *是有效的句柄，但不是线程的句柄。** ZX_ERR_BAD_STATE ** * current_value *与* value_ptr *的值不匹配。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [`zx_futex_requeue()`]  -[`zx_futex_requeue（）`]
 - [`zx_futex_wait()`]  -[`zx_futex_wait（）`]
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

