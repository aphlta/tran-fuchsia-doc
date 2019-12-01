 
# zx_channel_call  zx_channel_call 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Send a message to a channel and await a reply.  向频道发送消息并等待回复。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_channel_call(zx_handle_t handle,
                            uint32_t options,
                            zx_time_t deadline,
                            const zx_channel_call_args_t* args,
                            uint32_t* actual_bytes,
                            uint32_t* actual_handles);
```
 

 
## DESCRIPTION  描述 

`zx_channel_call()` is like a combined [`zx_channel_write()`], [`zx_object_wait_one()`], and [`zx_channel_read()`], with the addition of a feature where a transaction id atthe front of the message payload *bytes* is used to match reply messages with sendmessages, enabling multiple calling threads to share a channel without any additionaluserspace bookkeeping. zx_channel_call（）类似于[zx_channel_write（）]，[zx_object_wait_one（）]和[zx_channel_read（）]的组合，并增加了一个功能，该功能在消息有效负载的最前面* bytes *用于将回复消息与sendmessage进行匹配，从而使多个调用线程可以共享一个通道，而无需进行任何额外的用户空间簿记。

The write and read phases of this operation behave like [`zx_channel_write()`] and [`zx_channel_read()`] with the difference that their parameters are provided via the`zx_channel_call_args_t` structure. 此操作的写入和读取阶段的行为类似于[`zx_channel_write（）]和[`zx_channel_read（）`]，区别在于它们的参数是通过zx_channel_call_args_t结构提供的。

The first four bytes of the written and read back messages are treated as a transaction ID of type `zx_txid_t`.  The kernel generates a txid for thewritten message, replacing that part of the message as read from userspace.The kernel generated txid will be between 0x80000000 and 0xFFFFFFFF, and willnot collide with any txid from any other `zx_channel_call()` in progress againstthis channel endpoint.  If the written message has a length of fewer than fourbytes, an error is reported. 写入和读取的消息的前四个字节被视为类型为zx_txid_t的事务ID。内核会为写入的消息生成一个txid，替换从用户空间读取的那部分消息。内核生成的txid将介于0x80000000和0xFFFFFFFF之间，并且不会与此通道端点的任何其他`zx_channel_call（）`进行的txid发生冲突。 。如果书面消息的长度小于四字节，则会报告错误。

When the outbound message is written, simultaneously an interest is registered for inbound messages of the matching txid. 写入出站消息时，同时会为匹配的txid的入站消息注册一个兴趣。

*deadline* may be automatically adjusted according to the job's [timer slack] policy. *最后期限*可能会根据作业的[计时器松弛]策略自动进行调整。

While the slack-adjusted *deadline* has not passed, if an inbound message arrives with a matching txid, instead of being added to the tail of the generalinbound message queue, it is delivered directly to the thread waiting in`zx_channel_call()`. 尽管没有经过松弛调整的“截止期限”，但是如果入站消息以匹配的txid到达，而不是被添加到generalinbound消息队列的末尾，而是直接传递到在zx_channel_call（）中等待的线程。

If such a reply arrives after the slack-adjusted *deadline* has passed, it will arrive in the general inbound message queue, cause **ZX_CHANNEL_READABLE** to besignaled, etc. 如果经过松弛调整的*最后期限*之后收到此类答复，它将进入常规的入站消息队列，使** ZX_CHANNEL_READABLE **发出信号，依此类推。

Inbound messages that are too large to fit in *rd_num_bytes* and *rd_num_handles* are discarded and **ZX_ERR_BUFFER_TOO_SMALL** is returned in that case. 太大而无法容纳* rd_num_bytes *和* rd_num_handles *的入站消息，在这种情况下将返回** ZX_ERR_BUFFER_TOO_SMALL **。

As with [`zx_channel_write()`], the handles in *handles* are always consumed by `zx_channel_call()` and no longer exist in the calling process. 与[`zx_channel_write（）`]一样，* handles *中的句柄始终由`zx_channel_call（）`占用，并且在调用过程中不再存在。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CHANNEL** and have **ZX_RIGHT_READ** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CHANNEL **，并且具有** ZX_RIGHT_READ **和** ZX_RIGHT_WRITE **。

All wr_handles of *args* must have **ZX_RIGHT_TRANSFER**.  * args *的所有wr_handles必须具有** ZX_RIGHT_TRANSFER **。

 
## RETURN VALUE  返回值 

`zx_channel_call()` returns **ZX_OK** on success and the number of bytes and count of handles in the reply message are returned via *actual_bytes* and*actual_handles*, respectively. zx_channel_call（）成功返回** ZX_OK **，并分别通过* actual_bytes *和* actual_handles *返回回复消息中的字节数和句柄数。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle, any element in *handles* is not a valid handle, or there are duplicates among the handlesin the *handles* array. ** ZX_ERR_BAD_HANDLE ** * handle *不是有效的句柄，* handles *中的任何元素都不是有效的句柄，或者* handles *数组中的handles中有重复项。

**ZX_ERR_WRONG_TYPE**  *handle* is not a channel handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是通道句柄。

**ZX_ERR_INVALID_ARGS**  any of the provided pointers are invalid or null, or *wr_num_bytes* is less than four, or *options* is nonzero. ** ZX_ERR_INVALID_ARGS **任何提供的指针无效或为空，或者* wr_num_bytes *小于4，或者* options *非零。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE** or any element in *handles* does not have **ZX_RIGHT_TRANSFER**. ** ZX_ERR_ACCESS_DENIED ** * handle *没有** ZX_RIGHT_WRITE **或* handles *中的任何元素没有** ZX_RIGHT_TRANSFER **。

**ZX_ERR_PEER_CLOSED**  The other side of the channel was closed or became closed while waiting for the reply. ** ZX_ERR_PEER_CLOSED **通道的另一侧已关闭或在等待答复时已关闭。

**ZX_ERR_CANCELED**  *handle* was closed while waiting for a reply. TODO(ZX-4233): Transferring a channel with pending calls currently leads to undefined behavior. Withthe current implementation, transferring such a channel does not interrupt thepending calls, as it does not close the underlying channel endpoint. Programs shouldbe aware of this behavior, but they **must not** rely on it. ** ZX_ERR_CANCELED ** *句柄*在等待回复时已关闭。 TODO（ZX-4233）：当前传输带有未决呼叫的通道会导致未定义的行为。在当前的实现中，转移这样的信道不会中断未决的呼叫，因为它不会关闭底层的信道端点。程序应该意识到这种行为，但是它们“绝对不能”依赖它。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_OUT_OF_RANGE**  *wr_num_bytes* or *wr_num_handles* are larger than the largest allowable size for channel messages. ** ZX_ERR_OUT_OF_RANGE ** * wr_num_bytes *或* wr_num_handles *大于通道消息的最大允许大小。

**ZX_ERR_BUFFER_TOO_SMALL**  *rd_num_bytes* or *rd_num_handles* are too small to contain the reply message. ** ZX_ERR_BUFFER_TOO_SMALL ** * rd_num_bytes *或* rd_num_handles *太小，无法包含回复消息。

**ZX_ERR_NOT_SUPPORTED**  one of the handles in *handles* was *handle* (the handle to the channel being written to). ** ZX_ERR_NOT_SUPPORTED ** * handles *中的句柄之一是* handle *（正在写入的通道的句柄）。

 
## NOTES  笔记 

The facilities provided by `zx_channel_call()` can interoperate with message dispatchers using [`zx_channel_read()`] and [`zx_channel_write()`] directly, provided the following rulesare observed: 只要遵守以下规则，`zx_channel_call（）`提供的功能可以使用[`zx_channel_read（）]和[`zx_channel_write（）]直接与消息分发程序进行互操作。

 
1. A server receiving synchronous messages via [`zx_channel_read()`] should ensure that the txid of incoming messages is reflected back in outgoing responses via [`zx_channel_write()`]so that clients using `zx_channel_call()` can correctly route the replies. 1.通过[`zx_channel_read（）]接收同步消息的服务器应确保传入消息的txid通过[`zx_channel_write（）]反映在传出响应中，以便使用`zx_channel_call（）`的客户端可以正确路由回覆。

 
2. A client sending messages via [`zx_channel_write()`] that will be replied to should ensure that it uses txids between 0 and 0x7FFFFFFF only, to avoid colliding with other threadscommunicating via `zx_channel_call()`. 2.通过[zx_channel_write（）]发送消息的客户端将得到答复，应确保它仅使用0到0x7FFFFFFF之间的txid，以避免与通过zx_channel_call（）通信的其他线程发生冲突。

If a `zx_channel_call()` returns due to **ZX_ERR_TIMED_OUT**, if the server eventually replies, at some point in the future, the reply *could* match another outbound request (provided about2^31 `zx_channel_call()`s have happened since the original request.  This syscall is designedaround the expectation that timeouts are generally fatal and clients do not expect to continuecommunications on a channel that is timing out. 如果`zx_channel_call（）`由于** ZX_ERR_TIMED_OUT **而返回，则如果服务器最终在将来的某个时间点进行答复，则答复*可以*匹配另一个出站请求（大约2 ^ 31`zx_channel_call（）提供了此系统调用是根据以下预期而设计的：超时通常是致命的，并且客户不希望继续在超时的通道上进行通信。

 
## SEE ALSO  也可以看看 

 
 - [timer slack](/docs/concepts/objects/timer_slack.md)  -[计时器松弛]（/ docs / concepts / objects / timer_slack.md）
 - [`zx_channel_create()`]  -[`zx_channel_create（）`]
 - [`zx_channel_read()`]  -[`zx_channel_read（）`]
 - [`zx_channel_write()`]  -[`zx_channel_write（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

