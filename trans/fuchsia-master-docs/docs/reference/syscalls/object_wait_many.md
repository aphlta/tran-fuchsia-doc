 
# zx_object_wait_many  zx_object_wait_many 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Wait for signals on multiple objects.  等待多个对象上的信号。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_wait_many(zx_wait_item_t* items,
                                size_t num_items,
                                zx_time_t deadline);
```
 

 
## DESCRIPTION  描述 

`zx_object_wait_many()` is a blocking syscall which causes the caller to wait until either the *deadline* passes or at least one of the specifiedsignals is asserted by the object to which the associated handle refers.If an object is already asserting at least one of the specified signals,the wait ends immediately. zx_object_wait_many（）是一个阻塞的系统调用，它使调用者等待，直到* deadline *通过或相关句柄所引用的对象断言了至少一个指定信号。如果一个对象已经断言了至少一个在指定信号中，等待立即结束。

```
typedef struct {
    zx_handle_t handle;
    zx_signals_t waitfor;
    zx_signals_t pending;
} zx_wait_item_t;
```
 

The caller must provide *count* `zx_wait_item_t`s in the *items* array, containing the handle and signals bitmask to wait for for each item. 调用者必须在* items *数组中提供* count *`zx_wait_item_t`s，其中包含句柄和信号位掩码，以等待每个项目。

The *deadline* parameter specifies a deadline with respect to **ZX_CLOCK_MONOTONIC** and will be automatically adjusted according to the job's[timer slack] policy.  **ZX_TIME_INFINITE** is a special value meaning waitforever. * deadline *参数指定相对于** ZX_CLOCK_MONOTONIC **的截止日期，并将根据作业的[timer slack]策略自动调整。 ** ZX_TIME_INFINITE **是一个特殊值，表示永远等待。

Upon return, the *pending* field of *items* is filled with bitmaps indicating which signals are pending for each item. 返回时，* items *的* pending *字段填充有位图，指示每个项目的未决信号。

The *pending* signals in *items* may not reflect the actual state of the object's signals if the state of the object was modified by another thread orprocess.  (For example, a Channel ceases asserting **ZX_CHANNEL_READABLE**once the last message in its queue is read). 如果对象的状态被另一个线程或进程修改，则* items *中的* pending *信号可能无法反映该对象的信号的实际状态。 （例如，一旦读取了队列中的最后一条消息，Channel将停止断言** ZX_CHANNEL_READABLE **）。

The maximum number of items that may be waited upon is **ZX_WAIT_MANY_MAX_ITEMS**, which is 8.  To wait on more things at once use [Ports](/docs/concepts/objects/port.md). 可以等待的最大项目数是** ZX_WAIT_MANY_MAX_ITEMS **，即8。要同时等待更多内容，请使用[端口]（/ docs / concepts / objects / port.md）。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Every entry of *items* must have a *handle* field with **ZX_RIGHT_WAIT**.  * items *的每个条目都必须具有* handle *字段和** ZX_RIGHT_WAIT **。

 
## RETURN VALUE  返回值 

`zx_object_wait_many()` returns **ZX_OK** if any of *waitfor* signals were observed on their respective object before *deadline* passed. 如果在传递* deadline *之前在其各自的对象上观察到任何* waitfor *信号，则zx_object_wait_many（）返回** ZX_OK **。

In the event of **ZX_ERR_TIMED_OUT**, *items* may reflect state changes that occurred after the deadline passed, but before the syscall returned. 在** ZX_ERR_TIMED_OUT **的情况下，* items *可能反映状态变化，该变化发生在截止日期之后但在syscall返回之前。

In the event of **ZX_ERR_CANCELED**, one or more of the items being waited upon have had their handles closed, and the *pending* field for those itemswill have the **ZX_SIGNAL_HANDLE_CLOSED** bit set. 在** ZX_ERR_CANCELED **的情况下，正在等待的一个或多个项目的句柄已关闭，并且这些项目的* pending *字段将设置** ZX_SIGNAL_HANDLE_CLOSED **位。

For any other return value, the *pending* fields of *items* are undefined.  对于任何其他返回值，* items *的* pending *字段均未定义。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *items* isn't a valid pointer.  ** ZX_ERR_INVALID_ARGS ** *项目*不是有效的指针。

**ZX_ERR_OUT_OF_RANGE**  *count* is greater than **ZX_WAIT_MANY_MAX_ITEMS**.  ** ZX_ERR_OUT_OF_RANGE ** * count *大于** ZX_WAIT_MANY_MAX_ITEMS **。

**ZX_ERR_BAD_HANDLE**  one of *items* contains an invalid handle.  ** ZX_ERR_BAD_HANDLE ** *其中一项*包含无效的句柄。

**ZX_ERR_ACCESS_DENIED**  One or more of the provided *handles* does not have **ZX_RIGHT_WAIT** and may not be waited upon. ** ZX_ERR_ACCESS_DENIED **提供的一个或多个*句柄*没有** ZX_RIGHT_WAIT **，可能不会等待。

**ZX_ERR_CANCELED**  One or more of the provided *handles* was invalidated (e.g., closed) during the wait. ** ZX_ERR_CANCELED **在等待期间，一个或多个提供的*句柄*无效（例如，关闭）。

**ZX_ERR_TIMED_OUT**  The specified deadline passed before any of the specified signals are observed on any of the specified handles. ** ZX_ERR_TIMED_OUT **在任何指定句柄上观察到任何指定信号之前经过的指定截止日期。

**ZX_ERR_NOT_SUPPORTED**  One of the *items* contains a handle that cannot be waited one (for example, a Port handle). ** ZX_ERR_NOT_SUPPORTED **其中一个* item *包含一个不能等待的句柄（例如，Port句柄）。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## BUGS  臭虫 

*pending* more properly should be called *observed*.  *待处理*更恰当地称为*观察*。

 
## SEE ALSO  也可以看看 

 
 - [timer slack](/docs/concepts/objects/timer_slack.md)  -[计时器松弛]（/ docs / concepts / objects / timer_slack.md）
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

