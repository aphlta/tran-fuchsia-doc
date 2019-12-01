 
# zx_timer_set  zx_timer_set 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Start a timer.  启动一个计时器。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_timer_set(zx_handle_t handle,
                         zx_time_t deadline,
                         zx_duration_t slack);
```
 

 
## DESCRIPTION  描述 

`zx_timer_set()` starts a one-shot timer that will fire when *deadline* passes. If a previous call to `zx_timer_set()` waspending, the previous timer is canceled and**ZX_TIMER_SIGNALED** is de-asserted as needed. `zx_timer_set（）`启动一个一次性计时器，当*截止期限*通过时将触发。如果先前对`zx_timer_set（）`的调用正在等待，则先前的计时器将被取消，并且** ZX_TIMER_SIGNALED **将根据需要取消激活。

The *deadline* parameter specifies a deadline with respect to **ZX_CLOCK_MONOTONIC**. To wait for a relative interval,use [`zx_deadline_after()`] returned value in *deadline*. * deadline *参数指定相对于** ZX_CLOCK_MONOTONIC **的截止日期。要等待相对间隔，请在[最后期限*]中使用[`zx_deadline_after（）`]返回值。

To fire the timer immediately pass a *deadline* less than or equal to **0**.  要触发计时器，请立即传递小于或等于** 0 **的*最后期限*。

When the timer fires it asserts **ZX_TIMER_SIGNALED**. To de-assert this signal call [`zx_timer_cancel()`] or `zx_timer_set()` again. 计时器触发时，它会断言** ZX_TIMER_SIGNALED **。要取消声明该信号，请再次调用[`zx_timer_cancel（）`]或`zx_timer_set（）`。

The *slack* parameter specifies a range from *deadline* - *slack* to *deadline* + *slack* during which the timer is allowed to fire. The systemuses this parameter as a hint to coalesce nearby timers. * slack *参数指定从* deadline *-* slack *到* deadline * + * slack *的范围，在该范围内允许计时器触发。系统使用此参数作为合并附近计时器的提示。

The precise coalescing behavior is controlled by the *options* parameter specified when the timer was created. **ZX_TIMER_SLACK_EARLY** allows onlyfiring in the *deadline* - *slack* interval and **ZX_TIMER_SLACK_LATE**allows only firing in the *deadline* + *slack* interval. The defaultoption value of 0 is **ZX_TIMER_SLACK_CENTER** and allows both early andlate firing with an effective interval of *deadline* - *slack* to*deadline* + *slack* 精确的合并行为由创建计时器时指定的* options *参数控制。 ** ZX_TIMER_SLACK_EARLY **仅允许在*截止时间*-*松弛*间隔内触发，**** ZX_TIMER_SLACK_LATE **仅允许在*截止时间* + *松弛*间隔内触发。默认选项值0为** ZX_TIMER_SLACK_CENTER **，并允许以有效期限* deadline *-* slack *到* deadline * + * slack *的早期触发和延迟触发

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_TIMER** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_TIMER **类型并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_timer_set()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_timer_set（）成功时返回** ZX_OK **。如果发生故障，将返回负错误值。

 

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* lacks the right **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少正确的** ZX_RIGHT_WRITE **。

**ZX_ERR_OUT_OF_RANGE**  *slack* is negative.  ** ZX_ERR_OUT_OF_RANGE ** *松弛*为负。

 
## SEE ALSO  也可以看看 

 
 - [`zx_deadline_after()`]  -[`zx_deadline_after（）`]
 - [`zx_timer_cancel()`]  -[`zx_timer_cancel（）`]
 - [`zx_timer_create()`]  -[`zx_timer_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

