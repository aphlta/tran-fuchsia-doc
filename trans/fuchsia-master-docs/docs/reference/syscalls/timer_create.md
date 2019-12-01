 
# zx_timer_create  zx_timer_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a timer.  创建一个计时器。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_timer_create(uint32_t options,
                            zx_clock_t clock_id,
                            zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_timer_create()` creates a timer, an object that can signal when a specified point in time has been reached. The only valid*clock_id* is **ZX_CLOCK_MONOTONIC**. zx_timer_create（）创建一个计时器，该对象可以在达到指定时间点时发出信号。唯一有效的* clock_id *是** ZX_CLOCK_MONOTONIC **。

The *options* value specifies the coalescing behavior which controls whether the system can fire the time earlier or laterdepending on other pending timers. * options *值指定合并行为，该行为控制系统是否可以根据其他挂起的计时器来提前或延迟触发时间。

The possible values are:  可能的值为：

 
+ **ZX_TIMER_SLACK_CENTER**  + ** ZX_TIMER_SLACK_CENTER **
+ **ZX_TIMER_SLACK_EARLY**  + ** ZX_TIMER_SLACK_EARLY **
+ **ZX_TIMER_SLACK_LATE**  + ** ZX_TIMER_SLACK_LATE **

Passing 0 in options is equivalent to **ZX_TIMER_SLACK_CENTER**.  在选项中传递0等效于** ZX_TIMER_SLACK_CENTER **。

See [timer slack](/docs/concepts/objects/timer_slack.md) for more information.  有关更多信息，请参见[timer slack]（/ docs / concepts / objects / timer_slack.md）。

The returned handle has the **ZX_RIGHT_DUPLICATE**, **ZX_RIGHT_TRANSFER**, **ZX_RIGHT_WRITE**, **ZX_RIGHT_SIGNAL**, **ZX_RIGHT_WAIT**, and**ZX_RIGHT_INSPECT** rights. 返回的句柄具有** ZX_RIGHT_DUPLICATE **，** ZX_RIGHT_TRANSFER **，** ZX_RIGHT_WRITE **，** ZX_RIGHT_SIGNAL **，** ZX_RIGHT_WAIT **和** ZX_RIGHT_INSPECT **权限。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_timer_create()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_timer_create（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer or NULL or *options* is not one of the **ZX_TIMER_SLACK** values or *clock_id* isany value other than **ZX_CLOCK_MONOTONIC**. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针或NULL或* options *不是** ZX_TIMER_SLACK **值之一或* clock_id *是除ZX_CLOCK_MONOTONIC **以外的任何值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_deadline_after()`]  -[`zx_deadline_after（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_timer_cancel()`]  -[`zx_timer_cancel（）`]
 - [`zx_timer_set()`]  -[`zx_timer_set（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

