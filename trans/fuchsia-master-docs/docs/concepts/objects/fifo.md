 
# FIFO  先进先出 

 
## NAME  名称 

FIFO - first-in first-out interprocess queue  FIFO-先进先出进程间队列

 
## SYNOPSIS  概要 

FIFOs are intended to be the control plane for shared memory transports.  Their read and write operations are more efficient than[sockets](socket.md) or [channels](channel.md), but there are severerestrictions on the size of elements and buffers. FIFO旨在用作共享内存传输的控制平面。它们的读写操作比[sockets]（socket.md）或[channels]（channel.md）更有效，但对元素和缓冲区的大小有严格的限制。

 
## DESCRIPTION  描述 

TODO  去做

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_fifo_create()`] - create a new fifo  -[`zx_fifo_create（）`]-创建一个新的fifo
 - [`zx_fifo_read()`] - read data from a fifo  -[`zx_fifo_read（）`]-从FIFO读取数据
 - [`zx_fifo_write()`] - write data to a fifo  -[`zx_fifo_write（）`]-将数据写入FIFO

