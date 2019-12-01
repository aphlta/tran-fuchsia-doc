 
# Port  港口 

 
## NAME  名称 

port - Signaling and mailbox primitive  端口-信令和邮箱原语

 
## SYNOPSIS  概要 

Ports allow threads to wait for packets to be delivered from various events. These events include explicit queueing on the port,asynchronous waits on other handles bound to the port, andasynchronous message delivery from IPC transports. 端口允许线程等待各种事件传递的数据包。这些事件包括端口上的显式排队，绑定到该端口的其他句柄上的异步等待以及来自IPC传输的异步消息传递。

 
## DESCRIPTION  描述 

TODO  去做

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_port_create()`] - create a port  -[`zx_port_create（）`]-创建一个端口
 - [`zx_port_queue()`] - send a packet to a port  -[`zx_port_queue（）`]-将数据包发送到端口
 - [`zx_port_wait()`] - wait for packets to arrive on a port  -[`zx_port_wait（）`]-等待数据包到达端口

