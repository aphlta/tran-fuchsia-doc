 
# zx_object_wait_one  zx_object_wait_one 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wait for signals on an object.  等待对象上的信号。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_wait_one(zx_handle_t handle,
                               zx_signals_t signals,
                               zx_time_t deadline,
                               zx_signals_t* observed);
```
 

 
## DESCRIPTION  描述 

`zx_object_wait_one()` is a blocking syscall which causes the caller to wait until either the *deadline* passes or the object to which *handle* refersasserts at least one of the specified *signals*. If the object is alreadyasserting at least one of the specified *signals*, the wait ends immediately. zx_object_wait_one（）是一个阻塞的系统调用，它使调用者等待，直到* deadline *通过或* handle *所引用的对象断言至少一个指定的* signal *。如果对象已经声明了至少一个指定的* signals *，则等待立即结束。

Upon return, if non-NULL, *observed* is a bitmap of *all* of the signals which were observed asserted on that object while waiting. 返回时，如果非NULL，则* observed *是观察到的所有*信号在等待时在该对象上断言的位图。

The *observed* signals may not reflect the actual state of the object's signals if the state of the object was modified by another thread orprocess.  (For example, a Channel ceases asserting **ZX_CHANNEL_READABLE**once the last message in its queue is read). 如果对象的状态是由另一个线程或进程修改的，则*观察到的*信号可能无法反映该对象的信号的实际状态。 （例如，一旦读取了队列中的最后一条消息，Channel将停止断言** ZX_CHANNEL_READABLE **）。

The *deadline* parameter specifies a deadline with respect to **ZX_CLOCK_MONOTONIC** and will be automatically adjusted according to the job's[timer slack] policy.  **ZX_TIME_INFINITE** is a special value meaning waitforever. * deadline *参数指定相对于** ZX_CLOCK_MONOTONIC **的截止日期，并将根据作业的[timer slack]策略自动调整。 ** ZX_TIME_INFINITE **是一个特殊值，表示永远等待。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_WAIT**.  *句柄*必须具有** ZX_RIGHT_WAIT **。

 
## RETURN VALUE  返回值 

`zx_object_wait_one()` returns **ZX_OK** if any of *signals* were observed on the object before *deadline* passes. 如果在* deadline *通过之前在对象上观察到任何* signal *，`zx_object_wait_one（）`将返回** ZX_OK **。

In the event of **ZX_ERR_TIMED_OUT**, *observed* may reflect state changes that occurred after the deadline passed, but before the syscall returned. 在** ZX_ERR_TIMED_OUT **的情况下，*观察到*可能反映在截止日期过去之后但在系统调用返回之前发生的状态更改。

In the event of **ZX_ERR_CANCELED**, *handle* has been closed, and *observed* will have the **ZX_SIGNAL_HANDLE_CLOSED** bit set. 在** ZX_ERR_CANCELED **的情况下，*句柄*已关闭，并且*被观察*将设置** ZX_SIGNAL_HANDLE_CLOSED **位。

For any other return value, *observed* is undefined.  对于任何其他返回值，未定义* observed *。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *observed* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *观察到的*是无效的指针。

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WAIT** and may not be waited upon. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WAIT **，可能不会等待。

**ZX_ERR_CANCELED**  *handle* was invalidated (e.g., closed) during the wait.  ** ZX_ERR_CANCELED ** *句柄*在等待期间无效（例如，关闭）。

**ZX_ERR_TIMED_OUT**  The specified deadline passed before any of the specified *signals* are observed on *handle*. ** ZX_ERR_TIMED_OUT **在*句柄*上观察到任何指定*信号*之前经过的指定截止日期。

**ZX_ERR_NOT_SUPPORTED**  *handle* is a handle that cannot be waited on (for example, a Port handle). ** ZX_ERR_NOT_SUPPORTED ** * handle *是无法等待的句柄（例如，Port句柄）。

 
## SEE ALSO  也可以看看 

 
 - [timer slack](/docs/concepts/objects/timer_slack.md)  -[计时器松弛]（/ docs / concepts / objects / timer_slack.md）
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

