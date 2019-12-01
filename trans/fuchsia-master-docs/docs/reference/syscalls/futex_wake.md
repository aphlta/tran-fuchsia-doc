 
# zx_futex_wake  zx_futex_wake 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wake some number of threads waiting on a futex, optionally transferring ownership to the thread which was woken in the process.  唤醒等待futex的一些线程，可以选择将所有权转移到进程中被唤醒的线程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_wake(const zx_futex_t* value_ptr, uint32_t wake_count);
```
 

 
## DESCRIPTION  描述 

Waking a futex causes *wake_count* threads waiting on the *value_ptr* futex to be woken up. 唤醒futex会导致唤醒* value_ptr * futex的* wake_count *个线程。

Waking up zero threads is not an error condition.  Passing in an unallocated address for *value_ptr* is not an error condition. 唤醒零线程不是错误情况。传递* value_ptr *的未分配地址不是错误条件。

 
## OWNERSHIP  所有权 

A successful call to `zx_futex_wake()` results in the owner of the futex being set to nothing, regardless of the wake count.  In order to transfer ownership ofa futex, use the [`zx_futex_wake_single_owner()`] variant instead.[`zx_futex_wake_single_owner()`] will attempt to wake exactly one thread from thefutex wait queue.  If there is at least one thread to wake, the owner of thefutex will be set to the thread which was woken.  Otherwise, the futex will haveno owner. 对`zx_futex_wake（）`的成功调用将导致futex的所有者被设置为空，无论唤醒计数如何。为了转移futex的所有权，请改用[`zx_futex_wake_single_owner（）`]。[`zx_futex_wake_single_owner（）`]将尝试从thefutex等待队列中唤醒一个线程。如果至少有一个线程要唤醒，则thefutex的所有者将设置为被唤醒的线程。否则，futex将没有所有者。

See *Ownership and Priority Inheritance* in [futex](/docs/concepts/objects/futex.md) for details. 有关详细信息，请参见[futex]（/ docs / concepts / objects / futex.md）中的*所有权和优先级继承*。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_wake()` returns **ZX_OK** on success.  zx_futex_wake（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *value_ptr* is not aligned.  ** ZX_ERR_INVALID_ARGS ** * value_ptr *不对齐。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [`zx_futex_requeue()`]  -[`zx_futex_requeue（）`]
 - [`zx_futex_wait()`]  -[`zx_futex_wait（）`]
 - [`zx_futex_wake_single_owner()`]  -[`zx_futex_wake_single_owner（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

