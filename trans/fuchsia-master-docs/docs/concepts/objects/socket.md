 
# Socket  插座 

 
## NAME  名称 

Socket - Bidirectional streaming IPC transport  套接字-双向流IPC传输

 
## SYNOPSIS  概要 

Sockets are a bidirectional stream transport. Unlike channels, sockets only move data (not handles). 套接字是双向流传输。与通道不同，套接字只能移动数据（而不是句柄）。

 
## DESCRIPTION  描述 

Data is written into one end of a socket via [`zx_socket_write()`] and read from the opposing end via [`zx_socket_read()`]. 数据通过[`zx_socket_write（）]写入套接字的一端，并通过[`zx_socket_read（）]从另一端读取。

Upon creation, both ends of the socket are writable and readable. Via the **ZX_SOCKET_SHUTDOWN_READ** and **ZX_SOCKET_SHUTDOWN_WRITE** options to[`zx_socket_shutdown()`], one end of the socket can be closed for reading and/orwriting. 创建后，套接字的两端都是可写和可读的。通过[zx_socket_shutdown（）]的** ZX_SOCKET_SHUTDOWN_READ **和** ZX_SOCKET_SHUTDOWN_WRITE **选项，可以关闭套接字的一端以进行读取和/或写入。

 
## PROPERTIES  性质 

The following properties may be queried from a socket object:  可以从套接字对象中查询以下属性：

**ZX_PROP_SOCKET_RX_THRESHOLD** size of the read threshold of a socket, in bytes. When the bytes queued on the socket (available for reading) is equal toor greater than this value, the **ZX_SOCKET_READ_THRESHOLD** signal is asserted.Read threshold signalling is disabled by default (and when set, writinga value of 0 for this property disables it). ** ZX_PROP_SOCKET_RX_THRESHOLD **套接字的读取阈值大小，以字节为单位。当套接字上排队的字节（可读取）等于或大于此值时，将声明** ZX_SOCKET_READ_THRESHOLD **信号。默认情况下禁用读取阈值信令（并且设置时，为此属性写入0值将禁用它）。

**ZX_PROP_SOCKET_TX_THRESHOLD** size of the write threshold of a socket, in bytes. When the space available for writing on the socket is equal to orgreater than this value, the **ZX_SOCKET_WRITE_THRESHOLD** signal is asserted.Write threshold signalling is disabled by default (and when set, writing avalue of 0 for this property disables it). ** ZX_PROP_SOCKET_TX_THRESHOLD **套接字的写阈值大小，以字节为单位。当可在套接字上写入的空间等于该值时，将声明** ZX_SOCKET_WRITE_THRESHOLD **信号。默认情况下将禁用写阈值信令（并且设置时，为此属性写入0值将禁用它）。

From the point of view of a socket handle, the receive buffer contains the data that is readable via [`zx_socket_read()`] from that handle (having been writtenfrom the opposing handle), and the transmit buffer contains the data that iswritten via [`zx_socket_write()`] to that handle (and readable from the opposinghandle). 从套接字句柄的角度来看，接收缓冲区包含可从该句柄通过[`zx_socket_read（）`]读取的数据（已从相反的句柄写入），而发送缓冲区包含通过[该句柄的“ zx_socket_write（）”）（并且可以从对面的句柄读取）。

 
## SIGNALS  讯号 

The following signals may be set for a socket object:  可以为套接字对象设置以下信号：

**ZX_SOCKET_READABLE** data is available to read from the socket  ** ZX_SOCKET_READABLE **数据可从套接字读取

**ZX_SOCKET_WRITABLE** data may be written to the socket  ** ZX_SOCKET_WRITABLE **数据可能会写入套接字

**ZX_SOCKET_PEER_CLOSED** the other endpoint of this socket has been closed. ** ZX_SOCKET_PEER_CLOSED **该套接字的另一个端点已关闭。

**ZX_SOCKET_PEER_WRITE_DISABLED** writing is disabled permanently for the other endpoint either because of passing **ZX_SOCKET_SHUTDOWN_READ** to this endpointor passing **ZX_SOCKET_SHUTDOWN_WRITE** to the peer. Reads on a socket endpointwith this signal raised will succeed so long as there is data in the socket thatwas written before writing was disabled. ** ZX_SOCKET_PEER_WRITE_DISABLED **永久禁用其他端点的写入，这是因为将** ZX_SOCKET_SHUTDOWN_READ **传递给该端点，或者是将** ZX_SOCKET_SHUTDOWN_WRITE **传递给了对等端。只要在禁用写操作之前已在套接字中写入了数据，在发出此信号的情况下，套接字端点上的读取将成功进行。

**ZX_SOCKET_WRITE_DISABLED** writing is disabled permanently for this endpoint either because of passing **ZX_SOCKET_SHUTDOWN_WRITE** to this endpoint orpassing **ZX_SOCKET_SHUTDOWN_READ** to the peer. ** ZX_SOCKET_WRITE_DISABLED **永久禁用了此端点的写入，这是因为将** ZX_SOCKET_SHUTDOWN_WRITE **传递到此端点，或者是将** ZX_SOCKET_SHUTDOWN_READ **传递给了对等端。

**ZX_SOCKET_READ_THRESHOLD** data queued up on socket for reading exceeds the read threshold. ** ZX_SOCKET_READ_THRESHOLD **在套接字上排队等待读取的数据超过了读取阈值。

**ZX_SOCKET_WRITE_THRESHOLD** space available on the socket for writing exceeds the write threshold. ** ZX_SOCKET_WRITE_THRESHOLD **套接字上可用于写入的空间超过了写入阈值。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_socket_create()`] - create a new socket  -[`zx_socket_create（）`]-创建一个新的套接字
 - [`zx_socket_read()`] - read data from a socket  -[`zx_socket_read（）`]-从套接字读取数据
 - [`zx_socket_shutdown()`] - prevent reading or writing  -[`zx_socket_shutdown（）`]-禁止读写
 - [`zx_socket_write()`] - write data to a socket  -[`zx_socket_write（）`]-将数据写入套接字

