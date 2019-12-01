 
# zx_futex_wait  zx_futex_wait 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wait on a futex.  等待一个futex。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_wait(const zx_futex_t* value_ptr,
                          zx_futex_t current_value,
                          zx_handle_t new_futex_owner,
                          zx_time_t deadline);
```
 

 
## DESCRIPTION  描述 

`zx_futex_wait()` atomically verifies that *value_ptr* still contains the value *current_value* and sleeps until the futex is made available by a call to`zx_futex_wake`. Optionally, the thread can also be woken up after the*deadline* (with respect to **ZX_CLOCK_MONOTONIC**) passes. *deadline* may beautomatically adjusted according to the job's [timer slack] policy. zx_futex_wait（）原子地验证* value_ptr *仍然包含值* current_value *并休眠直到通过调用`zx_futex_wake`使futex可用。可选地，还可以在*截止日期*之后（相对于** ZX_CLOCK_MONOTONIC **）唤醒线程。可以根据作业的[计时器松弛]策略自动调整*截止日期*。

 
## SPURIOUS WAKEUPS  唤醒 

A component that uses futexes should be prepared to handle spurious wakeups.  A spurious wakeup is a situation where `zx_futex_wait()`returns successfully even though the component did not wake the waiterby calling [`zx_futex_wake()`]. 应该准备使用futex的组件来处理虚假唤醒。虚假唤醒是这样的情况，即使组件没有通过调用[`zx_futex_wake（）来唤醒服务员，`zx_futex_wait（）`仍成功返回。

Zircon's implementation of futexes currently does not generate spurious wakeups itself.  However, commonly-used algorithms that usefutexes can sometimes generate spurious wakeups.  For example, theusual implementation of `mutex_unlock` can potentially produce a[`zx_futex_wake()`] call on a memory location after the location has beenfreed and reused for unrelated purposes. Zircon对futexes的实现当前本身不会产生虚假唤醒。但是，使用futex的常用算法有时会产生伪唤醒。例如，mutex_unlock的通常实现可能会在释放该存储位置并将其重新用于无关目的之后，对该存储位置产生[[zx_futex_wake（）]]调用。

 
## OWNERSHIP  所有权 

A successful call to `zx_futex_wait()` results in the owner of the futex being set to the thread referenced by the *new_futex_owner* handle, or to nothing if*new_futex_owner* is **ZX_HANDLE_INVALID**. 对`zx_futex_wait（）`的成功调用会导致将futex的所有者设置为* new_futex_owner *句柄引用的线程，或者如果* new_futex_owner *为** ZX_HANDLE_INVALID **则不设置任何内容。

See *Ownership and Priority Inheritance* in [futex](/docs/concepts/objects/futex.md) for details. 有关详细信息，请参见[futex]（/ docs / concepts / objects / futex.md）中的*所有权和优先级继承*。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_wait()` returns **ZX_OK** on success.  zx_futex_wait（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  One of the following is true:  ** ZX_ERR_INVALID_ARGS **以下条件之一为真：
+ *value_ptr* is not a valid userspace pointer  + * value_ptr *不是有效的用户空间指针
+ *value_ptr* is not aligned to a `sizeof(zx_futex_t)` boundary.  + * value_ptr *未与`sizeof（zx_futex_t）`边界对齐。
+ *new_futex_owner* is currently a member of the waiters for *value_ptr*.  + * new_futex_owner *当前是* value_ptr *服务员的成员。

**ZX_ERR_BAD_HANDLE**  *new_futex_owner* is not **ZX_HANDLE_INVALID**, and not a valid handle. **ZX_ERR_WRONG_TYPE**  *new_futex_owner* is a valid handle, but is not a handle to a thread.**ZX_ERR_BAD_STATE**  *current_value* does not match the value at *value_ptr*.**ZX_ERR_TIMED_OUT**  The thread was not woken before *deadline* passed. ** ZX_ERR_BAD_HANDLE ** * new_futex_owner *不是** ZX_HANDLE_INVALID **，并且不是有效的句柄。 ** ZX_ERR_WRONG_TYPE ** * new_futex_owner *是有效的句柄，但不是线程的句柄。** ZX_ERR_BAD_STATE ** * current_value *与* value_ptr *的值不匹配。** ZX_ERR_TIMED_OUT **线程未唤醒在*截止日期*通过之前。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [timer slack](/docs/concepts/objects/timer_slack.md)  -[计时器松弛]（/ docs / concepts / objects / timer_slack.md）
 - [`zx_futex_requeue()`]  -[`zx_futex_requeue（）`]
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

