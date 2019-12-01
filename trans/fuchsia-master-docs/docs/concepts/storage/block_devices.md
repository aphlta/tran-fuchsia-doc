 
# Block Devices  块设备 

Fuchsia Block device drivers are, like other drivers on the system, implemented as userspace services which are accessible via IPC. Programs using block deviceswill have one or more handles to these underlying drivers. Similar to filesystemclients, which may send “read” or “write” requests to servers by encoding theserequests within RPC messages, programs may act as clients to block devices, andmay transmit RPC messages to a “device host” (referred to as “devhost” withinZircon). The devhost process then transforms these requests intodriver-understood “I/O transactions”, where they are actually transmitted to theparticular block device driver, and eventually to real hardware. 紫红色块设备驱动程序与系统上的其他驱动程序一样，实现为可通过IPC访问的用户空间服务。使用块设备的程序将具有这些基本驱动程序的一个或多个句柄。类似于文件系统客户端，可以通过在RPC消息中对这些请求进行编码来向服务器发送“读取”或“写入”请求，程序可以充当阻止设备的客户端，并且可以将RPC消息传输到“设备主机”（称为“ devhost” insideZircon）。然后，devhost进程将这些请求转换为驱动程序可理解的“ I / O事务”，在此将它们实际传输到特定的块设备驱动程序，并最终传输到实际硬件。

Particular block device drivers (USB, AHCI / SATA, Ramdisk, GPT, etc) implement the [`ZX_PROTOCOL_BLOCK_CORE`prototol](/zircon/system/public/zircon/device/block.h),which allows clients to queue transactions and query the block device. 特定的块设备驱动程序（USB，AHCI / SATA，Ramdisk，GPT等）实现[`ZX_PROTOCOL_BLOCK_CORE`prototol]（/ zircon / system / public / zircon / device / block.h），该驱动程序允许客户端将事务排队和查询块设备。

 
## Fast Block I/O  快速块I / O 

Block device drivers are often responsible for taking large portions of memory, and queueing requests to a particular device to either “read into” or “writefrom” a portion of memory. Unfortunately, as a consequence of transmittingmessages of a limited size from an RPC protocol into an “I/O transaction”,repeated copying of large buffers is often required to access block devices. 块设备驱动程序通常负责占用很大一部分内存，并将对特定设备的请求排队以“读”或“写”一部分内存。不幸的是，由于将有限大小的消息从RPC协议传输到“ I / O事务”中，通常需要重复复制大缓冲区才能访问块设备。

