 
# zx_futex_wake_single_owner  zx_futex_wake_single_owner 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wake some number of threads waiting on a futex, optionally transferring ownership to the thread which was woken in the process.  唤醒等待futex的一些线程，可以选择将所有权转移到进程中被唤醒的线程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_futex_wake_single_owner(const zx_futex_t* value_ptr);
```
 

 
## DESCRIPTION  描述 

See [`zx_futex_wake()`] for a full description.  有关完整说明，请参见[`zx_futex_wake（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_futex_wake_single_owner()` returns **ZX_OK** on success.  zx_futex_wake_single_owner（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *value_ptr* is not aligned.  ** ZX_ERR_INVALID_ARGS ** * value_ptr *不对齐。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [`zx_futex_requeue()`]  -[`zx_futex_requeue（）`]
 - [`zx_futex_wait()`]  -[`zx_futex_wait（）`]
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

