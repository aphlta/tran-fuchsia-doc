 
# Channel  渠道 

 
## NAME  名称 

channel - Bidirectional interprocess communication  通道-双向进程间通信

 
## SYNOPSIS  概要 

A channel is a bidirectional transport of messages consisting of some amount of byte data and some number of handles. 通道是消息的双向传输，包含一定数量的字节数据和一定数量的句柄。

 
## DESCRIPTION  描述 

Channels maintain an ordered queue of messages to be delivered in either direction. A message consists of some amount of data and some number of handles.A call to [`zx_channel_write()`] enqueues one message, and a call to[`zx_channel_read()`] dequeues one message (if any are queued). A thread can blockuntil messages are pending via [`zx_object_wait_one()`] or other waitingmechanisms. 通道维护要在任一方向传递的消息的有序队列。一条消息由一定数量的数据和一定数量的句柄组成。对[`zx_channel_write（）]的调用使一条消息入队，对[`zx_channel_read（）`]的调用使一条消息出队（如果有排队）。线程可以阻止消息通过[`zx_object_wait_one（）`或其他等待机制挂起。

Alternatively, a call to [`zx_channel_call()`] enqueues a message in one direction of the channel, waits for a corresponding response, anddequeues the response message. In call mode, corresponding responsesare identified via the first 4 bytes of the message, called thetransaction ID. The kernel supplies distinct transaction IDs (always with thehigh bit set) for messages written with [`zx_channel_call()`]. 可替代地，对[`zx_channel_call（）]的调用使消息在通道的一个方向上排队，等待相应的响应，然后使响应消息出队。在呼叫模式下，通过消息的前4个字节（称为事务ID）识别相应的响应。内核为使用[`zx_channel_call（）]编写的消息提供不同的事务ID（始终设置高位）。

The process of sending a message via a channel has two steps. The first is to atomically write the data into the channel and move ownership of all handles inthe message into this channel. This operation always consumes the handles: atthe end of the call, all handles either are all in the channel or are alldiscarded. The second operation, channel read, is similar: on successall the handles in the next message are atomically moved into thereceiving process' handle table. On failure, the channel retainsownership unless the **ZX_CHANNEL_READ_MAY_DISCARD** optionis specified, then they are dropped. 通过通道发送消息的过程分为两个步骤。第一种是将数据原子写入通道，并将消息中所有句柄的所有权移入该通道。此操作始终消耗句柄：在调用结束时，所有句柄要么全部在通道中，要么全部丢弃。第二个操作，即通道读取，是类似的：成功后，下一条消息中的所有句柄都被原子地移到接收进程的句柄表中。失败时，除非指定** ZX_CHANNEL_READ_MAY_DISCARD **选项，否则通道保留所有权，然后将其删除。

Unlike many other kernel object types, channels are not duplicatable. Thus, there is only ever one handle associated with a channel endpoint, and the process holdingthat handle is considered the owner. Only the owner can read or write messages or sendthe channel endpoint to another process. 与许多其他内核对象类型不同，通道是不可复制的。因此，只有一个句柄与通道端点关联，并且拥有该句柄的进程被视为所有者。仅所有者可以读取或写入消息或将通道终结点发送到另一个进程。

Furthermore, when ownership of a channel endpoint goes from one process to another, even if a write was in progress, the ordering of messages is guaranteedto be parsimonious; messages before the transfer event originate from theprevious owner and messages after the transfer belong to the new owner. The sameapplies if a read was in progress when the endpoint was transferred. 此外，当通道端点的所有权从一个进程转到另一个进程时，即使正在进行写操作，也可以保证消息的顺序是简约的。转移事件之前的消息来自先前的所有者，转移之后的消息属于新所有者。如果在传输端点时正在进行读取，则同样适用。

The above sequential guarantee is not provided for other kernel objects, even if the last remaining handle is stripped of the **ZX_RIGHT_DUPLICATE** right. 即使最后一个剩余句柄被剥夺了** ZX_RIGHT_DUPLICATE **权限，也不会为其他内核对象提供上述顺序保证。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_channel_call()`] - synchronously send a message and receive a reply  -[`zx_channel_call（）`]-同步发送消息并接收回复
 - [`zx_channel_create()`] - create a new channel  -[`zx_channel_create（）`]-创建一个新频道
 - [`zx_channel_read()`] - receive a message from a channel  -[`zx_channel_read（）`]-接收来自频道的消息
 - [`zx_channel_write()`] - write a message to a channel  -[`zx_channel_write（）`]-向频道写消息

<br>  <br>

 
 - [`zx_object_wait_one()`] - wait for signals on one object  -[`zx_object_wait_one（）`]-等待一个对象上的信号

 
## SEE ALSO  也可以看看 

 
+ [Zircon concepts](/docs/concepts/kernel/concepts.md)  + [锆石概念]（/ docs / concepts / kernel / concepts.md）
+ [Handles](/docs/concepts/objects/handles.md)  + [句柄]（/ docs / concepts / objects / handles.md）

