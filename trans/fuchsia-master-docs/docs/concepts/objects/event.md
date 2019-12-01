 
# Event  事件 

 
## NAME  名称 

event - Signalable event for concurrent programming  事件-用于并发编程的可发信号事件

 
## SYNOPSIS  概要 

Events are user-signalable objects. The 8 signal bits reserved for userspace (**ZX_USER_SIGNAL_0** through **ZX_USER_SIGNAL_7**) may be set,cleared, and waited upon. 事件是用户可发送信号的对象。可以设置，清除并等待为用户空间保留的8个信号位（** ZX_USER_SIGNAL_0 **至** ZX_USER_SIGNAL_7 **）。

 
## DESCRIPTION  描述 

TODO  去做

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_event_create()`] - create an event  -[`zx_event_create（）`]-创建一个事件
 - [`zx_object_signal()`] - set or clear the user signals on an object  -[`zx_object_signal（）`]-设置或清除对象上的用户信号

 
## SEE ALSO  也可以看看 

 
 - [eventpair](eventpair.md) - linked pairs of signalable objects  -[eventpair]（eventpair.md）-可通知对象的链接对

