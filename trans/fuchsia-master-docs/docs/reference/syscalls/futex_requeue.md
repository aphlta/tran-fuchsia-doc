 
# zx_futex_requeue  zx_futex_requeue 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wake some number of threads waiting on a futex, and move more waiters to another wait queue.  唤醒一些在futex上等待的线程，然后将更多的服务员移到另一个等待队列。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_requeue(const zx_futex_t* value_ptr,
                             uint32_t wake_count,
                             zx_futex_t current_value,
                             const zx_futex_t* requeue_ptr,
                             uint32_t requeue_count,
                             zx_handle_t new_requeue_owner);
```
 

 
## DESCRIPTION  描述 

Requeuing is a generalization of waking. First, the kernel verifies that the value in *current_value* matches the value of the futex at*value_ptr*, and if not reports **ZX_ERR_BAD_STATE**. After waking *wake_count*threads, *requeue_count* threads are moved from the original futex'swait queue to the wait queue corresponding to *requeue_ptr*, anotherfutex. 重新排队是唤醒的一般化。首先，内核验证* current_value *中的值是否与futex at * value_ptr *的值匹配，如果没有，则报告** ZX_ERR_BAD_STATE **。唤醒* wake_count *个线程后，* requeue_count *个线程从原始futex的等待队列移至与另一个线程* requeue_ptr *对应的等待队列。

This requeueing behavior may be used to avoid thundering herds on wake.  这种重新排队的行为可以用来避免追捕时雷声震撼。

 
## OWNERSHIP  所有权 

A requeue operation targets two futexes, the _wake futex_ and the _requeue futex_.  The ownership implications for each are discussed separately.Generally, if the call fails for any reason, no changes to ownership for eitherfutex are made. 重新排队操作的目标是两个futex，即_wake futex_和_requeue futex_。通常，如果呼叫由于任何原因而失败，则不会更改两个Fufutex的所有权。

See *Ownership and Priority Inheritance* in [futex](/docs/concepts/objects/futex.md) for details. 有关详细信息，请参见[futex]（/ docs / concepts / objects / futex.md）中的*所有权和优先级继承*。

 
### Effects on the _wake futex_ target  对_wake futex_目标的影响 

A successful call to `zx_futex_requeue()` results in the owner of the futex being set to nothing, regardless of the wake count.  In order to transfer ownership ofa futex, use the [`zx_futex_requeue_single_owner()`] variant instead.[`zx_futex_requeue_single_owner()`] will attempt to wake exactly one thread from thefutex wait queue.  If there is at least one thread to wake, the owner of the futex will beset to the thread which was woken.  Otherwise, the futexwill have no owner. 对`zx_futex_requeue（）`的成功调用将导致futex的所有者被设置为空，无论唤醒计数如何。为了转让futex的所有权，请改用[`zx_futex_requeue_single_owner（）`变体。[`zx_futex_requeue_single_owner（）`]将尝试从thefutex等待队列中唤醒一个线程。如果至少有一个线程要唤醒，则futex的所有者将设置为被唤醒的线程。否则，futex将没有所有者。

 
### Effects on the _requeue futex_ target  对_requeue futex_目标的影响 

A successful call to `zx_futex_requeue()` or [`zx_futex_requeue_single_owner()`] results in the owner of the futex being set to the thread referenced by the*new_requeue_owner* handle, or to nothing if *new_requeue_owner* is**ZX_HANDLE_INVALID**. 成功调用`zx_futex_requeue（）`或[`zx_futex_requeue_single_owner（）`]会导致将futex的所有者设置为* new_requeue_owner *句柄引用的线程，如果* new_requeue_owner *为** ZX_HANDLE_INVALID **，则将其设置为空。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_requeue()` returns **ZX_OK** on success.  zx_futex_requeue（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  One of the following is true:  ** ZX_ERR_INVALID_ARGS **以下条件之一为真：
+ Either *value_ptr* or *requeue_ptr* is not a valid userspace pointer  + * value_ptr *或* requeue_ptr *不是有效的用户空间指针
+ Either *value_ptr* or *requeue_ptr* is not aligned to a `sizeof(zx_futex_t)` boundary.  + * value_ptr *或* requeue_ptr *均未与`sizeof（zx_futex_t）`边界对齐。
+ *value_ptr* is the same futex as *requeue_ptr*  + * value_ptr *与* requeue_ptr *是同一个futex
+ *new_requeue_owner* is currently a member of the waiters for either *value_ptr* or *requeue_ptr*  + * new_requeue_owner *当前是* value_ptr *或* requeue_ptr *的服务员成员

**ZX_ERR_BAD_HANDLE**  *new_requeue_owner* is not **ZX_HANDLE_INVALID**, and not a valid handle. **ZX_ERR_WRONG_TYPE**  *new_requeue_owner* is a valid handle, but is not a handle to a thread.**ZX_ERR_BAD_STATE**  *current_value* does not match the value at *value_ptr*. ** ZX_ERR_BAD_HANDLE ** * new_requeue_owner *不是** ZX_HANDLE_INVALID **，并且不是有效的句柄。 ** ZX_ERR_WRONG_TYPE ** * new_requeue_owner *是有效的句柄，但不是线程的句柄。** ZX_ERR_BAD_STATE ** * current_value *与* value_ptr *的值不匹配。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [`zx_futex_requeue_single_owner()`]  -[`zx_futex_requeue_single_owner（）`]
 - [`zx_futex_wait()`]  -[`zx_futex_wait（）`]
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

