 
# Zircon Signals  锆石信号 

 
## Introduction  介绍 

A signal is a single bit of information that waitable zircon kernel objects expose to applications.  Each object can expose one or more signals; some are generic and someare specific to the type of object. 信号是可等待的锆石内核对象向应用程序公开的一小部分信息。每个对象都可以暴露一个或多个信号。有些是通用的，有些是针对对象类型的。

For example, the signal **ZX_CHANNEL_READABLE** indicates "this channel endpoint has messages to read", and **ZX_PROCESS_TERMINATED** indicates "this process stopped running." 例如，信号** ZX_CHANNEL_READABLE **指示“此通道端点有要读取的消息”，而信号** ZX_PROCESS_TERMINATED **指示“此进程已停止运行”。

The signals for an object are stored in a uint32 bitmask, and their values (which are object-specific) are defined in the header[`zircon/types.h`](/zircon/system/public/zircon/types.h).The typedef `zx_signals_t` is used to refer to signal bitmasks in syscalls and other APIs. 对象的信号存储在uint32位掩码中，其值（特定于对象）在header [`zircon / types.h`]（/ zircon / system / public / zircon / types.h）中定义typedef`zx_signals_t`用于引用系统调用和其他API中的信号位掩码。

Most objects are waitable.  Ports are an example of a non-waitable object. To determine if an object is waitable, call [`zx_object_get_info()`].with **ZX_INFO_HANDLE_BASIC** topic and test for **ZX_OBJ_PROP_WAITABLE**. 大多数对象都是可以等待的。端口是不可等待对象的示例。要确定对象是否可等待，请使用** ZX_INFO_HANDLE_BASIC **主题调用[`zx_object_get_info（）`。]并测试** ZX_OBJ_PROP_WAITABLE **。

 
## State, State Changes and their Terminology  状态，状态变化及其术语 

A signal is said to be **Active** when its bit is 1 and **Inactive** when its bit is 0.  当信号的位为1时，它被称为“有效”，而当其位为0时，则被称为“无效”。

A signal is said to be **Asserted** when it is made **Active** in response to an event (even if it was already **Active**), and is said to be **Deasserted** when it is made**Inactive** in response to an event (even if it was already **Inactive**). 当响应某个事件（即使它已经是“活动”）时，使该信号“活动”时，该信号被称为“断言”，当该信号被响应时，则被称为“断言”。响应事件而被设为“无效”（即使该事件已经“无效”）。

For example:  When a message is written into a Channel endpoint, the **ZX_CHANNEL_READABLE** signal of the opposing endpoint is **asserted** (which causes that signal to become **active**,if it were not already active).  When the last message in a Channel endpoint'squeue is read from that endpoint, the **ZX_CHANNEL_READABLE** signal of that endpoint is**deasserted** (which causes that signal to become **inactive**) 例如：当消息写入Channel端点时，相对端点的** ZX_CHANNEL_READABLE **信号被断言**（如果该信号尚未激活，则该信号变为**活跃**）。 。从该端点读取Channel端点队列中的最后一条消息时，该端点的** ZX_CHANNEL_READABLE **信号将被取消声明**（这将导致该信号变为**无效**）。

 
## Observing Signals  观察信号 

The syscalls [`zx_object_wait_one()`], [`zx_object_wait_many()`], and [`zx_object_wait_async()`], in combination with a Port, can be used to wait forspecified signals on one or more objects. 系统调用[`zx_object_wait_one（）]，[`zx_object_wait_many（）]和[`zx_object_wait_async（）]与Port结合使用，可以用于等待一个或多个对象上的指定信号。

 
## Common Signals  常见信号 

 
### ZX_SIGNAL_HANDLE_CLOSED  ZX_SIGNAL_HANDLE_CLOSED 

This synthetic signal only exists in the results of [`zx_object_wait_one()`] or [`zx_object_wait_many()`] and indicates that a handle that wasbeing waited upon has been been closed causing the wait operation to be aborted. 该合成信号仅存在于[`zx_object_wait_one（）]或[`zx_object_wait_many（）`]的结果中，并指示正在等待的句柄已关闭，导致等待操作被中止。

This signal can only be obtained as a result of the above two wait calls when the wait itself returns with **ZX_ERR_CANCELED**. 当等待本身以** ZX_ERR_CANCELED **返回时，只能通过上述两次等待调用才能获得该信号。

 
## User Signals  用户信号 

There are eight User Signals (**ZX_USER_SIGNAL_0** through **ZX_USER_SIGNAL_7**) which may asserted or deasserted using the [`zx_object_signal()`] and [`zx_object_signal_peer()`] syscalls,provided the handle has the appropriate rights (**ZX_RIGHT_SIGNAL** or **ZX_RIGHT_SIGNAL_PEER**,respectively).  These User Signals are always initially inactive, and are only modified bythe object signal syscalls. 可以使用[`zx_object_signal（）`]和[`zx_object_signal_peer（）`系统调用来断言或取消断言八个用户信号（** ZX_USER_SIGNAL_0 **至** ZX_USER_SIGNAL_7 **），前提是该句柄具有适当的权限（ ** ZX_RIGHT_SIGNAL **或** ZX_RIGHT_SIGNAL_PEER **）。这些用户信号最初始终是不活动的，并且只能通过对象信号系统调用进行修改。

 
## See Also  也可以看看 

 
 - [`zx_object_signal()`]  -[`zx_object_signal（）`]
 - [`zx_object_signal_peer()`]  -[`zx_object_signal_peer（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]

 

 

