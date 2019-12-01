 
# zx_timer_cancel  zx_timer_cancel 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Cancel a timer.  取消计时器。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_timer_cancel(zx_handle_t handle);
```
 

 
## DESCRIPTION  描述 

`zx_timer_cancel()` cancels a pending timer that was started with [`zx_timer_set()`]. zx_timer_cancel（）取消以[`zx_timer_set（）]开始的未决计时器。

Upon success the pending timer is canceled and the **ZX_TIMER_SIGNALED** signal is de-asserted. If a new pending timer is immediately neededrather than calling `zx_timer_cancel()` first, call [`zx_timer_set()`]with the new deadline. 成功后，挂起的计时器将被取消，并且** ZX_TIMER_SIGNALED **信号将无效。如果立即需要一个新的挂起计时器，而不是首先调用`zx_timer_cancel（）`，请使用新的截止日期调用[`zx_timer_set（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_TIMER** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_TIMER **类型并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_timer_cancel()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_timer_cancel（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* lacks the right **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少正确的** ZX_RIGHT_WRITE **。

 
## NOTE  注意 

Calling this function before [`zx_timer_set()`] has no effect.  在[`zx_timer_set（）`]之前调用此函数无效。

 
## SEE ALSO  也可以看看 

 
 - [`zx_timer_create()`]  -[`zx_timer_create（）`]
 - [`zx_timer_set()`]  -[`zx_timer_set（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

