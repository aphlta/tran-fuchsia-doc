 
# Event Pair  事件对 

 
## NAME  名称 

eventpair - Mutually signalable pair of events for concurrent programming  eventpair-可相互发信号的事件对，用于并发编程

 
## SYNOPSIS  概要 

Event Pairs are linked pairs of user-signalable objects. The 8 signal bits reserved for userspace (**ZX_USER_SIGNAL_0** through**ZX_USER_SIGNAL_7**) may be set or cleared on the local or opposingendpoint of an Event Pair. 事件对是用户可标记对象的链接对。可以在事件对的本地或相对端点上设置或清除为用户空间保留的8个信号位（** ZX_USER_SIGNAL_0 **至** ZX_USER_SIGNAL_7 **）。

 
## DESCRIPTION  描述 

TODO  去做

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_eventpair_create()`] - create a connected pair of events  -[`zx_eventpair_create（）`]-创建一对关联的事件

<br>  <br>

 
 - [`zx_object_signal_peer()`] - set or clear the user signals in the opposite end  -[`zx_object_signal_peer（）`]-设置或清除另一端的用户信号

