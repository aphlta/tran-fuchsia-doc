 
# zx_object_wait_async  zx_object_wait_async 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Subscribe for signals on an object.  订阅对象上的信号。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_wait_async(zx_handle_t handle,
                                 zx_handle_t port,
                                 uint64_t key,
                                 zx_signals_t signals,
                                 uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_object_wait_async()` is a non-blocking syscall which causes packets to be enqueued on *port* when the specified condition is met.Use [`zx_port_wait()`] to retrieve the packets. zx_object_wait_async（）是一个非阻塞的系统调用，当满足指定条件时，它将使数据包在* port *上排队。使用[`zx_port_wait（）`]检索数据包。

*handle* points to the object that is to be watched for changes and must be a waitable object.  * handle *指向要监视更改的对象，并且必须是可等待的对象。

The *options* argument can be 0 or it can be ZX_WAIT_ASYNC_TIMESTAMP which causes the system to capture a timestamp when the wait triggered. * options *参数可以为0，也可以为ZX_WAIT_ASYNC_TIMESTAMP，这会导致系统在等待触发时捕获时间戳。

The *signals* argument indicates which signals on the object specified by *handle* will cause a packet to be enqueued, and if **any** of those signals are asserted when`zx_object_wait_async()` is called, or become asserted afterwards, a packet will beenqueued on *port* containing all of the currently-asserted signals (not just the oneslisted in the *signals* argument).  Once a packet has been enqueued the asynchronouswaiting ends.  No further packets will be enqueued. Note that signals are OR'dinto the state maintained by the port thus you may see any combination ofrequested signals when [`zx_port_wait()`] returns. * signals *参数指示由* handle *指定的对象上的哪些信号将使数据包入队，并且如果在调用zx_object_wait_async（）或之后声明了这些信号中的任何**，一个数据包将在* port *上排队，其中包含所有当前声明的信号（而不仅仅是* signals *参数中列出的信号）。数据包入队后，异步等待结束。不再有其他数据包入队。请注意，信号是与端口保持的状态“或”的关系，因此当[`zx_port_wait（）`]返回时，您可能会看到请求信号的任意组合。

[`zx_port_cancel()`] will terminate the operation and if a packet was in the queue on behalf of the operation, that packet will be removed from the queue. [`zx_port_cancel（）`]将终止操作，并且如果某个分组代表该操作在队列中，则将从队列中删除该分组。

If *handle* is closed, the operation will also be terminated, but packets already in the queue are not affected. 如果* handle *关闭，该操作也将终止，但是队列中已有的数据包将不受影响。

Packets generated via this syscall will have *type* set to **ZX_PKT_TYPE_SIGNAL_ONE** and the union is of type `zx_packet_signal_t`: 通过此系统调用生成的数据包的* type *设置为** ZX_PKT_TYPE_SIGNAL_ONE **，联合的类型为`zx_packet_signal_t`：

```
typedef struct zx_packet_signal {
    zx_signals_t trigger;
    zx_signals_t observed;
    uint64_t count;
    zx_time_t timestamp;       // depends on ZX_WAIT_ASYNC_TIMESTAMP
    uint64_t reserved1;
} zx_packet_signal_t;
```
 

*trigger* is the signals used in the call to `zx_object_wait_async()`, *observed* is the signals actually observed, *count* is a per object defined count of pending operationsand *timestamp* is clock-monotonic time when the object state transitioned to meet thetrigger condition. If options does not include ZX_WAIT_ASYNC_TIMESTAMP the timestamp isreported as 0. * trigger *是调用zx_object_wait_async（）时使用的信号，* observed *是实际观察到的信号，* count *是每个对象定义的未决操作计数，* timestamp *是对象状态时的时钟单调时间过渡到满足触发条件。如果选项不包含ZX_WAIT_ASYNC_TIMESTAMP，则时间戳记将报告为0。

Use the `zx_port_packet_t`'s *key* member to track what object this packet corresponds to and therefore match *count* with the operation. 使用zx_port_packet_t的* key *成员跟踪此数据包所对应的对象，并因此将* count *与该操作匹配。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_WAIT**.  *句柄*必须具有** ZX_RIGHT_WAIT **。

*port* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  *端口*必须为** ZX_OBJ_TYPE_PORT **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_object_wait_async()` returns **ZX_OK** if the subscription succeeded.  如果订阅成功，则zx_object_wait_async（）返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *options* is not 0 or **ZX_WAIT_ASYNC_TIMESTAMP**.  ** ZX_ERR_INVALID_ARGS ** *选项*不为0或** ZX_WAIT_ASYNC_TIMESTAMP **。

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle or *port* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * handle *不是有效的句柄或* port *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *port* is not a Port handle.  ** ZX_ERR_WRONG_TYPE ** *端口*不是端口句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WAIT** or *port* does not have **ZX_RIGHT_WRITE**. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WAIT **或*端口*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_NOT_SUPPORTED**  *handle* is a handle that cannot be waited on.  ** ZX_ERR_NOT_SUPPORTED ** * handle *是无法等待的句柄。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## NOTES  笔记 

See [signals](/docs/concepts/kernel/signals.md) for more information about signals and their terminology.  有关信号及其术语的更多信息，请参见[signals]（/ docs / concepts / kernel / signals.md）。

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_port_cancel()`]  -[`zx_port_cancel（）`]
 - [`zx_port_queue()`]  -[`zx_port_queue（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

